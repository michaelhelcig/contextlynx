from django.urls import path
from . import views
from .apis import note_api

urlpatterns = [
    # path('', views.create_note, name='create_note'),
    path('notes/', views.MyNotesView.as_view(), name='notes'),
    path('knowledge/', views.my_knowledge, name='knowledge'),
    
    # API endpoints
    path('api/notes/', note_api.note, name='new_note'),
    
    # URL pattern for writing a note (the form page)
    path('notes/create', views.create_note, name='create_note'),
]


