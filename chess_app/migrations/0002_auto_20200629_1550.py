# Generated by Django 3.0.7 on 2020-06-29 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chess_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chessboard',
            name='black',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='chessboard',
            name='white',
            field=models.TextField(default=None),
        ),
    ]
