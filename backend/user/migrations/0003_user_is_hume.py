# Generated by Django 3.2.4 on 2021-08-10 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_hume',
            field=models.BooleanField(default=False),
        ),
    ]
