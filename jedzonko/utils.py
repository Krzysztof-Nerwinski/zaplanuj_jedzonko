# Universal functions
from django.urls import reverse
from urllib.parse import urlencode

from jedzonko.models import *

meals = {
    '1': 'Śniadanie',
    '2': 'Drugie śniadanie',
    '3': 'Obiad',
    '4': 'Podwieczorek',
    '5': 'Kolacja',
    '6': 'Potrenigowy',
    '7': 'Przedtreningowy',
}

messages = {
    'already_logged_in': "Użytkownik jest już zalogowany!",
    'wrong_user_data': "Zła nazwa użytkownika lub hasło, spróbuj ponownie!",
    'wrong_data': "Proszę wypełnij poprawnie wszystkie pola.",
    'user_exists': "Użytkownik już istnieje, wybierz inny login/email",
    'vote_up': 'Dodano głos na przepis',
    'vote_down': 'Odjęto głos z przepisu',
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


def create_redirect_param(view_name, param):
    base_url = reverse(view_name)
    message_text = param
    message = urlencode({'message': message_text})
    return f'{base_url}?{message}'
