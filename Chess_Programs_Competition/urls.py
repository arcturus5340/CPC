from django.urls import path
from main import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('make_random_move/', views.make_random_move),
] + static('static', document_root=settings.STATIC_ROOT)
