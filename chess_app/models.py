from django.db import models


class ChessBoard(models.Model):
    id = models.AutoField(primary_key=True)
    fen = models.TextField(default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    white = models.TextField()
    black = models.TextField()


class PGN(models.Model):
    id = models.IntegerField(primary_key=True)
    event = models.TextField(default=None, null=True)
    site = models.TextField(default=None, null=True)
    date = models.TextField(default=None, null=True)
    round = models.TextField(default=None, null=True)
    white = models.TextField(default=None, null=True)
    black = models.TextField(default=None, null=True)
    result = models.TextField(default=None, null=True)
    moves = models.TextField(default='')
