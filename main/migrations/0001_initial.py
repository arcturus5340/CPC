# Generated by Django 3.0.7 on 2020-06-27 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChessBoard',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fen', models.TextField(default='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')),
            ],
        ),
    ]
