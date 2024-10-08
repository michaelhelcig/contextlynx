from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from .apis import note_api

urlpatterns = [
    # Redirect root URL to notes/create/
    path('', RedirectView.as_view(url='/create/', permanent=True)),

    # General views
    path('notes/', views.MyNotesView.as_view(), name='notes'),
    path('knowledge/', views.GraphView.as_view(), name='knowledge'),
    path('notes/<uuid:slug>/related/', views.NoteDetailRelatedView.as_view(), name='notes_detail_related'),
    path('notes/latest/related/', views.NoteDetailRelatedView.as_view(), name='notes_detail_related_latest'),
    path('create/', views.CreateNoteView.as_view(), name='create_note'),

    # API endpoints
    path('api/notes/', note_api.note, name='new_note'),
]

# Custom 404 handler
handler404 = 'core.views.Error404View'