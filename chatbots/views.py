from rest_framework.views import APIView
from rest_framework.response import Response
# 부모의 부모폴더 즉 local_gourmet 폴더의 setting.py에서 바로가져오기
from django.conf import settings
from openai import OpenAI

from .bots import recipe_bot


class ChatbotsAPIView(APIView):
    def post(self, request):
        user_message = request.data.get("message")
        chatbots_reponse = recipe_bot(user_message)
        return Response({"message": chatbots_reponse})
