from datetime import datetime
from django.shortcuts import render
from django.views import View
from jedzonko.models import *
from jedzonko.utils import count


class IndexView(View):

    def get(self, request):
        return render(request, "index.html")


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
                                                          'weekly_plan': weekly_plan,
                                                          'days':DayName.DAYS})


class RecipeView(View):

    def get(self, request, id):
        return render(request, "test.html")


class RecipeListView(View):

    def get(self, request):
        return render(request, "test.html")


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
        return render(request, "test.html")
