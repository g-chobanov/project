# Generated by Django 4.1.7 on 2023-02-18 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songster', '0002_rename_featuredartists_song_featured_artists_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='img_url',
            field=models.CharField(default=123, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='writeup',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]