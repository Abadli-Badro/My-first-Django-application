# Generated by Django 4.1.4 on 2023-01-07 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_alter_fournisseur_tel_fournisseur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='Tel_client',
            field=models.IntegerField(),
        ),
    ]
