#coding=utf-8
import importlib
import sys
importlib.reload(sys)
import json
import hashlib
from datetime import datetime
import dateutil.relativedelta
import time
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework import generics
from rest_framework import filters

from .models import Doc_info,Doc_token
from pro_up.models import Pro_info,Pro_token
from sup_med.models import Sup_info,Sup_token
from oursite.settings import SECRET_KEY
from .serializers import *
from django.db.models import Q
from django.http import FileResponse
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ZJTAutoTestingPlatform.settings")
import django
django.setup()


class TokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        # 直接在请求头中获取token
        token = request._request.GET.get('token')
        token_obj = models.Doc_token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("医生认证失败")
        else:
            datetime_now = datetime.now()
            if token_obj.expiration_time > datetime_now:
                # 在 rest framework 内部会将两个字段赋值给request，以供后续操作使用
                return (token_obj.doc, token_obj)
            else:
                raise exceptions.AuthenticationFailed("医生token过期,请重新登录")

    def authenticate_header(self, request):
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        pass


# 生成token
def md5(username):
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(SECRET_KEY + str(time.time()), encoding='utf-8'))
    return m.hexdigest()

#医生登录界面
@api_view(['POST'])
def doc_login(request):
    if request.method == 'POST':
        doc = request.data.get('doc',None)
        dname = doc.get('dname',None)
        dpassword = doc.get('dpassword',None)
        #plmanager = request.data.get('plmanager',None)
        #plpassword = request.data.get('plpassword',None)
        print(doc)
        print(dname)
        print(dpassword)
        if not all([doc,dname,dpassword]):
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg": "the info must be complete!"}))
        if dname != "":
            if dpassword != "":
                try:
                    db_search = Doc_info.objects.get(dname=dname)
                    if db_search.dpassword != dpassword:
                        print("密码错误")
                        return Response(status=status.HTTP_401_UNAUTHORIZED, data=json.dumps({"msg": "password errorrr"}))
                    else:
                        did = db_search.did
                        token = md5(str(did))
                        expiration_time = datetime.now() + dateutil.relativedelta.relativedelta(weeks=1)
                        print(expiration_time, type(expiration_time))
                        defaults = {
                            "token": token,
                            "expiration_time": expiration_time
                        }
                        print("333")
                        Doc_token.objects.update_or_create(doc=db_search, defaults=defaults)
                        print("登录成功")
                        return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "llogin successful", "token": token}))
                except Exception as e:
                    print(str(e))
                    print("该医生不存在")
                    return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "this doc is not exist"}))
            else:
                print("密码为空")
                return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msgg":"the info must be complete"}))
        else:
            print("用户名为空")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msggg":"the info must be complete"}))
        

#doc注册界面
@api_view(['POST'])
def doc_register(request):
    if request.method == 'POST':
        print(request.data)
        doc = request.data.get('doc',None)
        if not doc:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"the info must be complete"}))
        dname = doc.get('dname',None)
        dpassword = doc.get('dpassword',None)
        #dprove = doc.get('dprove',None)
        #plmanager = request.data.get('plmanager',None)
        #plpassword = request.data.get('plpassword',None)
        print(dpassword)
        print(dname)
        if not all([doc,dname,dpassword]):
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msgg": "the info must be complete"}))
        
        if dname !=  "":
            if dpassword != "":
                try: 
                    db_search = Doc_info.objects.filter(dname=dname)
                    if not db_search:
                            
                        new_db = Doc_info()
                        new_db.dname = dname
                        new_db.dpassword = dpassword
                        #new_db.dprove = dprove
                        new_db.save() 
                        print("注册成功")
                        return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "register success"}))
                    else:
                        print("该医生已存在")
                        return Response(status=status.HTTP_300_MULTIPLE_CHOICES, data=json.dumps({"msg": "this doc has been in registration"}))
                except Exception as e:
                    print(str(e))
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "errorrr"}))       
            else:
                print("密码为空")
                return  Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msgg":"the info must be complete"}))
        else:
            print("账户为空")
            return  Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msggg":"the info must be complete"}))
