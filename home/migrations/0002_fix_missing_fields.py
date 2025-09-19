# Generated manually to fix all missing database fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        # Add missing archived field to Project model
        migrations.AddField(
            model_name='project',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='archived'),
        ),
        
        # Ensure CyberChallenge has all required fields
        migrations.AddField(
            model_name='cyberchallenge',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        
        migrations.AddField(
            model_name='cyberchallenge',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        
        migrations.AddField(
            model_name='cyberchallenge',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
