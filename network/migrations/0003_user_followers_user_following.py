# Generated by Django 4.2 on 2023-06-06 13:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_posts"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="followers",
            field=models.ManyToManyField(
                blank=True, related_name="userprofile", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="following",
            field=models.ManyToManyField(
                blank=True, related_name="userprofile", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
