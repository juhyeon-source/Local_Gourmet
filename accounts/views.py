from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *


@api_view(["POST"])
#api_view의 기능 중 POST 메소드를 쓴다는건가?
def signup(request):
    """
    signup: 회원 가입 FBV
    """

    # 반환값 및 status_code 초기값 설정
    result = {
        "result": False,
        "msg": None
    }
    status_code = HTTP_400_BAD_REQUEST
    # 결과값이 false일때 400에러코드가 뜨고, 메세지코드는 none

    # POST 입력 데이터 Serialization
    serializer = AccountSerializer(data=request.data)
    # 아래에서 serializer라고 정의 할건,
    # serializers.py안에 있는 AccountSerializer(data는 요청받아온 data를 의미)

    # POST 입력값 검증
    if serializer.is_valid():
        # 새 가입 계정 생성
        # 유효성 검사
        # serializer을 통해 직렬화 한 데이터들의 값이 맞다면
        data = serializer.save()
        #아래 내용의 데이터 값들이 맞다면 serializer을 통해 직렬화 한 data들을 저장
        # 반환값 내용 및 status_code 수정
        result.pop("msg") #pop....?이 뭐야
        result["user"] = data #위에 serializer를 통해 직렬화가 완료되어 저장한 데이터들을 의미
        result["result"] = True #결과값이 옳다
        status_code = HTTP_200_OK #정상적으로 생성됐다는 상태값

    else:
        #입력값이 맞지 않다면, serializer에 저장되어있는 errors를 메세지값으로 보여줘
        #입력값 검증 실패 시, 입력값 이상 내역 반환
        result["msg"] = serializer.errors

    # API 처리 결과 반환
    return Response(data=result,
                    status=status_code)


class AccountLogInView(APIView):
    def login(self, request):
        pass


def logout(self, request):
    pass


class AccountDetailView(APIView):
    pass
