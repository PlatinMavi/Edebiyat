# Generated by Django 4.1.3 on 2023-04-16 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_comment_interest_rate_literatureobject_interest_rate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='message',
            new_name='content',
        ),
    ]