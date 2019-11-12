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
