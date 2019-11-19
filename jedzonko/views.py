import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from jedzonko.utils import *
from re import split as re_split


class IndexView(View):
    def get(self, request):
        recipe = Recipe.objects.all()
        slug_about = check_slug('about')
        slug_contact = check_slug('contact')
        list = []
        carusel = []
        for i in recipe:
            list.append(i.id)
        random.shuffle(list)
        for i in range(3):
            carusel.append((Recipe.objects.get(pk=list[i]).name, Recipe.objects.get(pk=list[i]).description))
        return render(request, "index.html",
                      context={'carusel': carusel, 'slug_about': slug_about, 'slug_contact': slug_contact})


class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request):
        message = request.GET.get('message')
        plans_no = count(Plan)
        recipes_no = count(Recipe)
        day_names = DayName.objects.all().order_by("order")
        last_plan = Plan.objects.all().order_by('-created')[0]
        weekly_plan = []
        for day_number in day_names:
            meals = last_plan.recipeplan_set.filter(day_name=day_number.id).order_by('order')
            day = DayName.objects.get(id=day_number.id).get_day_name_display()
            weekly_plan.append((meals, day))
        return render(request, "dashboard.html", context={'message': message,
                                                          'plans_no': plans_no,
                                                          'recipes_no': recipes_no,
                                                          'last_plan': last_plan,
                                                          'weekly_plan': weekly_plan})


class RecipeView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        ingredients = re_split(r'[.,;\r]', recipe.ingredients)  # split on [dot|comma|semicolon|newline]
        return render(request, "app-recipe-details.html", context={'recipe': recipe,
                                                                   'ingredients': ingredients})

    @method_decorator(login_required)
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
    @method_decorator(login_required)
    def get(self, request):
        recipes = Recipe.objects.order_by('-votes', "created")
        paginator = Paginator(recipes, 10)  # Show 10 recipes per page
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {"object_list": recipes})

    @method_decorator(login_required)
    def post(self, request):
        searched_name = request.POST.get('searched_name')
        recipes = Recipe.objects.filter(name__icontains=searched_name).order_by('-votes', "created")
        paginator = Paginator(recipes, 10)  # Show 10 recipes per page
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {"object_list": recipes})


class RecipeAddView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "app-add-recipe.html")

    @method_decorator(login_required)
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
                                          'message': messages['wrong_data']})
        Recipe.objects.create(name=recipe_name, description=recipe_description, preparation_time=recipe_time,
                              instructions=recipe_instructions, ingredients=recipe_ingredients)
        return redirect('recipe_list')


class RecipeModifyView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        form = 'app-edit-recipe.html'
        return render(request, form, context={'recipe_name': recipe.name, 'recipe_description': recipe.description,
                                              'recipe_time': recipe.preparation_time,
                                              'recipe_ingredients': recipe.ingredients,
                                              'recipe_instructions': recipe.instructions})

    @method_decorator(login_required)
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
                                          'message': messages['wrong_data']})
        Recipe.objects.create(name=recipe_name, preparation_time=recipe_time, description=recipe_description,
                              ingredients=recipe_ingredients, instructions=recipe_instructions)
        return redirect('recipe_list')


class RecipeDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        plan_id = RecipePlan.objects.get(id=id).plan_id
        RecipePlan.objects.get(id=id).delete()

        return redirect('plan', plan_id)


class PlanView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        plan = Plan.objects.get(id=id)
        day_names = DayName.objects.all().order_by("order")
        weekly_plan = []
        for day_number in day_names:
            meals = plan.recipeplan_set.filter(day_name=day_number.id).order_by('order')
            day = DayName.objects.get(id=day_number.id).get_day_name_display()
            weekly_plan.append((meals, day))
        return render(request, "app-details-schedules.html", context={'plan': plan,
                                                                      'weekly_plan': weekly_plan})


class PlanAddView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "app-add-schedules.html")

    @method_decorator(login_required)
    def post(self, request):
        plan_name = request.POST.get('plan_name')
        plan_description = request.POST.get('plan_description')
        if '' in (plan_name, plan_description):
            return render(request, "app-add-schedules.html", context={'message': messages['wrong_data']})
        Plan.objects.create(name=plan_name, description=plan_description)
        last_id = Plan.objects.all().order_by('-id')[0].id
        return redirect('plan', last_id)


class PlanAddRecipeView(View):
    last_plan = Plan.objects.all().order_by('-created')[0]
    last_recipe = Recipe.objects.all().order_by('-created')[0]

    @method_decorator(login_required)
    def get(self, request, plan_id_def=last_plan, recipe_id_def=last_plan):
        plan_list = Plan.objects.all()
        recipe_list = Recipe.objects.all()
        day_list = DayName.objects.all()
        return render(request, "app-schedules-meal-recipe.html",
                      context={'plan_list': plan_list, 'recipe_list': recipe_list, 'day_list': day_list,
                               'meals': meals, "plan_id_def": plan_id_def, "recipe_id_def": recipe_id_def})

    @method_decorator(login_required)
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
    @method_decorator(login_required)
    def get(self, request):
        plans = Plan.objects.order_by('name')
        paginator = Paginator(plans, 3)  # Show 50 recipes per page
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, 'app-schedules.html', {"object_list": plans})


class PlanModifyView(View):
    @method_decorator(login_required)
    def get(self, request, id):
        temp_plan = Plan.objects.get(id=id)
        return render(request, "app-edit-schedules.html", context={'plan': temp_plan})

    @method_decorator(login_required)
    def post(self, request, id):
        temp_id = request.POST.get('plan_id')
        temp_plan = Plan.objects.get(id=temp_id)
        temp_plan.name = request.POST.get('plan_name')
        temp_plan.description = request.POST.get('plan_description')
        form = 'app-edit-schedules.html'
        if '' in (temp_plan.name, temp_plan.description):
            return render(request, form, context={'plan': temp_plan,
                                                  'message': messages['wrong_data']})
        temp_plan.save()
        return redirect('plan', temp_id)


class AboutView(View):
    def get(self, request):
        slug_about = check_slug('about')
        slug_contact = check_slug('contact')
        slug = check_slug('about')
        return render(request, 'dynamic.html',
                      context={'slug': slug, 'slug_about': slug_about, 'slug_contact': slug_contact})


class ContactView(View):
    def get(self, request):
        slug_about = check_slug('about')
        slug_contact = check_slug('contact')
        slug = check_slug('contact')
        return render(request, 'dynamic.html',
                      context={'slug': slug, 'slug_about': slug_about, 'slug_contact': slug_contact})


class CreateUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            url = create_redirect_param('dashboard', messages['already_logged_in'])
            return redirect(url)
        return render(request, 'create_user.html')

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        user_login = request.POST.get("login")
        user_password = request.POST.get("password")
        user_email = request.POST.get("email")
        if not "" in (user_login, user_password, user_email):
            if User.objects.filter(username=user_login) or User.objects.filter(email=user_email):
                return render(request, 'create_user.html', context={'message': messages['user_exists']})
            temp_message = f"Utworzono użytkownika {user_login}"
            url = create_redirect_param('login', temp_message)
            return redirect(url)
        else:
            return render(request, 'create_user.html', context={'message': messages['wrong_data']})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            url = create_redirect_param('dashboard', messages['already_logged_in'])
            return redirect(url)
        return render(request, 'login.html')

    def post(self, request):
        next_page = request.GET.get('next')
        if next_page is None:
            next_page = 'dashboard'
        user_login = request.POST.get("login")
        user_password = request.POST.get("password")
        user = authenticate(username=user_login, password=user_password)
        if user is not None:
            login(request, user)
            return redirect(next_page)
        else:
            return render(request, 'login.html', context={'message': messages['wrong_user_data']})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
