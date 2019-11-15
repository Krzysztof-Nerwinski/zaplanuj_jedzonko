#Universal functions
from jedzonko.models import *


def count(model):
    return model.objects.all().count()

def validate_int(variable):
    try:
        var2 = int(variable)
    except ValueError:
        return False
    return var2

