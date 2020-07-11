#coding=utf-8
import importlib
import sys
importlib.reload(sys)
import json
import hashlib
import time
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework import filters

from .models import Pro_info
from .serializers import Pro_searchSerializer


class ProListView(generics.ListAPIView):
    queryset = Pro_info.objects.all()
    serializer_class = Pro_searchSerializer 
    filter_backends = [filters.SearchFilter]
    search_fields = ['pname', 'category','symptoms','usage','pkeyword']
    def user_test(request):
        return  Response(data=json.dumps({"msg":"信息不完整"}))