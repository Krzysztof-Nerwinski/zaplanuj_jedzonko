from datetime import datetime
import random
from django.shortcuts import render, redirect
from django.views import View
from jedzonko.models import *
from jedzonko.utils import count
import datetime

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


        return render(request, "index.html", context={'recipe_one_name': recipe_one_name, 'recipe_one_description': recipe_one_description,
                                                      'recipe_two_name': recipe_two_name, 'recipe_two_description': recipe_two_description,
                                                      'recipe_three_name': recipe_three_name, 'recipe_three_description': recipe_three_description
        })



class DashboardView(View):

    def get(self, request):
        plans_no = count(Plan)
        recipes_no = count(Recipe)
        return render(request, "dashboard.html",context={'plans_no':plans_no,
                                                         'recipes_no':recipes_no})


class RecipeView(View):

    def get(self, request, id):
        return render(request, "test.html")


class RecipeListView(View):

    def get(self, request):
        return render(request, "test.html")


class RecipeAddView(View):

    def get(self, request):

        return render(request, "app-add-recipe.html")

    def post(self, request):

        recipe_name = request.POST.get('recipe_name')
        recipe_time = (request.POST.get('recipe_time'))
        recipe_description = request.POST.get('recipe_description')
        recipe_ingredients = request.POST.get('recipe_ingredients')



        if recipe_name !="" and recipe_time !="" and recipe_description !="" and recipe_ingredients !="" :
            recipe_time_int = int(recipe_time)
            if recipe_time_int > 0:
                Recipe.objects.create(name=recipe_name, ingredients=recipe_ingredients, description=recipe_description,
                                      preparation_time=recipe_time_int)
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
        return render(request, "test.html")



class PlanListView(View):

    def get(self, request):
        return render(request, "test.html")
