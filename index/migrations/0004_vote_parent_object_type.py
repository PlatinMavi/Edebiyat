# Generated by Django 4.1.3 on 2023-04-08 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_vote_delete_vote2'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='parent_object_type',
            field=models.TextField(choices=[('a', 'Yorum'), ('b', 'Eser')], default='a'),
        ),
    ]