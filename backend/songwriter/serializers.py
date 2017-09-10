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


class VerseReadSerializer(serializers.ModelSerializer):
    # harmonizations = HarmonizationSerializer(many=True, read_only=True)

    class Meta:
        model = Verse
        fields = (
            'id',
            'order',
            'content',
            'paragraph',
            'harmonizations',
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
            'paragraph',
            'harmonizations',
            'added_date',
            'updated_date'
        )


class HarmonizationReadSerializer(serializers.ModelSerializer):
    chord = ChordSerializer()

    class Meta:
        model = Harmonization
        fields = (
            'id',
            'chord',
            'verse',
            'spot_in_verse',
            'added_date',
            'updated_date'
        )


class HarmonizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harmonization
        fields = (
            'id',
            'chord',
            'verse',
            'spot_in_verse',
            'added_date',
            'updated_date'
        )


class ParagraphSerializer(serializers.ModelSerializer):
    verses = VerseReadSerializer(many=True, read_only=True)

    class Meta:
        model = Paragraph
        fields = (
            'id',
            'order',
            'song',
            'verses',
            'is_refrain',
            'added_date',
            'updated_date'
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
            'page_number',
            'old_page_number',
            'comments',
            'added_date',
            'updated_date'
        )


class SongLaTeXCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongLaTeXCode
        fields = ('id', 'code')


class SongReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    editor = EditorSerializer()
    theme = ThemeSerializer(many=True)
    paragraphs = ParagraphSerializer(many=True, read_only=True)
    latex_code = SongLaTeXCodeSerializer()

    class Meta:
        model = Song
        fields = (
            'id',
            'title',
            'author',
            'editor',
            'theme',
            'paragraphs',
            'latex_code',
            'rights_paid',
            'page_number',
            'old_page_number',
            'secli_number',
            'sacem_number',
            'comments',
            'added_date',
            'updated_date'
        )
