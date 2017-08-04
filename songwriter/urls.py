# coding: utf-8

from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from songwriter import views

urlpatterns = [
    url(r'^songs/list/$', views.SongList.as_view()),
    url(r'^songs/(?P<pk>[0-9]+)/$', views.SongDetail.as_view()),
    url(r'^authors/list/$', views.AuthorList.as_view()),
    url(r'^authors/(?P<pk>[0-9]+)/$', views.AuthorDetail.as_view()),
    url(r'^editors/list/$', views.EditorList.as_view()),
    url(r'^editors/(?P<pk>[0-9]+)/$', views.EditorDetail.as_view()),
    url(r'^themes/list/$', views.ThemeList.as_view()),
    url(r'^themes/(?P<pk>[0-9]+)/$', views.ThemeDetail.as_view()),
    url(r'^chords/list/$', views.ChordList.as_view()),
    url(r'^chords/(?P<pk>[0-9]+)/$', views.ChordDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)