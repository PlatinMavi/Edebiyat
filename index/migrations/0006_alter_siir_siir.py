# Generated by Django 4.0.6 on 2023-03-21 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_remove_siir_foto_siir_siir'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siir',
            name='siir',
            field=models.TextField(max_length=512),
        ),
    ]