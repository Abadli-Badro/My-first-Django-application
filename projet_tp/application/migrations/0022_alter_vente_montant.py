# Generated by Django 4.1.4 on 2023-01-13 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0021_remove_stocker_produits_remove_stocker_stocks_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vente',
            name='Montant',
            field=models.IntegerField(default=0),
        ),
    ]