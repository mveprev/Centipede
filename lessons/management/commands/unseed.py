from django.core.management.base import BaseCommand, CommandError
from lessons.models import UserManager, User, TermDates


class Command(BaseCommand):
    def handle(self, *args, **options):

        User.objects.filter(is_superuser=False).delete()
        TermDates.objects.all().delete()
