# Universal functions
from jedzonko.models import *

error_info = "Nie zapisano do bazy. Proszę wypełnij poprawnie wszystkie pola."

def count(model):
    return model.objects.all().count()


def validate_int(variable):
    try:
        var2 = int(variable)
    except ValueError:
        return False
    return var2


def validate_positive_int(number):
    number = validate_int(number)
    if number < 0 and number:
        return False
    return number




