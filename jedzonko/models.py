from django.db import models


# Create your models here.

class DayName(models.Model):
    DAYS = (
        ('PN', 'Poniedziałek'),
        ('WT', 'Wtorek'),
        ('ŚR', 'Środa'),
        ('CZW', 'Czwartek'),
        ('PT', 'Piątek'),
        ('SB', 'Sobota'),
        ('ND', 'Niedziela'),
    )
    day_name = models.CharField(max_length=3, choices=DAYS)
    order = models.IntegerField(unique=True)


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.PositiveIntegerField()
    votes = models.IntegerField(default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipe = models.ManyToManyField(Recipe, through='RecipePlan')


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField
    day_name = models.ForeignKey(DayName, on_delete=models.CASCADE, null=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True)


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
