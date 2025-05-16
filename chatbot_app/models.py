from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid


class ChatSession(models.Model):
    """Tracks individual chat sessions with users"""
    session_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_sessions')
    created_at = models.DateTimeField(default=timezone.now)
    last_interaction = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.user:
            return f"Chat Session {self.session_id} - {self.user.email}"
        return f"Chat Session {self.session_id} - Guest"


class ChatMessage(models.Model):
    """Stores individual messages within a chat session"""
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=50, default='user', help_text="Either 'user' or 'bot'")
    message = models.TextField()
    metadata = models.JSONField(null=True, blank=True, help_text="Additional data about the message, like sentiment analysis")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} message at {self.timestamp}"


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


class PageContentManager(models.Manager):
    def create_default_entries(self):
        """Create default entries if none exist."""
        if not self.exists():
            defaults = [
                {
                    'title': 'AppAttack',
                    'content': 'AppAttack is our flagship security testing platform that helps identify vulnerabilities in mobile applications.',
                    'keywords': 'appattack, security, mobile, testing, vulnerabilities',
                    'priority': 100
                },
                {
                    'title': 'VR Security',
                    'content': 'Our VR Security training provides immersive cybersecurity education in virtual reality environments.',
                    'keywords': 'vr, virtual reality, security, training, education',
                    'priority': 90
                },
                {
                    'title': 'Join Us',
                    'content': 'To join Hardhat Enterprises, visit our careers page or contact us directly. We\'re always looking for talented individuals.',
                    'keywords': 'join, careers, jobs, employment, opportunities',
                    'priority': 80
                },
                {
                    'title': 'Projects',
                    'content': 'Our key projects include AppAttack, VR Security Training, Threat Mirror, and various cybersecurity research initiatives.',
                    'keywords': 'projects, initiatives, research, security',
                    'priority': 70
                }
            ]
            
            for entry in defaults:
                self.create(**entry)
            return True
        return False


class PageContent(models.Model):
    """Stores searchable content pages"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    keywords = models.TextField(help_text="Comma-separated keywords for search matching")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.IntegerField(default=0, help_text="Higher priority items appear first in search results")
    
    objects = PageContentManager()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-priority', '-updated_at']


class CustomChatbotResponse(models.Model):
    """Stores custom responses for the chatbot based on keywords"""
    keywords = models.TextField(help_text="Comma-separated keywords that will trigger this response")
    response = models.TextField(help_text="The response that the chatbot should give when keywords are matched")
    priority = models.IntegerField(default=0, help_text="Higher priority responses will be checked first (0-10)")
    is_active = models.BooleanField(default=True, help_text="Whether this custom response is currently active")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, 
                              help_text="Associate this response with a specific project (optional)")
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = "Custom Chatbot Response"
        verbose_name_plural = "Custom Chatbot Responses"

    def __str__(self):
        return f"Response for: {self.keywords[:50]}..." 