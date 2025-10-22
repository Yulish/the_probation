from .models import Users, Coords, Image, PerevalAdded
from .serializers import ImageSerializer, UserSerializer, CoordsSerializer, PerevalAddedSerializer
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'new':
            return Response({'error': 'Изменения разрешены только для записей со статусом "new".'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)



class PerevalAddedViewset(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Получаем данные пользователя
        user_data = validated_data.pop('user')

        # Парсим fio на first_name и last_name (если fio передано)
        fio = user_data.get('fio')
        if fio:
            parts = fio.split()
            if len(parts) >= 2:
                user_data['last_name'] = parts[0]  # Фамилия
                user_data['first_name'] = parts[1]  # Имя
            else:
                user_data['first_name'] = fio

        user, created = Users.objects.get_or_create_with_update(**user_data)

        # Создаём объект PerevalAdded
        pereval = PerevalAdded.objects.create(**validated_data, user=user)

        # Возвращаем ответ
        return Response({'id': pereval.id, 'message': 'Отправлено успешно', 'status': 201})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'new':
            return Response({
                'state': 0,
                'message': 'Запись уже обработана модератором и не может быть изменена'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({
                'state': 1,
                'message': 'Запись успешно обновлена'
            }, status=status.HTTP_200_OK)
        else:
            errors = ', '.join([f"{field}: {error}" for field, error_list in serializer.errors.items() for error in error_list])
            return Response({
                'state': 0,
                'message': f'Ошибка валидации данных: {errors}'
            }, status=status.HTTP_400_BAD_REQUEST)

class SubmitDataView(APIView):
    def post(self, request):
        serializer = PerevalAddedSerializer(data=request.data)
        if serializer.is_valid():
            pereval = serializer.save()
            logger.info(f"Создан PerevalAdded с ID {pereval.id}")
            return Response({
                'success': True,
                'id': pereval.id,
                'beautyTitle': pereval.beautyTitle
            }, status=status.HTTP_201_CREATED)
        else:
            logger.error(f"Ошибки валидации: {serializer.errors}")
            print(f"DEBUG: Serializer errors: {serializer.errors}")  # Для отладки в консоли
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class pereval_detail(APIView):

    def get(self, request, pk):
        pereval = get_object_or_404(PerevalAdded, pk=pk)
        serializer = PerevalAddedSerializer(pereval)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        pereval = get_object_or_404(PerevalAdded, pk=pk)

        if pereval.status != 'new':
            return Response({
                'state': 0,
                'message': 'Запись уже обработана модератором и не может быть изменена'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = PerevalAddedSerializer(pereval, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'state': 1,
                'message': 'Запись успешно обновлена'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'state': 0,
                'message': 'Ошибка валидации данных',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)