import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from jedzonko.models import *
from jedzonko.utils import count, check_slug, validate_int, validate_positive_int, error_info, meals
from re import split as re_split
from django.contrib import messages
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
        return render(request, "index.html", context={'carusel': carusel, 'slug_about': slug_about})


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
        ingredients = re_split(r'[.,\r]', recipe.ingredients)  # split on [dot|comma|newline]
        return render(request, "app-recipe-details.html", context={'recipe': recipe,
                                                                   'ingridients': ingredients})

    def post(self, request, id):
        if 'vote_up' in request.POST:  # like
            temp_id = request.POST.get('recipe_id')
            recipe = Recipe.objects.get(id=temp_id)
            recipe.votes += 1
            recipe.save()
            return redirect('recipe', id)
        elif 'vote_down' in request.POST:  # dislike
            temp_id = request.POST.get('recipe_id')
            recipe = Recipe.objects.get(id=temp_id)
            recipe.votes -= 1
            recipe.save()
            return redirect('recipe', id)


class RecipeListView(View):
    def get(self, request):
        recipes = Recipe.objects.order_by('-votes', "created")
        paginator = Paginator(recipes, 10)  # Show 10 recipes per page
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {"object_list": recipes})

    def post(self, request):
        searched_name = request.POST.get('searched_name')
        recipes = Recipe.objects.filter(name__icontains=searched_name).order_by('-votes', "created")
        paginator = Paginator(recipes, 10)  # Show 10 recipes per page
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {"object_list": recipes})


class RecipeAddView(View):

    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        recipe_name = request.POST.get('recipe_name')
        recipe_time = request.POST.get('recipe_time')
        recipe_description = request.POST.get('recipe_description')
        recipe_ingredients = request.POST.get('recipe_ingredients')
        recipe_instructions = request.POST.get('recipe_instructions')
        recipe_time = validate_positive_int(recipe_time)
        form = 'app-add-recipe.html'
        if not recipe_time or "" in (recipe_name, recipe_description, recipe_ingredients, recipe_instructions):
            return render(request, form, {'recipe_name': recipe_name, 'recipe_description': recipe_description,
                                          'recipe_ingredients': recipe_ingredients,
                                          'recipe_time': recipe_time, 'recipe_instructions': recipe_instructions,
                                          'info': error_info})
        Recipe.objects.create(name=recipe_name, description=recipe_description, preparation_time=recipe_time,
                              instructions=recipe_instructions, ingredients=recipe_ingredients)
        return redirect('recipe_list')


class RecipeModifyView(View):

    def get(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        form = 'app-edit-recipe.html'
        return render(request, form, context={'recipe_name': recipe.name, 'recipe_description': recipe.description,
                                              'recipe_time': recipe.preparation_time,
                                              'recipe_ingredients': recipe.ingredients,
                                              'recipe_instructions': recipe.instructions})

    def post(self, request, id):
        recipe_name = request.POST.get('recipe_name')
        recipe_time = request.POST.get('recipe_time')
        recipe_description = request.POST.get('recipe_description')
        recipe_ingredients = request.POST.get('recipe_ingredients')
        recipe_instructions = request.POST.get('recipe_instructions')
        recipe_time = validate_positive_int(recipe_time)
        form = 'app-edit-recipe.html'
        if not recipe_time or "" in (recipe_name, recipe_description, recipe_ingredients, recipe_instructions):
            return render(request, form, {'recipe_name': recipe_name, 'recipe_description': recipe_description,
                                          'recipe_time': recipe_time, 'recipe_ingredients': recipe_ingredients,
                                          'recipe_instructions': recipe_instructions,
                                          'info': error_info})
        Recipe.objects.create(name=recipe_name, preparation_time=recipe_time, description=recipe_description,
                              ingredients=recipe_ingredients, instructions=recipe_instructions)
        return redirect('recipe_list')


class RecipeDeleteView(View):

    def get(self, request, id):
        plan_id = RecipePlan.objects.get(id=id).plan_id
        RecipePlan.objects.get(id=id).delete()

        return redirect('plan', plan_id)


class PlanView(View):
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        day_names = DayName.objects.all()
        weekly_plan = []
        for day_number in day_names:
            meals = plan.recipeplan_set.filter(day_name=day_number.id).order_by('order')
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

        Plan.objects.create(name=plan_name, description=plan_description)
        last_id = Plan.objects.all().order_by('-id')[0].id
        return redirect('plan', last_id)


class PlanAddRecipeView(View):

    def get(self, request):
        plan_list = Plan.objects.all()
        recipe_list = Recipe.objects.all()
        day_list = DayName.objects.all()

        return render(request, "app-schedules-meal-recipe.html",
                      context={'plan_list': plan_list, 'recipe_list': recipe_list, 'day_list': day_list, 'meals': meals})

    def post(self, request):
        plan_id = request.POST.get('plan_id')
        meal_no = request.POST.get('meal_no')
        meal_name = meals.get(meal_no)
        day_name = request.POST.get('day_name')
        recipe_id = request.POST.get('recipe_id')

        RecipePlan.objects.create(meal_name=meal_name, order=meal_no, day_name=DayName.objects.get(id=day_name),
                                  plan=Plan.objects.get(id=plan_id), recipe=Recipe.objects.get(id=recipe_id))

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
        temp_plan = Plan.objects.get(id=id)
        return render(request, "app-edit-schedules.html", context={'plan':temp_plan})

    def post(self,request,id):
        temp_id = request.POST.get('plan_id')
        temp_plan = Plan.objects.get(id=temp_id)
        temp_plan.name = request.POST.get('plan_name')
        temp_plan.description = request.POST.get('plan_description')
        form = 'app-edit-schedules.html'
        if '' in (temp_plan.name, temp_plan.description):
            return render(request,form,context={'plan':temp_plan,
                                                'info':error_info})
        temp_plan.save()
        return redirect('plan', temp_id)


class AboutView(View):
    def get(self, request):
        slug_about = check_slug('about')
        return render(request, 'about.html', context={'slug_about': slug_about})


class CreateUserView(View):
    def get(self, request):
        return render(request, 'create_user.html')

    def post(self, request):
        user_login = request.POST.get("login")
        user_password = request.POST.get("password")
        user_email = request.POST.get("email")
        if not "" in (user_login, user_password, user_email):
            User.objects.create_user(user_login, user_email, user_password)
            message = f"Utworzono użytkownika {user_login}"
            return render(request, 'create_user.html', context={'message': message})
        else:
            message = "Podano błędne dane"
            return render(request, 'create_user.html', context={'message': message})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        next_page = request.GET['next']
        user_login = request.POST.get("login")
        user_password = request.POST.get("password")
        user = authenticate(username=user_login, password=user_password)
        if user is not None:
            # A backend authenticated the credentials
            login(request,user)
            return redirect(next_page)
        else:
            # No backend authenticated the credentials
            return render(request, 'login.html', context={'message': "wrong password or login"})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')