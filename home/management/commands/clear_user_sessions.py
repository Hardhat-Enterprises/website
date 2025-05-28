from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Clear sessions for specific users or all expired sessions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            help='Email of the user whose sessions should be cleared',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Clear all expired sessions',
        )

    def handle(self, *args, **options):
        if options['all']:
            # Clear all expired sessions
            expired = Session.objects.filter(expire_date__lt=now())
            count = expired.count()
            expired.delete()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully cleared {count} expired sessions')
            )
            return

        if options['user_email']:
            try:
                user = User.objects.get(email=options['user_email'])
                # Clear all sessions for the user
                sessions = Session.objects.filter(expire_date__gte=now())
                count = 0
                for session in sessions:
                    if str(user.id) == session.get_decoded().get('_auth_user_id'):
                        session.delete()
                        count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully cleared {count} sessions for user {user.email}')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User with email {options["user_email"]} does not exist')
                )
        else:
            self.stdout.write(
                self.style.ERROR('Please provide either --user-email or --all option')
            ) 