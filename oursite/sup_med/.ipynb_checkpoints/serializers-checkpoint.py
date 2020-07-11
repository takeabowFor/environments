from rest_framework import serializers
from .models import Sup_info
from pro_up.models import Pro_info
from order_md.models import Order_info
from user_md.models import User_info

class Sup_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sup_info
        fields = ('sid','sname','spassword','sprove','saddress','rank','scert','logo','sintro','marked','stag','skeyword','profit',)

class Sup_clickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sup_info
        fields = ('sid','sname','spassword','saddress','sintro','stag','skeyword','sphone','sstate','likesum')
     

class Sup_searchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sup_info
        fields = ('sid','sname','sintro',)
     
class Pro_searchSerializer(serializers.ModelSerializer):
    #thumb = ThumbnailImageField(source="p_picture", size_alias='medium')
    class Meta:
        model = Pro_info
        fields = ('pid','pname','price','sid')

class Sup_check_orderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_info
        fields = ('sid','uid','ordno','ordprice','ordstatus','add_time','expno','unotes',)
   
   
   

    
    

