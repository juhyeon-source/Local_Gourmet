from django.urls import path
from . import views

urlpatterns = [
    path('', views.RecipeScraperView.as_view(), name='scrapper'),
]