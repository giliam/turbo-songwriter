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
from django.db.models import Q
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
top=3mm,
% includehead,
footskip=16pt,
includefoot}

\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
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
\\titlespacing*{\\section}{0pt}{0cm}{-0.09cm}
\\titlespacing*{\\subsection}{0pt}{0cm}{0.21cm}

% ------------
% PARAGRAPHS
% ------------
\\setlength{\\parindent}{0pt}
\\usepackage[final,tracking=true,kerning=true,spacing=true,stretch=10,shrink=10]{microtype}

% ------------
% CHORDS
% ------------

\\usepackage{color}
\\definecolor{gray}{gray}{0.45}

\\newcommand{\\accords}[1]{\\hfill {\\color{gray} \\emph{#1}}}
\\newcommand{\\accord}[1]{#1}


\\begin{document}

    """


def _get_default_footer():
    return """
\\end{document}
    """


def _get_available_lines_per_page():
    return 32


def _get_factor_bold_letters():
    return 1.2

def _get_nb_characters_per_line():
    return 75.


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
    def get_queryset(self):
        queryset = models.Song.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

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
    def get_queryset(self):
        queryset = models.Song.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

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
    def get_queryset(self):
        queryset = models.Paragraph.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    serializer_class = serializers.ParagraphSerializer


class ParagraphDetail(generics.RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        queryset = models.Paragraph.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
    
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
    def get_queryset(self):
        queryset = models.SongsGroup.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return serializers.GroupListSerializer
        return serializers.GroupCreateSerializer


class SongsGroupFastList(generics.ListCreateAPIView):
    queryset = models.SongsGroup.objects.all()

    serializer_class = serializers.GroupOnlyListSerializer


class SongsGroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SongsGroup.objects.all()
    serializer_class = serializers.GroupSerializer


@csrf_exempt
@api_view(['GET', 'PUT'])
def convert_to_tex(request, song_id):
    return edit_tex(request, song_id, True)


def _print_harmonization_of_verse(verse):
    if verse.harmonizations.exists():
        chords_to_add = {}
        for harmonization in verse.harmonization_set.all():
            chords_to_add[harmonization.start_spot_in_verse] = {
                "end": harmonization.end_spot_in_verse,
                "note": harmonization.chord.note,
            }
        
        has_to_be_underlined = False
        current_chord = None
        text_output = ""
        chord_output = "\\accords{"
        for i, letter in enumerate(verse.content):
            if has_to_be_underlined and i == current_chord["end"]:
                text_output += letter + "}"
                has_to_be_underlined = False
                current_chord = None
            elif i in chords_to_add.keys():
                text_output += "\\underline{" + letter
                current_chord = chords_to_add[i]
                if current_chord["end"] == i:
                    text_output += "}"
                else:
                    has_to_be_underlined = True
                if chord_output != "\\accords{":
                    chord_output += "\\quad"
                chord_output += "\\accord{%s}" % (current_chord["note"],)
            else:
                text_output += letter
        chord_output += "}"
        return text_output, chord_output
    else:
        return verse.content, ""


def _get_length_line(verse_text, is_bold=False):
    if is_bold:
        return len(verse_text)*_get_factor_bold_letters()/_get_nb_characters_per_line()
    else:
        return len(verse_text)/_get_nb_characters_per_line()


def _convert_song_to_tex(song):
    tex_output = []
    nb_lines = 0
    if not song.is_refrain:
        tex_output.append("\\section{%s}" % (song.title,))
        tex_output.append(u"\\subsection{%s - %s}" % (song.author,song.editor,))        
        # for the title
        nb_lines += 3

    if song.page_number and song.old_page_number:
        tex_output.append(u"\\cfoot{%s (%s)}" % (song.page_number, song.old_page_number))
    elif song.page_number:
        tex_output.append(u"\\cfoot{%s}" % (song.page_number, ))
    elif song.old_page_number:
        tex_output.append(u"\\cfoot{%s}" % (song.old_page_number, ))

    for paragraph in song.paragraphs.all():
        for verse in paragraph.verses.all():
            verse_text, harmonization_content = _print_harmonization_of_verse(verse)
            if paragraph.is_refrain:
                tex_output.append(u"\\textbf{%s}" % (verse_text,))
                size_line = _get_length_line(verse_text, True)
            else:
                tex_output.append(verse_text)
                size_line = _get_length_line(verse_text)
            tex_output.append(harmonization_content)
            tex_output.append("\\newline")
            nb_lines += 1
            if size_line >= 1:
                nb_lines += 1
        tex_output.append("\\newline")
        nb_lines += 1
    tex_output.pop()
    full_output = "\n".join([line for line in tex_output if line.strip() != ""]).strip()
    return nb_lines, full_output


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
        latex_code.nb_lines, latex_code.code = _convert_song_to_tex(song)
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
    harmonizations = models.Harmonization.objects.filter(verse__paragraph__song__id=song_id).select_related('chord')
    serializer = serializers.HarmonizationReadSerializer(harmonizations, context={'request': request}, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['GET'])
def get_author_songs(request, author_id):
    songs = models.Song.objects.filter(author__id=author_id).select_related('author')
    serializer = serializers.SongListSerializer(songs, context={'request':request}, many=True)
    return response.Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def get_editor_songs(request, editor_id):
    songs = models.Song.objects.filter(editor__id=editor_id).select_related('author')
    serializer = serializers.SongListSerializer(songs, context={'request':request}, many=True)
    return response.Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def get_theme_songs(request, theme_id):
    songs = models.Song.objects.filter(theme__id=theme_id).select_related('author')
    serializer = serializers.SongListSerializer(songs, context={'request':request}, many=True)
    return response.Response(serializer.data)


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

    songs = models.Song.objects.filter(
        Q(selected=True)|Q(groups__selected=True)
    ).prefetch_related(
        'author'
    ).prefetch_related(
        'editor'
    ).prefetch_related(
        'theme'
    ).prefetch_related(
        'latex_code'
    ).prefetch_related(
        'paragraphs'
    ).prefetch_related(
        'paragraphs__verses'
    ).prefetch_related(
        'paragraphs__verses__harmonizations'
    )

    base_lines_per_page = _get_available_lines_per_page()
    available_lines_per_page = base_lines_per_page

    for song in songs.all():
        tex_code += "\n\n"

        if not hasattr(song, 'latex_code'):
            latex_code = models.SongLaTeXCode()
            latex_code.song = song
            latex_code.nb_lines, latex_code.code = _convert_song_to_tex(song)
            # latex_code.save()
            song.latex_code = latex_code

        # if the song we try to add has more lines than remaining lines for this page AND we are not on a new page
        if song.latex_code.nb_lines < available_lines_per_page or available_lines_per_page == base_lines_per_page:
            # if we are following another song, add newline
            tex_code += song.latex_code.code
            if not available_lines_per_page == base_lines_per_page:
                tex_code += "\\newline\n"
                available_lines_per_page -= 1
            available_lines_per_page -= song.latex_code.nb_lines
        else:
            tex_code += "\\newpage\n"
            tex_code += song.latex_code.code
            available_lines_per_page = (base_lines_per_page - song.latex_code.nb_lines) % base_lines_per_page

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

    return response.Response({"url_tex":"media/tex/full.tex", "url_pdf":"media/pdf/whole_book.pdf"})


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
            song.id: song for song in models.Song.objects.all().select_related(
                'author'
            ).select_related(
                'editor'
            ).prefetch_related(
                'theme'
            ).select_related(
                'latex_code'
            ).prefetch_related(
                'paragraphs'
            ).prefetch_related(
                'paragraphs__verses'
            ).prefetch_related(
                'paragraphs__verses__harmonizations'
            )
        }
    else:
        songs_ids = map(int, songs_ids.split("/"))
        songs = {
            song.id: song for song in models.Song.objects.filter(pk__in=songs_ids).select_related(
                'author'
            ).select_related(
                'editor'
            ).prefetch_related(
                'theme'
            ).select_related(
                'latex_code'
            ).prefetch_related(
                'paragraphs'
            ).prefetch_related(
                'paragraphs__verses'
            ).prefetch_related(
                'paragraphs__verses__harmonizations'
            )
        }

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

        base_lines_per_page = _get_available_lines_per_page()
        available_lines_per_page = base_lines_per_page

        for song in songs.values():
            latex_code.code += "\n% /!\ Do not delete these commented lines /!\ %\n"
            latex_code.code += "% /!\ song #" + str(song.id) + " /!\ %\n"

            if hasattr(song, "latex_code"):
                nb_lines, code = song.latex_code.nb_lines, song.latex_code.code
            else:
                nb_lines, code = _convert_song_to_tex(song)


            # if the song we try to add has more lines than remaining lines for this page AND we are not on a new page
            if nb_lines < available_lines_per_page or available_lines_per_page == base_lines_per_page:
                latex_code.code += code
                available_lines_per_page -= nb_lines
            else:
                latex_code.code += "\\newpage\n"
                latex_code.code += code
                available_lines_per_page = base_lines_per_page

        latex_code.code += "\n% /!\ Do not delete these commented lines /!\ %\n"
        if additional_latex_content.filter(name="footer").exists():
            latex_code.code += additional_latex_content.get(name="footer").code
        else:
            latex_code.code += _get_default_footer()

        serializer = serializers.AdditionalLaTeXContentSerializer(
            latex_code, 
            context={"request":request}
        )
        return response.Response(serializer.data)


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
                print("Handles song", song)
                best_ratio, closest_titles = get_closest_songs(song.title.upper(), titles)
                print("Found results")
                # if the best ratio is not even bigger than #arbitrary threshold, 
                # there is no use to look for author
                if best_ratio > 0.8 and hasattr(song, "author") and song.author:
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

                print("Found best fit ?", output[song.id])
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
            output += "\\subsection{%s}\n" % (song.title[0], )
        output += "%s - %s \\\\ \n" % (song.title, song.page_number)
    return output
        

def _get_thematic_summary(songs, themes):
    output = "\\section{Index thématique}\n"
    for theme in themes.order_by('name'):
        output += "\\subsection{%s}\n" % (theme.name, )
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
    songs_serializer = serializers.SongBookElementSerializer(songs, many=True)
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


@api_view(['GET'])
def get_song_details(request, song_id):
    song = models.Song.objects.filter(pk=song_id).values(
        'id',
        'title',
        'author',
        'author_id',
        'author__firstname',
        'author__lastname',
        'editor',
        'editor_id',
        'editor__name',
        'latex_code',
        'is_refrain',
        'rights_paid',
        'page_number',
        'old_page_number',
        'secli_number',
        'sacem_number',
        'comments',
        'added_date',
        'updated_date',
    )
    themes = models.Theme.objects.filter(song__id=song_id)
    paragraphs = models.Paragraph.objects.filter(song__id=song_id)
    verses = models.Verse.objects.filter(paragraph__song__id=song_id)

    serializer_themes = serializers.ThemeSerializer(themes, many=True, context={'request': request})
    serializer_paragraphs = serializers.ParagraphOnlySerializer(paragraphs, many=True)
    serializer_verses = serializers.VerseOnlySerializer(verses, many=True)
    
    dict_song = song.get(pk=song_id)
    dict_themes = serializer_themes.data
    dict_paragraphs = serializer_paragraphs.data
    dict_verses = serializer_verses.data

    output = {
        "song": dict(dict_song),
        "themes": list(dict_themes),
        "paragraphs": list(dict_paragraphs),
        "verses": list(dict_verses)
    }
    return response.Response(output)


@csrf_exempt
@api_view(['POST'])
def add_song_with_verses(request):
    if request.method == "POST":
        json_data = json.loads(request.body.decode('utf-8'))
        song = models.Song()
        song.title = json_data["title"]
        song.author = models.Author.objects.get(id=json_data["author"])
        song.editor = models.Editor.objects.get(id=json_data["editor"])
        song.is_refrain = json_data["is_refrain"]
        song.secli_number = json_data["secli_number"]
        song.page_number = json_data["page_number"]
        song.old_page_number = json_data["old_page_number"]
        song.comments = json_data["comments"]
        song.save()
        song.theme = models.Theme.objects.filter(id__in=json_data["theme"]).all()

        verses = json_data["verses"].strip().split("\n")
        j = 0

        paragraph = models.Paragraph()
        paragraph.song = song
        paragraph.order = j
        paragraph.save()

        i = 0
        for line in verses:
            line = line.strip()
            if line == "":
                paragraph = models.Paragraph()
                paragraph.song = song
                j += 1
                i = 0
                paragraph.order = j
                paragraph.save()
            else:
                if line[0] == "_" and line[1] == "_":
                    paragraph.is_refrain = True
                    paragraph.save()
                    line = line[2:]
                
                # is refrain
                verse = models.Verse()
                verse.paragraph = paragraph
                verse.content = line
                verse.order = i
                i += 1
                verse.save()

        return response.Response({'id': song.id})
    else:
        return response.Response({})


@csrf_exempt
@api_view(['GET'])
def get_songs_without_author(request):
    songs = models.Song.objects.filter(
        author=None
    ).select_related(
        'latex_code'
    ).select_related(
        'author'
    ).select_related(
        'editor'
    ).prefetch_related(
        'theme'
    )
    serializer = serializers.SongOtherListSerializer(songs, context={'request':request}, many=True)
    return response.Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def get_songs_without_editor(request):
    songs = models.Song.objects.filter(
        editor=None
    ).select_related(
        'latex_code'
    ).select_related(
        'author'
    ).select_related(
        'editor'
    ).prefetch_related(
        'theme'
    )
    serializer = serializers.SongOtherListSerializer(songs, context={'request':request}, many=True)
    return response.Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def get_songs_with_latex_code(request):
    songs = models.Song.objects.exclude(
        latex_code=None
    ).select_related(
        'latex_code'
    ).select_related(
        'author'
    ).select_related(
        'editor'
    ).prefetch_related(
        'theme'
    )
    serializer = serializers.SongOtherListSerializer(songs, context={'request':request}, many=True)
    return response.Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def get_songs_without_page_number(request):
    songs = models.Song.objects.filter(
        page_number=0, 
        old_page_number=0
    ).select_related(
        'latex_code'
    ).select_related(
        'author'
    ).select_related(
        'editor'
    ).prefetch_related(
        'theme'
    )
    serializer = serializers.SongOtherListSerializer(songs, context={'request':request}, many=True)
    return response.Response(serializer.data)


@csrf_exempt
@api_view(['GET'])
def get_songs_with_edition_last_date(request):
    songs = models.Song.objects.all()
    serializer = serializers.SongOtherListSerializer(songs, context={'request':request}, many=True)
    return response.Response(serializer.data)