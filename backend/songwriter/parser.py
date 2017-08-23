#-*- coding: utf-8 -*-

import re
import codecs

from xml.dom import minidom


class Lyric(object):
    def __init__(self, content=None, refrain=False):
        self.content = content
        self.refrain = refrain
        self.new_paragraph = False

    def __str__(self):
        return self.content

    def __unicode__(self):
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


class Parser(object):

    def __init__(self, path="../../file/word/document.xml"):
        self.doc = minidom.parse(path)
        self.root = self.doc.documentElement
        self.body = self.root.firstChild

        self.output = "" 

        self.special_nodes = "w:br"

    def get_text_of_node_p(self, node):
        content_nodes = node.getElementsByTagName('w:t')
        output = ""
        for content_node in content_nodes:
            output += content_node.childNodes[0].nodeValue.replace("\n", "").replace("\t", "")
        return output.strip()


    def parse(self):        
        output += """
        \\documentclass[preprint,11pt]{book}
        \\usepackage[utf8]{inputenc}
        \\usepackage[francais]{babel}
        \\setcounter{secnumdepth}{0}
        \\setcounter{tocdepth}{1}
        \\begin{document}

        """


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
                    output += unicode(current_song) + "\n"
                if break_page_to_do:
                    output += u"\\newpage" + "\n"

                output += u"\\section{%s}" % (content_title_mode,) + "\n"
                current_song = Song(content_title_mode, None, [])

            elif author_mode:
                content_author_mode = self.get_text_of_node_p(node)
                output += u"\subsection{%s}" % (content_author_mode,) + "\n"
                current_song.author = content_author_mode

            else:
                if not current_song is None and current_song.ready_for_lyrics():
                    lyric = Verse(self.get_text_of_node_p(node), refrain_mode)
                    current_song.lyrics.append(lyric)

        if not current_song is None:
            output += unicode(current_song) + "\n"


        output += u"\\tableofcontents"
        output += u"\\end{document}"

        with codecs.open("out.tex", "w", encoding="utf-8") as f:
            f.write(output)