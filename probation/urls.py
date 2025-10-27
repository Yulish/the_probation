from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from job_training.views import SubmitDataListView, PerevalAddedViewset, SubmitDataDetailView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="API для данных о перевалах",
        default_version='v1',
        description="Документация для мобильного приложения и REST API ФСТР",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="ishmakova1@yandex.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('api/submitData/', SubmitDataListView.as_view(), name='submit-data-list'),
    path('api/submitData/<int:pk>/', SubmitDataDetailView.as_view(), name='submit-data-detail'),
    # path('api/submitData/', SubmitDataView.as_view(), name='submit_data_list'),
    # path('api/submitData/<int:pk>/', SubmitDataView.as_view(), name='submit_data_detail'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)