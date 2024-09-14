from django.urls import path
from . import views
from .apis import note_api

urlpatterns = [

    path('notes/', views.MyNotesView.as_view(), name='notes'),
    path('knowledge/', views.GraphView.as_view(), name='knowledge'),

    # API endpoints
    path('api/notes/', note_api.note, name='new_note'),
    
    # URL pattern for writing a note (the form page)
    path('notes/create', views.create_note, name='create_note'),
]


