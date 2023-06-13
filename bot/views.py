from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient


class VerificationView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TgUserSerializer

    def patch(self, request: Request, *args, **kwargs) -> Response:
        serializer = TgUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tg_user: TgUser = serializer.save(user=request.user)

        TgClient().send_message(chat_id=tg_user.chat_id, text='Bot token verified')

        return Response(serializer.data)
