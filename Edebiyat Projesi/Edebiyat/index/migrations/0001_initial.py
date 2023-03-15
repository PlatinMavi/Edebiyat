# Generated by Django 4.0.6 on 2023-03-15 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dergi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=255)),
                ('yayinci', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Kitap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=255)),
                ('yazar', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Siir',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=255)),
                ('yazar', models.CharField(max_length=255)),
            ],
        ),
    ]
