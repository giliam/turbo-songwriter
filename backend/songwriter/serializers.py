#coding:utf-8

from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework import pagination
from songwriter import models


class ResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'groups')


class ChordSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='chords_detail', format='json')

    class Meta:
        model = models.Chord
        fields = (
            'id',
            'url',
            'note',
        )


class AuthorSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='authors_detail', format='json')

    class Meta:
        model = models.Author
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
        model = models.Editor
        fields = (
            'id',
            'url',
            'name',
            'added_date',
            'updated_date'
        )


class HarmonizationReadSerializer(serializers.ModelSerializer):
    chord = ChordSerializer()

    class Meta:
        model = models.Harmonization
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
        model = models.Harmonization
        fields = (
            'id',
            'chord',
            'verse',
            'start_spot_in_verse',
            'end_spot_in_verse',
            'added_date',
            'updated_date'
        )


class ThemeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='themes_detail', format='json')

    class Meta:
        model = models.Theme
        fields = (
            'id',
            'url',
            'name',
            'added_date',
            'updated_date'
        )


class VerseReadSerializer(serializers.ModelSerializer):
    # harmonizations = HarmonizationSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='verses_detail', format='json')

    class Meta:
        model = models.Verse
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

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related(
            'harmonizations'
        )
        
        return queryset


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Verse
        fields = (
            'id',
            'order',
            'content',
            'paragraph',
            'harmonizations',
            'added_date',
            'updated_date'
        )


class VerseOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Verse
        fields = (
            'id',
            'order',
            'content',
            'paragraph',
            'added_date',
            'updated_date'
        )


class ParagraphSerializer(serializers.ModelSerializer):
    verses = VerseReadSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='paragraphs_detail', format='json')

    class Meta:
        model = models.Paragraph
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

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related(
            'song'
        ).prefetch_related(
            'verses'
        )

        return queryset


class ParagraphOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paragraph
        fields = (
            'id',
            'order',
            'song',
            'is_refrain',
            'added_date',
            'updated_date'
        )


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Song
        fields = (
            'id',
            'selected', 
            'order_value',
            'title',
            'author',
            'editor',
            'theme',
            'is_refrain',
            'rights_paid',
            'secli_number',
            'sacem_number',
            'page_number',
            'old_page_number',
            'comments',
            'added_date',
            'updated_date', 
            'is_song'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related(
            'author'
        ).select_related(
            'editor'
        ).select_related(
            'theme'
        )

        return queryset


class SongLaTeXCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SongLaTeXCode
        fields = ('id', 'code', 'is_compiled')


class SongReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    editor = EditorSerializer()
    theme = ThemeSerializer(many=True)
    paragraphs = ParagraphSerializer(many=True, read_only=True)
    latex_code = SongLaTeXCodeSerializer()
    url = serializers.HyperlinkedIdentityField(view_name='songs_detail', format='json')

    class Meta:
        model = models.Song
        fields = (
            'id',
            'url',
            'title',
            'author',
            'editor',
            'theme',
            'paragraphs',
            'latex_code',
            'is_refrain',
            'rights_paid',
            'page_number',
            'old_page_number',
            'secli_number',
            'sacem_number',
            'comments',
            'added_date',
            'updated_date'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related(
            'author'
        ).select_related(
            'editor'
        ).prefetch_related(
            'theme'
        ).prefetch_related(
            'paragraphs'
        )
        return queryset



class SongOnlyReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    editor = EditorSerializer()
    theme = ThemeSerializer(many=True)
    latex_code = SongLaTeXCodeSerializer()

    class Meta:
        model = models.Song
        fields = (
            'id',
            'title',
            'author',
            'editor',
            'theme',
            'latex_code',
            'is_refrain',
            'rights_paid',
            'page_number',
            'old_page_number',
            'secli_number',
            'sacem_number',
            'comments',
            'added_date',
            'updated_date'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related(
            'author'
        ).select_related(
            'editor'
        ).prefetch_related(
            'theme'
        )
        return queryset

class SongListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='songs_detail', format='json')

    class Meta:
        model = models.Song
        fields = (
            'id',
            'url',
            'title',
            'is_refrain',
            'page_number',
            'old_page_number',
            'secli_number',
            'get_printable_author',
        )

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset


class AdditionalLaTeXContentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='additional_latexcode_detail', format='json')

    class Meta:
        model = models.AdditionalLaTeXContent
        fields = (
            'id',
            'url',
            'name',
            'code',
        )


class GroupListSerializer(serializers.ModelSerializer):
    songs = SongListSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='songs_detail', format='json')

    class Meta:
        model = models.SongsGroup
        fields = (
            'id',
            'name',
            'songs',
            'url',
            'selected',
            'order_value'
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SongsGroup
        fields = (
            'id', 
            'selected', 
            'order_value', 
            'name', 
            'songs', 
            'is_song'
        )


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SongsGroup
        fields = (
            'id', 
            'name', 
            'songs', 
            'selected', 
            'order_value'
        )

    def create(self, validated_data):
        name = validated_data.get('name')
        # Get the songs ids
        songs = validated_data.pop('songs')

        # Create our group
        song_group = models.SongsGroup.objects.create(**validated_data)
        # Process the songs.
        for song in songs:
            song_group.songs.add(song.id)

        song_group.save()

        return song_group