import random
import factory

from factory.fuzzy import FuzzyInteger, FuzzyChoice
from factory.django import DjangoModelFactory, Password

from .models import User, Student, Course, Project

PROJECTS = set(Project.objects.all())
COURSES = Course.objects.all()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    password = Password('f@ct0ryb0y')
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")


class StudentFactory(DjangoModelFactory):

    class Meta:
        model = Student

    id = FuzzyInteger(220000123, 999999999)
    user = factory.SubFactory(UserFactory)
    year = FuzzyInteger(2023, 2023)
    trimester = FuzzyChoice(Student.TRIMESTERS, getter=lambda c: c[0])
    unit = FuzzyChoice(Student.UNITS, getter=lambda c: c[0])
    course = FuzzyChoice(COURSES)
    p1 = FuzzyChoice(PROJECTS)
    p2 = factory.LazyAttribute(lambda o: random.choice(list(PROJECTS - {o.p1})))
    p3 = factory.LazyAttribute(lambda o: random.choice(list(PROJECTS - {o.p1, o.p2})))


