from django.core.management.base import BaseCommand
from Elo.models import Player
from django.db import transaction

class Command(BaseCommand):
    help = 'Updates the last_week_ranking for all players. Run this every Monday at 00:00.'

    def handle(self, *args, **options):
        # We need to save the current_ranking to last_week_ranking
        players = Player.objects.all()
        
        with transaction.atomic():
            for player in players:
                # current_ranking dynamically computes their rank
                player.last_week_ranking = player.current_ranking
                player.save(update_fields=['last_week_ranking'])

        self.stdout.write(self.style.SUCCESS('Successfully updated last_week_ranking for all players.'))
