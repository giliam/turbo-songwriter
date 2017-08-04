# coding:utf-8

from django.contrib.auth.models import User

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
