from django.urls import path
from main import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('add_board/', views.add_board),
    path('get_boards/', views.get_boards),
] + static('static', document_root=settings.STATIC_ROOT)
