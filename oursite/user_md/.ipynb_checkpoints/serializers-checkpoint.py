from rest_framework import serializers
from .models import User_info,Receiveinfo,Cart,Likestores,Records

class User_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_info
        fields = ('uid','uname','upassword','ID_num','uphone','BC_num')

class ReceiveinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiveinfo
        fields = ('uid','rid','rname','raddress','rphone')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('uid','pid','psum')

class LikestoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likestores
        fields = ('uid','sid')


class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = ('uid','pid','stime')
        ordering = ["-stime"]