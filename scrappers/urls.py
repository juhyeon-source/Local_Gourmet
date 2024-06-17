from django.urls import path
from . import views
from .views import ExampleView, health_check

urlpatterns = [
    path('', views.RecipeScraperView.as_view(), name='scrapper'),
    path('example/', ExampleView.as_view(), name='example'),
    path('health/', health_check, name='health_check'),
]

# 헬스체크 테스트 코드 삽입