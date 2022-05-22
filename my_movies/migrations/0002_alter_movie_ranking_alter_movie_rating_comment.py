# Generated by Django 4.0.4 on 2022-05-04 21:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='ranking',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rating',
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_movies.movie')),
            ],
            options={
                'verbose_name_plural': 'comments',
            },
        ),
    ]
