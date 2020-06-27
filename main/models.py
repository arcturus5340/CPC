from django.db import models

class ChessBoard(models.Model):
    id = models.AutoField(primary_key=True)
    fen = models.TextField(default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')