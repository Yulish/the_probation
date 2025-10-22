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

class PerevalAddedViewset(viewsets.ModelViewSet):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer
    user = UserSerializer()

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
            return Response({
                'state': 0,
                'message': 'Ошибка валидации данных',
                'errors': serializer.errors
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

    def get(self, request):
        perevals = PerevalAdded.objects.all()
        serializer = PerevalAddedSerializer(perevals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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