# Generated by Django 4.0.4 on 2022-05-03 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('description', models.CharField(max_length=500)),
                ('rating', models.IntegerField()),
                ('ranking', models.FloatField()),
                ('review', models.CharField(max_length=500)),
                ('img_url', models.URLField(max_length=300)),
            ],
        ),
    ]