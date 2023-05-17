from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Users(AbstractUser):
    set_choices = (
        ('男','男'),
        ('女','女')
    )

    age = models.CharField(verbose_name='年龄',max_length=16,default=18)
    set = models.CharField(verbose_name='性别',max_length=12,default='男',choices=set_choices)

    class Meta:
        verbose_name = u"用户表"
        verbose_name_plural = u"用户表"


class Case_item(models.Model):
    name = models.CharField(verbose_name='标题',max_length=1200,default='')
    text = models.CharField(verbose_name='实体',max_length=240,default='')
    itype = models.CharField(verbose_name='频道',max_length=240,default='')
    biaoqian = models.CharField(verbose_name='标签',max_length=240,default='')
    lianjie = models.CharField(verbose_name='链接',max_length=540,default='')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"短视频表"
        verbose_name_plural = u"短视频表"

class Pinfen(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    case = models.ForeignKey(Case_item,on_delete=models.CASCADE)
    data = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    def __str__(self):
        return self.case

    class Meta:
        verbose_name = u"点赞表"
        verbose_name_plural = u"点赞表"


class PinLun(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    case = models.ForeignKey(Case_item,on_delete=models.CASCADE)
    content = models.TextField(verbose_name='评论',default='')
    data = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    def __str__(self):
        return self.case.name

    class Meta:
        verbose_name = u"评论表"
        verbose_name_plural = u"评论表"



class Biaoqian(models.Model):
    user = models.ForeignKey(Users,on_delete=models.CASCADE)
    biaoqian = models.CharField(verbose_name='标签',default='',max_length=300)
    fenshu = models.FloatField(verbose_name='热度',default=0)
    data = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    def __str__(self):
        return self.biaoqian

    class Meta:
        verbose_name = u"用户标签表"
        verbose_name_plural = verbose_name
