# Generated by Django 4.2 on 2023-06-08 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0008_alter_posts_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="posts",
            name="content",
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
