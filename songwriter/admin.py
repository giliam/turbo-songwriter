# coding:utf-8
from django.contrib import admin

from songwriter.models import (
    Author,
    Editor,
    Theme,
    Chord,
    Song,
    Paragraph,
    Verse,
    Harmonization
)

admin.site.register(Author)
admin.site.register(Editor)
admin.site.register(Theme)
admin.site.register(Chord)
admin.site.register(Song)
admin.site.register(Paragraph)
admin.site.register(Verse)
admin.site.register(Harmonization)
