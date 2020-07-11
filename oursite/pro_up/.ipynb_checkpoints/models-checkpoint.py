from django.db import models
#from django.db import models
from datetime import datetime
from sup_med.models import Sup_info,Sup_token
from django.utils import timezone


#Create your models here.
class Pro_info(models.Model):
    #自增属性，设置为主键
    pid = models.AutoField(primary_key = True)
    sid = models.ForeignKey(to='sup_med.Sup_info',to_field = 'sid', on_delete = models.CASCADE)
    p_picture = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    pname = models.CharField(max_length=256)
    ptype = models.CharField(max_length=256)
    price = models.FloatField()
    psize = models.CharField(max_length=256)
    symptoms = models.CharField(max_length=256)
    pusage = models.CharField(max_length=256)
    para= models.CharField(max_length=256)
    problems = models.CharField(max_length=256)
    pkeyword = models.CharField(max_length=256)
    address = models.CharField(max_length=256,default="")
    stock = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    #ptime = models.DateTimeField(auto_now_add = True)#加入时间字段
    ptime = models.DateTimeField(default=datetime.now,null=True)#加入时间字段
    
    def __str__(self):
        return str(self.pid)

class Pro_token(models.Model):
    pro = models.OneToOneField(to='Pro_info', to_field='pid', unique=True, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=64, verbose_name="商品token")
    expiration_time = models.DateTimeField(default=datetime.now, verbose_name="过期时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Mate:
        managed = True
        db_table = "pro_token"
        verbose_name = "商品token"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.token

     
