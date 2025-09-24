from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from home.models import (
    Announcement, Article, ContactSubmission, Contact, Course, CyberChallenge,
    Experience, JobApplication, Job, LeaderBoardTable, Project, SecurityEvent,
    Skill, Student, UserBlogPage, UserChallenge, DDT_contact, Progress,
    Profile, Passkey, BlogPost, Smishingdetection_join_us, Projects_join_us,
    AdminNotification, APIModel, Folder, VaultDocument, PasswordHistory,
    Webpage, TeamMember, JobAlert, GraduateProgram, CareerFAQ, Quiz,
    QuizQuestion, QuizAttempt, QuizAnswer, Report, AppAttackReport,
    PenTestingRequest, SecureCodeReviewRequest, AdminSession, Resource, Tip,
    TipRotationState, UserDeletionRequest, UserDevice
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
        self.create_profiles_and_password_history()

        # Content and notifications
        self.create_announcements()
        self.create_admin_notifications()
        self.create_articles()
        self.create_contact_submissions()
        self.create_contacts()
        self.create_team_members()
        self.create_reports()
        self.create_api_models()
        self.create_webpages()
        self.create_folders_and_vault_documents()

        # Challenges and quizzes
        self.create_cyber_challenges()
        self.create_quizzes()
        self.create_experiences()

        # Jobs and programs
        self.create_jobs()
        self.create_job_alerts()
        self.create_job_applications()
        self.create_graduate_programs()
        self.create_career_faqs()

        # Leaderboard & events
        self.create_leader_board_tables()
        self.create_security_events()

        # Blog and user challenge progress
        self.create_user_blog_pages()
        self.create_user_challenges()

        # Reports and requests
        self.create_appattack_reports()
        self.create_pen_and_secure_code_requests()

        # Admin sessions, resources, tips
        self.create_admin_sessions()
        self.create_resources()
        self.create_tips_and_rotation()

        # Devices and deletion requests
        self.create_user_devices()
        self.create_user_deletion_requests()

        # Misc additional
        self.create_additional_models()

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))

    def clear_data(self):
        """Clear existing data from all models"""
        models_to_clear = [
            # Dependent/child records first
            QuizAnswer, QuizAttempt, QuizQuestion, UserChallenge, Progress,
            JobApplication, LeaderBoardTable, SecurityEvent, Article,
            UserBlogPage, Experience, ContactSubmission, Contact, Report,
            AdminSession, PasswordHistory, VaultDocument, Folder,
            TipRotationState, Tip, Resource, BlogPost,
            AppAttackReport, PenTestingRequest, SecureCodeReviewRequest,
            TeamMember, JobAlert, CareerFAQ, GraduateProgram, Webpage,
            APIModel, AdminNotification,
            # Core domain
            CyberChallenge, Quiz, Job, Announcement, Course, Project, Skill,
            # Misc join-us/contact
            DDT_contact, Smishingdetection_join_us, Projects_join_us,
            # User-related auxiliaries
            Profile, UserDevice, UserDeletionRequest, Passkey,
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

        # Ensure at least one staff/superuser exists for admin flows
        if not User.objects.filter(is_staff=True).exists():
            admin_email = 'admin@example.com'
            if not User.objects.filter(email=admin_email).exists():
                admin = User.objects.create_superuser(
                    email=admin_email,
                    password='adminpassword123',
                    first_name='Admin',
                    last_name='User'
                )
                self.stdout.write(f'Created superuser: {admin.email}')
            else:
                admin = User.objects.get(email=admin_email)
                admin.is_staff = True
                admin.is_superuser = True
                admin.save(update_fields=["is_staff", "is_superuser"])
                self.stdout.write(f'Ensured staff/superuser: {admin.email}')

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

    def create_profiles_and_password_history(self):
        """Create Profile and PasswordHistory entries for users"""
        self.stdout.write('Creating profiles and password history...')
        User = get_user_model()
        for user in User.objects.all():
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user, bio=self.generate_lorem_text(20))
            if not PasswordHistory.objects.filter(user=user).exists():
                PasswordHistory.objects.create(user=user, encoded_password=user.password)

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

    def create_admin_notifications(self):
        self.stdout.write('Creating admin notifications...')
        User = get_user_model()
        users = list(User.objects.all())
        types = ['feedback', 'update', 'alert', 'info']
        for i in range(8):
            AdminNotification.objects.create(
                title=f"Notification {i+1}",
                message=self.generate_lorem_text(25),
                notification_type=random.choice(types),
                related_user=random.choice(users) if users and random.choice([True, False]) else None
            )
        self.stdout.write('Created admin notifications')

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

    def create_api_models(self):
        self.stdout.write('Creating API models...')
        for i in range(5):
            APIModel.objects.get_or_create(
                name=f"API {i+1}",
                defaults={
                    'field_name': 'Default Value',
                    'description': self.generate_lorem_text(30)
                }
            )

    def create_webpages(self):
        self.stdout.write('Creating webpages...')
        for i in range(5):
            Webpage.objects.get_or_create(
                title=f"Page {i+1}",
                defaults={
                    'url': f"/page-{i+1}/"
                }
            )

    def create_folders_and_vault_documents(self):
        self.stdout.write('Creating folders and vault documents...')
        User = get_user_model()
        users = list(User.objects.all()[:5])
        for user in users:
            folder, _ = Folder.objects.get_or_create(name="My Docs", owner=user, parent=None)
            # Create a small text file in vault
            file_content = ContentFile(b"Sample vault document content", name=f"doc-{user.id}.txt")
            VaultDocument.objects.create(
                file=file_content,
                original_name=f"Document for {user.email}",
                content_type="text/plain",
                size_bytes=file_content.size,
                description="Auto generated test document",
                visibility=VaultDocument.VIS_PUBLIC,
                uploaded_by=user,
            )

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

    def create_team_members(self):
        """Create a few team members"""
        self.stdout.write('Creating team members...')
        members = [
            ('Alice Johnson', 'Security Analyst'),
            ('Bob Smith', 'Penetration Tester'),
            ('Carol Davis', 'Software Engineer'),
            ('Dan Brown', 'Data Scientist'),
        ]
        for name, role in members:
            if not TeamMember.objects.filter(name=name).exists():
                img = ContentFile(b"fake image bytes", name=f"{name.split()[0].lower()}.jpg")
                TeamMember.objects.create(name=name, role=role, image=img)
        
    def create_reports(self):
        """Create a few moderation reports"""
        self.stdout.write('Creating reports...')
        for i in range(5):
            Report.objects.create(
                blog_id=i+1,
                blog_name=f"Blog {i+1}",
                reason=self.generate_lorem_text(15),
                created_at=timezone.now() - timedelta(days=random.randint(0, 20))
            )

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

    def create_job_alerts(self):
        self.stdout.write('Creating job alerts...')
        for i in range(5):
            email = f"jobalert{i+1}@example.com"
            JobAlert.objects.get_or_create(email=email)

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

    def create_quizzes(self):
        self.stdout.write('Creating quizzes and questions...')
        quizzes_data = [
            ("Network Fundamentals", 'network'),
            ("Web Security Basics", 'web'),
            ("Crypto 101", 'crypto'),
            ("General Awareness", 'general'),
        ]
        quizzes = []
        for title, category in quizzes_data:
            quiz, _ = Quiz.objects.get_or_create(
                title=title,
                category=category,
                defaults={'description': self.generate_lorem_text(25), 'is_active': True}
            )
            quizzes.append(quiz)
            if quiz.questions.count() == 0:
                for i in range(5):
                    correct = random.choice(['a', 'b', 'c', 'd'])
                    QuizQuestion.objects.create(
                        quiz=quiz,
                        question_text=f"{title} Q{i+1}: {self.generate_lorem_text(8)}?",
                        option_a="Option A",
                        option_b="Option B",
                        option_c="Option C",
                        option_d="Option D",
                        correct_answer=correct,
                        difficulty=random.choice(['easy','medium','hard']),
                        points=10,
                        explanation=self.generate_lorem_text(12)
                    )
        # Create attempts for a few users
        User = get_user_model()
        users = list(User.objects.all()[:5])
        for user in users:
            quiz = random.choice(quizzes)
            attempt = QuizAttempt.objects.create(user=user, quiz=quiz, max_possible_score=quiz.questions.count()*10)
            total = 0
            for q in quiz.questions.all():
                selected = random.choice(['a','b','c','d'])
                correct = selected == q.correct_answer
                pts = 10 if correct else 0
                QuizAnswer.objects.create(
                    attempt=attempt,
                    question=q,
                    selected_answer=selected,
                    is_correct=correct,
                    points_earned=pts
                )
                total += pts
            attempt.total_score = total
            attempt.is_completed = True
            attempt.save(update_fields=['total_score','is_completed'])

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

    def create_graduate_programs(self):
        self.stdout.write('Creating graduate programs...')
        programs = [
            ("Cybersecurity Graduate Program", 'cybersecurity'),
            ("Software Engineering Graduate Program", 'software_engineering'),
            ("Data Science Graduate Program", 'data_science'),
        ]
        for title, prog_type in programs:
            GraduateProgram.objects.get_or_create(
                title=title,
                defaults={
                    'description': self.generate_lorem_text(40),
                    'duration_months': random.choice([6,12,18]),
                    'program_type': prog_type,
                    'start_date': timezone.now().date() + timedelta(days=30),
                    'application_deadline': timezone.now().date() + timedelta(days=60),
                    'is_active': True,
                    'overview': self.generate_lorem_text(60),
                    'curriculum': self.generate_lorem_text(60),
                    'benefits': self.generate_lorem_text(40),
                    'requirements': self.generate_lorem_text(40),
                    'application_process': self.generate_lorem_text(30),
                }
            )

    def create_career_faqs(self):
        self.stdout.write('Creating career FAQs...')
        faqs = [
            ("How do I apply?", 'application'),
            ("What are the benefits?", 'benefits'),
            ("How can I grow?", 'growth'),
            ("General info", 'general'),
        ]
        for i, (q, cat) in enumerate(faqs, start=1):
            CareerFAQ.objects.get_or_create(
                question=q,
                defaults={'answer': self.generate_lorem_text(30), 'category': cat, 'order': i}
            )

    def create_appattack_reports(self):
        self.stdout.write('Creating AppAttack reports...')
        for year in [2023, 2024]:
            content = ContentFile(b"PDF content placeholder", name=f"appattack_{year}.pdf")
            AppAttackReport.objects.get_or_create(
                year=year,
                title=f"AppAttack Report {year}",
                defaults={'pdf': content}
            )

    def create_pen_and_secure_code_requests(self):
        self.stdout.write('Creating pentesting and secure code requests...')
        for i in range(5):
            PenTestingRequest.objects.create(
                name=f"Requester {i+1}",
                email=f"pentest{i+1}@example.com",
                github_repo_link="https://github.com/example/repo",
                project_description=self.generate_lorem_text(20),
                terms_accepted=True,
            )
            SecureCodeReviewRequest.objects.create(
                name=f"SCR {i+1}",
                email=f"scr{i+1}@example.com",
                github_repo_link="https://github.com/example/scr",
                project_description=self.generate_lorem_text(20),
                terms_accepted=True,
            )

    def create_admin_sessions(self):
        self.stdout.write('Creating admin sessions...')
        User = get_user_model()
        admins = list(User.objects.filter(is_staff=True)[:2]) or list(User.objects.all()[:2])
        for user in admins:
            AdminSession.objects.get_or_create(
                user=user,
                session_key=str(uuid.uuid4()).replace('-', '')[:40],
                defaults={
                    'ip_address': f"10.0.0.{random.randint(2,254)}",
                    'user_agent': 'Mozilla/5.0 (Test Agent)',
                    'is_active': True,
                }
            )

    def create_resources(self):
        self.stdout.write('Creating resources...')
        for i in range(3):
            title = f"Resource {i+1}"
            content = ContentFile(b"Example resource file", name=f"resource_{i+1}.txt")
            Resource.objects.get_or_create(
                title=title,
                defaults={
                    'summary': self.generate_lorem_text(25),
                    'category': Resource.Category.OTHER,
                    'file': content,
                    'is_published': True,
                }
            )

    def create_tips_and_rotation(self):
        self.stdout.write('Creating daily tips and rotation state...')
        tips = [
            "Use strong, unique passwords.",
            "Enable two-factor authentication.",
            "Beware of phishing emails.",
            "Keep your software updated.",
            "Use a password manager.",
            "Verify website certificates.",
            "Backup important data regularly.",
            "Avoid public Wi-Fi for sensitive tasks.",
            "Review app permissions.",
            "Lock your devices when not in use.",
        ]
        for t in tips:
            Tip.objects.get_or_create(text=t)
        TipRotationState.objects.get_or_create(lock="default")

    def create_user_devices(self):
        self.stdout.write('Creating user devices...')
        User = get_user_model()
        for user in User.objects.all():
            UserDevice.objects.get_or_create(
                user=user,
                device_fingerprint=str(uuid.uuid4()),
                defaults={
                    'device_name': 'Chrome on macOS',
                    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X)',
                    'ip_address': f"172.16.0.{random.randint(2,254)}",
                }
            )

    def create_user_deletion_requests(self):
        self.stdout.write('Creating user deletion requests...')
        User = get_user_model()
        candidates = list(User.objects.all()[:1])
        for user in candidates:
            if not hasattr(user, 'deletion_request'):
                UserDeletionRequest.objects.create(
                    user=user,
                    scheduled_for=timezone.now() + timedelta(days=30)
                )
