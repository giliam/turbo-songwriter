# coding: utf-8

from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from songwriter import views

urlpatterns = [
    url(r'^$', views.main, 
        name="main"),
    url(r'^songs/list/$', views.SongList.as_view(), 
        name="songs_list"),
    url(r'^songs/(?P<pk>[0-9]+)/$', views.SongDetail.as_view(), 
        name="songs_detail"),
    url(r'^song/convert/to/tex/(?P<song_id>[0-9]+)/$', views.convert_to_tex, 
        name="song_convert_to_tex"),
    url(r'^song/edit/tex/(?P<song_id>[0-9]+)/$', views.edit_tex, 
        name="song_convert_to_tex"),

    url(r'^authors/list/$', views.AuthorList.as_view(), 
        name="authors_list"),
    url(r'^authors/(?P<pk>[0-9]+)/$', views.AuthorDetail.as_view(), 
        name="authors_detail"),
    
    url(r'^editors/list/$', views.EditorList.as_view(), 
        name="editors_list"),
    url(r'^editors/(?P<pk>[0-9]+)/$', views.EditorDetail.as_view(), 
        name="editors_detail"),
    
    url(r'^themes/list/$', views.ThemeList.as_view(), 
        name="themes_list"),
    url(r'^themes/(?P<pk>[0-9]+)/$', views.ThemeDetail.as_view(), 
        name="themes_detail"),
    
    url(r'^paragraphs/list/$', views.ParagraphList.as_view(), 
        name="paragraphs_list"),
    url(r'^paragraphs/(?P<pk>[0-9]+)/$', views.ParagraphDetail.as_view(), 
        name="paragraphs_detail"),
    
    url(r'^verses/list/$', views.VerseList.as_view(), 
        name="verses_list"),
    url(r'^verses/(?P<pk>[0-9]+)/$', views.VerseDetail.as_view(), 
        name="verses_detail"),
    url(r'^verses/invert/(?P<verse_id_top>[0-9]+)/and/(?P<verse_id_bottom>[0-9]+)/$', 
        views.invert_verse, name="verses_invert"),
    
    url(r'^harmonization/list/$', views.HarmonizationList.as_view(), 
        name="harmonization_list"),
    url(r'^harmonization/(?P<pk>[0-9]+)/$', views.HarmonizationDetail.as_view(), 
        name="harmonization_detail"),
    
    url(r'^chords/list/$', views.ChordList.as_view(), 
        name="chords_list"),
    url(r'^chords/(?P<pk>[0-9]+)/$', views.ChordDetail.as_view(), 
        name="chords_detail"),
    
    url(r'^latexcode/list/$', views.SongLaTeXCodeList.as_view(), 
        name="latexcode_list"),
    url(r'^latexcode/(?P<pk>[0-9]+)/$', views.SongLaTeXCodeDetail.as_view(), 
        name="latexcode_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)