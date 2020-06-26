from django.db import models

class ChessBoard(models.Model):
    id = models.AutoField(primary_key=True)
    board = models.BinaryField()
