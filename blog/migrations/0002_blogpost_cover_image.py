# Generated by Django 4.2.11 on 2024-05-01 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_covers/'),
        ),
    ]
