import random
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View

from jedzonko.models import *
from jedzonko.utils import count
import datetime
import urllib

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
        return render(request, "test.html")


class RecipeListView(View):
    def get(self, request):
        recipes = Recipe.objects.order_by('-votes', "created")
        paginator = Paginator(recipes, 3)  # Show 50 recipes per page
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {"object_list": recipes})


class RecipeAddView(View):

    def get(self, request):

        return render(request, "app-add-recipe.html")

    def post(self, request):

        recipe_name = request.POST.get('recipe_name')
        recipe_time = (request.POST.get('recipe_time'))
        recipe_description = request.POST.get('recipe_description')
        recipe_ingredients = request.POST.get('recipe_ingredients')
        recipe_instructions = request.POST.get('recipe_instructions')



        if recipe_name !="" and recipe_time !="" and recipe_description !="" and recipe_ingredients !="" :
            recipe_time_int = int(recipe_time)
            if recipe_time_int > 0:
                Recipe.objects.create(name=recipe_name, ingredients=recipe_ingredients, description=recipe_description,
                                      preparation_time=recipe_time_int, instructions = recipe_instructions)
                return redirect('recipe_list')
            else:
                return render(request, 'app-add-recipe.html', context={'add_data': "Wypełnij poprawnie wszystkie pola"})
        else:
            return render(request, 'app-add-recipe.html', context={'add_data': "Wypełnij poprawnie wszystkie pola"})



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
        plan_list = Plan.objects.all()
        recipe_list = Recipe.objects.all()
        day_list = DayName.objects.all()


        return render(request, "app-schedules-meal-recipe.html", context= {'plan_list': plan_list, 'recipe_list': recipe_list, 'day_list': day_list })

    def post(self, request):
        plan_id = request.POST.get('plan_id')
        meal_name = request.POST.get('meal_name')
        meal_no = request.POST.get('meal_no')
        day_name = request.POST.get('day_name')
        recipe_id = request.POST.get('recipe_id')

        RecipePlan.objects.create(meal_name=meal_name, order=meal_no, day_name=DayName.objects.get(id=day_name), plan=Plan.objects.get(id=plan_id), recipe=Recipe.objects.get(id=recipe_id))

        return redirect('plan', plan_id)



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
