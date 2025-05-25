"""
Django management command to create sample data for testing.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from home.models import User, APIModel, Article, BlogPost, CyberChallenge

class Command(BaseCommand):
    help = 'Creates sample data for testing search functions'

    def handle(self, *args, **options):
        """Handle the command execution."""
        self.stdout.write(self.style.SUCCESS("\n=== Creating sample data for testing ===\n"))
        
        # Create a test user if needed
        try:
            user = User.objects.get(email="test@example.com")
            self.stdout.write("Using existing test user")
        except User.DoesNotExist:
            user = User.objects.create(
                email="test@example.com",
                first_name="Test",
                last_name="User"
            )
            self.stdout.write(self.style.SUCCESS("Created test user"))
        
        # Create APIModel entries
        api_models = [
            {
                'name': "Security API",
                'field_name': "auth_token",
                'description': "An API for handling security authentication"
            },
            {
                'name': "Data Processing API",
                'field_name': "data_field",
                'description': "An API for processing and analyzing data"
            },
            {
                'name': "User Management API",
                'field_name': "user_field",
                'description': "An API for user management and authentication"
            }
        ]
        
        for api_data in api_models:
            _, created = APIModel.objects.get_or_create(
                name=api_data['name'],
                defaults={
                    'field_name': api_data['field_name'],
                    'description': api_data['description']
                }
            )
            if created:
                self.stdout.write(f"Created APIModel: {api_data['name']}")
            else:
                self.stdout.write(f"APIModel already exists: {api_data['name']}")
        
        # Create Article entries
        articles = [
            {
                'title': "Introduction to Cybersecurity",
                'content': "<p>Learn about the basics of cybersecurity and how to protect yourself online</p>",
                'featured': True
            },
            {
                'title': "Data Protection Best Practices",
                'content': "<p>Best practices for protecting your data from cyber threats and hackers</p>",
                'featured': False
            }
        ]
        
        for article_data in articles:
            _, created = Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'content': article_data['content'],
                    'author': user,
                    'featured': article_data['featured']
                }
            )
            if created:
                self.stdout.write(f"Created Article: {article_data['title']}")
            else:
                self.stdout.write(f"Article already exists: {article_data['title']}")
        
        # Create BlogPost entries
        blog_posts = [
            {
                'title': "Security Tips for Remote Work",
                'body': "Tips for maintaining security while working remotely",
                'page_name': "blog"
            },
            {
                'title': "The Future of AI",
                'body': "Exploring the future of artificial intelligence and its security implications",
                'page_name': "blog"
            }
        ]
        
        for blog_data in blog_posts:
            _, created = BlogPost.objects.get_or_create(
                title=blog_data['title'],
                defaults={
                    'body': blog_data['body'],
                    'page_name': blog_data['page_name']
                }
            )
            if created:
                self.stdout.write(f"Created BlogPost: {blog_data['title']}")
            else:
                self.stdout.write(f"BlogPost already exists: {blog_data['title']}")
        
        # Create CyberChallenge entries
        challenges = [
            {
                'title': "Web Security Challenge",
                'description': "Test your web security knowledge with this challenge",
                'question': "What is XSS?",
                'choices': {"a": "Cross-Site Scripting", "b": "Cross-Server Sharing", "c": "Complex Security System"},
                'correct_answer': "a",
                'explanation': "XSS stands for Cross-Site Scripting, a type of web vulnerability",
                'difficulty': "medium",
                'category': "web",
                'points': 10
            },
            {
                'title': "Network Security Challenge",
                'description': "Test your network security knowledge",
                'question': "What is a firewall?",
                'choices': {"a": "A physical wall", "b": "Security software/hardware", "c": "A type of virus"},
                'correct_answer': "b",
                'explanation': "A firewall is security software/hardware that monitors and filters network traffic",
                'difficulty': "easy",
                'category': "network",
                'points': 5
            }
        ]
        
        for challenge_data in challenges:
            _, created = CyberChallenge.objects.get_or_create(
                title=challenge_data['title'],
                defaults={
                    'description': challenge_data['description'],
                    'question': challenge_data['question'],
                    'choices': challenge_data['choices'],
                    'correct_answer': challenge_data['correct_answer'],
                    'explanation': challenge_data['explanation'],
                    'difficulty': challenge_data['difficulty'],
                    'category': challenge_data['category'],
                    'points': challenge_data['points']
                }
            )
            if created:
                self.stdout.write(f"Created CyberChallenge: {challenge_data['title']}")
            else:
                self.stdout.write(f"CyberChallenge already exists: {challenge_data['title']}")
        
        self.stdout.write(self.style.SUCCESS("\nSample data creation completed successfully!")) 