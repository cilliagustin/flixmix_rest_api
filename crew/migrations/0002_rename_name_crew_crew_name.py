# Generated by Django 3.2.18 on 2023-04-01 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crew', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crew',
            old_name='name',
            new_name='crew_name',
        ),
    ]
