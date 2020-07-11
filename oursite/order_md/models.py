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
from user_md.models import User_info, Receiveinfo

class Order_info(models.Model):
    ordno = models.AutoField(primary_key = True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="下单时间")
    uid = models.ForeignKey(to='user_md.User_info', to_field='uid', on_delete=models.CASCADE)
    unotes = models.CharField(max_length=2048,null=True)
    sid = models.ForeignKey(to='sup_med.Sup_info', to_field='sid', on_delete=models.CASCADE)
    ordprice = models.FloatField()
    ordstatus = models.CharField(max_length=32, default="未发货")
    expno = models.IntegerField(null=True)
    
    class Meta:
        ordering = ['-add_time']

    def __str__(self):
        return str(self.ordno)
     

class Ordproducts(models.Model):
    ordno = models.ForeignKey(to='Order_info', to_field='ordno', on_delete=models.CASCADE)
    pid = models.ForeignKey(to='pro_up.Pro_info', to_field='pid', on_delete=models.CASCADE)
    psum = models.IntegerField()
    

    def __str__(self):
        return str(self.pid)

'''class Ordinfo(models.Model):
    ordno = models.ForeignKey(to='Order_info', to_field='ordno', on_delete=models.CASCADE)
    pid = models.ForeignKey(to='pro_up.Pro_info', to_field='pid', on_delete=models.CASCADE)
    psum = models.IntegerField()
    add_time = models.DateTimeField(default=datetime.now, verbose_name="下单时间")
    uid = models.ForeignKey(to='user_md.User_info', to_field='uid', on_delete=models.CASCADE)
    unotes = models.CharField(max_length=256,null=True)
    sid = models.ForeignKey(to='sup_med.Sup_info', to_field='sid', on_delete=models.CASCADE)
    ordprice = models.FloatField()
    ordstatus = models.CharField(max_length=32, default="未发货")
    expno = models.IntegerField(null=True)'''
    

class Ordpay(models.Model):
    payid = models.AutoField(primary_key = True)
    ordno = models.ForeignKey(to='Order_info', to_field='ordno', on_delete=models.CASCADE)
    paytime = models.DateTimeField(default=datetime.now, verbose_name="支付时间")   

    def __str__(self):
        return str(self.payid)

class Ordrec(models.Model):
    ordno = models.ForeignKey(to='Order_info', to_field='ordno', on_delete=models.CASCADE)
    uid = models.ForeignKey(to='user_md.User_info', to_field='uid', on_delete=models.CASCADE)
    rid = models.ForeignKey(to='user_md.Receiveinfo', to_field='rid', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.rid)

class Ordcom(models.Model):
    ordno = models.ForeignKey(to='Order_info', to_field='ordno', on_delete=models.CASCADE)
    uid = models.ForeignKey(to='user_md.User_info', to_field='uid', on_delete=models.CASCADE)
    pid = models.ForeignKey(to='pro_up.Pro_info', to_field='pid', on_delete=models.CASCADE)
    comment = models.CharField(max_length=2048, null=True)
    
    def __str__(self):
        return str(self.comment)

class Rx_order(models.Model):
    ordno = models.ForeignKey(to='Order_info', to_field='ordno', on_delete=models.CASCADE)
    uid = models.ForeignKey(to='user_md.User_info', to_field='uid', on_delete=models.CASCADE)
    Rx = models.CharField(max_length=256)
    
    def __str__(self):
        return str(self.ordno)

class test(models.Model):
    image = models.CharField(max_length=256)
    