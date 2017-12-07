#-*- coding: utf-8 -*-

import codecs
import os
import re
import shutil
import subprocess
import tempfile

from xml.dom import minidom

from songwriter import models

class Lyric(object):
    def __init__(self, content=None, refrain=False):
        self.content = content
        self.refrain = refrain
        self.new_paragraph = False

    def __str__(self):
        return self.content

class NewParagraph(Lyric):
    def __init__(self):
        self.refrain = False
        self.content = "\paragraph{}"
        self.new_paragraph = True


class Song(object):
    def __init__(self, title=None, author=None, lyrics=[]):
        self.title = title
        self.author = author
        self.lyrics = lyrics

    def _parse_author_name(self, author_name):
        if author_name.count(".") == 1:
            parts = author_name.split(".", 1)
            return (parts[0] + ".", parts[1])
        elif author_name.count(".") > 1:
            parts = author_name[::-1].split(".", 1)
            return (parts[1][::-1] + ".", parts[0][::-1])
        else:
            return ("", author_name)

    def ready_for_lyrics(self):
        return not self.title is None and not self.author is None

    def __str__(self):
        if len(self.lyrics) == 0:
            return ""

        output = ""

        last_is_new_line = False
        for lyric in self.lyrics:
            if lyric.new_paragraph:
                last_is_new_line = True

            if lyric.content == "":
                continue

            if lyric.refrain:
                output += u"\\textbf{%s}" % (lyric.content,) + "\n"
            else:
                output += lyric.content + "\n"

            if not last_is_new_line:
                output += "\\newline" + "\n"

            last_is_new_line = False

        return output

    def clean_song(self):
        still_empty = self.title.strip() == ""

        # first round of cleaning
        new_lyrics = []
        for i, lyric in enumerate(self.lyrics):
            # removes empty lyrics but doesn't remove paragraph
            if lyric.content.strip() == "" and not lyric.new_paragraph:
                continue
            if still_empty and not lyric.content.strip().replace("\paragraph{}", "") == "":
                still_empty = False
            new_lyrics.append(lyric)

        self.lyrics = new_lyrics

        new_lyrics = []
        for i, lyric in enumerate(self.lyrics):
            # removes new paragraphs doublons
            if lyric.new_paragraph and len(self.lyrics) > i+1 and self.lyrics[i+1].new_paragraph:
                continue
            new_lyrics.append(lyric)
        self.lyrics = new_lyrics

        # removes empty paragraphs
        new_lyrics = []
        for i, lyric in enumerate(self.lyrics):
            if lyric.new_paragraph:
                # if doesn't have any lyric, is an empty paragraph
                if len(self.lyrics[i:]) == 1:
                    continue
            new_lyrics.append(lyric)
        self.lyrics = new_lyrics

        return still_empty

    def save_song(self, db_data):
        empty_song = self.clean_song()
        if empty_song:
            return db_data

        song = models.Song()
        song.title = self.title
        if self.author and ("–" in self.author or "-" in self.author):
            if "–" in self.author:
                copyrights = self.author.split("–")
            elif "-" in self.author:
                copyrights = self.author.split("-")

            # print("Author", copyrights[0].strip())
            author_name = copyrights[0].strip()
            if not author_name in db_data["authors"].keys():
                author = models.Author()
                author.firstname, author.lastname = self._parse_author_name(author_name)
                print("Base : ", author_name, "\n", "firstname:", author.firstname, "Lastname:", author.lastname)
                author.save()
                song.author = author
                db_data["authors"][author_name] = author
            else:
                song.author = db_data["authors"][author_name]

            # print("Editor", copyrights[1].strip())
            editor_name = copyrights[1].strip()
            if not editor_name in db_data["editors"].keys():
                editor = models.Editor()
                editor.name = editor_name
                editor.save()
                song.editor = editor
                db_data["editors"][editor_name] = editor
            else:
                song.editor = db_data["editors"][editor_name]

        elif self.author:
            if not self.author in db_data["authors"].keys():
                author = models.Author()
                author.firstname, author.lastname = self._parse_author_name(self.author)
                print("Base : ", self.author, "\n", "firstname:", author.firstname, "Lastname:", author.lastname)
                author.save()
                song.author = author
                db_data["authors"][self.author] = author
            else:
                song.author = db_data["authors"][self.author]
        
        print("Saves", self.title, song.author)
        
        song.save()

        order_paragraph = 0
        order_verse = 0
        current_paragraph = None

        for i, lyric in enumerate(self.lyrics):
            if lyric.new_paragraph:
                order_verse = 0
                current_paragraph = models.Paragraph()
                current_paragraph.order = order_paragraph
                order_paragraph += 1
                current_paragraph.song = song
                # print("New paragraph", i, "current len", len(self.lyrics), self.lyrics[i:])
                if len(self.lyrics) > i:
                    current_paragraph.is_refrain = self.lyrics[i+1].refrain
                else:
                    current_paragraph.is_refrain = False
                current_paragraph.save()
            elif lyric.content.strip() != "":
                db_lyric = models.Verse()
                if current_paragraph is None:
                    current_paragraph = models.Paragraph()
                    current_paragraph.order = order_paragraph
                    order_paragraph += 1
                    current_paragraph.song = song
                    current_paragraph.is_refrain = len(self.lyrics) >= i and self.lyrics[i].refrain
                    current_paragraph.save()
                db_lyric.paragraph = current_paragraph
                db_lyric.content = lyric.content
                db_lyric.order = order_verse
                order_verse += 1
                db_lyric.save()

        return db_data




class Parser(object):

    def __init__(self, path="../../data/file/word/document.xml"):
        self.doc = minidom.parse(path)
        self.root = self.doc.documentElement
        self.body = self.root.firstChild

        self.output = ""
        self.all_songs = []

        self.tokens_to_replace = [
            {
                "from": "´",
                "to": "'",
            },
        ]

        self.special_nodes = "w:br"

    def get_text_of_node_p(self, node):
        content_nodes = node.getElementsByTagName('w:t')
        output = ""
        for content_node in content_nodes:
            output += content_node.childNodes[0].nodeValue.replace("\n", "").replace("\t", "")
        return output.strip().replace("’", "'")


    def parse(self):
        self.output += """
        \\documentclass[preprint,11pt]{book}
        \\usepackage[utf8]{inputenc}
        \\usepackage[francais]{babel}
        \\setcounter{secnumdepth}{0}
        \\setcounter{tocdepth}{1}
        \\begin{document}

        """

        self.all_songs = []
        current_song = None
        break_page_to_do = False
        break_paragraph = False
        for node in self.root.getElementsByTagName('w:p'):

            full_content = self.get_text_of_node_p(node)
            if full_content.strip() == "":
                if not current_song is None:
                    current_song.lyrics.append(NewParagraph())

            title_mode = False
            content_title_mode = ""
            author_mode = False
            content_author_mode = ""
            refrain_mode = False

            b_style = node.getElementsByTagName('w:b')
            for b_node in b_style:
                refrain_mode = True
            br_style = node.getElementsByTagName('w:br')
            for br_node in br_style:
                if br_node.getAttribute("w:type") == "page":
                    break_page_to_do = True

            titre_style = node.getElementsByTagName('w:pPr')
            for node_titre in titre_style:
                sub_node_titre = node_titre.getElementsByTagName('w:pStyle')
                for sub_node in sub_node_titre:
                    if sub_node.getAttribute("w:val") == "1TitreChant":
                        title_mode = True
                    elif sub_node.getAttribute("w:val") == "2auteurs":
                        author_mode = True
                    elif sub_node.getAttribute("w:val") == "refrains":
                        refrain_mode = True



            if title_mode:
                content_title_mode = self.get_text_of_node_p(node)
                if not current_song is None:
                    self.output += str(current_song) + "\n"
                    self.all_songs.append(current_song)
                if break_page_to_do:
                    self.output += u"\\newpage" + "\n"

                self.output += u"\\section{%s}" % (content_title_mode,) + "\n"
                current_song = Song(content_title_mode, None, [])

            elif author_mode:
                content_author_mode = self.get_text_of_node_p(node)
                self.output += u"\subsection{%s}" % (content_author_mode,) + "\n"
                current_song.author = content_author_mode

            else:
                if not current_song is None and current_song.ready_for_lyrics():
                    lyric = Lyric(self.get_text_of_node_p(node), refrain_mode)
                    current_song.lyrics.append(lyric)

        if not current_song is None:
            self.output += str(current_song) + "\n"


        self.output += u"\\tableofcontents"
        self.output += u"\\end{document}"

        for replace_token in self.tokens_to_replace:
            self.output = self.output.replace(replace_token["from"], replace_token["to"])

        with codecs.open("out.tex", "w", encoding="utf-8") as f:
            f.write(self.output)

    def save_songs(self):
        db_data = {
            "authors":{},
            "editors":{},
        }
        for song in self.all_songs:
            db_data = song.save_song(db_data)

    def compile(self):
        """
        Generates the pdf from string
        """

        current = os.getcwd()
        temp = tempfile.mkdtemp()
        os.chdir(temp)

        f = open('out.tex','w')
        f.write(self.output)
        f.close()

        proc=subprocess.Popen(['pdflatex','out.tex'])
        # subprocess.Popen(['pdflatex',tex])
        proc.communicate()

        shutil.copy("out.pdf",current)
        shutil.rmtree(temp)


if __name__ == "__main__":
    parser = Parser()
    parser.parse()
    parser.save_songs()