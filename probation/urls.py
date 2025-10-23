from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from job_training.views import SubmitDataView, PerevalAddedViewset



urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
path('api/submitData/', SubmitDataView.as_view(), name='submit_data_list'),
    path('api/submitData/<int:pk>/', SubmitDataView.as_view(), name='submit_data_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)