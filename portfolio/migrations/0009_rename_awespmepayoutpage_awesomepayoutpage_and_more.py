# Generated by Django 5.2.1 on 2025-05-14 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_homepage_credit_cards_page_homepage_crypto_page_and_more'),
        ('portfolio', '0008_cryptoindexpage'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AwespmePayOutPage',
            new_name='AwesomePayOutPage',
        ),
        migrations.RenameModel(
            old_name='CeditCardsIndexPage',
            new_name='CreditCardsIndexPage',
        ),
    ]
