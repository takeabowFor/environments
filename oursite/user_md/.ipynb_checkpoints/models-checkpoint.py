from django.db import models
from datetime import datetime
'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ZJTAutoTestingPlatform.settings")
import django
django.setup()
'''
from pro_up.models import Pro_info
from sup_med.models import Sup_info

class User_info(models.Model):
    uid = models.AutoField(primary_key = True)
    uname = models.CharField(max_length=256)
    upassword = models.CharField(max_length=32)
    ID_num = models.CharField(max_length=32, null=True)
    BC_num = models.CharField(max_length=32, null=True)
    uphone = models.CharField(max_length=32)
    uimage = models.CharField(max_length=256, default='static/user_md/空.jpg')

    def __str__(self):
        return str(self.uname)

class User_token(models.Model):
    user = models.OneToOneField(to='User_info', to_field='uid', unique=True, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=64, verbose_name="用户token")
    expiration_time = models.DateTimeField(default=datetime.now, verbose_name="过期时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    
    class Mate:
        managed = True
        db_table = "user_token"
        verbose_name = "用户token"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.token

     
class Receiveinfo(models.Model):
    uid = models.ForeignKey(to='User_info', to_field='uid', on_delete=models.CASCADE)
    rid = models.AutoField(primary_key = True)
    rname = models.CharField(max_length=256)
    raddress = models.CharField(max_length=512)
    rphone = models.CharField(max_length=32)

    def __str__(self): 
        return str(self.raddress)

class Cart(models.Model):
    uid = models.ForeignKey(to='User_info', to_field='uid', on_delete=models.CASCADE)
    pid = models.ForeignKey(to='pro_up.Pro_info', to_field='pid', on_delete=models.CASCADE)
    psum= models.IntegerField()
    
    def __str__(self):
        return str(self.psum)

class Likestores(models.Model):
    uid = models.ForeignKey(to='User_info', to_field='uid', on_delete=models.CASCADE)
    sid = models.ForeignKey(to='sup_med.Sup_info', to_field='sid', on_delete=models.CASCADE)
  
   
#    def __str__(self):
#        return self.sid

class Records(models.Model):
    uid = models.ForeignKey(to='User_info', to_field='uid', on_delete=models.CASCADE)
    pid = models.ForeignKey(to='pro_up.Pro_info', to_field='pid', on_delete=models.CASCADE)
    stime = models.DateTimeField(default=datetime.now, verbose_name="浏览时间")    
    
    class Meta:
        ordering = ['-stime'] 
      
    def __str__(self):
        return str(self.stime)