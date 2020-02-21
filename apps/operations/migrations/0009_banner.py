# Generated by Django 2.2.7 on 2020-02-17 11:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0008_auto_20200212_1849'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建的时间')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('image', models.ImageField(max_length=200, upload_to='banner/%Y/%m', verbose_name='图片')),
                ('url', models.URLField(max_length=100, verbose_name='访问地址')),
                ('index', models.IntegerField(default=0, verbose_name='顺序')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
            },
        ),
    ]
