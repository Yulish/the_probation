from .models import Users, Coords, Image, PerevalAdded
from .serializers import ImageSerializer, UserSerializer, CoordsSerializer, PerevalAddedSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response

import logging
logger = logging.getLogger(__name__)


class UserViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer

    def list(self, request, format=None):
        return Response([])

class CoordsViewset(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer

class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class PerevalAddedViewset(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer
    user = UserSerializer()


class SubmitDataListView(APIView):

    @swagger_auto_schema(
        operation_description="Добавить новый перевал. Принимает данные о перевале и сохраняет их.",
        request_body=PerevalAddedSerializer,
        responses={
            201: openapi.Response("Успешно создано", examples={"application/json": {"success": True, "id": 1, "beautyTitle": "Название"}}),
            400: openapi.Response("Ошибка валидации", examples={"application/json": {"error": "Описание ошибки"}})
        }
    )
    def post(self, request):
        serializer = PerevalAddedSerializer(data=request.data)
        if serializer.is_valid():
            pereval = serializer.save()
            logger.info(f"Создан PerevalAdded с ID {pereval.id}")
            return Response({
                'success': True,
                'id': pereval.id,
                'beautyTitle': pereval.beautyTitle,
                'status': pereval.status
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Получить список данных о перевалах по email пользователя.",
        manual_parameters=[
            openapi.Parameter('user__email', openapi.IN_QUERY, description="Email пользователя для фильтрации списка", type=openapi.TYPE_STRING, required=True)
        ],
        responses={
            200: openapi.Response("Успешно", PerevalAddedSerializer(many=True)),
            400: openapi.Response("Ошибка", examples={"application/json": {"error": "user__email parameter is required"}})
        }
    )
    def get(self, request):
        user_email = request.query_params.get('user__email')
        if not user_email:
            return Response({'error': 'user__email parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        perevals = PerevalAdded.objects.filter(user__email=user_email)
        serializer = PerevalAddedSerializer(perevals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmitDataDetailView(APIView):

    @swagger_auto_schema(
        operation_description="Получить детали перевала по ID.",
        responses={
            200: openapi.Response("Успешно", PerevalAddedSerializer),
            404: openapi.Response("Не найдено", examples={"application/json": {"error": "Pereval not found"}})
        }
    )


    def get(self, request, pk):
        pereval = get_object_or_404(PerevalAdded, pk=pk)
        serializer = PerevalAddedSerializer(pereval)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Обновить данные перевала по ID (только если статус 'new').",
        request_body=PerevalAddedSerializer,
        responses={
            200: openapi.Response("Успешно обновлено", PerevalAddedSerializer),
            400: openapi.Response("Ошибка валидации или статус не позволяет", examples={"application/json": {"error": "Описание"}}),
            403: openapi.Response("Запрещено", examples={"application/json": {"error": "Можно редактировать только записи со статусом 'new'"}})
        }
    )
    def patch(self, request, pk):
        pereval = get_object_or_404(PerevalAdded, pk=pk)
        if pereval.status != 'new':
            return Response({
                'state': 0,
                'message': 'Запись уже обработана модератором и не может быть изменена'
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = PerevalAddedSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Обновлён PerevalAdded с ID {pereval.id}")
            return Response({
                'state': 1,
                'message': 'Запись успешно обновлена'
            }, status=status.HTTP_200_OK)
        return Response({
            'state': 0,
            'message': 'Ошибка валидации данных',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


