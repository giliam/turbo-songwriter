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
    url = serializers.HyperlinkedIdentityField(view_name='authors_detail', format='json')

    class Meta:
        model = Author
        fields = (
            'id',
            'url',
            'firstname',
            'lastname',
            'added_date',
            'updated_date'
        )


class EditorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='editors_detail', format='json')

    class Meta:
        model = Editor
        fields = (
            'id',
            'url',
            'name',
            'added_date',
            'updated_date'
        )


class ThemeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='themes_detail', format='json')

    class Meta:
        model = Theme
        fields = (
            'id',
            'url',
            'name',
            'added_date',
            'updated_date'
        )


class ChordSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='chords_detail', format='json')

    class Meta:
        model = Chord
        fields = (
            'id',
            'url',
            'note',
        )


class VerseReadSerializer(serializers.ModelSerializer):
    # harmonizations = HarmonizationSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='verses_detail', format='json')

    class Meta:
        model = Verse
        fields = (
            'id',
            'url',
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
            'start_spot_in_verse',
            'end_spot_in_verse',
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
            'start_spot_in_verse',
            'end_spot_in_verse',
            'added_date',
            'updated_date'
        )


class ParagraphSerializer(serializers.ModelSerializer):
    verses = VerseReadSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='paragraphs_detail', format='json')

    class Meta:
        model = Paragraph
        fields = (
            'id',
            'url',
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
        fields = ('id', 'code', 'is_compiled')


class SongReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    editor = EditorSerializer()
    theme = ThemeSerializer(many=True)
    paragraphs = ParagraphSerializer(many=True, read_only=True)
    latex_code = SongLaTeXCodeSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='songs_detail', format='json')

    class Meta:
        model = Song
        fields = (
            'id',
            'url',
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


class SongListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='songs_detail', format='json')

    class Meta:
        model = Song
        fields = (
            'id',
            'url',
            'title'
        )
