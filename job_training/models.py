from django.contrib.auth.models import AbstractUser, UserManager
from django.core.files.base import ContentFile
from django.db import models
from django.utils import timezone
from django.conf import settings
import base64
import logging

logger = logging.getLogger(__name__)


class MyUserManager(UserManager):
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('Password is required')

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class Users(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    fio  = models.CharField(max_length=50, unique=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = MyUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

    @staticmethod
    def get_or_create_with_update(**user_data):
        email = user_data.get('email')
        if not email:
            raise ValueError("Email is required")

        username = user_data.get('username') or email
        user_data['username'] = username

        user, created = Users.objects.get_or_create(
            email=email,
            defaults=user_data
        )
        if not created:
            for key, value in user_data.items():
                if hasattr(user, key) and key not in ['email']:
                    setattr(user, key, value)
            user.save()
        return user, created


    # def get_or_create_with_update(**user_data):
    #     email = user_data.get('email')
    #     if not email:
    #         raise ValueError("Email is required")
    #
    #     username = user_data.get('email')
    #     # username = user_data.get('username') or email
    #     user_data['username'] = username
    #
    #     user, created = Users.objects.get_or_create(
    #         email=email,
    #         defaults=user_data
    #     )
    #     if not created:
    #         for key, value in user_data.items():
    #             if hasattr(user, key) and key not in ['email']:
    #                 setattr(user, key, value)
    #         user.save()
    #     return user, created


class PerevalLevel(models.Model):
    winter = models.CharField(max_length=10, null=True, blank=True, verbose_name='Зима')
    summer = models.CharField(max_length=10, null=True, blank=True, verbose_name='Лето')
    autumn = models.CharField(max_length=10, null=True, blank=True, verbose_name='Осень')
    spring = models.CharField(max_length=10, null=True, blank=True, verbose_name='Весна')

    class Meta:
        verbose_name = "Уровень сложности"
        verbose_name_plural = "Уровни сложности"

    def __str__(self):
        return f"Зима: {self.winter or 'Не указан'}, Лето: {self.summer or 'Не указан'}, Осень: {self.autumn or 'Не указан'}, Весна: {self.spring or 'Не указан'}"


class ModerationStatus(models.TextChoices):
    NEW = 'new', 'Новый'
    PENDING = 'pending', 'На рассмотрении'
    ACCEPTED = 'accepted', 'Принят'
    REJECTED = 'rejected', 'Отклонён'



class Coords(models.Model):
    latitude = models.FloatField(verbose_name="Широта", help_text="Широта в градусах")
    longitude = models.FloatField(verbose_name="Долгота", help_text="Долгота в градусах")
    height = models.IntegerField(verbose_name="Высота", help_text="Высота в метрах")

    class Meta:
        verbose_name = "Координаты"
        verbose_name_plural = "Координаты"

    @classmethod
    def get_or_create_coords(cls, latitude, longitude, height, **defaults):
        coord, created = cls.objects.get_or_create(
            latitude=latitude,
            longitude=longitude,
            height=height,
            defaults=defaults
        )
        return coord, created

    def __str__(self):
        return f"Координаты: {self.latitude}, {self.longitude}, {self.height} м"

class Image(models.Model):
    title = models.TextField(verbose_name="Название файла")  # Было filename, теперь title
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Изображение")
    added_at = models.DateTimeField(default=timezone.now, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    @classmethod
    def create_from_base64(cls, title, base64_data):
        try:
            img_bytes = base64.b64decode(base64_data)
            if ',' in base64_data:
                header, data_part = base64_data.split(',', 1)
                ext = header.split('/')[-1].split(';')[0] if '/' in header else 'png'  # По умолчанию png
            else:
                ext = 'png'
            file_name = f"{title}.{ext}"
            content_file = ContentFile(img_bytes, name=file_name)
            return cls.objects.create(title=title, image=content_file)
        except Exception as e:
            logger.error(f"Ошибка при обработке изображения {title}: {e}")
            raise ValueError(f"Неверный base64 для изображения {title}")


    def __str__(self):
        return self.title



class PerevalAdded(models.Model):
    beautyTitle = models.TextField(verbose_name="Красивое название", help_text="Красивое название перевала")
    title = models.TextField(verbose_name="Название", help_text="Основное название перевала")
    other_titles = models.TextField(null=True, blank=True, verbose_name="Другие названия", help_text="Альтернативные названия")
    connect = models.TextField(null=True, blank=True, verbose_name="Связь", help_text="Информация о связи/доступе")
    add_time = models.DateTimeField(default=timezone.now, verbose_name="Время добавления")
    user = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Пользователь", related_name='perevals')
    coord = models.ForeignKey(Coords, on_delete=models.CASCADE, verbose_name="Координаты", related_name='perevals')
    level = models.ForeignKey(PerevalLevel, on_delete=models.CASCADE, related_name='perevals')
    status = models.CharField(max_length=10, choices=ModerationStatus.choices, default=ModerationStatus.NEW, verbose_name="Статус модерации")
    moderated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Модератор", related_name='moderated_perevals')
    moderated_at = models.DateTimeField(null=True, blank=True, verbose_name="Время модерации")

    class Meta:
        verbose_name = "Перевал"
        verbose_name_plural = "Перевалы"


    @classmethod
    def create_with_related(cls, user_data, coord_data, images_data, level_data, **pereval_data):
        email = user_data.get('email')
        if not email:
            raise ValueError("Email обязателен для пользователя!")

        user, _ = Users.get_or_create_with_update(
            email=user_data["email"]
        )


        coord, _ = Coords.get_or_create_coords(**coord_data)

        level_obj, _ = PerevalLevel.objects.get_or_create(**level_data)

        pereval = cls.objects.create(user=user, coord=coord, level=level_obj, **pereval_data)

        for img_data in images_data:
            image = Image.create_from_base64(img_data['title'], img_data['data'])
            PerevalImages.objects.create(pereval=pereval, image=image)

        return pereval

    def __str__(self):
        return self.title


class PerevalImages(models.Model):
    pereval = models.ForeignKey('PerevalAdded', on_delete=models.CASCADE, related_name='pereval_images')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='pereval_images')

    class Meta:
        unique_together = ('pereval', 'image')  # Чтобы избежать дубликатов
        verbose_name = "Связь перевал-изображение"
        verbose_name_plural = "Связи перевал-изображение"
