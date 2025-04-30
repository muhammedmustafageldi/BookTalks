import pytest

def test_equal_or_not_equal():
    assert isinstance('this is a string', str)


@pytest.fixture
def default_student():
    return Student('Musti', "Geldi", 24, 212211019)

def test_person_initialization(default_student):
    assert default_student.first_name == 'Musti', 'The first name should be Musti.'


class Student:
    def __init__(self, first_name: str, last_name: str, age: int, number: int):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.number = number
