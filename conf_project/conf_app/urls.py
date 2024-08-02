from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name='Home'),
    path("all", views.all_videos, name='All Videos'),
    path("themes", views.themes, name='Themes'),
    path("tags", views.tags, name='Tags'),
    path("rockstars", views.rockstar, name='Themes'),
    path("conf/<int:conf_id>/", views.conf, name='conf'),
    path("theme/<str:theme>/", views.theme, name='Theme'),
    path("tag/<str:tag>/", views.tag, name='Tag'),
    path("speaker/<int:speaker_id>/", views.speaker, name='speaker'),
    path("aboutus", views.aboutus, name='Aboutus'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)