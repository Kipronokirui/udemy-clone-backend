# Generated by Django 4.2.2 on 2023-06-05 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_episode_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to='course_images'),
        ),
    ]
