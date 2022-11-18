from django.core.management.base import BaseCommand, CommandError
from lessons.models import UserManager, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("The unseed command has not been implemented yet!")
        print("TO DO: Create an unseed command following the instructions of the assignment carefully.")


User.objects.filter(is_superuser=False).delete()
