#Universal functions
from jedzonko.models import *


def count(model):
    return model.objects.all().count()