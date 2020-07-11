from django.db import models
#from django.db import models
from datetime import datetime


#Create your models here.
class Sup_info(models.Model):
    sid = models.AutoField(primary_key = True)
    sname = models.CharField(max_length=256)
    spassword = models.CharField(max_length=64)
    #资质认证改为图片，不为空
    sprove = models.CharField(max_length=256)
    saddress = models.CharField(max_length=1024,null=True)
    rank = models.IntegerField(null=True)
    scert= models.CharField(max_length=1024,null=True)
    #logo商家头像，不为空
    logo = models.CharField(max_length=256,default="static/sup_med/空.jpg")
    sintro = models.CharField(max_length=2048, null=True)
    marked= models.IntegerField(default=0)
    stag = models.CharField(max_length=2048,null=True)
    skeyword = models.CharField(max_length=2048,null=True)
    profit = models.FloatField(null=True)
    sphone = models.CharField(max_length=32,null=True)
    likesum = models.IntegerField(default=0)
    sstate = models.CharField(max_length=32,default="待审核")
    


    def __str__(self):
        return self.sname

class Sup_token(models.Model):
    sup = models.OneToOneField(to='Sup_info', to_field='sid', unique=True, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=64, verbose_name="商家token")
    expiration_time = models.DateTimeField(default=datetime.now, verbose_name="过期时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Mate:
        managed = True
        db_table = "sup_token"
        verbose_name = "商家token"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.token
     

    
    


     


    
