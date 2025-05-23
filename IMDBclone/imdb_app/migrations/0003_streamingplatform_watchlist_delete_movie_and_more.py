# Generated by Django 5.2 on 2025-04-26 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0002_movie_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreamingPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('about', models.TextField()),
                ('website', models.URLField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('storyline', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
        migrations.AddField(
            model_name='streamingplatform',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='platforms', to='imdb_app.watchlist'),
        ),
    ]
