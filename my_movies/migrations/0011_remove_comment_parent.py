# Generated by Django 4.0.4 on 2022-05-18 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_movies', '0010_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
    ]
