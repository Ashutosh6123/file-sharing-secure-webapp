from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import MagicLoginToken

class Command(BaseCommand):
    help = 'Clean up expired magic login tokens'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Remove tokens older than this many days (default: 7)',
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        
        # Delete expired tokens
        expired_tokens = MagicLoginToken.objects.filter(expires_at__lt=timezone.now())
        expired_count = expired_tokens.count()
        expired_tokens.delete()
        
        # Delete old tokens (used or unused)
        old_tokens = MagicLoginToken.objects.filter(created_at__lt=cutoff_date)
        old_count = old_tokens.count()
        old_tokens.delete()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully cleaned up {expired_count} expired tokens and {old_count} old tokens'
            )
        )
