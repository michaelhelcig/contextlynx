from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.utils.safestring import mark_safe
import json

from openai import project

from .models import NodeTopic, NodeNote, Edge, Project


def error_404(request, exception=None):
    return redirect('/create')

def create_note(request):
    return render(request, 'core/create_note.html')

class MyNotesView(ListView):
    model = NodeNote
    template_name = 'core/notes_list.html'
    context_object_name = 'notes'
    ordering = ['-created_at']


class GraphView(TemplateView):
    template_name = 'core/knowledge.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        project = Project.get_or_create_default_project(user)

        nodes = []
        links = []

        colors = {
            "PERSON": "#FFB74D",
            "ORGANIZATION": "#FFB3BA",
            "LOCATION": "#C5E1A5",
            "OTHER": "#B3E5FC"
        }

        # Add NodeTopics
        for topic in NodeTopic.objects.filter(project=project):
            nodes.append({
                "id": f"topic_{topic.id}",
                "title": topic.title,
                "type": "NodeTopic",
                "color": colors[topic.data_type] if topic.data_type in colors else colors["OTHER"],
                "edgeCount": topic.edge_count()
            })

        # Add NodeNotes
        for note in NodeNote.objects.filter(project=project):
            nodes.append({
                "id": f"note_{note.id}",
                "title": note.title,
                "color": "lightgrey",
                "type": "NodeNote"
            })

        # Add edges
        edges = set(Edge.objects.filter(project=project))
        for edge in edges:
            links.append({
                "source": f"{'topic' if isinstance(edge.from_node, NodeTopic) else 'note'}_{edge.from_node.id}",
                "target": f"{'topic' if isinstance(edge.to_node, NodeTopic) else 'note'}_{edge.to_node.id}",
                "similarity": edge.similarity
            })

        graph_data = {
            "nodes": nodes,
            "links": links
        }

        context['graph_data'] = mark_safe(json.dumps(graph_data))
        return context