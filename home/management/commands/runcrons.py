from __future__ import print_function
import traceback
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import close_old_connections

from django_cron import CronJobManager, get_class, get_current_time
from django_cron.models import CronJobLog

DEFAULT_LOCK_TIME = 24 * 60 * 60  # 24 hours setup


class Command(BaseCommand):
    help = "Runs the cron jobs defined in CRON_CLASSES in settings.py"

    def add_arguments(self, parser):
        parser.add_argument('cron_classes', nargs='*', help="Specific cron classes to run")
        parser.add_argument('--force', action='store_true', help="Force cron runs even if not scheduled")
        parser.add_argument(
            '--silent', action='store_true', help="Suppress console output"
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help="Do not actually run crons, just simulate",
        )

    def handle(self, *args, **options):
        """
        Iterates over all the CRON_CLASSES (or the ones passed in as arguments)
        and executes them.
        """
        if not options['silent']:
            self.stdout.write("Running Crons\n")
            self.stdout.write("=" * 40)

        # Initialize cron classes
        cron_classes = options.get('cron_classes', [])
        cron_class_names = cron_classes or getattr(settings, 'CRON_CLASSES', [])

        # Debug: Print detected CRON_CLASSES
        if not options['silent']:
            self.stdout.write(f"Detected CRON_CLASSES: {cron_class_names}")

        try:
            # Load cron classes
            crons_to_run = [get_class(x) for x in cron_class_names]
            if not options['silent']:
                self.stdout.write(f"Loaded cron jobs: {crons_to_run}")
        except ImportError:
            error = traceback.format_exc()
            self.stderr.write(
                f"ERROR: Invalid cron class names: {cron_class_names}\n{error}"
            )
            return

        for cron_class in crons_to_run:
            try:
                if not options['silent']:
                    self.stdout.write(f"Running cron job: {cron_class}")
                run_cron_with_cache_check(
                    cron_class,
                    force=options['force'],
                    silent=options['silent'],
                    dry_run=options['dry_run'],
                    stdout=self.stdout,
                )
            except Exception as e:
                self.stderr.write(f"ERROR: Cron job {cron_class} failed with error: {str(e)}\n{traceback.format_exc()}")

        # Clear old log entries and close database connections
        clear_old_log_entries()
        close_old_connections()

#run_cron_with_cache_check
def run_cron_with_cache_check(
    cron_class, force=False, silent=False, dry_run=False, stdout=None
):
    """
    Runs the cron job with a cache check.

    :param cron_class: The cron class to run.
    :param force: Force execution even if not scheduled.
    :param silent: Suppress output if True.
    :param dry_run: Simulate execution without running the job.
    :param stdout: Console output stream.
    """
    with CronJobManager(
        cron_class, silent=silent, dry_run=dry_run, stdout=stdout
    ) as manager:
        manager.run(force)


def clear_old_log_entries():
    """
   # Removes old log entries based on the DJANGO_CRON_DELETE_LOGS_OLDER_THAN setting.
    """
    if hasattr(settings, 'DJANGO_CRON_DELETE_LOGS_OLDER_THAN'):
        delta = timedelta(days=settings.DJANGO_CRON_DELETE_LOGS_OLDER_THAN)
        old_logs = CronJobLog.objects.filter(end_time__lt=get_current_time() - delta)
        count = old_logs.count()
        old_logs.delete()
        print("Cleared {count} cron job logs older than {delta.days} days..")

