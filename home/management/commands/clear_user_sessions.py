import logging
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()
session_logger = logging.getLogger('session_security_logger')  # Unified audit logger

class Command(BaseCommand):
    help = 'Cleanup expired sessions or clear sessions for a specific user.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user-email',
            type=str,
            help='Email of the user whose sessions should be cleared'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Clear all expired sessions'
        )
        parser.add_argument(
            '--older-than-days',
            type=int,
            help='Only delete sessions expired more than N days ago'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Preview sessions that would be deleted without deleting them'
        )

    def handle(self, *args, **options):
        user_email = options.get('user_email')
        clear_all = options.get('all')
        older_than_days = options.get('older_than_days')
        dry_run = options.get('dry_run')

        if clear_all and user_email:
            self.stdout.write(self.style.ERROR(
                'Please provide only one of --user-email or --all.'
            ))
            return

        if clear_all:
            cutoff = now()
            if older_than_days:
                cutoff -= timedelta(days=older_than_days)

            expired_sessions = Session.objects.filter(expire_date__lt=cutoff)
            count = expired_sessions.count()

            if dry_run:
                self.stdout.write(self.style.WARNING(
                    f"[Dry Run] {count} expired sessions before {cutoff} would be deleted."
                ))
                session_logger.info(
                    f"Dry run: {count} expired sessions matched for deletion | cutoff={cutoff}"
                )
            else:
                expired_sessions.delete()
                self.stdout.write(self.style.SUCCESS(
                    f"Successfully deleted {count} expired sessions before {cutoff}."
                ))
                session_logger.info(
                    f"Deleted {count} expired sessions | cutoff={cutoff}"
                )
            return

        if user_email:
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"User with email {user_email} does not exist."
                ))
                session_logger.error(
                    f"Session cleanup failed: user not found | email={user_email}"
                )
                return

            matched_sessions, failures = self.get_user_sessions(user)
            count = len(matched_sessions)

            for session in matched_sessions:
                if dry_run:
                    session_logger.info(
                        f"Dry run: Session {session.session_key} would be deleted | user={user.email}"
                    )
                else:
                    session.delete()
                    session_logger.info(
                        f"Deleted session {session.session_key} | user={user.email}"
                    )

            if dry_run:
                self.stdout.write(self.style.WARNING(
                    f"[Dry Run] {count} sessions would be deleted for user {user.email}."
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"Successfully deleted {count} sessions for user {user.email}."
                ))

            if failures:
                self.stdout.write(self.style.WARNING(
                    f"{failures} sessions could not be decoded and were skipped."
                ))
            return

        self.stdout.write(self.style.ERROR(
            'Please provide either --user-email or --all option.'
        ))

    def get_user_sessions(self, user):
        """Return sessions matching the given user ID."""
        matched = []
        failures = 0
        for session in Session.objects.all():
            try:
                data = session.get_decoded()
                if str(user.id) == data.get('_auth_user_id'):
                    matched.append(session)
            except Exception as e:
                failures += 1
                session_logger.warning(
                    f"Failed to decode session {session.session_key} | error={e}"
                )
        return matched, failures