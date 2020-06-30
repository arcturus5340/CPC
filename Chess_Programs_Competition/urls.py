from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from chess_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('add_board/', views.add_board),
    path('update_boards/', views.update_boards),
    path('get_fen/<int:board_id>', views.get_fen),
    path('move/<int:player_hash>/<str:move_uci>', views.move),
    path('get_report/<int:board_id>', views.get_report),
] + static('static', document_root=settings.STATIC_ROOT)
