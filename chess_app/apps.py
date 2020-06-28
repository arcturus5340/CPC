from django.apps import AppConfig


class ChessAppConfig(AppConfig):
    name = 'chess_app'

    def ready(self):
        from chess_app import boardUpdater
        boardUpdater.start()