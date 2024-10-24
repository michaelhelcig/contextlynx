from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.utils.safestring import mark_safe
import json
from .models import NodeTopic, NodeNote, Edge, Project
from .services import NoteService
from .services.background_worker_service import BackgroundWorkerService
import random
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(login_required(login_url='/login'), name='dispatch')
class Error404View(View):
    def get(self, request, exception=None):
        return redirect('/create')


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CreateNoteView(View):
    template_name = 'core/create_note.html'

    def get(self, request):
        user = request.user
        username = user.username.capitalize()
        project=Project.get_or_create_default_project(user)

        welcome_messages = [
            f"Hi, {username}! What insights would you like to jot down today?",
            f"Hello, {username}! Ready to add some new notes to your knowledge database?",
            f"Greetings, {username}! Let's capture your thoughts and ideas.",
            f"Ahoy, {username}! What would you like to document today?",
            f"Hey there, {username}! Start writing your next great note.",
            f"Welcome, {username}! What knowledge will you share today?",
            f"Salutations, {username}! It's time to organize your thoughts.",
            f"Howdy, {username}! What notes can we create for you today?",
            f"Hiya, {username}! Let's make some notes to remember.",
            f"What’s up, {username}? Ready to start documenting your ideas?"
        ]

        if project.read_only:
            selected_message = "This project is read-only. You can't add new notes."
        else:
            selected_message = random.choice(welcome_messages)

        context = {
            'welcome_message': selected_message,
            'project': project
        }

        return render(request, self.template_name, context)

@method_decorator(login_required(login_url='/login'), name='dispatch')
class MyNotesView(TemplateView):
    template_name = 'core/notes_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        project = Project.get_or_create_default_project(user)
        notes = NodeNote.objects.filter(project=project).order_by('-created_at')
        context = {
            'notes': notes
        }
        return context

@method_decorator(login_required(login_url='/login'), name='dispatch')
class NoteDetailRelatedView(TemplateView):
    template_name = 'core/notes_detail_related.html'
    context_object_name = 'current_note'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        project = Project.get_or_create_default_project(user)
        node_uuid = self.kwargs.get('slug')

        current_note = None

        if node_uuid is None or node_uuid == 'latest':
            node = NodeNote.objects.filter(project=project).order_by('-created_at').first()
            current_note = node
        else:
            node = NodeNote.objects.filter(uuid=node_uuid).first()

            if node is None:
                node = NodeTopic.objects.filter(uuid=node_uuid).first()
            else:
                current_note = node


        if node is not None:
            related_notes = NoteService().related_notes(node, 10)
            
            if current_note is None and len(related_notes) > 0:
                current_note = related_notes[0]

            related_notes = [note for note in related_notes if note.id != current_note.id]

            context['current_note'] = current_note
            context['related_notes'] = related_notes

        return context


@method_decorator(login_required(login_url='/login'), name='dispatch')
class GraphView(TemplateView):
    template_name = 'core/knowledge.html'

    def _scale_similarity(self, similarity):
        return (similarity + 1) / 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        project = Project.get_or_create_default_project(user)

        BackgroundWorkerService().recalculate_node_embeddings_if_necessary(project)

        nodes = []
        links = []

        colors = {
            "PERSON": "#FF6F61",  # Coral
            "ORGANIZATION": "#6D8B74",  # Sage Green
            "LOCATION": "#6C5B7B",  # Deep Lavender
            "OTHER": "#F8B400",  # Vibrant Amber
            "CONCEPT": "#CE93D8",  # Light Lavender
            "DATE": "#FF8C00",  # Dark Orange
            "EVENT": "#4CAF50",  # Medium Green
            "PRODUCT": "#FF5722",  # Deep Orange
            "WORK_OF_ART": "#AB47BC",  # Light Purple
            "LAW": "#E91E63",  # Pink
            "LANGUAGE": "#2196F3",  # Blue
            "QUANTITY": "#FFC107",  # Amber
            "TIME": "#00BCD4",  # Light Blue
            "URL": "#8E24AA",  # Purple
            "EMAIL": "#FF9800",  # Orange
            "PHONE_NUMBER": "#03A9F4",  # Light Blue
            "NATIONALITY": "#E64A19",  # Red-Orange
            "RELIGION": "#9E9D24",  # Olive Green
            "VEHICLE": "#00BFAE",  # Teal
            "ANIMAL": "#4CAF50",  # Green
            "PLANT": "#8BC34A",  # Lime Green
            "MEDICAL_CONDITION": "#F44336",  # Red
            "SPORTS_TEAM": "#03A9F4",  # Light Blue
            "INDUSTRY": "#FFC107",  # Amber
            "COMPANY": "#FF5722"  # Deep Orange
        }

        # Add NodeTopics
        for topic in NodeTopic.objects.filter(project=project):
            if not topic.disabled:
                nodes.append({
                    "id": f"topic_{topic.id}",
                    "uuid": f"{topic.uuid}",
                    "title": f"{topic.title}",
                    "type": "NodeTopic",
                    "color": colors[topic.data_type] if topic.data_type in colors else colors["OTHER"],
                    "edgeCount": topic.edge_count()
                })

        # Add NodeNotes
        for note in NodeNote.objects.filter(project=project):
            if not note.disabled:
                nodes.append({
                    "id": f"note_{note.id}",
                    "uuid": f"{note.uuid}",
                    "title": f"{note.title}",
                    "color": "lightgrey",
                    "type": "NodeNote"
                })

        # Add edges
        edges = set(Edge.objects.filter(project=project))
        for edge in edges:
            if not edge.from_node.disabled and not edge.to_node.disabled:
                links.append({
                    "source": f"{'topic' if isinstance(edge.from_node, NodeTopic) else 'note'}_{edge.from_node.id}",
                    "target": f"{'topic' if isinstance(edge.to_node, NodeTopic) else 'note'}_{edge.to_node.id}",
                    "similarity": self._scale_similarity(edge.similarity),
                    "color": 'red' if edge.predicted else 'black'
                })

        graph_data = {
            "nodes": nodes,
            "links": links
        }

        context['graph_data'] = mark_safe(json.dumps(graph_data))
        return context