from rest_framework import serializers
from .models import Doc_info
#from pro_up.models import Pro_info

class Doc_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doc_info
        fields = ('did','dname','dpassword','dprove','dtitle','dintro','dphone','dstate','skilled','dscore',)

class Doc_clickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doc_info
        fields = ('did','dname','dpassword','dprove','dtitle','dintro','dphone','dstate','skilled','dscore',)
     
'''
class Sup_searchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sup_info
        fields = ('sid','sname','sintro',)
'''  


    
    
    
    

