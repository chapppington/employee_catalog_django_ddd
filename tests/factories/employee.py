from factory import Faker
from factory.django import DjangoModelFactory

from core.apps.employee.models.employee import EmployeeModel


class EmployeeModelFactory(DjangoModelFactory):
    last_name = Faker("last_name")
    first_name = Faker("first_name")
    middle_name = Faker("first_name")
    position = Faker("job")
    date_hired = Faker("date")
    salary = Faker("pydecimal", left_digits=6, right_digits=2, positive=True)
    manager = None

    class Meta:
        model = EmployeeModel
