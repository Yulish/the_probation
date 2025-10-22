from rest_framework import serializers
from .models import Users, Coords, Image, PerevalAdded, PerevalImages, PerevalLevel
from django.utils.dateparse import parse_datetime
import base64
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['fio', 'email', 'phone']
        extra_kwargs = {
            'email': {'required': True},
            'fio': {'required': False},
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
    user = serializers.DictField(write_only=True)
    coord = CoordsSerializer()
    images = ImageSerializer(many=True, required=False)
    level = serializers.DictField(child=serializers.CharField(allow_blank=True), write_only=True)

    class Meta:
        model = PerevalAdded
        fields = [
            'beautyTitle', 'title', 'other_titles', 'connect', 'add_time',
            'user', 'coord', 'level', 'images', 'status'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.user:
            data['user'] = UserSerializer(instance.user).data
        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user, created = Users.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'fio': user_data.get('fio'),
                'phone': user_data.get('phone'),
            }
        )
        coord_data = validated_data.pop('coord')
        images_data = validated_data.pop('images', [])
        level_data = validated_data.pop('level', {})


        return PerevalAdded.create_with_related(
            user_data=user_data,
            coord_data=coord_data,
            images_data=images_data,
            level_data=level_data,
            **validated_data
        )

    def update(self, instance, validated_data):
        validated_data.pop('user', None)


        coord_data = validated_data.pop('coord', None)
        if coord_data:
            coord_serializer = CoordsSerializer(instance.coord, data=coord_data, partial=True)
            if coord_serializer.is_valid():
                coord_serializer.save()

        level_data = validated_data.pop('level', None)
        if level_data:
            level_obj, _ = PerevalLevel.objects.get_or_create(**level_data)
            instance.level = level_obj

        images_data = validated_data.pop('images', None)
        if images_data is not None:
            instance.pereval_images.all().delete()
            for img_data in images_data:
                image = Image.create_from_base64(img_data['title'], img_data['data'])
                PerevalImages.objects.create(pereval=instance, image=image)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def validate_add_time(self, value):
        if isinstance(value, str):
            parsed = parse_datetime(value)
            if parsed is None:
                raise serializers.ValidationError("Неверный формат даты и времени. Используйте формат YYYY-MM-DD HH:MM:SS")
            return parsed
        return value

