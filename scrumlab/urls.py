"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jedzonko.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('main/', DashboardView.as_view(), name='dashboard'),
    path('recipe/<int:id>/', RecipeView.as_view(), name='recipe'),
    path('recipe/list/', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/add/', RecipeAddView.as_view(), name='recipe_add'),
    path('recipe/modify/<int:id>/', RecipeModifyView.as_view(), name='recipe_modify'),
    path('recipe/delete/<int:id>/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('plan/<int:id>/', PlanView.as_view(), name='plan'),
    path('plan/list/', PlanListView.as_view(), name='plan_list'),
    path('plan/add/', PlanAddView.as_view(), name='plan_add'),
    path('plan/add-recipe/', PlanAddRecipeView.as_view(), name='plan_add_recipe'),
    path('plan/modify/<int:id>/', PlanModifyView.as_view(), name='plan_modify'),

]
