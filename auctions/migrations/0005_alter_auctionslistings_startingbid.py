# Generated by Django 4.2 on 2023-05-05 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_rename_bid_bid_bidproduct_bid_bidprice"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auctionslistings",
            name="startingbid",
            field=models.IntegerField(default="startingbid"),
        ),
    ]
