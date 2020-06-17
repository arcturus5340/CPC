from django.urls import path
from main import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
] + static('static', document_root=settings.STATIC_ROOT)
