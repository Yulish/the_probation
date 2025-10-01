from django.contrib import admin
from django.urls import path, include
from job_training.views import SubmitDataView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('api/submitData/', SubmitDataView.as_view(), name='submitData'),


]
