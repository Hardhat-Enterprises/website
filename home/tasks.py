from datetime import timedelta
from home.models import ExampleModel
from django_cron import CronJobBase, Schedule
from django.utils import timezone

#class for runing cron job
class CleanStaleRecordsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Run daily
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'home.clean_stale_records_cron_job'  # Unique identifier for this cron job

    def do(self):
        try:
            print("Executing CleanStaleRecordsCronJob...")

            # Calculate the stale threshold
            stale_threshold = timezone.now() - timedelta(days=30)
            print(f"Stale threshold: {stale_threshold}")

            # Fetch stale records
            stale_records = ExampleModel.objects.filter(updated_at__lt=stale_threshold)
            print(f"Found {stale_records.count()} stale records.")

            # Delete stale records
            deleted_count, _ = stale_records.delete()
            print(f"Cleaned {deleted_count} stale records.")

            return f"Successfully cleaned {deleted_count} stale records."
        except Exception as e:
            print(f"Error in cron job: {e}")
            raise
