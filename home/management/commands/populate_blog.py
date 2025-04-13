from django.core.management.base import BaseCommand
from home.models import Article, User
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populates the blog with sample articles'

    def handle(self, *args, **kwargs):
        # Get the admin user
        try:
            user = User.objects.get(email='s223751702@deakin.edu.au')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user not found. Please create an admin user first.'))
            return

        # Sample articles data
        articles = [
            {
                'title': 'The Future of AI in Cybersecurity',
                'content': '''
                <h2>Introduction</h2>
                <p>Artificial Intelligence is revolutionizing the way we approach cybersecurity. From automated threat detection to predictive analytics, AI is becoming an essential tool in the fight against cyber threats.</p>
                
                <h2>Current Applications</h2>
                <p>AI is currently being used in several key areas of cybersecurity:</p>
                <ul>
                    <li>Automated threat detection</li>
                    <li>Behavioral analysis</li>
                    <li>Predictive analytics</li>
                    <li>Incident response</li>
                </ul>
                
                <h2>Future Prospects</h2>
                <p>The future of AI in cybersecurity looks promising, with advancements in machine learning and deep learning algorithms enabling more sophisticated threat detection and prevention mechanisms.</p>
                ''',
                'date': timezone.now()
            },
            {
                'title': 'Zero Trust Architecture: A New Security Paradigm',
                'content': '''
                <h2>What is Zero Trust?</h2>
                <p>Zero Trust Architecture represents a fundamental shift in how we approach network security. It operates on the principle of "never trust, always verify."</p>
                
                <h2>Key Principles</h2>
                <ul>
                    <li>Verify explicitly</li>
                    <li>Use least privilege access</li>
                    <li>Assume breach</li>
                </ul>
                
                <h2>Implementation Strategies</h2>
                <p>Implementing Zero Trust requires a comprehensive approach that includes network segmentation, identity verification, and continuous monitoring.</p>
                ''',
                'date': timezone.now()
            },
            {
                'title': 'Building Secure Web Applications: Best Practices',
                'content': '''
                <h2>Security First Approach</h2>
                <p>Security should be a fundamental consideration in every stage of web application development.</p>
                
                <h2>Essential Practices</h2>
                <ul>
                    <li>Input validation</li>
                    <li>Secure authentication</li>
                    <li>Data encryption</li>
                    <li>Regular security testing</li>
                </ul>
                
                <h2>Common Vulnerabilities</h2>
                <p>Understanding and addressing common vulnerabilities is crucial for building secure applications.</p>
                ''',
                'date': timezone.now()
            },
            {
                'title': 'AppAttack: Revolutionizing Mobile Security Testing',
                'content': '''
                <h2>About AppAttack</h2>
                <p>Our latest project, AppAttack, is setting new standards in mobile application security testing.</p>
                
                <h2>Key Features</h2>
                <ul>
                    <li>Automated vulnerability scanning</li>
                    <li>Real-time threat detection</li>
                    <li>Comprehensive security reports</li>
                </ul>
                
                <h2>Impact</h2>
                <p>AppAttack is helping developers identify and fix security vulnerabilities before they become critical issues.</p>
                ''',
                'date': timezone.now()
            },
            {
                'title': 'Blockchain Technology in Cybersecurity',
                'content': '''
                <h2>Blockchain Basics</h2>
                <p>Blockchain technology is not just for cryptocurrencies. Its decentralized nature and cryptographic security features make it an ideal solution for various cybersecurity applications.</p>
                
                <h2>Applications</h2>
                <ul>
                    <li>Secure identity management</li>
                    <li>Data integrity verification</li>
                    <li>Decentralized authentication</li>
                </ul>
                
                <h2>Future Potential</h2>
                <p>The potential applications of blockchain in cybersecurity are vast and still being explored.</p>
                ''',
                'date': timezone.now()
            },
            {
                'title': 'The Rise of Ransomware: Prevention and Response',
                'content': '''
                <h2>Understanding Ransomware</h2>
                <p>Ransomware attacks are becoming increasingly sophisticated and damaging.</p>
                
                <h2>Prevention Strategies</h2>
                <ul>
                    <li>Regular backups</li>
                    <li>Employee training</li>
                    <li>Security updates</li>
                    <li>Access controls</li>
                </ul>
                
                <h2>Response Plan</h2>
                <p>Having a robust incident response plan is crucial for minimizing the impact of ransomware attacks.</p>
                ''',
                'date': timezone.now()
            }
        ]

        # Create articles
        for article_data in articles:
            Article.objects.get_or_create(
                title=article_data['title'],
                defaults={
                    'content': article_data['content'],
                    'date': article_data['date'],
                    'author': user
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated blog with sample articles')) 