# Generated by Django 4.1.7 on 2023-04-05 12:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_kitap_key_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kitap',
            name='key_name',
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('author_name', models.CharField(max_length=30, verbose_name='Kullanıcı Adı')),
                ('message', models.CharField(max_length=1000, verbose_name='Mesaj')),
                ('parent', models.ForeignKey(default='lorem_ipsum', on_delete=django.db.models.deletion.SET_DEFAULT, to='index.kitap', verbose_name='Yorum Yapılan Eser')),
            ],
        ),
    ]
