# Generated by Django 4.2.11 on 2025-02-22 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_remove_listing_bids_remove_listing_comments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=999999999),
        ),
    ]
