from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from home.models import UserDeletionRequest

class Command(BaseCommand):
    help = "Deletes user accounts that have been scheduled for deletion after 30 days"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_requests = UserDeletionRequest.objects.filter(
            scheduled_for__lte=now,
            is_executed=False
        )
        if not expired_requests.exists():
            self.stdout.write("No expired deletion requests to process.")
            return

        for deletion_request in expired_requests:
            user = deletion_request.user
            self.stdout.write(
                f"Deleting user {user.username} (scheduled for {deletion_request.scheduled_for})"
            )

            user.delete()  #user is deleted

            deletion_request.is_executed = True
            deletion_request.executed_at = now
            deletion_request.save()

        self.stdout.write(self.style.SUCCESS("Expired accounts deletion task complete."))