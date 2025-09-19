# Generated manually - Comprehensive migration combining multiple updates

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        # ===== LEADERBOARD TABLE UPDATES =====
        migrations.AlterModelOptions(
            name='leaderboardtable',
            options={'ordering': ['-total_points', 'rank']},
        ),
        migrations.RunSQL(
            "ALTER TABLE home_leaderboardtable ADD COLUMN IF NOT EXISTS last_updated timestamp with time zone;",
            reverse_sql="ALTER TABLE home_leaderboardtable DROP COLUMN IF EXISTS last_updated;"
        ),
        migrations.RunSQL(
            "ALTER TABLE home_leaderboardtable ADD COLUMN IF NOT EXISTS rank integer DEFAULT 0 NOT NULL;",
            reverse_sql="ALTER TABLE home_leaderboardtable DROP COLUMN IF EXISTS rank;"
        ),
        migrations.AlterUniqueTogether(
            name='leaderboardtable',
            unique_together={('user', 'category')},
        ),
        
        # ===== PROJECT MODEL UPDATES =====
        # Note: archived field addition is handled conditionally to avoid conflicts
        migrations.RunSQL(
            "ALTER TABLE home_project ADD COLUMN IF NOT EXISTS archived boolean DEFAULT false NOT NULL;",
            reverse_sql="ALTER TABLE home_project DROP COLUMN IF EXISTS archived;"
        ),
        
        # ===== CYBERCHALLENGE MODEL UPDATES =====
        migrations.RunSQL(
            "ALTER TABLE home_cyberchallenge ADD COLUMN IF NOT EXISTS created_at timestamp with time zone;",
            reverse_sql="ALTER TABLE home_cyberchallenge DROP COLUMN IF EXISTS created_at;"
        ),
        migrations.RunSQL(
            "ALTER TABLE home_cyberchallenge ADD COLUMN IF NOT EXISTS is_active boolean DEFAULT true NOT NULL;",
            reverse_sql="ALTER TABLE home_cyberchallenge DROP COLUMN IF EXISTS is_active;"
        ),
        migrations.RunSQL(
            "ALTER TABLE home_cyberchallenge ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone;",
            reverse_sql="ALTER TABLE home_cyberchallenge DROP COLUMN IF EXISTS updated_at;"
        ),
        
        # ===== CODE EXECUTION MODELS =====
        migrations.CreateModel(
            name='CodeTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('basics', 'Python Basics'), ('data_structures', 'Data Structures'), ('algorithms', 'Algorithms'), ('oop', 'Object-Oriented Programming'), ('file_handling', 'File Handling'), ('web_scraping', 'Web Scraping'), ('data_analysis', 'Data Analysis'), ('machine_learning', 'Machine Learning'), ('security', 'Security'), ('networking', 'Networking')], max_length=20)),
                ('difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=15)),
                ('template_code', models.TextField()),
                ('expected_output', models.TextField(blank=True, null=True)),
                ('hints', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['category', 'difficulty', 'title'],
            },
        ),
        migrations.CreateModel(
            name='CompilerSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_execution_time', models.IntegerField(default=5)),
                ('max_memory_limit', models.IntegerField(default=128)),
                ('max_code_length', models.IntegerField(default=1000)),
                ('allowed_modules', models.JSONField(default=list)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CodeExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(default='python', max_length=20)),
                ('code', models.TextField()),
                ('input_data', models.TextField(blank=True, null=True)),
                ('output', models.TextField(blank=True, null=True)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('execution_time', models.FloatField(default=0.0)),
                ('memory_used', models.IntegerField(default=0)),
                ('is_successful', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CodeSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_code', models.TextField()),
                ('is_correct', models.BooleanField(default=False)),
                ('execution_time', models.FloatField(default=0.0)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.codetemplate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-submitted_at'],
                'unique_together': {('user', 'template')},
            },
        ),
    ]
