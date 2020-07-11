from django.db import models
#from django.db import models
from datetime import datetime


#Create your models here.
class Doc_info(models.Model):
    did = models.AutoField(primary_key = True)
    dname = models.CharField(max_length=50)
    dpassword = models.CharField(max_length=50)
    #资质材料
    dprove = models.CharField(max_length=50)
    #职称
    dtitle = models.CharField(max_length=50,null=True)
    #简介
    dintro = models.CharField(max_length=50,null=True)
    dphone = models.CharField(max_length=50,null=True)
    dstate = models.CharField(max_length=50,default="待审核")
    #主治
    skilled = models.CharField(max_length=50,null=True)
    #满意度
    dscore = models.FloatField(null=True)
    
    def __str__(self):
        return self.sname

class Doc_token(models.Model):
    doc = models.OneToOneField(to='Doc_info', to_field='did', unique=True, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=64, verbose_name="医生token")
    expiration_time = models.DateTimeField(default=datetime.now, verbose_name="过期时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Mate:
        managed = True
        db_table = "doc_token"
        verbose_name = "医生token"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.token
     


     


    
