# coding:utf-8

import os
import shutil
import subprocess
import tempfile

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


@csrf_exempt
@api_view(['GET', 'PUT'])
def convert_to_tex(request, song_id):
    return edit_tex(request, song_id, True)


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
        tex_output = "\\section{%s}" % (song.title,) + "\n"
        tex_output += u"\subsection{%s - %s}" % (song.author,song.editor,) + "\n"

        for paragraph in song.paragraphs.all():
            tex_output += "\\paragraph{}\n"
            for verse in paragraph.verses.all():
                if paragraph.is_refrain:
                    tex_output += u"\\textbf{%s}" % (verse.content,) + "\n"
                else:
                    tex_output += verse.content + "\n"
                tex_output += "\\newline\n"
        latex_code.code = tex_output
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
    os.chdir(temp)

    additional_latex_content = models.AdditionalLaTeXContent.objects.all()

    if additional_latex_content.filter(name="header").exists():
        header = additional_latex_content.get(name="header").code
    else:
        header = """
\\documentclass[preprint,11pt]{book}
\\usepackage[utf8]{inputenc}
\\usepackage[francais]{babel}
\\setcounter{secnumdepth}{0}
\\setcounter{tocdepth}{1}
\\begin{document}
    """

    if additional_latex_content.filter(name="footer").exists():
        footer = additional_latex_content.get(name="footer").code
    else:
        footer = """
\\tableofcontents
\\end{document}
"""
    tex_code = header

    tex_code += song.latex_code.code

    tex_code += footer

    f = open('out.tex','w')
    f.write(tex_code)
    f.close()

    proc=subprocess.Popen(['pdflatex','out.tex'])
    proc.communicate()

    os.rename('out.pdf',"song_" + str(song.id) + ".pdf")
    shutil.copy("song_" + str(song.id) + ".pdf", current + "/media/pdf/")
    shutil.rmtree(temp)

    song.latex_code.is_compiled = True
    song.latex_code.save()

    return JsonResponse({"url":"media/pdf/song_" + str(song.id) + ".pdf", "is_compiled": True}, safe=False)


class AdditionalLaTeXContentList(generics.ListCreateAPIView):
    queryset = models.AdditionalLaTeXContent.objects.all()
    serializer_class = serializers.AdditionalLaTeXContentSerializer


class AdditionalLaTeXContentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AdditionalLaTeXContent.objects.all()
    serializer_class = serializers.AdditionalLaTeXContentSerializer