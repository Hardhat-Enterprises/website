# Generated by Django 5.0.4 on 2024-09-19 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_remove_project_code_alter_feedback_feedback_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='code',
        ),
        migrations.AddField(
            model_name='userchallenge',
            name='page_name',
            field=models.CharField(default=0, max_length=100),
        ),
    ]
