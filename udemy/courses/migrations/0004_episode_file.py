# Generated by Django 4.2.2 on 2023-06-05 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_sector_sector_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='courses'),
        ),
    ]