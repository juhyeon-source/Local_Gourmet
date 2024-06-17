import requests
from bs4 import BeautifulSoup
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Recipe
from .serializers import RecipeSerializer
from django.http import HttpResponse

class ExampleView(APIView):
    def get(self, request):
        data = {
            'message': 'Hello from backend'
        }
        return Response(data, status=status.HTTP_200_OK)

def health_check(request):
    return HttpResponse(status=200)

class RecipeScraperView(APIView):
    def get(self, request, format=None):
        all_recipes = []
        url = "https://www.10000recipe.com/ranking/home_new.html?dtype=d&rtype=r"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        recipes = soup.find("div", class_="container sub_bg").find_all("li")[6:]
        
        # 기존 DB 데이터 삭제
        Recipe.objects.all().delete()
        
        # 'common_vod_label' 클래스 요소 제거, 제거 안하면 영상 썸네일의 플레이버튼이 나와버림.
        for element in soup.find_all(class_="common_vod_label"):
            element.decompose()
        
        # 썸네일 이미지 자체를 추출
        for recipe in recipes:
            image_element = recipe.find("img")
            if image_element:
                image = image_element.get('src')
            else:
                image = None
            # 레시피 URL 추출
            url_element = recipe.find("a", class_="common_sp_link")
            if url_element:
                recipe_url = f"https://www.10000recipe.com/{url_element['href']}"
            else:
                recipe_url = None
            # 제목 추출
            title_element = recipe.find("div", class_="common_sp_caption_tit line2")
            if title_element:
                title = title_element.text.strip()
            else:
                title = "No Title"
            # 조회수 추출
            viewcount_element = recipe.find("span", class_="common_sp_caption_buyer")
            if viewcount_element:
                viewcount = viewcount_element.text.strip()
            else:
                viewcount = "0"

            recipe_data = {
                "image": image,
                "url": recipe_url,
                "title": title,
                "viewcount": viewcount
            }
            all_recipes.append(recipe_data)

        serializer = RecipeSerializer(data=all_recipes, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # 데이터베이스에 저장
        return Response(serializer.data, status=status.HTTP_200_OK)