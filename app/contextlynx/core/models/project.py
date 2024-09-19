from django.db import models
from .user import User
import uuid

class Project(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    icon = models.CharField(max_length=16, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)


    @staticmethod
    def get_or_create_default_project(user):
        """
        Get or create the default project for the given user.
        """
        project, created = Project.objects.get_or_create(
            user=user,
            title='Default Project',
            defaults={
                'icon': '📁'
            }
        )
        return project

    def __str__(self):
        return f"{self.title} ({self.uuid})"
