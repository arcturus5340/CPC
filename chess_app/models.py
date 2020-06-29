from django.db import models


class ChessBoard(models.Model):
    id = models.AutoField(primary_key=True)
    fen = models.TextField(default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    moves = models.TextField(default='')
    pgn_meta = models.TextField(default=None)
    white = models.TextField(default=None)
    black = models.TextField(default=None)


class PGN(models.Model):
    id = models.AutoField(primary_key=True)
    src = models.TextField(default=None)
