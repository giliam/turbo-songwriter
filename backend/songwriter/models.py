# coding:utf-8

from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    firstname = models.CharField(
        max_length=150, 
        default="",
        blank=True
    )
    lastname = models.CharField(
        max_length=150, 
        default="",
        blank=True
    )

    added_date = models.DateTimeField(
        _('date added to the database'),
        auto_now_add=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        _('date updated to the database'),
        auto_now=True
    )

    class Meta:
        ordering = ['lastname', 'firstname']

    def __str__(self):
        return u"{0} {1}".format(self.firstname, self.lastname.upper())

    def get_comparable(self):
        if self.firstname:
            return u"{1} {0}.".format(self.firstname.upper()[0], self.lastname.upper())
        else:
            return u"{0}.".format(self.lastname.upper())


class Editor(models.Model):
    name = models.CharField(
        max_length=150, 
        default="",
        blank=True
    )

    added_date = models.DateTimeField(
        _('date added to the database'),
        auto_now_add=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        _('date updated to the database'),
        auto_now=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return u"{0}".format(self.name)


class Theme(models.Model):
    name = models.CharField(
        max_length=150,
        default="",
        blank=False
    )

    added_date = models.DateTimeField(
        _('date added to the database'),
        auto_now_add=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        _('date updated to the database'),
        auto_now=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return u"Theme: {0}".format(self.name)


class Chord(models.Model):
    note = models.CharField(
        max_length=15,
        blank=False,
        default=""
    )

    class Meta:
        ordering = ['note']

    def __str__(self):
        return u"Note: {0}".format(self.note)


class BookElement(models.Model):
    selected = models.BooleanField(
        default=False,
        blank=False
    )
    order_value = models.IntegerField(
        default=0
    )

    class Meta:
        abstract = True

    def print(self):
        return ""

    def is_song(self):
        return isinstance(self, Song)


class Song(BookElement):
    title = models.CharField(
        max_length=150,
        default="",
        blank=False
    )

    author = models.ForeignKey(Author, null=True, related_name="+")
    editor = models.ForeignKey(Editor, null=True, related_name="+")
    theme = models.ManyToManyField(Theme, blank=True)

    rights_paid = models.BooleanField(
        default=True,
        verbose_name=_("rights paid")
    )
    secli_number = models.CharField(
        max_length=150, 
        default="",
        blank=True
    )
    sacem_number = models.CharField(
        max_length=150, 
        default="",
        blank=True
    )

    is_refrain = models.BooleanField(
        default=False,
        verbose_name=_("is a refrain song?").capitalize()
    )

    page_number = models.CharField(
        max_length=20,
        default="0",
        blank=True
    )
    old_page_number = models.CharField(
        max_length=20,
        default="0",
        blank=True
    )

    comments = models.TextField(
        blank=True,
        verbose_name=_("comments").capitalize()
    )

    added_date = models.DateTimeField(
        _('date added to the database'),
        auto_now_add=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        _('date updated to the database'),
        auto_now=True
    )

    def get_printable_author(self):
        if self.author:
            return self.author.get_comparable()
        else:
            return "Unknown"

    class Meta:
        ordering = ['title']

    def __str__(self):
        return u"Song: {0}".format(self.title)

    def print(self):
        return str(self)


class SongsGroup(BookElement):
    name = models.CharField(
        max_length=150,
        default="",
        blank=False
    )
    songs = models.ManyToManyField(Song, related_name='groups')

    added_date = models.DateTimeField(
        _('date added to the database'),
        auto_now_add=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        _('date updated to the database'),
        auto_now=True
    )

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return u"Group {0}".format(self.name)

    def print(self):
        return str(self)


class Paragraph(models.Model):
    order = models.PositiveIntegerField()
    song = models.ForeignKey(Song, related_name='paragraphs')

    is_refrain = models.BooleanField(
        default=False,
        verbose_name=_("is a refrain paragraph?").capitalize()
    )

    added_date = models.DateTimeField(
        _('date added to the database'),
        auto_now_add=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        _('date updated to the database'),
        auto_now=True
    )

    class Meta:
        ordering = ['song', 'order']

    def __str__(self):
        return u"Paragraph: #{0}".format(self.order)


class Verse(models.Model):
    order = models.PositiveIntegerField()
    paragraph = models.ForeignKey(Paragraph, related_name='verses')

    content = models.TextField(blank=False)

    harmonizations = models.ManyToManyField(Chord, through="Harmonization")

    added_date = models.DateTimeField(
        _('date added to the database'),
        auto_now_add=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        _('date updated to the database'),
        auto_now=True
    )

    class Meta:
        ordering = ['paragraph', 'order']

    def __str__(self):
        return u"Verse #{1}: {0}".format(self.content, self.order)


class Harmonization(models.Model):
    verse = models.ForeignKey(Verse)
    chord = models.ForeignKey(Chord)

    start_spot_in_verse = models.PositiveIntegerField()
    end_spot_in_verse = models.PositiveIntegerField()

    added_date = models.DateTimeField(
        _('date added to the database'),
        auto_now_add=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        _('date updated to the database'),
        auto_now=True
    )

    class Meta:
        ordering = ['verse', 'start_spot_in_verse']

    def __str__(self):
        return u"Harmonization"


class SongLaTeXCode(models.Model):
    song = models.OneToOneField(
        Song,
        on_delete=models.CASCADE,
        related_name='latex_code'
    )
    code = models.TextField(
        blank=True,
        verbose_name=_("LaTeX code of a song").capitalize()
    )
    nb_lines = models.PositiveIntegerField(default=0)
    is_compiled = models.BooleanField(
        default=False,
        verbose_name=_("is compiled?").capitalize()
    )

    added_date = models.DateTimeField(
        _('date added to the database'),
        auto_now_add=True,
        blank=True
    )
    updated_date = models.DateTimeField(
        _('date updated to the database'),
        auto_now=True
    )

    def __str__(self):
        return u"LaTeX code of song {}".format(self.song)


class AdditionalLaTeXContent(models.Model):
    name = models.CharField(
        max_length=150,
        default="",
        blank=False
    )

    code = models.TextField(
        blank=True,
        verbose_name=_("LaTeX code").capitalize()
    )

    def __str__(self):
        return u"Additional LaTeX code {}".format(self.name)