# Generated by Django 4.1.4 on 2023-01-12 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0017_rename_produits_bl_effectuer_vente_produits_vente'),
    ]

    operations = [
        migrations.AddField(
            model_name='stocker',
            name='Prix_Vente_Produit',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bon_livraison',
            name='Remise_BL',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='facture',
            name='Remise_Facture',
            field=models.IntegerField(default=0),
        ),
    ]
