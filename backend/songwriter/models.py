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

class Song(models.Model):
    title = models.CharField(
        max_length=150,
        default="",
        blank=False
    )

    author = models.ForeignKey(Author, related_name="+")
    editor = models.ForeignKey(Editor, related_name="+")
    theme = models.ManyToManyField(Theme)

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

    class Meta:
        ordering = ['title']

    def __str__(self):
        return u"Song: {0}".format(self.title)


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

    spot_in_verse = models.PositiveIntegerField()

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
        ordering = ['verse', 'spot_in_verse']

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