# coding:utf-8

import csv
import json
import difflib
import os
import re
import shutil
import subprocess
import tempfile

import slugify

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework import mixins
from rest_framework import generics
from rest_framework import response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from songwriter import models
from songwriter import serializers


def _get_default_header():
    return """
\\documentclass[a6paper,9pt]{book}

\\usepackage{geometry}
\\geometry{a6paper,
left=5mm,
bottom=4mm,
right=5mm,
top=5mm}

\\usepackage[utf8]{inputenc}
\\usepackage[francais]{babel}
\\usepackage{times}
\\usepackage{relsize}

% ------------
% PAGE NUMBER
% ------------
\\setcounter{secnumdepth}{0}
\\setcounter{tocdepth}{1}
\\usepackage{fancyhdr}
\\pagestyle{fancy}

% ------------
% TITLES
% ------------
\\usepackage{titlesec}

% \\titleformat{<command>}[<shape>]{<format>}{<label>}{<sep>}{<before-code>}[<after-code>]
\\titleformat{\\subsection}[display]{\\small\\itshape}{}{}{}[\\vspace{-0.3cm}\\rule{\\textwidth}{0.1pt}]

% \\titleformat*{<command>}{<style>}
\\titleformat*{\\section}{\\normalsize\\bfseries\\relscale{1.07}}

% \\titlespacing*{<command>}{<left>}{<before-sep>}{<after-sep>}
\\titlespacing*{\\section}{0pt}{0cm}{0cm}
\\titlespacing*{\\subsection}{0pt}{0cm}{0.21cm}

% ------------
% PARAGRAPHS
% ------------
\\setlength{\\parindent}{-10pt}

\\begin{document}
    """


def _get_default_footer():
    return """
\\end{document}
    """


@api_view(['GET'])
def api_root(request, format=None):
    return response.Response({
        'songs_list': reverse('songs_list', request=request, format=format),
        'authors_list': reverse('authors_list', request=request, format=format),
        'editors_list': reverse('editors_list', request=request, format=format),
        'themes_list': reverse('themes_list', request=request, format=format),
        'paragraphs_list': reverse('paragraphs_list', request=request, format=format),
        'verses_list': reverse('verses_list', request=request, format=format),
        'harmonization_list': reverse('harmonization_list', request=request, format=format),
        'chords_list': reverse('chords_list', request=request, format=format),
        'latexcode_list': reverse('latexcode_list', request=request, format=format),
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class SongList(generics.ListCreateAPIView):
    queryset = models.Song.objects.all()
    queryset = queryset.prefetch_related('author')

    def get_serializer_class(self):
        # Thanks to https://stackoverflow.com/a/41313121
        # Define your HTTP method-to-serializer mapping freely.
        # This also works with CoreAPI and Swagger documentation,
        # which produces clean and readable API documentation,
        # so I have chosen to believe this is the way the
        # Django REST Framework author intended things to work:
        if self.request.method in ('GET',):
            # Since the ReadSerializer does nested lookups
            # in multiple tables, only use it when necessary
            return serializers.SongListSerializer
        return serializers.SongSerializer


class SongListPaginate(SongList):
    pagination_class = serializers.ResultsSetPagination


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Song.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return serializers.SongReadSerializer
        return serializers.SongSerializer


class AuthorList(generics.ListCreateAPIView):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class AuthorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Author.objects.all()
    serializer_class = serializers.AuthorSerializer


class EditorList(generics.ListCreateAPIView):
    queryset = models.Editor.objects.all()
    serializer_class = serializers.EditorSerializer


class EditorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Editor.objects.all()
    serializer_class = serializers.EditorSerializer


class ThemeList(generics.ListCreateAPIView):
    queryset = models.Theme.objects.all()
    serializer_class = serializers.ThemeSerializer


class ThemeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Theme.objects.all()
    serializer_class = serializers.ThemeSerializer


class ChordList(generics.ListCreateAPIView):
    queryset = models.Chord.objects.all()
    serializer_class = serializers.ChordSerializer


class ChordDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Chord.objects.all()
    serializer_class = serializers.ChordSerializer


class ParagraphList(generics.ListCreateAPIView):
    queryset = models.Paragraph.objects.all()
    serializer_class = serializers.ParagraphSerializer


class ParagraphDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Paragraph.objects.all()
    serializer_class = serializers.ParagraphSerializer


class VerseList(generics.ListCreateAPIView):
    queryset = models.Verse.objects.all()
        
    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return serializers.VerseReadSerializer
        return serializers.VerseSerializer


class VerseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Verse.objects.all()
        
    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return serializers.VerseReadSerializer
        return serializers.VerseSerializer


class HarmonizationList(generics.ListCreateAPIView):
    queryset = models.Harmonization.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return serializers.HarmonizationReadSerializer
        return serializers.HarmonizationSerializer


class HarmonizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Harmonization.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return serializers.HarmonizationReadSerializer
        return serializers.HarmonizationSerializer


class SongLaTeXCodeList(generics.ListCreateAPIView):
    queryset = models.SongLaTeXCode.objects.all()
    serializer_class = serializers.SongLaTeXCodeSerializer


class SongLaTeXCodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SongLaTeXCode.objects.all()
    serializer_class = serializers.SongLaTeXCodeSerializer


class SongsGroupList(generics.ListCreateAPIView):
    queryset = models.SongsGroup.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return serializers.GroupListSerializer
        return serializers.GroupCreateSerializer


class SongsGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SongsGroup.objects.all()
    serializer_class = serializers.GroupSerializer


@csrf_exempt
@api_view(['GET', 'PUT'])
def convert_to_tex(request, song_id):
    return edit_tex(request, song_id, True)


def _convert_song_to_tex(song):
    tex_output = "\\section{%s}" % (song.title,) + "\n"
    tex_output += u"\subsection{%s - %s}" % (song.author,song.editor,) + "\n"
    if song.page_number and song.old_page_number:
        tex_output += u"\cfoot{%s (%s)}\n" % (song.page_number, song.old_page_number)
    elif song.page_number:
        tex_output += u"\cfoot{%s}\n" % (song.page_number, )
    elif song.old_page_number:
        tex_output += u"\cfoot{%s}\n" % (song.old_page_number, )

    for paragraph in song.paragraphs.all():
        tex_output += "\\paragraph{}\n"
        for verse in paragraph.verses.all():
            if paragraph.is_refrain:
                tex_output += u"\\textbf{%s}" % (verse.content,) + "\n"
            else:
                tex_output += verse.content + "\n"
            tex_output += "\\newline\n"
    tex_output += "\\newline\n"
    return tex_output


@csrf_exempt
@api_view(['GET', 'PUT'])
def edit_tex(request, song_id, force=False):
    song = get_object_or_404(models.Song, pk=song_id)

    # TODO: adds PUT/DELETE actions

    if models.SongLaTeXCode.objects.filter(song=song).exists():
        latex_code = song.latex_code
    else:        
        latex_code = models.SongLaTeXCode()
        latex_code.song = song
        # The LaTeX code doesn't exist, force the change
        force = True
    
    if force:
        latex_code.code = _convert_song_to_tex(song)
        latex_code.is_compiled = False
        latex_code.save()

    if request.method == "GET" or force:
        serializer = serializers.SongLaTeXCodeSerializer(latex_code)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        serializer = serializers.SongLaTeXCodeSerializer(latex_code, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def invert_verses(request, verse_id_top, verse_id_bottom):
    verse_top = get_object_or_404(models.Verse, pk=verse_id_top)
    verse_bottom = get_object_or_404(models.Verse, pk=verse_id_bottom)

    order = verse_top.order
    verse_top.order = verse_bottom.order
    verse_bottom.order = order
    verse_top.save()
    verse_bottom.save()
    return JsonResponse({}, safe=False)


@csrf_exempt
def invert_paragraphs(request, paragraph_id_top, paragraph_id_bottom):
    paragraph_top = get_object_or_404(models.Paragraph, pk=paragraph_id_top)
    paragraph_bottom = get_object_or_404(models.Paragraph, pk=paragraph_id_bottom)

    order = paragraph_top.order
    paragraph_top.order = paragraph_bottom.order
    paragraph_bottom.order = order
    paragraph_top.save()
    paragraph_bottom.save()
    return JsonResponse({}, safe=False)


@csrf_exempt
@api_view(['GET'])
def get_song_harmonizations(request, song_id):
    harmonizations = models.Harmonization.objects.filter(verse__paragraph__song__id=song_id)
    serializer = serializers.HarmonizationReadSerializer(harmonizations, context={'request': request}, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['GET'])
def get_author_songs(request, author_id):
    songs = models.Song.objects.filter(author__id=author_id)
    serializer = serializers.SongListSerializer(songs, context={'request':request}, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['GET'])
def get_editor_songs(request, editor_id):
    songs = models.Song.objects.filter(editor__id=editor_id)
    serializer = serializers.SongListSerializer(songs, context={'request':request}, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['GET'])
def get_theme_songs(request, theme_id):
    songs = models.Song.objects.filter(theme__id=theme_id)
    serializer = serializers.SongListSerializer(songs, context={'request':request}, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@api_view(['GET'])
def compile_tex(request, song_id):
    """
    Generates the pdf from string
    """
    song = get_object_or_404(models.Song, pk=song_id)

    current = os.getcwd()
    temp = tempfile.mkdtemp()

    additional_latex_content = models.AdditionalLaTeXContent.objects.all()

    if additional_latex_content.filter(name="header").exists():
        header = additional_latex_content.get(name="header").code
    else:
        header = _get_default_header()

    if additional_latex_content.filter(name="footer").exists():
        footer = additional_latex_content.get(name="footer").code
    else:
        footer = _get_default_footer()

    tex_code = header

    tex_code += song.latex_code.code

    tex_code += footer

    f = open(os.path.join(temp, 'out.tex'),'w')
    f.write(tex_code)
    f.close()

    proc=subprocess.Popen(['pdflatex', '-output-directory=' + temp, os.path.join(temp, 'out.tex')])
    proc.communicate()

    os.rename(
        os.path.join(temp, 'out.pdf'),
        os.path.join(temp, "song_" + str(song.id) + ".pdf")
    )
    shutil.copy(
        os.path.join(temp, "song_" + str(song.id) + ".pdf"), 
        os.path.join(current, "media/pdf/")
    )
    shutil.rmtree(temp)

    song.latex_code.is_compiled = True
    song.latex_code.save()

    return JsonResponse({"url":"media/pdf/song_" + str(song.id) + ".pdf", "is_compiled": True}, safe=False)


@csrf_exempt
@api_view(['GET'])
def get_whole_tex_code(request):
    """
    Generates the whole latex code
    """
    current = os.getcwd()
    temp = tempfile.mkdtemp()

    additional_latex_content = models.AdditionalLaTeXContent.objects.all()

    if additional_latex_content.filter(name="header").exists():
        header = additional_latex_content.get(name="header").code
    else:
        header = _get_default_header()

    if additional_latex_content.filter(name="footer").exists():
        footer = additional_latex_content.get(name="footer").code
    else:
        footer = _get_default_footer()

    tex_code = header

    songs = models.Song.objects.filter(selected=True)

    for song in songs.all():
        tex_code += "\n\n"
        if hasattr(song, 'latex_code'):
            tex_code += song.latex_code.code
        else:
            latex_code = models.SongLaTeXCode()
            latex_code.song = song
            latex_code.code = _convert_song_to_tex(song)
            latex_code.save()
            tex_code += latex_code.code

    themes = models.Theme.objects.all()
    tex_code += "\\newpage"
    tex_code += _get_summary(songs)
    tex_code += "\\newpage"
    tex_code += _get_thematic_summary(songs, themes)

    tex_code += footer

    f = open(os.path.join(temp, 'out.tex'),'w')
    f.write(tex_code)
    f.close()

    proc=subprocess.Popen(['pdflatex', '-output-directory=' + temp, os.path.join(temp, 'out.tex')])
    proc.communicate()

    os.rename(os.path.join(temp, 'out.pdf'),os.path.join(temp, 'whole_book.pdf'))
    os.rename(os.path.join(temp, 'out.tex'),os.path.join(temp, 'full.tex'))
    shutil.copy(os.path.join(temp, "full.tex"), current + "/media/tex/")
    shutil.copy(os.path.join(temp, "whole_book.pdf"), current + "/media/pdf/")
    shutil.rmtree(temp)

    return JsonResponse({"url_tex":"media/tex/full.tex", "url_pdf":"media/pdf/whole_book.pdf"}, safe=False)


class AdditionalLaTeXContentList(generics.ListCreateAPIView):
    queryset = models.AdditionalLaTeXContent.objects.all()
    serializer_class = serializers.AdditionalLaTeXContentSerializer


class AdditionalLaTeXContentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AdditionalLaTeXContent.objects.all()
    serializer_class = serializers.AdditionalLaTeXContentSerializer


@csrf_exempt
@api_view(['GET', 'POST'])
def edit_multiple_songs_tex(request, songs_ids, force=False):
    if songs_ids == "all":
        songs = {
            song.id: song for song in models.Song.objects.all()
        }
    else:
        songs_ids = songs_ids.split("/")
        songs = {}
        for song_id in songs_ids:
            song = get_object_or_404(models.Song, pk=song_id)
            songs[song_id] = song

    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        songs_latex_codes = json_data["code"].split("% /!\ Do not delete these commented lines /!\ %")
        id_song_reg = re.compile(r'% /!\\ song #([0-9]+) /!\\ %')
        for song_code in songs_latex_codes[1:-1]:
            song_lines_lists = song_code.strip().split("\n")
            song_id_latex = id_song_reg.search(song_lines_lists[0])
            if song_id_latex:
                song_id_latex = int(song_id_latex.group(1))
            else:
                return JsonResponse({})
            song_code = "\n".join(song_lines_lists[1:])
            if songs[song_id_latex].latex_code:
                songs[song_id_latex].latex_code.code = song_code.strip()
                songs[song_id_latex].latex_code.save()
            else:
                latex_code = models.SongLaTeXCode()
                latex_code.song = songs[song_id_latex]
                latex_code.code = song_code.strip()
                latex_code.is_compiled = False
                latex_code.save()
        return JsonResponse({})

    else:
        latex_code = models.AdditionalLaTeXContent()

        additional_latex_content = models.AdditionalLaTeXContent.objects.all()

        if additional_latex_content.filter(name="header").exists():
            latex_code.code = additional_latex_content.get(name="header").code
        else:
            latex_code.code = _get_default_header()


        for song in songs.values():
            latex_code.code += "\n% /!\ Do not delete these commented lines /!\ %\n"
            latex_code.code += "% /!\ song #" + str(song.id) + " /!\ %\n"
            if song.latex_code:
                latex_code.code += song.latex_code.code + "\n"
            else:
                latex_code.code += _convert_song_to_tex(song) + "\n"

        latex_code.code += "% /!\ Do not delete these commented lines /!\ %\n"
        if additional_latex_content.filter(name="footer").exists():
            latex_code.code += additional_latex_content.get(name="footer").code
        else:
            latex_code.code += _get_default_footer()

        serializer = serializers.AdditionalLaTeXContentSerializer(
            latex_code, 
            context={"request":request}
        )
        return JsonResponse(serializer.data)


def get_closest_songs(song_title, titles_list, number_min_elements=3):
    min_score = [
        # Stores (score, id_element)
        (0,0) for i in range(number_min_elements)
    ]

    for k, title in enumerate(titles_list):
        score = difflib.SequenceMatcher(None, song_title.strip(), title.strip()).ratio()
        # if the score is better than the worse 
        if score > min_score[0][0]:
            min_score[0] = (score, k)
            # then, sorts the dictionaries by value
            min_score.sort(key=lambda t: t[0])

    return min_score[-1][0], [k for (score, k) in min_score]


def get_code_song(data, code_columns_id):
    out = ""
    for code_column in code_columns_id:
        if not data[code_column].strip() == "":
            out = data[code_column]
    return out


@csrf_exempt
@api_view(['GET', 'POST'])
def find_copyrights_data(request, songs_ids):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        songs = models.Song.objects.filter(id__in=[d["id"] for d in json_data])

        new_codes = {}
        for elements in json_data:
            try:
                new_codes[elements["id"]] = elements["chosenNumber"].strip()
            except:
                pass
        for song in songs.all():
            if song.id in new_codes.keys():
                song.secli_number = new_codes[song.id]
                song.save()

        return JsonResponse({})
    else:
        if songs_ids == "all":
            songs = {
                song.id: song for song in models.Song.objects.all()
            }
        else:
            songs_ids = songs_ids.split("/")
            songs = {}
            for song_id in songs_ids:
                song = get_object_or_404(models.Song, pk=song_id)
                songs[song_id] = song

        if not os.path.isfile('../data/copyrights_data.csv'):
            return JsonResponse({})
        else:
            copyrights_structure = {}
            titles = {}

            with open('../data/copyrights_data_structure.json', 'r') as f:
                copyrights_structure = json.loads(f.read())
            with open('../data/copyrights_data.csv', 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
                titles = []
                rows = []
                for row in spamreader:
                    titles.append(row[copyrights_structure["title"]].upper())
                    rows.append(row)
            
            output = {
                song.id: {} for song in songs.values()
            }

            for song in songs.values():
                best_ratio, closest_titles = get_closest_songs(song.title.upper(), titles)
                
                # if the best ratio is not even bigger than #arbitrary threshold, 
                # there is no use to look for author
                if best_ratio > 0.8:
                    best_ratio = 0
                    best_song_id = 0
                    for title_id in closest_titles:
                        if type(copyrights_structure["author"]) == list:
                            for author_id_column in copyrights_structure["author"]:
                                score = difflib.SequenceMatcher(
                                    None, 
                                    song.author.get_comparable(), 
                                    rows[title_id][author_id_column]
                                ).ratio()
                                
                                if score > best_ratio:
                                    best_ratio = score
                                    best_song_id = title_id
                        else:
                            score = difflib.SequenceMatcher(
                                None, 
                                song.author.get_comparable(), 
                                rows[title_id][copyrights_structure["author"]]
                            ).ratio()
                            
                            if score > best_ratio:
                                best_ratio = score
                                best_song_id = title_id
                
                    # adds arbitrary threshold for unique song choice
                    if best_ratio > 0.8:
                        best_song = rows[best_song_id]
                        output[song.id] = {
                            "code": get_code_song(
                                best_song, 
                                copyrights_structure["number"]
                            ),
                            "title": best_song[copyrights_structure["title"]],
                            "selected": True,
                        }
                        if type(copyrights_structure["author"]) == list:
                            output[song.id]["author"] = []
                            for author_id_column in copyrights_structure["author"]:
                                output[song.id]["author"].append(best_song[author_id_column])
                        else:
                            output[song.id]["author"] = best_song[copyrights_structure["author"]]

                # if the best fit has not been found,
                # returns the whole choices given by titles comparisons
                if output[song.id] == {}:
                    output[song.id] = []
                    for title_id in closest_titles:
                        close_song = rows[title_id]
                        dic_song = {
                            "code": get_code_song(
                                close_song, 
                                copyrights_structure["number"]
                            ),
                            "title": close_song[copyrights_structure["title"]],
                            "selected": False,
                        }
                        if type(copyrights_structure["author"]) == list:
                            dic_song["author"] = []
                            for author_id_column in copyrights_structure["author"]:
                                dic_song["author"].append(close_song[author_id_column])
                        else:
                            dic_song["author"] = close_song[copyrights_structure["author"]]
                        output[song.id].append(dic_song)

            return JsonResponse(output)


@csrf_exempt
@api_view(['GET', 'POST'])
def guess_pages_numbers(request, songs_ids):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        songs = models.Song.objects.filter(id__in=[d["id"] for d in json_data])

        new_pages = {}
        for elements in json_data:
            try:
                new_pages[elements["id"]] = elements["page"].strip()
            except:
                pass
        for song in songs.all():
            if song.id in new_pages.keys():
                song.old_page_number = new_pages[song.id]
                song.save()
                # print("Song", song.title, "new page is", song.page)
        return JsonResponse({})
    else:
        if songs_ids == "all":
            songs = {
                song.id: song for song in models.Song.objects.all()
            }
        else:
            songs_ids = songs_ids.split("/")
            songs = {}
            for song_id in songs_ids:
                song = get_object_or_404(models.Song, pk=song_id)
                songs[song_id] = song

        if not os.path.isfile('../data/pages_data.csv'):
            return JsonResponse({})
        else:
            pages_structure = {}
            titles = {}

            with open('../data/pages_data_structure.json', 'r') as f:
                pages_structure = json.loads(f.read())
            with open('../data/pages_data.csv', 'r') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
                pages_data = []
                titles = []
                for row in spamreader:
                    titles.append(row[pages_structure["title"]].upper())
                    pages_data.append(row[pages_structure["page"]])
            
            output = {
                song.id: None for song in songs.values()
            }

            for song in songs.values():
                best_ratio, closest_titles = get_closest_songs(
                    song.title.upper(), 
                    titles, 
                    number_min_elements=1
                )

                if best_ratio > 0.8:
                    output[song.id] = (pages_data[closest_titles[0]], titles[closest_titles[0]])

            return JsonResponse(output)


def _get_summary(songs):
    output = "\\section{Sommaire}\n"
    last_letter = ""
    for song in songs.order_by('title'):
        first_letter = _simplify_title_letters(song.title[0])
        if first_letter != last_letter:
            last_letter = first_letter
            output += "\\subsection{%s}\n\\paragraph{}\n" % (song.title[0], )
        output += "%s - %s \\\\ \n" % (song.title, song.page_number)
    return output
        

def _get_thematic_summary(songs, themes):
    output = "\\section{Index thématique}\n"
    for theme in themes.order_by('name'):
        output += "\\subsection{%s}\n\\paragraph{}\n" % (theme.name, )
        songs_filtered = songs.filter(theme=theme)
        for song in songs_filtered.all():
            output += "%s - %s \\\\ \n" % (song.title, song.page_number)
    return output


def _simplify_title_letters(title):
    return slugify.slugify(title).upper()


@csrf_exempt
@api_view(['GET'])
def book_elements_list(request):
    songs = models.Song.objects.order_by('-selected', 'order_value').all()
    groups = models.SongsGroup.objects.order_by('-selected', 'order_value').all()
    songs_serializer = serializers.SongSerializer(songs, many=True)
    groups_serializer = serializers.GroupSerializer(groups, many=True)

    output_data = songs_serializer.data+groups_serializer.data
    output_data = sorted(
        output_data, 
        key=lambda t: list(t.items())[2][1])
    output_data = sorted(
        output_data, 
        key=lambda t: not list(t.items())[1][1])
    return JsonResponse(output_data, safe=False)


@csrf_exempt
@api_view(['PUT'])
def update_book_elements_list(request):
    if request.method == "PUT":
        json_data = json.loads(request.body.decode('utf-8'))
        songs_list = {
            item["id"]: item 
            for item in json_data if item["is_song"]
        }
        groups_list = {
            item["id"]: item
            for item in json_data if not item["is_song"]
        }
        songs = models.Song.objects.filter(id__in=songs_list.keys())
        groups = models.SongsGroup.objects.filter(id__in=groups_list.keys())

        for song in songs.all():
            song.selected = songs_list[song.id]["selected"]
            song.order_value = songs_list[song.id]["order_value"]
            song.save()

        for group in groups.all():
            group.selected = groups_list[group.id]["selected"]
            group.order_value = groups_list[group.id]["order_value"]
            group.save()

        return JsonResponse({})
    else:
        return JsonResponse({})