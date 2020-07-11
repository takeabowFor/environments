from rest_framework import serializers
from .models import Order_info, Ordproducts, Ordpay, Ordrec, Ordcom, test

class Order_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_info
        fields = ('ordno','add_time','sid','ordprice','ordstatus')

class Order_clickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_info
        fields = ('ordno','add_time','unotes','sid','ordprice','ordstatus','expno')
     
class Order_expSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_info
        fields = ('ordno','expno')
 
class Order_proSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordproducts
        fields = ('ordno','pid','psum')

class OrdcomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ordcom
        fields = ('uid','pid','comment')

     
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = test
        fields = '__all__'