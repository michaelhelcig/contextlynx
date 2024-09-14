from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import NodeNote, NodeTopic

def create_note(request):
    return render(request, 'core/create_note.html')

class MyNotesView(ListView):
    model = NodeNote
    template_name = 'core/my_notes.html'
    context_object_name = 'notes'
    ordering = ['-created_at']

def my_knowledge(request):
    return render(request, 'core/my_knowledge.html')

