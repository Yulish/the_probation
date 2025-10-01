from rest_framework import serializers
from .models import Users, Coords, Image, PerevalAdded
from django.utils.dateparse import parse_datetime
import base64
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['last_name', 'first_name', 'email', 'phone']
        extra_kwargs = {
            'email': {'required': True},
            'last_name': {'required': False},
            'first_name': {'required': False},
            'phone': {'required': False},
        }


class ImageSerializer(serializers.ModelSerializer):
    data = serializers.CharField(write_only=True)

    class Meta:
        model = Image
        fields = ['title', 'data']

    def create(self, validated_data):
        data_b64 = validated_data.pop('data')
        try:
            validated_data['data'] = base64.b64decode(data_b64)
        except Exception:
            raise serializers.ValidationError("Неверный формат данных изображения (должен быть base64)")
        return super().create(validated_data)



class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']




class PerevalAddedSerializer(serializers.ModelSerializer):
    user = serializers.DictField()
    coord = CoordsSerializer()
    images = ImageSerializer(many=True, required=False)
    level = serializers.DictField(child=serializers.CharField(allow_blank=True), write_only=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'beautyTitle', 'title', 'other_titles', 'connect', 'add_time',
            'user', 'coord', 'level', 'images'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coord_data = validated_data.pop('coord')
        images_data = validated_data.pop('images', [])
        level_data = validated_data.pop('level', {})

        user, _ = Users.get_or_create_with_update(**user_data)
        # user, _ = Users.objects.get_or_create(
        #     email=user_data.get('email'),
        #     defaults={
        #         'username': user_data.get('email'),  # Или как у тебя
        #         'first_name': user_data.get('first_name', ''),
        #         'last_name': user_data.get('last_name', ''),
        #         'phone': user_data.get('phone', ''),
        #     }
        # )

        return PerevalAdded.create_with_related(
            user_data=user_data,
            coord_data=coord_data,
            images_data=images_data,
            level_data=level_data,
            **validated_data
        )

    def validate_add_time(self, value):
        if isinstance(value, str):
            parsed = parse_datetime(value)
            if parsed is None:
                raise serializers.ValidationError("Неверный формат даты и времени. Используйте формат YYYY-MM-DD HH:MM:SS")
            return parsed
        return value


