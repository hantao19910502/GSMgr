# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.db import models
from userinfo.models import User
from openserver.models import GameProject

# Create your models here.
class MergerServerTask(models.Model):
    STATUS = (
        (1, "新提交"),
        (2, "合服中"),
        (3, "失败"),
        (4, "完成"),
        (5, "警告"),
    )


    description = models.CharField(max_length=200, verbose_name="合服描述")
    operator = models.ForeignKey(User, verbose_name="操作人")
    gameproject = models.ForeignKey(GameProject,verbose_name="游戏项目")
    operatetime = models.DateTimeField(auto_now=True, verbose_name="创建时间")
    status = models.IntegerField(choices=STATUS, default=1, verbose_name="任务状态")
    execoutput = models.TextField(verbose_name="执行日志")

    def __unicode__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('mergerserver:mergerservertask_detail', kwargs={'pk': self.pk})

class MergerGroupInTask(models.Model):
    task = models.ForeignKey(MergerServerTask, verbose_name="合服任务单")
    targetid = models.CharField(max_length=255, unique=True, verbose_name="合成服名称")
