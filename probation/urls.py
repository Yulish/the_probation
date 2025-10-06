from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from job_training.views import SubmitDataView, PerevalAddedViewset, pereval_detail



urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('api/submitData/', include([
        path('', SubmitDataView.as_view(), name='submitData'),
        path('<int:pk>/', PerevalAddedViewset.as_view({
        'get': 'retrieve',
        'patch': 'partial_update'
    }), name='pereval-detail'),
    ])),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)