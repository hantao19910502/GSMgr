# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('openserver', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MergerGroupInTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('targetid', models.CharField(unique=True, max_length=255, verbose_name='\u5408\u6210\u670d\u540d\u79f0')),
            ],
        ),
        migrations.CreateModel(
            name='MergerServerTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200, verbose_name='\u5408\u670d\u63cf\u8ff0')),
                ('operatetime', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('status', models.IntegerField(default=1, verbose_name='\u4efb\u52a1\u72b6\u6001', choices=[(1, '\u65b0\u63d0\u4ea4'), (2, '\u5408\u670d\u4e2d'), (3, '\u5931\u8d25'), (4, '\u5b8c\u6210'), (5, '\u8b66\u544a')])),
                ('execoutput', models.TextField(verbose_name='\u6267\u884c\u65e5\u5fd7')),
                ('gameproject', models.ForeignKey(verbose_name='\u6e38\u620f\u9879\u76ee', to='openserver.GameProject')),
                ('operator', models.ForeignKey(verbose_name='\u64cd\u4f5c\u4eba', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='mergergroupintask',
            name='task',
            field=models.ForeignKey(verbose_name='\u5408\u670d\u4efb\u52a1\u5355', to='mergerserver.MergerServerTask'),
        ),
    ]
