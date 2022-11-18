from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import faker.providers
from lessons.models import UserManager, User
import random


# Instruments that can be selected by students/customers.
INSTRUMENTS = [
    "Piano",
    "Drums",
    "Flute",
    "Violin",
    "Bass Guitar",
    "Guitar",
    "Electric Guitar",
    "Saxophone",
    "Trumpet",
    "Harp",
    "Xylophone",
    "Cello",
    "Harmonica",
    "Clarinet",
    "Banjo",
    "Trombone",
]

# email address
# first name
# last name
# password
# role -> student, administrator, director
#


class Provider(faker.providers.BaseProvider):
    def music_school_instruments(self):
        return self.random_element(INSTRUMENTS)


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        self.faker.add_provider(Provider)

    def handle(self, *args, **options):
        # print("The seed command has not been implemented yet!")
        # print("TO DO: Create a seed command following the instructions of the assignment carefully.")
        #
        # print(self.faker.address())
        # print(self.faker.ascii_free_email())
        # print(self.faker.music_school_instruments())

        User.objects.create(email="john.doe@example.org", first_name="John",
                            last_name="Doe")
        User.objects.create(email="petra.pickles@example.org",
                            first_name="Petra", last_name="Pickles", is_staff=True)
        User.objects.create(email="marty.major@example.org",  first_name="Marty",
                            last_name="Major", is_staff=True, is_superuser=True)

        for _ in range(0, 97):
            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = first_name.lower() + "-" + last_name.lower() + \
                "@" + self.faker.free_email_domain()

            User.objects.create(email=email, first_name=first_name,
                                last_name=last_name)
