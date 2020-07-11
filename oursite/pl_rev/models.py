from django.db import models
from datetime import datetime
'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ZJTAutoTestingPlatform.settings")
import django
django.setup()
'''
#from pro_up.models import Pro_info
#from sup_med.models import Sup_info

class Plmanager_info(models.Model):
    plid = models.AutoField(primary_key = True)
    plmanager = models.CharField(max_length=32)
    plpassword = models.CharField(max_length=32)

    def __str__(self):
        return str(self.plid)

class Plmanager_token(models.Model):
    pl = models.OneToOneField(to='Plmanager_info', to_field='plid', unique=True, on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=64, verbose_name="平台管理员token")
    expiration_time = models.DateTimeField(default=datetime.now, verbose_name="过期时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    
    class Mate:
        managed = True
        db_table = "plmanager_token"
        verbose_name = "平台管理员token"
        verbose_name_plural = verbose_name
    
    def __str__(self):
        return self.token

