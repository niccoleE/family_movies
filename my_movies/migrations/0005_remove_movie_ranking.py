# Generated by Django 4.0.4 on 2022-05-11 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_movies', '0004_comment_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='ranking',
        ),
    ]
