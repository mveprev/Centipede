from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import faker.providers
from lessons.models import UserManager, User, Lesson, TermDates, Children, Schedule, Payment
from lessons.forms import ScheduleForm
import random
import datetime
from datetime import date, time, timedelta
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

LESSON_INTERVALS = [
    7,
    14,
    30,

]

TERMS = [
    1,
    2,
    3,
    4,
    5,
    6
]

LESSON_NUMBER = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
]

TIME_NUMBER = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12
]

PAYMENTS = [
    10,
    20,
    30,
    40,
    50,
    60,
    70,
    80,
    90,
    100,
    125,
    150,
    175,
    200,
]

TEACHERS = [
    1,
    2,
    3,
    4,
    5,
]

HOUR = [
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
]

MINUTES = [
    00,
    15,
    30,
    45,
]

DATES = [
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
]


class Provider(faker.providers.BaseProvider):
    def music_school_instruments(self):
        return self.random_element(INSTRUMENTS)

    def lesson_durations(self):
        return self.random_element(DURATIONS)

    def lesson_terms(self):
        return self.random_element(TERMS)

    def lesson_number(self):
        return self.random_element(LESSON_NUMBER)

    def lesson_intervals(self):
        return self.random_element(LESSON_INTERVALS)

    def time_number(self):
        return self.random_element(TIME_NUMBER)

    def lesson_payments(self):
        return self.random_element(PAYMENTS)

    def lesson_teachers(self):
        return self.random_element(TEACHERS)

    def lesson_hours(self):
        return self.random_element(HOUR)

    def lesson_minutes(self):
        return self.random_element(MINUTES)

    def lesson_dates(self):
        return self.random_element(DATES)


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

        # Model account passwords
        password_data = make_password('Password123')

        # Model Term Dates
        term0 = TermDates.objects.create(
            name="Term 0",
            start_date=datetime.date(2022, 12, 1),
            end_date=datetime.date(2022, 12, 12),
        )

        term1 = TermDates.objects.create(
            name="Term 1",
            start_date=datetime.date(2022, 12, 13),
            end_date=datetime.date(2022, 12, 30),
        )

        term2 = TermDates.objects.create(
            name="Term 2",
            start_date=datetime.date(2023, 2, 13),
            end_date=datetime.date(2023, 5, 30),
        )

        term3 = TermDates.objects.create(
            name="Term 3",
            start_date=datetime.date(2023, 6, 1),
            end_date=datetime.date(2023, 7, 30),
        )

        term4 = TermDates.objects.create(
            name="Term 4",
            start_date=datetime.date(2023, 8, 13),
            end_date=datetime.date(2023, 9, 30),
        )

        term5 = TermDates.objects.create(
            name="Term 5",
            start_date=datetime.date(2023, 10, 13),
            end_date=datetime.date(2023, 11, 30),
        )

        term6 = TermDates.objects.create(
            name="Term 6",
            start_date=datetime.date(2023, 12, 13),
            end_date=datetime.date(2024, 1, 30),
        )

        # Model Teacher

        teacher1 = User.objects.create(
            email="paul.smith@example.org",
            password=password_data,
            first_name="Paul",
            last_name="Smith",
            is_teacher=True,
        )

        teacher2 = User.objects.create(
            email="laura.slater@example.org",
            password=password_data,
            first_name="Laura",
            last_name="Slater",
            is_teacher=True,
        )

        teacher3 = User.objects.create(
            email="norma.noe@example.org",
            password=password_data,
            first_name="Norma",
            last_name="Noe",
            is_teacher=True,
        )

        teacher4 = User.objects.create(
            email="lee.roberts@example.org",
            password=password_data,
            first_name="Lee",
            last_name="Robber",
            is_teacher=True,
        )

        teacher5 = User.objects.create(
            email="dwayne.johnson@example.org",
            password=password_data,
            first_name="Dwayne",
            last_name="Johnson",
            is_teacher=True,
        )

        # Creation of default accounts per handbook
        john = User.objects.create(
            email="john.doe@example.org",
            password=password_data,
            first_name="John",
            last_name="Doe",
        )

        User.objects.create(
            email="petra.pickles@example.org",
            password=password_data,
            first_name="Petra",
            last_name="Pickles",
            is_staff=True,
        )

        User.objects.create(
            email="marty.major@example.org",
            password=password_data,
            first_name="Marty",
            last_name="Major",
            is_staff=True,
            is_superuser=True
        )

        # Creation of John Doe's child's account and linking child to John Doe.

        alice = User.objects.create(
            email="alice.doe@example.org",
            password=password_data,
            first_name="Alice",
            last_name="Doe",
        )

        aliceChildren = Children.objects.create(
            first_name=alice.first_name,
            last_name=alice.last_name,
            age=17,
            email=alice.email,
            id=alice.pk,
            parent=john,
        )

        # Creation of John Doe's child without an account

        bobChildren = Children.objects.create(
            first_name="Bob",
            last_name="Doe",
            age=12,
            id=self.faker.unique.random_int(),
            parent=john,
        )

        now = datetime.datetime.now()

        johnDoePastLesson = Lesson.objects.create(
            term=term0,
            mondayMorning=True,
            lessons=1,
            desiredInterval=7,
            duration=30,
            furtherInfo="I want to learn piano",
            id=17,
            user=john,
            is_confirmed=True,
            invoiceNum=(str(john.pk)[:4]).zfill(4) + "-" + (str(0)[:4]).zfill(4),
            studentNum=(str(john.pk)[:4]).zfill(4),
            invoiceEmail=john.email,
        )

        Schedule.objects.create(
            teacher=teacher3,
            lesson=johnDoePastLesson,
            start_time=time(8, 30, 00),
            start_date=term0.start_date,
            interval=johnDoePastLesson.desiredInterval,
            number_of_lessons=johnDoePastLesson.lessons,
            duration=johnDoePastLesson.duration,
        )
        # Updating Payment View for John Doe

        johnPastPayment = Payment.objects.create(
            student=john,
            amount_paid=30,
            balance_before=-30,
            balance_after=0,
        )

        john.outstanding_balance = johnPastPayment.balance_after
        john.save()

        # Creation of lesson for deafult user John Doe

        johnDoeLesson = Lesson.objects.create(
            term=term1,
            mondayMorning=True,
            lessons=2,
            desiredInterval=7,
            duration=30,
            furtherInfo="I want to learn piano",
            id=10,
            user=john,
            is_confirmed=True,
            invoiceNum=(str(john.pk)[:4]).zfill(4) + "-" + (str(1)[:4]).zfill(4),
            studentNum=(str(john.pk)[:4]).zfill(4),
            invoiceEmail=john.email,
        )

        # Creation of Schedule for John Doe
        Schedule.objects.create(
            teacher=teacher3,
            lesson=johnDoeLesson,
            start_time=time(8, 30, 00),
            start_date=term1.start_date,
            interval=johnDoeLesson.desiredInterval,
            number_of_lessons=johnDoeLesson.lessons,
            duration=johnDoeLesson.duration,
        )
        # Updating Payment View for John Doe

        johnPayment = Payment.objects.create(
            student=john,
            amount_paid=10,
            balance_before=-60,
            balance_after=-50,
        )

        john.outstanding_balance += johnPayment.balance_after
        john.save()

        # Creation of lesson for John Doe's children user Alice Doe and non-user Bob Doe

        Lesson.objects.create(
            term=term1,
            tuesdayMorning=True,
            lessons=2,
            desiredInterval=7,
            duration=45,
            furtherInfo="I want to learn piano",
            id=11,
            user=john,
            children=aliceChildren,
            is_confirmed=False,
            invoiceNum=(str(john.pk)[:4]).zfill(4) + "-" + (str(3)[:4]).zfill(4),
            studentNum=(str(alice.pk)[:4]).zfill(4),
            invoiceEmail=john.email,
        )

        pastAliceLesson = Lesson.objects.create(
            term=term0,
            tuesdayMorning=True,
            lessons=1,
            desiredInterval=30,
            duration=45,
            furtherInfo="I want to learn piano",
            id=8,
            user=john,
            children=aliceChildren,
            is_confirmed=True,
            invoiceNum=(str(alice.pk)[:4]).zfill(4) + "-" + (str(2)[:4]).zfill(4),
            studentNum=(str(alice.pk)[:4]).zfill(4),
            invoiceEmail=alice.email,
        )

        Schedule.objects.create(
            # time_stamp=models.DateTimeField(auto_now=True),
            teacher=teacher3,
            lesson=pastAliceLesson,
            start_time=time(10, 30, 00),
            start_date=term0.start_date,
            interval=pastAliceLesson.desiredInterval,
            number_of_lessons=pastAliceLesson.lessons,
            duration=pastAliceLesson.duration,
        )

        # Updating Payment View for Alice Doe

        alicePayment = Payment.objects.create(
            student=alice,
            amount_paid=45,
            balance_before=-45,
            balance_after=0,
        )

        alice.outstanding_balance = alicePayment.balance_after
        alice.save()

    # Creation of past Lesson for Bob Doee

        pastBobLesson = Lesson.objects.create(
            term=term0,
            mondayMorning=True,
            lessons=1,
            desiredInterval=30,
            duration=30,
            furtherInfo="I want to learn piano",
            id=12,
            user=john,
            children=bobChildren,
            is_confirmed=True,
            invoiceNum=(str(john.pk)[:4]).zfill(4) + "-" + (str(1)[:4]).zfill(4),
            studentNum=(str(john.pk)[:4]).zfill(4),
            invoiceEmail=john.email,
        )

        Schedule.objects.create(
            teacher=teacher1,
            lesson=pastBobLesson,
            start_time=time(8, 30, 00),
            start_date=term0.start_date,
            interval=pastBobLesson.desiredInterval,
            number_of_lessons=pastBobLesson.lessons,
            duration=pastBobLesson.duration,
        )

        # Updating Payment View for John Doe on behalf of Bob Doe

        Payment.objects.create(
            student=john,
            amount_paid=30,
            balance_before=-30,
            balance_after=0,
        )

        john.outstanding_balance += johnPayment.balance_after
        john.save()

        # Creation of random users and data using faker.

        # Function to determine the term of the lesson booked for seeded users.

        def termGenerator(self, termNumber):
            if termNumber == 1:
                return term1
            elif termNumber == 2:
                return term2
            elif termNumber == 3:
                return term3
            elif termNumber == 4:
                return term4
            elif termNumber == 5:
                return term5
            elif termNumber == 6:
                return term6

        # Matching function to determine the availability of the seeded users.

        def timeGenerator(self, timeNumber):

            fakeNumber = self.faker.time_number()

            if timeNumber == fakeNumber:
                return True
            else:
                return False

        # Matching function to determine the teacher of the seeded users.
        def teacherGenerator(self, teacherNumber):
            if teacherNumber == 1:
                return teacher1
            elif teacherNumber == 2:
                return teacher2
            elif teacherNumber == 3:
                return teacher3
            elif teacherNumber == 4:
                return teacher4
            elif teacherNumber == 5:
                return teacher5

        # Function to ensure lesson booking times don't clash for seeded users.

        # Creation of seeded users without confirmed lessons and payments.

        for _ in range(0, 43):

            # password_data_general = self.faker.password(
            #     length=11, special_chars=True, upper_case=True)

            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = first_name.lower() + "-" + last_name.lower() + \
                "@" + self.faker.free_email_domain()

            newUser = User.objects.create(
                email=email,
                password=password_data,
                first_name=first_name,
                last_name=last_name,
            )

            Lesson.objects.create(
                term=termGenerator(self, self.faker.lesson_terms()),

                mondayMorning=timeGenerator(self, self.faker.time_number()),
                mondayAfternoon=timeGenerator(self, self.faker.time_number()),
                mondayNight=timeGenerator(self, self.faker.time_number()),
                tuesdayMorning=timeGenerator(self, self.faker.time_number()),
                tuesdayAfternoon=timeGenerator(self, self.faker.time_number()),
                tuesdayNight=timeGenerator(self, self.faker.time_number()),
                wednesdayMorning=timeGenerator(self, self.faker.time_number()),
                wednesdayAfternoon=timeGenerator(self, self.faker.time_number()),
                wednesdayNight=timeGenerator(self, self.faker.time_number()),
                thursdayMorning=timeGenerator(self, self.faker.time_number()),
                thursdayAfternoon=timeGenerator(self, self.faker.time_number()),
                thursdayNight=timeGenerator(self, self.faker.time_number()),
                fridayMorning=timeGenerator(self, self.faker.time_number()),
                fridayAfternoon=timeGenerator(self, self.faker.time_number()),
                fridayNight=True,

                lessons=self.faker.lesson_number(),
                desiredInterval=self.faker.lesson_intervals(),
                duration=self.faker.lesson_durations(),
                furtherInfo="I want to learn " + self.faker.music_school_instruments(),
                id=self.faker.unique.random_int(),
                user=newUser,
                # children=liamChildren,
                is_confirmed=False,
                invoiceNum=(str(newUser.pk)[:4]).zfill(4) + "-" + \
                (str(self.faker.unique.random_int())[:4]).zfill(4),
                studentNum=(str(newUser.pk)[:4]).zfill(4),
                invoiceEmail=newUser.email,
            )

            # Creation of seeded users with confirmed lessons and payments.

        for _ in range(0, 50):

            # password_data_general = self.faker.password(
            #     length=11, special_chars=True, upper_case=True)

            first_name = self.faker.first_name()
            last_name = self.faker.last_name()
            email = first_name.lower() + "-" + last_name.lower() + \
                "@" + self.faker.free_email_domain()

            newUser = User.objects.create(
                email=email,
                password=password_data,
                first_name=first_name,
                last_name=last_name,
            )

            userLesson = Lesson.objects.create(
                term=termGenerator(self, self.faker.lesson_terms()),

                mondayMorning=timeGenerator(self, self.faker.time_number()),
                mondayAfternoon=timeGenerator(self, self.faker.time_number()),
                mondayNight=timeGenerator(self, self.faker.time_number()),
                tuesdayMorning=timeGenerator(self, self.faker.time_number()),
                tuesdayAfternoon=timeGenerator(self, self.faker.time_number()),
                tuesdayNight=timeGenerator(self, self.faker.time_number()),
                wednesdayMorning=timeGenerator(self, self.faker.time_number()),
                wednesdayAfternoon=timeGenerator(self, self.faker.time_number()),
                wednesdayNight=timeGenerator(self, self.faker.time_number()),
                thursdayMorning=timeGenerator(self, self.faker.time_number()),
                thursdayAfternoon=timeGenerator(self, self.faker.time_number()),
                thursdayNight=timeGenerator(self, self.faker.time_number()),
                fridayMorning=timeGenerator(self, self.faker.time_number()),
                fridayAfternoon=timeGenerator(self, self.faker.time_number()),
                fridayNight=True,

                lessons=self.faker.lesson_number(),
                desiredInterval=self.faker.lesson_intervals(),
                duration=self.faker.lesson_durations(),
                furtherInfo="I want to learn " + self.faker.music_school_instruments(),
                id=self.faker.unique.random_int(),
                user=newUser,
                # children=liamChildren,
                is_confirmed=True,
                invoiceNum=(str(newUser.pk)[:4]).zfill(4) + "-" + \
                (str(self.faker.unique.random_int())[:4]).zfill(4),
                studentNum=(str(newUser.pk)[:4]).zfill(4),
                invoiceEmail=newUser.email,
            )

            now = datetime.datetime.now()
            startDate = datetime.date(2022, 12, self.faker.lesson_dates())

            # Creation of Schedule for seeded usrs
            form_input = {
                'teacher': teacherGenerator(self, self.faker.lesson_teachers()),
                'start_time': time(self.faker.lesson_hours(), 00, 00),
                'start_date': startDate,
                'interval': userLesson.desiredInterval,
                'number_of_lessons': userLesson.lessons,
                'duration': userLesson.duration,
            }
            form = ScheduleForm(data=form_input)
            while not form.is_valid():
                form_input = {
                    'teacher': teacherGenerator(self, self.faker.lesson_teachers()),
                    'start_time': time(self.faker.lesson_hours(), 00, 00),
                    'start_date': startDate,
                    'interval': userLesson.desiredInterval,
                    'number_of_lessons': userLesson.lessons,
                    'duration': userLesson.duration,
                }
                form = ScheduleForm(data=form_input)

            newSchedule = form.save(commit=False)
            newSchedule.lesson = userLesson
            newSchedule.save()

            for i in range(1, newSchedule.number_of_lessons):
                subSchedule = Schedule.objects.create(
                    teacher=newSchedule.teacher,
                    lesson=newSchedule.lesson,
                    start_time=newSchedule.start_time,
                    start_date=newSchedule.start_date + timedelta(days=i*newSchedule.interval),
                    interval=newSchedule.interval,
                    number_of_lessons=newSchedule.number_of_lessons,
                    duration=newSchedule.duration,
                )
                subSchedule.save()

            # Updating Payment View for seeded usrs
            payment = self.faker.lesson_payments()
            newUserPayment = Payment.objects.create(
                payment_time=now,
                student=newUser,
                amount_paid=payment,
                balance_before=-(userLesson.duration*userLesson.lessons),
                balance_after=-(userLesson.duration*userLesson.lessons) + payment,
            )

            newUser.outstanding_balance = newUserPayment.balance_after
            newUser.save()
