from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import faker.providers
from lessons.models import UserManager, User, Lesson
import random
from django.contrib.auth.hashers import make_password


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

DURATIONS = [
    30,
    45,
    60,
]

DESIRED_INTERVALS = [
    1,
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

    def lesson_durations(self):
        return self.random_element(DURATIONS)


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')
        self.faker.add_provider(Provider)


# Function to create and input the dummy data.

    def handle(self, *args, **options):
        # print("The seed command has not been implemented yet!")
        # print("TO DO: Create a seed command following the instructions of the assignment carefully.")
        #
        # print(self.faker.address())
        # print(self.faker.ascii_free_email())
        # print(self.faker.music_school_instruments())

        password_data = make_password('Password123')

        john = User.objects.create(email="john.doe@example.org", password=password_data, first_name="John",
                                   last_name="Doe")
        Lesson.objects.create(availability=10, lessons=2, desiredInterval=1, duration=30, furtherInfo="I want to learn piano",
                              id=10, user=john, is_confirmed=False)
        Lesson.objects.create(availability=10, lessons=2, desiredInterval=1, duration=30, furtherInfo="I want to learn guitar",
                              id=12, user=john, is_confirmed=False)

        # User.objects.create(email="john.doe@example.org", password=password_data, first_name="John",
        #                     last_name="Doe")

        User.objects.create(email="petra.pickles@example.org", password=password_data,
                            first_name="Petra", last_name="Pickles", is_staff=True)
        User.objects.create(email="marty.major@example.org", password=password_data,  first_name="Marty",
                            last_name="Major", is_staff=True, is_superuser=True)

        for _ in range(0, 97):

            password_data_general = self.faker.password(
                length=11, special_chars=True, upper_case=True)

            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = first_name.lower() + "-" + last_name.lower() + \
                "@" + self.faker.free_email_domain()

            new_User = User.objects.create(email=email, first_name=first_name, password=password_data,
                                           last_name=last_name)

            Lesson.objects.create(availability=10, lessons=5, desiredInterval=1, duration=self.faker.lesson_durations(), furtherInfo="I want to learn " + self.faker.music_school_instruments()
                                  + ". ", id=self.faker.unique.random_int(), user=new_User, is_confirmed=False)
