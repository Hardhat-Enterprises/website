# Generated by Django 4.2.14 on 2025-04-14 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_merge_20250414_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='APIModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('field_name', models.CharField(default='Default Value', max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserBlogPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
