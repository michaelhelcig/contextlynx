from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import User, NodeNote, NodeTopic, WordEmbedding, Edge

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(NodeNote)
class NodeNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at', 'data_type', 'language')
    list_filter = ('data_type', 'language', 'created_at', 'updated_at')
    search_fields = ('title', 'data_raw', 'data_sanitized_md')
    raw_id_fields = ('user', 'word_embedding')

@admin.register(NodeTopic)
class NodeTopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'updated_at', 'disabled', 'language')
    list_filter = ('disabled', 'language', 'created_at', 'updated_at')
    search_fields = ('title',)
    raw_id_fields = ('user', 'word_embedding')

@admin.register(WordEmbedding)
class WordEmbeddingAdmin(admin.ModelAdmin):
    list_display = ('id', 'model')
    search_fields = ('model',)

@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = ('get_from_node', 'get_to_node', 'similarity')
    list_filter = ('from_content_type', 'to_content_type')
    search_fields = ('get_from_node', 'get_to_node')

    def get_from_node(self, obj):
        return obj.from_node
    get_from_node.short_description = 'From Node'

    def get_to_node(self, obj):
        return obj.to_node
    get_to_node.short_description = 'To Node'
