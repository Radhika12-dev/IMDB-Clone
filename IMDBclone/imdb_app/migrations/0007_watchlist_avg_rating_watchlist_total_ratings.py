# Generated by Django 5.2 on 2025-04-30 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0006_review_reviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='avg_rating',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='total_ratings',
            field=models.IntegerField(default=0),
        ),
    ]
