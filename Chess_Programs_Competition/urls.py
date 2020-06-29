from django.urls import path
from chess_app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('add_board/', views.add_board),
    path('update_boards/', views.update_boards),
    path('get_fen/<int:board_id>', views.get_fen),
    path('move/<int:player_hash>/<str:move_uci>', views.move),
] + static('static', document_root=settings.STATIC_ROOT)
