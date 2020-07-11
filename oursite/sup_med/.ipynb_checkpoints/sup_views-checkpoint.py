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

import base64
import cv2
import numpy as np
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ZJTAutoTestingPlatform.settings")
import django
django.setup()

from .models import Sup_info,Sup_token
from pro_up.models import Pro_info,Pro_token
from order_md.models import Order_info
from oursite.settings import SECRET_KEY
from .serializers import *
from django.db.models import Q



class TokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        # 直接在请求头中获取token
        token = request._request.GET.get('token')
        token_obj = models.Sup_token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("商家认证失败")
        else:
            datetime_now = datetime.now()
            if token_obj.expiration_time > datetime_now:
                # 在 rest framework 内部会将两个字段赋值给request，以供后续操作使用
                return (token_obj.sup, token_obj)
            else:
                raise exceptions.AuthenticationFailed("商家token过期,请重新登录")

    def authenticate_header(self, request):
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        pass


# 生成token
def md5(username):
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(SECRET_KEY + str(time.time()), encoding='utf-8'))
    return m.hexdigest()

#商家登录界面
@api_view(['POST'])
def sup_login(request):
    if request.method == 'POST':
        sup = request.data.get('sup',None)
        if not sup:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg": "信息不完整"}))
        sname = sup.get('sname', None)
        spassword = sup.get('spassword', None)
        #sprove = sup.get('sprove',None)
        print(sname)
        print(spassword)
        #print(sprove)
        if sname != "":
            if spassword != "":
                try:
                    db_search = Sup_info.objects.get(sname=sname)
                    if db_search.spassword != spassword:
                        print("密码错误")
                        return Response(status=status.HTTP_401_UNAUTHORIZED, data=json.dumps({"msg": "密码错误"}))
                    else:
                        sid = db_search.sid
                        token = md5(str(sid))
                        expiration_time = datetime.now() + dateutil.relativedelta.relativedelta(weeks=1)
                        print(expiration_time, type(expiration_time))
                        defaults = {
                            "token": token,
                            "expiration_time": expiration_time
                        }
                        Sup_token.objects.update_or_create(sup=db_search, defaults=defaults)
                        print("登录成功")
                        return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "登录成功", "token": token}))
                except Exception as e:
                    print(str(e))
                    print("该商家不存在")
                    return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "用户不存在"}))
            else:
                print("密码为空")
                return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        else:
            print("用户名为空")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        
        


    
 
#商家注册界面
@api_view(['POST'])
def sup_register(request):
    if request.method == 'POST':
        print(request.data)
        sup = request.data.get('sup',None)
        if not sup:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        sname = sup.get('sname',None)
        spassword = sup.get('spassword', None)
        p = sup.get("sprove")
        strs = p.split(",")[1]
        image_data = base64.b64decode(strs)
        #s = str(sname)+"_"+str(sname)
        s = str(sname)+"_sprove"
        imname = 'static/sup_med/'+str(s)+'.jpg'
        file = open(imname,'wb')
        file.write(image_data)
        file.close()
        sprove = imname
        print(sname)
        print(spassword)
        #print(sprove)
        if sname != "":
            if spassword != "":
                if sprove != "":
                    try:
                        db_search = Sup_info.objects.filter(sname=sname)
                        if not db_search:
                            
                            new_db = Sup_info()
                            new_db.sname = sname
                            new_db.spassword = spassword
                            new_db.sprove = sprove
                            new_db.save() 
                            print("注册成功")
                            return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "注册成功"}))
                        else:
                            print("该商户名已存在")
                            return Response(status=status.HTTP_300_MULTIPLE_CHOICES, data=json.dumps({"msg": "该商家已存在"}))
                    except Exception as e:
                        print(str(e))
                        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
                else:
                    print("认证图片为空")
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
            else:
                print("密码为空")
                return  Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        else:
            print("商家名为空")
            return  Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))


import pytz          
 #商家个人信息展示接口
@api_view(['POST'])  
def sinfo_show(request):
    if request.method == 'POST':
        print("a")
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = Sup_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.sup_id)
                sid = token_user.sup_id
                sup = Sup_info.objects.filter(sid=sid)
                if sup:
                    serializer = Sup_clickSerializer(sup, many=True)
                    print("获得序列化sup")
                    for item in serializer.data:
                        print(item)
                        #print(serializer.data)
                        sid = item["sid"]
                        sup1 = Sup_info.objects.filter(sid=sid).first()
                        path = os.path.join('http://120.24.164.113:8080/', sup1.sprove)
                        item["sprove"] = path
                        print(path)
                        path1 = os.path.join('http://120.24.164.113:8080/', sup1.logo)
                        item["logo"] = path1   
                    print(serializer.data)
                    return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"商家不存在"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))    
          
          
#商家个人信息修改
@api_view(['POST'])  
def sinfo_edit(request):
    if request.method == 'POST':
        print("a")
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = Sup_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.sup_id)
                sid = token_user.sup_id                           
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
        print(request.data)
        sup = request.data
        sname = sup.get('sname',None)
        spassword = sup.get('spassword',None)
        sprove = sup.get('sprove',None)
        #logo = sup.get('logo',None) #商家logo
        saddress = sup.get('saddress',None) #地址
        sintro = sup.get('sintro',None) #店铺介绍
        stag = sup.get('stag',None) #商家标签
        skeyword = sup.get('skeyword',None) #推荐搜索词
        sphone = sup.get('sphone',None)
        p = request.data.get("logo")
        sp = request.data.get("sprove")
        strs = p.split(",")[1]
        strs1 = sp.split(",")[1]
        image_data = base64.b64decode(strs)
        image_data1 = base64.b64decode(strs1)
        #s = str(sname)+"_"+str(sname)
        s = str(sname)+"_logo"
        s1 = str(sname)+"_sprove_update"
        imname = 'static/sup_med/'+str(s)+'.jpg'
        imname1 = 'static/sup_med/'+str(s1)+'.jpg'
        file = open(imname,'wb')
        file1 = open(imname1,'wb')
        file.write(image_data)
        file1.write(image_data1)
        file.close()
        file1.close()
        logo= imname
        sprove = imname1
        db_search1=Sup_info.objects.filter(sid=sid)
        print("1")
        try:
            if not db_search1:
                return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "您还未登录"}))
                print("2")
            else:
                db_search1.update(sname = sname)
                db_search1.update(spassword= spassword)
                db_search1.update(sprove = sprove)
                print(sprove)
                db_search1.update(saddress = saddress)
                db_search1.update(sintro = sintro)
                db_search1.update(stag = stag)
                db_search1.update(skeyword= skeyword)
                db_search1.update(sphone = sphone)
                db_search1.update(logo = logo)
                #db_search1.save()
                print("3")
                return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "修改成功"}))
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))


'''#商家查看订单接口
@api_view(['POST'])
def sup_check_order(request):
    if request.method == 'POST':
        #sid = request.data.get('sid',None)
        print("a")
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = Sup_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.sup_id)
                sid = token_user.sup_id 
                order = Order_info.objects.filter(sid=sid)
                dic = order.values()
                list1 = []
                #res = Ordinfo.objects.none()
                for item in dic:
                    #ordno = item["ordno"]
                    #objs = Ordproducts.objects.filter(ordno=ordno)
                    #objs1 = Order_info.objects.filter(ordno=ordno)
                    list1.append(item["ordno"])
                len1 = len(list1)
                i = 0
                print("222")
                res = Ordinfo.objects.none()
                while i<len1:
                    pro1 = Ordinfo.objects.filter(ordno=list1[i])
                    res = res | pro1
                    print("333")
                    print("555")
                    i+=1   

                if res:
                    serializer1 = Sup_check_orderProductSerializer(res, many=True)
                    print(serializer1.data)
                    return Response(status=status.HTTP_200_OK,data=json.dumps(serializer1.data))
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"您当前还没有待处理订单"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"})) '''
        
 
        
#商家查看订单接口
@api_view(['POST'])
def sup_check_order(request):
    if request.method == 'POST':
        #sid = request.data.get('sid',None)
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = Sup_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.sup_id)
                sid = token_user.sup_id 
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
        order = Order_info.objects.filter(sid=sid)
        print("333")
        if order:
            serializer1 = Sup_check_orderSerializer(order, many=True)
            print(serializer1.data)
            return Response(status=status.HTTP_200_OK,data=json.dumps(serializer1.data))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"您当前还没有待处理订单"}))
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"})) 
             
            
            
    


                
#商家端已上架商品展示
@api_view(['GET'])
def sup_pro_man(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = Sup_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.sup_id)
                sid = token_user.sup_id                           
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
        print(sid)
        sup = Sup_info.objects.filter(sid=sid)
        if sup:
            #商家的信息序列
            #serializer1 = Sup_clickSerializer(sup, many=True)
            #商家的商品set
            pro = Pro_info.objects.filter(sid=sid)
            if pro:
                #商家已上架商品的序列
                serializer2 = Pro_searchSerializer(pro, many=True)
                for item in serializer2.data:
                    #pro承接商家个人信息
                    #item["pro"] = serializer2.data
                    pro = Pro_info.objects.filter(pid=item["pid"]).first()
                    path = os.path.join('http://120.24.164.113:8080/', pro.p_picture)
                    item["p_picture"] = path
                    
                print(serializer2.data)
                return Response(status=status.HTTP_200_OK,data=json.dumps(serializer2.data))
            else:
                return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"该商家无商品"}))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"无此商家"}))

        
#查找商家
@api_view(['GET'])  
def search_sup(request):
    if request.method == 'GET':
        query = request.GET.get("search")
        result = Sup_info.objects.filter(Q(sname__icontains=query) | Q(sintro__icontains=query) | Q(stag__icontains=query) | Q(skeyword__icontains=query) | Q(saddress__icontains=query))
        if result:
            serializer = Sup_searchSerializer(result, many=True)
            for item in serializer.data:
                sup = Sup_info.objects.filter(sid=item["sid"]).first()
                path = os.path.join('http://120.24.164.113:8080/', sup.logo)
                item["logo"] = path
            print(serializer.data)
            return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"检索结果为空"}))
        
 
class SupListView(generics.ListAPIView):
    queryset = Sup_info.objects.all()
    serializer_class = Sup_searchSerializer 
    filter_backends = [filters.SearchFilter]
    search_fields = ['sname', 'sintro']
    def test(request):
        return  Response(data=json.dumps({"msg":"信息不完整"}))
   
