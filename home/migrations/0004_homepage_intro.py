# Generated by Django 5.2.1 on 2025-05-14 05:37

import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_credit_cards_page_homepage_crypto_page_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='intro',
            field=wagtail.fields.RichTextField(blank=True),
        ),
    ]
