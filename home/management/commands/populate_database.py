from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from home.models import (
    Announcement, Article, ContactSubmission, Contact, Course, CyberChallenge,
    Experience, JobApplication, Job, LeaderBoardTable, Project, SecurityEvent,
    Skill, Student, UserBlogPage, UserChallenge, DDT_contact, Progress,
    Profile, Passkey, BlogPost, Smishingdetection_join_us, Projects_join_us
)
from django.utils import timezone
from datetime import timedelta, date
import random
import string
from django.core.files.base import ContentFile
import uuid


class Command(BaseCommand):
    help = 'Populate database with test data - 10 entries per model'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force population even if database appears populated',
        )

    def is_database_populated(self):
        """Check if database already contains test data"""
        User = get_user_model()
        
        # Check if key models have data - if any have 5+ entries, assume populated
        checks = [
            User.objects.count() >= 5,
            Skill.objects.count() >= 5,
            Project.objects.count() >= 3,
            Course.objects.count() >= 5,
            CyberChallenge.objects.count() >= 5
        ]
        
        # If most checks pass, database is likely populated
        return sum(checks) >= 3

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            self.clear_data()
        elif self.is_database_populated() and not options['force']:
            self.stdout.write(self.style.WARNING('Database already populated. Skipping population script.'))
            self.stdout.write(self.style.SUCCESS('Use --clear flag to repopulate database or --force to populate anyway.'))
            return

        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Order matters - create dependencies first
        self.create_users()
        self.create_skills()
        self.create_projects()
        self.create_courses()
        self.create_students()
        self.create_announcements()
        self.create_articles()
        self.create_contact_submissions()
        self.create_contacts()
        self.create_cyber_challenges()
        self.create_experiences()
        self.create_jobs()
        self.create_job_applications()
        self.create_leader_board_tables()
        self.create_security_events()
        self.create_user_blog_pages()
        self.create_user_challenges()
        self.create_additional_models()

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))

    def clear_data(self):
        """Clear existing data from all models"""
        models_to_clear = [
            UserChallenge, JobApplication, Student, Progress, Profile, 
            LeaderBoardTable, SecurityEvent, Article, UserBlogPage,
            CyberChallenge, Experience, Job, ContactSubmission, Contact,
            Announcement, Course, Project, Skill, BlogPost, DDT_contact,
            Smishingdetection_join_us, Projects_join_us, Passkey
        ]
        
        for model in models_to_clear:
            model.objects.all().delete()
            self.stdout.write(f'Cleared {model.__name__}')

    def generate_fake_name(self):
        """Generate random names"""
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Chris', 'Lisa', 'Mark', 'Anna']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']
        return random.choice(first_names), random.choice(last_names)

    def generate_fake_email(self, first_name, last_name):
        """Generate fake email"""
        domains = ['deakin.edu.au', 'student.deakin.edu.au']
        return f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

    def generate_lorem_text(self, length=50):
        """Generate lorem ipsum style text"""
        words = ['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur', 'adipiscing', 'elit',
                'sed', 'do', 'eiusmod', 'tempor', 'incididunt', 'ut', 'labore', 'et', 'dolore',
                'magna', 'aliqua', 'enim', 'ad', 'minim', 'veniam', 'quis', 'nostrud',
                'exercitation', 'ullamco', 'laboris', 'nisi', 'aliquip', 'ex', 'ea', 'commodo',
                'consequat', 'duis', 'aute', 'irure', 'in', 'reprehenderit', 'voluptate',
                'velit', 'esse', 'cillum', 'fugiat', 'nulla', 'pariatur', 'excepteur', 'sint',
                'occaecat', 'cupidatat', 'non', 'proident', 'sunt', 'culpa', 'qui', 'officia',
                'deserunt', 'mollit', 'anim', 'id', 'est', 'laborum']
        return ' '.join(random.choices(words, k=length))

    def create_users(self):
        """Create 10 users"""
        User = get_user_model()
        self.stdout.write('Creating users...')
        
        for i in range(10):
            first_name, last_name = self.generate_fake_name()
            email = self.generate_fake_email(first_name, last_name)
            
            # Check if user already exists
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    password='testpassword123',
                    first_name=first_name,
                    last_name=last_name,
                    is_verified=True,
                    is_active=True
                )
                self.stdout.write(f'Created user: {user.email}')

    def create_skills(self):
        """Create 10 skills"""
        self.stdout.write('Creating skills...')
        
        skills_data = [
            ('Python Programming', 'Learn the fundamentals of Python programming language'),
            ('Web Security', 'Understanding web application security principles'),
            ('Network Security', 'Fundamentals of network security and protocols'),
            ('Django Framework', 'Learn Django web framework for Python'),
            ('JavaScript', 'Client-side programming with JavaScript'),
            ('Cybersecurity Basics', 'Introduction to cybersecurity concepts'),
            ('Database Management', 'Learn SQL and database design principles'),
            ('Git & GitHub', 'Version control with Git and collaboration on GitHub'),
            ('Linux Administration', 'System administration on Linux platforms'),
            ('Penetration Testing', 'Ethical hacking and penetration testing methodologies')
        ]
        
        for skill_name, description in skills_data:
            if not Skill.objects.filter(name=skill_name).exists():
                Skill.objects.create(
                    name=skill_name,
                    description=description,
                    slug=skill_name.lower().replace(' ', '-')
                )
                self.stdout.write(f'Created skill: {skill_name}')

    def create_projects(self):
        """Create projects with specified names"""
        self.stdout.write('Creating projects...')
        
        project_names = [
            'AppAttack',
            'PT-GUI', 
            'Deakin_CyberSafe_VR',
            'Policy Deployment Engine Team 1',  # This will need custom handling
            'Policy Deployment Engine Team 2',  # This will need custom handling
            'Smishing_Detection'
        ]
        
        # First create the standard project choices
        for project_choice in ['AppAttack', 'PT-GUI', 'Deakin_CyberSafe_VR', 'Smishing_Detection']:
            if not Project.objects.filter(title=project_choice).exists():
                Project.objects.create(title=project_choice)
                self.stdout.write(f'Created project: {project_choice}')
        
        # For the Policy Deployment Engine teams, we'll use the Company_Website_Development choice
        # since the model has specific choices defined
        policy_teams = ['Policy Deployment Engine Team 1', 'Policy Deployment Engine Team 2']
        for team_name in policy_teams:
            if not Project.objects.filter(title='Company_Website_Development').exists():
                Project.objects.create(title='Company_Website_Development')
                self.stdout.write(f'Created project: Company_Website_Development (for {team_name})')
                break  # Only create one instance
        
        # Fill remaining slots with other available choices
        remaining_choices = ['Malware', 'Deakin_Threat_Mirror']
        for choice in remaining_choices:
            if Project.objects.count() < 10 and not Project.objects.filter(title=choice).exists():
                Project.objects.create(title=choice)
                self.stdout.write(f'Created project: {choice}')

    def create_courses(self):
        """Create courses with specified data"""
        self.stdout.write('Creating courses...')
        
        courses_data = [
            ('Bachelor of Computer Science', 'S306', False),
            ('Bachelor of Computer Science (Honours)', 'S406', False),
            ('Bachelor of Artificial Intelligence', 'S308', False),
            ('Bachelor of Artificial Intelligence (Honours)', 'S408', False),
            ('Bachelor of Information Technology', 'S326', False),
            ('Bachelor of Arts / Bachelor of Information Technology', 'D310', False),
            ('Master of Information Technology', 'S727', True),
            ('Master of Information Systems', 'M722', True),
            ('Master of Data Science', 'S777', True),
            ('Master of Data Science (Professional)', 'S770', True),
        ]
        
        for title, code, is_postgrad in courses_data:
            if not Course.objects.filter(code=code).exists():
                Course.objects.create(
                    title=title,
                    code=code,
                    is_postgraduate=is_postgrad
                )
                self.stdout.write(f'Created course: {title} ({code})')

    def create_students(self):
        """Create 10 students"""
        self.stdout.write('Creating students...')
        
        User = get_user_model()
        users = list(User.objects.all()[:10])
        projects = list(Project.objects.all())
        
        for i, user in enumerate(users):
            student_id = 220000000 + i  # Generate unique student IDs
            
            if not Student.objects.filter(id=student_id).exists():
                # Randomly select 3 different projects for preferences
                project_prefs = random.sample(projects, min(3, len(projects)))
                
                student = Student.objects.create(
                    id=student_id,
                    user=user,
                    year=random.choice([2021, 2022, 2023, 2024]),
                    trimester=random.choice(['T1', 'T2', 'T3']),
                    unit=random.choice(['SIT782', 'SIT764', 'SIT378', 'SIT374']),
                    course=random.choice(['BCS', 'BIT', 'MIT', 'MCS', 'BAI']),
                    p1=project_prefs[0] if len(project_prefs) > 0 else None,
                    p2=project_prefs[1] if len(project_prefs) > 1 else None,
                    p3=project_prefs[2] if len(project_prefs) > 2 else None,
                    allocated=random.choice(projects) if projects else None
                )
                self.stdout.write(f'Created student: {student_id}')

    def create_announcements(self):
        """Create 10 announcements"""
        self.stdout.write('Creating announcements...')
        
        announcements = [
            'Welcome to the new semester! Check out our latest cybersecurity challenges.',
            'New project opportunities available for trimester 2024.',
            'Cybersecurity workshop scheduled for next week.',
            'Important: System maintenance scheduled for this weekend.',
            'New skills-based learning modules now available.',
            'Join our AppAttack project for hands-on penetration testing experience.',
            'Deakin CyberSafe VR project looking for new team members.',
            'Policy deployment project teams forming now.',
            'Smishing detection research opportunities available.',
            'End of semester showcase event coming soon.'
        ]
        
        for i, message in enumerate(announcements):
            Announcement.objects.create(
                message=message,
                isActive=random.choice([True, False]),
                created_at=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            self.stdout.write(f'Created announcement {i+1}')

    def create_articles(self):
        """Create 10 articles"""
        self.stdout.write('Creating articles...')
        
        User = get_user_model()
        users = list(User.objects.all())
        
        article_titles = [
            'Introduction to Cybersecurity Fundamentals',
            'Advanced Penetration Testing Techniques',
            'Web Application Security Best Practices',
            'Network Security and Threat Detection',
            'Secure Coding Practices in Python',
            'Understanding Malware Analysis',
            'Virtual Reality in Cybersecurity Training',
            'Policy Deployment in Enterprise Environments',
            'Smishing and Social Engineering Attacks',
            'Building Secure Web Applications with Django'
        ]
        
        for i, title in enumerate(article_titles):
            Article.objects.create(
                title=title,
                content=f'<p>{self.generate_lorem_text(100)}</p><p>{self.generate_lorem_text(150)}</p>',
                author=random.choice(users),
                featured=random.choice([True, False]),
                date=timezone.now().date() - timedelta(days=random.randint(0, 60))
            )
            self.stdout.write(f'Created article: {title}')

    def create_contact_submissions(self):
        """Create 10 contact submissions"""
        self.stdout.write('Creating contact submissions...')
        
        for i in range(10):
            first_name, last_name = self.generate_fake_name()
            email = self.generate_fake_email(first_name, last_name)
            
            ContactSubmission.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                message=self.generate_lorem_text(30),
                created_at=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            self.stdout.write(f'Created contact submission {i+1}')

    def create_contacts(self):
        """Create 10 contacts"""
        self.stdout.write('Creating contacts...')
        
        for i in range(10):
            first_name, last_name = self.generate_fake_name()
            
            Contact.objects.create(
                name=f"{first_name} {last_name}",
                email=self.generate_fake_email(first_name, last_name),
                message=self.generate_lorem_text(25)
            )
            self.stdout.write(f'Created contact {i+1}')

    def create_cyber_challenges(self):
        """Create 10 cyber challenges"""
        self.stdout.write('Creating cyber challenges...')
        
        challenges_data = [
            ('Basic SQL Injection', 'web', 'easy', 'mcq'),
            ('Network Scanning Techniques', 'network', 'medium', 'fix_code'),
            ('Cryptographic Hash Functions', 'crypto', 'hard', 'mcq'),
            ('Python Security Vulnerabilities', 'python', 'medium', 'fix_code'),
            ('JavaScript XSS Prevention', 'javascript', 'easy', 'mcq'),
            ('Linux File Permissions', 'linux', 'easy', 'fix_code'),
            ('Binary Exploitation Basics', 'binary_exploitation', 'hard', 'mcq'),
            ('Web Security Headers', 'web_security', 'medium', 'mcq'),
            ('Database Security', 'databases', 'medium', 'fix_code'),
            ('Reverse Engineering Challenge', 'reverse_engineering', 'hard', 'fix_code')
        ]
        
        for i, (title, category, difficulty, challenge_type) in enumerate(challenges_data):
            points = {'easy': 10, 'medium': 20, 'hard': 30}[difficulty]
            
            challenge = CyberChallenge.objects.create(
                title=title,
                description=self.generate_lorem_text(20),
                question=self.generate_lorem_text(15),
                difficulty=difficulty,
                category=category,
                points=points,
                challenge_type=challenge_type,
                time_limit=random.randint(30, 120),
                explanation=self.generate_lorem_text(25)
            )
            
            if challenge_type == 'mcq':
                challenge.choices = {
                    'A': 'Option A answer',
                    'B': 'Option B answer', 
                    'C': 'Option C answer',
                    'D': 'Option D answer'
                }
                challenge.correct_answer = random.choice(['A', 'B', 'C', 'D'])
                challenge.save()
            
            self.stdout.write(f'Created cyber challenge: {title}')

    def create_experiences(self):
        """Create 10 experiences"""
        self.stdout.write('Creating experiences...')
        
        experiences = [
            'Great learning experience with the cybersecurity program',
            'The hands-on projects really helped me understand the concepts',
            'Excellent mentorship from the teaching staff',
            'The virtual reality training was innovative and engaging',
            'Practical penetration testing skills gained through AppAttack',
            'Policy deployment project gave real-world experience',
            'Smishing detection research was eye-opening',
            'The collaborative environment fostered great teamwork',
            'Challenging but rewarding academic journey',
            'Skills learned here are directly applicable to industry'
        ]
        
        for i, feedback in enumerate(experiences):
            first_name, last_name = self.generate_fake_name()
            
            Experience.objects.create(
                name=f"{first_name} {last_name}",
                feedback=feedback,
                rating=random.randint(1, 5),
                created_at=timezone.now() - timedelta(days=random.randint(0, 90))
            )
            self.stdout.write(f'Created experience {i+1}')

    def create_jobs(self):
        """Create 10 jobs"""
        self.stdout.write('Creating jobs...')
        
        jobs_data = [
            ('Cybersecurity Analyst', 'Full-time cybersecurity position focusing on threat detection'),
            ('Penetration Tester', 'Ethical hacking role for security assessment'),
            ('Web Developer', 'Frontend and backend web development position'),
            ('Data Scientist', 'Data analysis and machine learning specialist'),
            ('Network Security Engineer', 'Network infrastructure security role'),
            ('Software Developer', 'Full-stack software development position'),
            ('DevOps Engineer', 'Infrastructure automation and deployment'),
            ('Security Consultant', 'Client-facing security advisory role'),
            ('Research Assistant', 'Academic research in cybersecurity'),
            ('IT Support Specialist', 'Technical support and system administration')
        ]
        
        for i, (title, description) in enumerate(jobs_data):
            Job.objects.create(
                title=title,
                description=f'<p>{description}</p><p>{self.generate_lorem_text(40)}</p>',
                location=random.choice(['Remote', 'OnSite']),
                job_type=random.choice(['FT', 'PT', 'CT']),
                posted_date=timezone.now().date() - timedelta(days=random.randint(0, 30)),
                closing_date=timezone.now().date() + timedelta(days=random.randint(7, 60))
            )
            self.stdout.write(f'Created job: {title}')

    def create_job_applications(self):
        """Create 10 job applications"""
        self.stdout.write('Creating job applications...')
        
        jobs = list(Job.objects.all())
        
        for i in range(10):
            first_name, last_name = self.generate_fake_name()
            
            # Create dummy file content
            resume_content = ContentFile(b'Dummy resume content', name=f'resume_{i}.pdf')
            cover_letter_content = ContentFile(b'Dummy cover letter content', name=f'cover_letter_{i}.pdf')
            
            JobApplication.objects.create(
                job=random.choice(jobs),
                name=f"{first_name} {last_name}",
                email=self.generate_fake_email(first_name, last_name),
                resume=resume_content,
                cover_letter=cover_letter_content,
                applied_date=timezone.now() - timedelta(days=random.randint(0, 30))
            )
            self.stdout.write(f'Created job application {i+1}')

    def create_leader_board_tables(self):
        """Create 10 leaderboard entries"""
        self.stdout.write('Creating leaderboard entries...')
        
        User = get_user_model()
        users = list(User.objects.all())
        categories = ['Overall', 'Web Security', 'Network Security', 'Programming', 'Cybersecurity']
        
        for i in range(10):
            LeaderBoardTable.objects.create(
                user=random.choice(users),
                category=random.choice(categories),
                total_points=random.randint(50, 1000)
            )
            self.stdout.write(f'Created leaderboard entry {i+1}')

    def create_security_events(self):
        """Create 10 security events"""
        self.stdout.write('Creating security events...')
        
        User = get_user_model()
        users = list(User.objects.all())
        event_types = ['login_success', 'login_failure', 'password_change', 'account_locked', 'suspicious_activity']
        
        for i in range(10):
            SecurityEvent.objects.create(
                user=random.choice(users) if random.choice([True, False]) else None,
                event_type=random.choice(event_types),
                ip_address=f"192.168.1.{random.randint(1, 255)}",
                timestamp=timezone.now() - timedelta(days=random.randint(0, 30)),
                details=self.generate_lorem_text(15)
            )
            self.stdout.write(f'Created security event {i+1}')

    def create_user_blog_pages(self):
        """Create 10 user blog pages"""
        self.stdout.write('Creating user blog pages...')
        
        blog_titles = [
            'My Journey into Cybersecurity',
            'Learning Penetration Testing',
            'Web Development Best Practices',
            'Data Science and Security',
            'Network Security Fundamentals',
            'Python Programming Tips',
            'Virtual Reality in Education',
            'Policy Implementation Strategies',
            'Understanding Social Engineering',
            'Building Secure Applications'
        ]
        
        for i, title in enumerate(blog_titles):
            first_name, last_name = self.generate_fake_name()
            
            UserBlogPage.objects.create(
                name=f"{first_name} {last_name}",
                title=title,
                description=self.generate_lorem_text(50),
                file=None,  # Base64 image field - leaving empty for now
                created_at=timezone.now() - timedelta(days=random.randint(0, 60)),
                isShow=random.choice([True, False])
            )
            self.stdout.write(f'Created user blog page: {title}')

    def create_user_challenges(self):
        """Create 10 user challenges"""
        self.stdout.write('Creating user challenges...')
        
        User = get_user_model()
        users = list(User.objects.all())
        challenges = list(CyberChallenge.objects.all())
        
        for i in range(10):
            user = random.choice(users)
            challenge = random.choice(challenges)
            
            # Avoid duplicates
            if not UserChallenge.objects.filter(user=user, challenge=challenge).exists():
                UserChallenge.objects.create(
                    user=user,
                    challenge=challenge,
                    completed=random.choice([True, False]),
                    score=random.randint(0, challenge.points) if challenges else random.randint(0, 30)
                )
                self.stdout.write(f'Created user challenge {i+1}')

    def create_additional_models(self):
        """Create entries for additional models"""
        self.stdout.write('Creating additional model entries...')
        
        # Create DDT_contact entries
        for i in range(10):
            first_name, last_name = self.generate_fake_name()
            DDT_contact.objects.create(
                fullname=f"{first_name} {last_name}",
                email=self.generate_fake_email(first_name, last_name),
                mobile=f"04{random.randint(10000000, 99999999)}",
                message=self.generate_lorem_text(20)
            )
        
        # Create BlogPost entries
        for i in range(10):
            BlogPost.objects.create(
                title=f"Blog Post {i+1}: {self.generate_lorem_text(5)}",
                body=self.generate_lorem_text(100),
                page_name=random.choice(['AppAttack', 'PT-GUI', 'VR', 'Smishing', 'DTM']),
                created_at=timezone.now() - timedelta(days=random.randint(0, 30))
            )
        
        # Create Smishingdetection_join_us entries
        for i in range(10):
            first_name, last_name = self.generate_fake_name()
            Smishingdetection_join_us.objects.create(
                name=f"{first_name} {last_name}",
                email=self.generate_fake_email(first_name, last_name),
                message=self.generate_lorem_text(20)
            )
        
        # Create Projects_join_us entries
        for i in range(10):
            first_name, last_name = self.generate_fake_name()
            Projects_join_us.objects.create(
                name=f"{first_name} {last_name}",
                email=self.generate_fake_email(first_name, last_name),
                message=self.generate_lorem_text(20),
                page_name=random.choice(['AppAttack', 'PT-GUI', 'VR', 'Smishing', 'DTM'])
            )
        
        self.stdout.write('Created additional model entries')