from django.core.management.base import BaseCommand
from home.views import leaderboard_update

class Command(BaseCommand):
    help = 'Update leaderboard with current user scores and rankings'

    def handle(self, *args, **options):
        self.stdout.write('Updating leaderboard...')
        try:
            leaderboard_update()
            self.stdout.write(
                self.style.SUCCESS('Successfully updated leaderboard rankings!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error updating leaderboard: {e}')
            )


