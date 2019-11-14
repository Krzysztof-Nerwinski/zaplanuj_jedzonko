#Universal functions
from jedzonko.models import *


def count(model):
    return model.objects.all().count()


def check_slug(slug_name):
    if Page.objects.filter(slug=slug_name).count() > 0:
        return Page.objects.get(slug=slug_name)
    return False
