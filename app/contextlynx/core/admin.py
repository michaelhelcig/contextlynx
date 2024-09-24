from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Project, Edge, NodeEmbedding, WordEmbedding, NodeNote, NodeTopic

# Project Admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'uuid', 'user', 'created_at', 'updated_at')
    search_fields = ('title', 'uuid')
    list_filter = ('created_at', 'updated_at', 'user')
    ordering = ('-created_at',)

# Edge Admin
@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_from_node', 'get_to_node', 'similarity', 'predicted', 'project', 'uuid')
    search_fields = ('project__title', 'similarity')
    list_filter = ('project',)

    def get_from_node(self, obj):
        return str(obj.from_node)
    get_from_node.short_description = 'From Node'

    def get_to_node(self, obj):
        return str(obj.to_node)
    get_to_node.short_description = 'To Node'

# NodeEmbedding Admin
@admin.register(NodeEmbedding)
class NodeEmbeddingAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'embedding_model')
    search_fields = ('embedding_model',)
    list_filter = ('project',)

# WordEmbedding Admin
@admin.register(WordEmbedding)
class WordEmbeddingAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'embedding_model')
    search_fields = ('embedding_model',)
    list_filter = ('project',)

# NodeNote Admin
@admin.register(NodeNote)
class NodeNoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_summary', 'data_type', 'created_at', 'updated_at')
    search_fields = ('title', 'short_summary')
    list_filter = ('data_type', 'created_at', 'updated_at')

# NodeTopic Admin
@admin.register(NodeTopic)
class NodeTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'data_type', 'language', 'disabled', 'created_at', 'updated_at')
    search_fields = ('title', 'data_type')
    list_filter = ('data_type', 'language', 'disabled')
