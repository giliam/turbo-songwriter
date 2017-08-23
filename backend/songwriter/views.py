# coding:utf-8

from django.contrib.auth.models import User
from django.shortcuts import render

from rest_framework import mixins
from rest_framework import generics

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
    serializer_class = serializers.SongSerializer


class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer


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
    return render(request, 'index.html', {})