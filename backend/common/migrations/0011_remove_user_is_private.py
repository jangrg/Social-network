# Generated by Django 3.1.2 on 2020-12-07 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_post_liked_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_private',
        ),
    ]
