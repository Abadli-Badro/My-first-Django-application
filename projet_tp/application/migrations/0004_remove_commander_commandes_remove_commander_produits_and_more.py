# Generated by Django 4.1.4 on 2023-01-07 23:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_alter_client_tel_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commander',
            name='Commandes',
        ),
        migrations.RemoveField(
            model_name='commander',
            name='Produits',
        ),
        migrations.RemoveField(
            model_name='etablire_bl',
            name='Bons',
        ),
        migrations.RemoveField(
            model_name='etablire_bl',
            name='Produits',
        ),
        migrations.RemoveField(
            model_name='etablire_facture',
            name='Factures',
        ),
        migrations.RemoveField(
            model_name='etablire_facture',
            name='Produits',
        ),
        migrations.AlterField(
            model_name='facture',
            name='Total_HT_Facture',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='facture',
            name='Total_TTC_Facture',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='etablire_facture',
            name='Factures',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='facture', to='application.facture'),
        ),
        migrations.AddField(
            model_name='etablire_facture',
            name='Produits',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='produitsFACTURE', to='application.product'),
        ),
    ]
