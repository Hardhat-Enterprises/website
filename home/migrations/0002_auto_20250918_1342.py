from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        # Add the missing 'archived' column to Project
        migrations.AddField(
            model_name='project',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        # Create the missing 'Tip' model/table
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
