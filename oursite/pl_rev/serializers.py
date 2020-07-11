from rest_framework import serializers
from .models import Plmanager_info

class Plmanager_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plmanager_info
        fields = ('plid','plmanager','plpassword',)

