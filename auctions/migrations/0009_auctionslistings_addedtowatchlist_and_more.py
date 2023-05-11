# Generated by Django 4.2 on 2023-05-09 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0008_remove_commentsauctions_product_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionslistings",
            name="addedtowatchlist",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="auctionslistings",
            name="watchlist_adder",
            field=models.CharField(default="None", max_length=64),
        ),
        migrations.AlterField(
            model_name="auctionslistings",
            name="is_closed",
            field=models.BooleanField(default=False),
        ),
    ]
