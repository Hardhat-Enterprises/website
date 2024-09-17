from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ("home", "0021_merge_20240522_0413"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "feedback_type",
                    models.CharField(
                        max_length=20,
                        choices=[
                            ("general", "General Feedback"),
                            ("bug", "Bug Report"),
                            ("improvement", "Improvement Suggestion"),
                            ("feature", "Request for a feature"),
                        ],
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL,
                        on_delete=django.db.models.deletion.CASCADE,
                        null=True,
                        blank=True,
                    ),
                ),
            ],
        ),
    ]
