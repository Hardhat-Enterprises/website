from django.db import models
from django.utils import timezone


class ChatSession(models.Model):
    """Tracks individual chat sessions with users"""
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_interaction = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Chat Session {self.session_id}"


class ChatMessage(models.Model):
    """Stores individual messages within a chat session"""
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    is_user_message = models.BooleanField(default=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{'User' if self.is_user_message else 'Bot'} message at {self.timestamp}"


class CompanyInformation(models.Model):
    """Stores general company information for the chatbot to reference"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    keywords = models.TextField(help_text="Comma-separated keywords for search matching")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    """Stores frequently asked questions and their answers"""
    question = models.TextField()
    answer = models.TextField()
    keywords = models.TextField(help_text="Comma-separated keywords for search matching")
    category = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question


class Project(models.Model):
    """Stores information about company projects"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    keywords = models.TextField(help_text="Comma-separated keywords for search matching")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductService(models.Model):
    """Stores information about products and services offered"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    features = models.TextField()
    keywords = models.TextField(help_text="Comma-separated keywords for search matching")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 