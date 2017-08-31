# coding:utf-8

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework import mixins
from rest_framework import generics
from rest_framework import response

from songwriter import models
from songwriter import serializers


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
            return serializers.SongReadSerializer
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
    serializer_class = serializers.VerseSerializer


class VerseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Verse.objects.all()
    serializer_class = serializers.VerseSerializer


class HarmonizationList(generics.ListCreateAPIView):
    queryset = models.Harmonization.objects.all()
    serializer_class = serializers.HarmonizationSerializer


class HarmonizationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Harmonization.objects.all()
    serializer_class = serializers.HarmonizationSerializer


class SongLaTeXCodeList(generics.ListCreateAPIView):
    queryset = models.SongLaTeXCode.objects.all()
    serializer_class = serializers.SongLaTeXCodeSerializer


class SongLaTeXCodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.SongLaTeXCode.objects.all()
    serializer_class = serializers.SongLaTeXCodeSerializer


def main(request):
    return HttpResponse("Main")

@csrf_exempt
def convert_to_tex(request, song_id):
    return edit_tex(request, song_id, True)

@csrf_exempt
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
            for verse in paragraph.verses.all():
                if paragraph.is_refrain:
                    tex_output += u"\\textbf{%s}" % (verse.content,) + "\n"
                else:
                    tex_output += verse.content + "\n"
                tex_output += "\\newline\n"
            tex_output += "\\newline\n"
        latex_code.code = tex_output
        latex_code.save()

    if request.method == "GET" or force:
        serializer = serializers.SongLaTeXCodeSerializer(latex_code)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        serializer = serializers.SongLaTeXCodeSerializer(latex_code, data=request.data)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def invert_verse(request, verse_id_top, verse_id_bottom):
    verse_top = get_object_or_404(models.Verse, pk=verse_id_top)
    verse_bottom = get_object_or_404(models.Verse, pk=verse_id_bottom)

    order = verse_top.order
    verse_top.order = verse_bottom.order
    verse_bottom.order = order
    verse_top.save()
    verse_bottom.save()
    return JsonResponse({}, safe=False)
