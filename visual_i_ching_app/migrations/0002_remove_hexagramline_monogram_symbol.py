# Generated by Django 4.2.1 on 2023-06-12 22:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visual_i_ching_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hexagramline',
            name='monogram_symbol',
        ),
    ]
