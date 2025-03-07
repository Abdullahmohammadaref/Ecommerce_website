# Generated by Django 4.2.11 on 2025-02-21 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_category_bid_bidder_alter_listing_picture_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='name',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='bid',
            name='bidder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidder', to=settings.AUTH_USER_MODEL),
        ),
    ]
