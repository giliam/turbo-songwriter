#coding:utf-8

from django.contrib.auth.models import User

from rest_framework import serializers

from songwriter.models import (Author, Harmonization,
    Editor, Theme, Chord, Song, Paragraph, Verse, SongLaTeXCode)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'groups')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = (
            'id',
            'firstname',
            'lastname',
            'added_date',
            'updated_date'
        )


class EditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = (
            'id',
            'name',
            'added_date',
            'updated_date'
        )


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = (
            'id',
            'name',
            'added_date',
            'updated_date'
        )


class ChordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chord
        fields = (
            'id',
            'note',
        )


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = (
            'id',
            'title',
            'author',
            'editor',
            'theme',
            'rights_paid',
            'secli_number',
            'sacem_number',
            'comments',
            'added_date',
            'updated_date'
        )


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = (
            'id',
            'order',
            'song',
            'is_refrain',
            'added_date',
            'updated_date'
        )


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = (
            'id',
            'order',
            'content',
            'harmonizations',
            'added_date',
            'updated_date'
        )


class HarmonizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harmonization
        fields = (
            'id',
            'verse',
            'chord',
            'spot_in_verse',
            'added_date',
            'updated_date'
        )


class SongLaTeXCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongLaTeXCode
        fields = ('id', 'song', 'code', 'added_date', 'updated_date')