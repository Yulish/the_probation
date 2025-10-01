from rest_framework import viewsets
from .models import Users, Coords, Image, PerevalAdded
from .serializers import ImageSerializer, UserSerializer, CoordsSerializer, PerevalAddedSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)


class UserViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = ImageSerializer

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

