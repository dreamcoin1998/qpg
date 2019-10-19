# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Youshengshu(models.Model):
    author = models.TextField(blank=True, null=True, verbose_name='作者')
    name = models.TextField(blank=True, null=True, verbose_name='书名')
    voice = models.TextField(blank=True, null=True, verbose_name='播音')
    type = models.CharField(max_length=12, blank=True, null=True, verbose_name='类型')
    link = models.TextField(blank=True, null=True, verbose_name='链接')
    time = models.DateField(blank=True, null=True, verbose_name='发布时间')
    status = models.CharField(max_length=12, blank=True, null=True, verbose_name='状态')
    ### 包含多少集信息和是否免费信息
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'youshengshu'
        verbose_name = '有声书'
        verbose_name_plural = verbose_name
