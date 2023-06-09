# Generated by Django 4.2.1 on 2023-07-01 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visual_i_ching_app', '0009_alter_userdetail_current_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='reading',
            name='is_public',
            field=models.BooleanField(db_comment='Readings are private by default, but can be made public so that others can access the reading via its unique URL.', default=False),
        ),
    ]
