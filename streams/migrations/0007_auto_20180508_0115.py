# Generated by Django 2.0.5 on 2018-05-08 01:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streams', '0006_auto_20180506_2129'),
    ]

    operations = [
        migrations.RenameField(
            model_name='streampost',
            old_name='down_votes',
            new_name='downvotes',
        ),
        migrations.RenameField(
            model_name='streampost',
            old_name='up_votes',
            new_name='upvotes',
        ),
    ]