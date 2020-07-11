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

from .models import Plmanager_info,Plmanager_token
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
        token_obj = models.Plmanager_token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("平台管理员认证失败")
        else:
            datetime_now = datetime.now()
            if token_obj.expiration_time > datetime_now:
                # 在 rest framework 内部会将两个字段赋值给request，以供后续操作使用
                return (token_obj.pl, token_obj)
            else:
                raise exceptions.AuthenticationFailed("平台管理员token过期,请重新登录")

    def authenticate_header(self, request):
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        pass


# 生成token
def md5(username):
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(SECRET_KEY + str(time.time()), encoding='utf-8'))
    return m.hexdigest()

#平台管理员登录界面
@api_view(['POST'])
def plmanager_login(request):
    if request.method == 'POST':
        pl = request.data.get('pl',None)
        #if not pl:
            #return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg": "信息不完整"}))
        plmanager = pl.get('plmanager',None)
        plpassword = pl.get('plpassword',None)
        #plmanager = request.data.get('plmanager',None)
        #plpassword = request.data.get('plpassword',None)
        print(plpassword)
        print(plmanager)
        if not all([pl,plmanager,plpassword]):
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msgg": "信息不完整"}))
        if plmanager != "":
            if plpassword != "":
                try:
                    db_search = Plmanager_info.objects.get(plmanager=plmanager)
                    if db_search.plpassword != plpassword:
                        print("密码错误")
                        return Response(status=status.HTTP_401_UNAUTHORIZED, data=json.dumps({"msg": "密码错误"}))
                    else:
                        plid = db_search.plid
                        token = md5(str(plid))
                        expiration_time = datetime.now() + dateutil.relativedelta.relativedelta(weeks=1)
                        print(expiration_time, type(expiration_time))
                        defaults = {
                            "token": token,
                            "expiration_time": expiration_time
                        }
                        print("333")
                        Plmanager_token.objects.update_or_create(pl=db_search, defaults=defaults)
                        print("登录成功")
                        return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "登录成功", "token": token}))
                except Exception as e:
                    print(str(e))
                    print("该管理员不存在")
                    return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "管理员不存在"}))
            else:
                print("密码为空")
                return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        else:
            print("用户名为空")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        
        
                    
                   
        

#平台管理员注册界面
@api_view(['POST'])
def plmanager_register(request):
    if request.method == 'POST':
        print(request.data)
        pl = request.data.get('pl',None)
        if not pl:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        plmanager = pl.get('plmanager',None)
        plpassword = pl.get('plpassword',None)
        #plmanager = request.data.get('plmanager',None)
        #plpassword = request.data.get('plpassword',None)
        print(plpassword)
        print(plmanager)
        if not all([pl,plmanager,plpassword]):
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msgg": "信息不完整"}))
        
        if plmanager !=  "":
            if plpassword != "":
                try: 
                    db_search = Plmanager_info.objects.filter(plmanager=plmanager)
                    if not db_search:
                            
                        new_db = Plmanager_info()
                        new_db.plmanager = plmanager
                        new_db.plpassword = plpassword
                        new_db.save() 
                        print("注册成功")
                        return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "注册成功"}))
                    else:
                        print("该管理员已存在")
                        return Response(status=status.HTTP_300_MULTIPLE_CHOICES, data=json.dumps({"msg": "该管理员已存在"}))
                except Exception as e:
                    print(str(e))
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))            
            else:
                print("密码为空")
                return  Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        else:
            print("密码为空")
            return  Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))

          
#查看商家资质          
import pytz          
@api_view(['GET'])
def show_supAuth(request):
    if request.method == 'GET':
        '''
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = Plmanager_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.plmanager_id)
                plid = token_user.plmanager_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msgg":"登录过期"}))
        '''
        result = []
        sup = Sup_info.objects.filter(sstate='待审核')
        for item in sup:
            re = {}
            re["sid"] = item.sid
            re["sname"] = item.sname
            re["saddress"] = item.saddress
            re["sstate"] = item.sstate
            s = Sup_info.objects.filter(sid=item.sid).first()
            path = os.path.join('http://120.24.164.113:8080/', s.sprove)
            re["sprove"] = path
            #re["pro"] = pro
            #re["image"] = str(path)
            result.append(re)
        return Response(status=status.HTTP_200_OK, data=json.dumps(result))
        
        
#审核商家资质       
import pytz          
@api_view(['POST'])
def check_supAuth(request):
    if request.method == 'POST':
        '''
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = Plmanager_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.plmanager_id)
                plid = token_user.plmanager_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
        '''
        print(request.data)
        sid = request.data.get('sid')
        result = request.data.get('result')
        print(result)
        if all([sid, result]):
            sup = Sup_info.objects.filter(sid=sid).first()
            if sup and sup.sstate == '待审核':
                if result == '通过':
                    print(result)
                    sup.sstate = '已认证'
                    sup.save()
                    return Response(status=status.HTTP_200_OK, data=json.dumps({'msg':'审核通过'}))
                else:
                    print(result)
                    sup.sstate = '认证失败'
                    sup.save()
                    return Response(status=status.HTTP_200_OK, data=json.dumps({'msg':'审核不通过qwq'}))
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({'msgg':'审核不了或审核过了'}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({'msgggg':'信息不完整'}))         

'''
#药品上架申请查看
import pytz          
@api_view(['GET'])
def show_upReq(request):
    if request.method == 'GET':
        result = []
        order = Order_info.objects.filter(ordstatus='待审核')
        for item in order:
            re = {}
            pro=[]
            db = Rx_order.objects.filter(ordno=item)
            ord_pro = Ordproducts.objects.filter(ordno=item)
            for i in ord_pro:
                p = Pro_info.objects.filter(pid=i.pid.pid).first()
                p_dict={}
                p_dict["pid"] = p.pid
                p_dict["pname"] = p.pname
                pro.append(p_dict)
            Rx = Rx_order.objects.filter(ordno=item.ordno).first()
            path = os.path.join('120.24.164.113:8080/', Rx.Rx.name)
            re["ordno"] = item.ordno
            re["pro"] = pro
            re["image"] = str(path)
            result.append(re)
        return Response(status=status.HTTP_200_OK, data=json.dumps(result))

#审核药品上架资格
import pytz          
@api_view(['POST'])
def check_upReq(request):
    if request.method == 'POST':
        print(request.data)
        ordno = request.data.get('ordno')
        result = request.data.get('result')
        print(result)
        if all([ordno, result]):
            order = Order_info.objects.filter(ordno=ordno).first()
            if order and order.ordstatus == '待审核':
                if result == '通过':
                    print(result)
                    order.ordstatus = '未发货'
                    order.save()
                    return Response(status=status.HTTP_200_OK, data=json.dumps({'msg':'审核通过'}))
                else:
                    order = Order_info.objects.filter(ordno=ordno)
                    order.delete()
                    pro = Ordproducts.objects.filter(ordno=ordno)
                    pro.delete()
                    ordpay = Ordpay.objects.filter(ordno=ordno)
                    ordpay.delete()
                    rec = Ordrec.objects.filter(ordno=ordno)
                    rec.delete()
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({'msg':'审核不通过，请重新下单'}))
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({'msg':'订单不能审核'}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({'msg':'信息不完整'}))
'''