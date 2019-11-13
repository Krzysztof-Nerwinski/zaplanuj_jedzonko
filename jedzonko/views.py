import random

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View

from jedzonko.models import *
from jedzonko.utils import count
from re import split as re_split

class IndexView(View):

    def get(self, request):
        recipe = Recipe.objects.all()
        list = []
        for i in recipe:
            list.append(i.id)

        random.shuffle(list)

        carusel_one = list[0]
        carusel_two = list[1]
        carusel_three = list[2]

        recipe_one_name = Recipe.objects.get(pk=carusel_one).name
        recipe_one_description = Recipe.objects.get(pk=carusel_one).description
        recipe_two_name = Recipe.objects.get(pk=carusel_two).name
        recipe_two_description = Recipe.objects.get(pk=carusel_two).description
        recipe_three_name = Recipe.objects.get(pk=carusel_three).name
        recipe_three_description = Recipe.objects.get(pk=carusel_three).description

        return render(request, "index.html",
                      context={'recipe_one_name': recipe_one_name, 'recipe_one_description': recipe_one_description,
                               'recipe_two_name': recipe_two_name, 'recipe_two_description': recipe_two_description,
                               'recipe_three_name': recipe_three_name,
                               'recipe_three_description': recipe_three_description
                               })


class DashboardView(View):

    def get(self, request):
        plans_no = count(Plan)
        recipes_no = count(Recipe)
        last_plan = Plan.objects.all().order_by('-created')[0]
        weekly_plan = []
        for day_number in range(1, 8):
            if bool(last_plan.recipeplan_set.filter(day_name=day_number)) is not False:
                weekly_plan.append(last_plan.recipeplan_set.filter(day_name=day_number).order_by('order'))
        return render(request, "dashboard.html", context={'plans_no': plans_no,
                                                          'recipes_no': recipes_no,
                                                          'last_plan': last_plan,
                                                          'weekly_plan': weekly_plan})


class RecipeView(View):

    def get(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        ingredients = re_split(r'\.|\,',recipe.ingredients)  #split on [dot|comma]
        return render(request, "app-recipe-details.html",context={'recipe':recipe,
                                                                  'ingridients':ingredients})


class RecipeListView(View):
    def get(self, request):
        recipes = Recipe.objects.order_by('-votes', "created")
        paginator = Paginator(recipes, 3)  # Show 50 recipes per page
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {"object_list": recipes})


class RecipeAddView(View):

    def get(self, request):
        return render(request, "test.html")


class RecipeModifyView(View):

    def get(self, request, id):
        return render(request, "test.html")


class PlanView(View):

    def get(self, request, id):
        return render(request, "test.html")


class PlanAddView(View):

    def get(self, request):
        return render(request, "test.html")


class PlanAddRecipeView(View):

    def get(self, request):
        return render(request, "test.html")


class PlanListView(View):

    def get(self, request):
        plans = Plan.objects.order_by('name')
        paginator = Paginator(plans, 3)  # Show 50 recipes per page
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, 'app-schedules.html', {"object_list": plans})


class PlanModifyView(View):
    def get(self, request, id):
        return render(request, "test.html")
