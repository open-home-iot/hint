# Generated by Django 2.1 on 2018-09-09 10:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0003_auto_20180909_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceconfiguration',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
