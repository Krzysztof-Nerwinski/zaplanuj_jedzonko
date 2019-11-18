# Universal functions
from jedzonko.models import *

error_info = "Nie zapisano do bazy. Proszę wypełnij poprawnie wszystkie pola."

meals = {
    '1': 'Śniadanie',
    '2': 'Drugie śniadanie',
    '4': 'Podwieczorek',
    '3': 'Obiad',
    '5': 'Kolacja',
    '6': 'Potrenigowy',
    '7': 'Przedtreningowy',
}


def count(model):
    return model.objects.all().count()


def check_slug(slug_name):
    if Page.objects.filter(slug=slug_name).count() > 0:
        return Page.objects.get(slug=slug_name)
    return False


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
