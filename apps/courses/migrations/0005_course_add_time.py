# Generated by Django 2.2.7 on 2020-02-07 11:34

from django.db import migrations, models
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20200107_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='add_time',
            field=models.DateTimeField(default=timezone.now, verbose_name='添加的时间'),
        ),
    ]
