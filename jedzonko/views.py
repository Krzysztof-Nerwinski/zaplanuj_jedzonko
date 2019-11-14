import random
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View

from jedzonko.models import *
from jedzonko.utils import count,check_slug
from re import split as re_split
import datetime
import urllib


class IndexView(View):

    def get(self, request):
        recipe = Recipe.objects.all()
        slug_about = check_slug('about')
        list = []
        carusel = []

        for i in recipe:
            list.append(i.id)
        random.shuffle(list)

        for i in range(3):
            carusel.append((Recipe.objects.get(pk=list[i]).name, Recipe.objects.get(pk=list[i]).description))
        return render(request, "index.html",context={'carusel':carusel,'slug_about':slug_about})


class DashboardView(View):

    def get(self, request):
        plans_no = count(Plan)
        recipes_no = count(Recipe)
        day_names = DayName.objects.all()
        last_plan = Plan.objects.all().order_by('-created')[0]
        weekly_plan = []
        for day_number in day_names:
            meals = last_plan.recipeplan_set.filter(day_name=day_number.id).order_by('order')
            day = DayName.objects.get(id=day_number.id).get_day_name_display()
            weekly_plan.append((meals, day))
        return render(request, "dashboard.html", context={'plans_no': plans_no,
                                                          'recipes_no': recipes_no,
                                                          'last_plan': last_plan,
                                                          'weekly_plan': weekly_plan})


class RecipeView(View):

    def get(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        ingredients = re_split(r'\.|\,', recipe.ingredients)  # split on [dot|comma]
        return render(request, "app-recipe-details.html", context={'recipe': recipe,
                                                                   'ingridients': ingredients})

    def post(self,request,id):
        if 'vote_up' in request.POST:               #like
            temp_id = request.POST.get('recipe_id')
            recipe = Recipe.objects.get(id=temp_id)
            recipe.votes += 1
            recipe.save()
            return redirect('recipe', id)
        elif 'vote_down' in request.POST:           #dislike
            temp_id = request.POST.get('recipe_id')
            recipe = Recipe.objects.get(id=temp_id)
            recipe.votes -= 1
            recipe.save()
            return redirect('recipe', id)


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
        recipe_instructions = request.POST.get('recipe_instruction')

        if recipe_name != "" and recipe_time != "" and recipe_description != "" and recipe_ingredients != "":
            recipe_time_int = int(recipe_time)
            if recipe_time_int > 0:
                Recipe.objects.create(name=recipe_name, description=recipe_description,
                                      preparation_time=recipe_time_int, instructions=recipe_instructions,
                                      ingredients=recipe_ingredients)
                return redirect('recipe_list')
            else:
                return render(request, 'app-add-recipe.html', context={'add_data': "Wypełnij poprawnie wszystkie pola"})
        else:
            return render(request, 'app-add-recipe.html', context={'add_data': "Wypełnij poprawnie wszystkie pola"})


class RecipeModifyView(View):

    def get(self, request, id):
        return render(request, "test.html")


class RecipeDeleteView(View):

    def get(self, request, id):
        return render(request, "test.html")


class PlanView(View):
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        day_names = DayName.objects.all()
        weekly_plan = []
        for day_number in day_names:
            meals =  plan.recipeplan_set.filter(day_name=day_number.id).order_by('order')
            day = DayName.objects.get(id=day_number.id).get_day_name_display()
            weekly_plan.append((meals, day))
        return render(request, "app-details-schedules.html", context={'plan': plan,
                                                                      'weekly_plan': weekly_plan})


class PlanAddView(View):

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        plan_name = request.POST.get('plan_name')
        plan_description = request.POST.get('plan_description')

        Plan.objects.create(name=plan_name, description = plan_description)
        last_id = Plan.objects.all().order_by('-id')[0].id
        return redirect('plan', last_id)



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


class AboutView(View):
    def get(self,request):
        slug_about = check_slug('about')
        return render(request,'about.html',context={'slug_about':slug_about})
