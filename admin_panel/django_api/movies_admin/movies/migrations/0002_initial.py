# Generated by Django 5.0.2 on 2024-10-28 18:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movies', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_comments', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='genrefilmwork',
            name='film_work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork'),
        ),
        migrations.AddField(
            model_name='genrefilmwork',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmWork', to='movies.genre'),
        ),
        migrations.AddField(
            model_name='personfilmwork',
            name='film_work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork'),
        ),
        migrations.AddField(
            model_name='personfilmwork',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.person'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(through='movies.PersonFilmWork', to='movies.person'),
        ),
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_reviews', to='profiles.profile'),
        ),
        migrations.AddField(
            model_name='review',
            name='film_work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork'),
        ),
        migrations.AddField(
            model_name='comment',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='movies.review'),
        ),
    ]