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

from .models import User_info, User_token, Receiveinfo, Cart, Likestores, Records
from pro_up.models import Pro_info
from sup_med.models import Sup_info
from oursite.settings import SECRET_KEY
from .serializers import User_infoSerializer, ReceiveinfoSerializer, CartSerializer, LikestoresSerializer, RecordsSerializer
from pro_up.serializers import Pro_clickSerializer,Pro_searchSerializer
from sup_med.serializers import Sup_infoSerializer, Sup_clickSerializer

class TokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        # 直接在请求头中获取token
        token = request._request.GET.get('token')
        token_obj = models.User_token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("用户认证失败")
        else:
            datetime_now = datetime.now()
            if token_obj.expiration_time > datetime_now:
                # 在 rest framework 内部会将两个字段赋值给request，以供后续操作使用
                return (token_obj.user, token_obj)
            else:
                raise exceptions.AuthenticationFailed("用户token过期,请重新登录")

    def authenticate_header(self, request):
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        pass


# 生成token
def md5(username):
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(SECRET_KEY + str(time.time()), encoding='utf-8'))
    return m.hexdigest()

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        print(request.data)
        user = request.data.get('user',None)
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg": "信息不完整"}))
        uphone = user.get('uphone', None)
        upassword = user.get('upassword', None)
        print(uphone)
        print(upassword)
        if uphone != "":
            if upassword != "":
                try:
                    db_search = User_info.objects.get(uphone=uphone)
                    if db_search.upassword != upassword:
                        print("密码错误")
                        return Response(status=status.HTTP_401_UNAUTHORIZED, data=json.dumps({"msg": "密码错误"}))
                    else:
                        uid = db_search.uid
                        token = md5(str(uid))
                        expiration_time = datetime.now() + dateutil.relativedelta.relativedelta(weeks=1)
                        print(expiration_time, type(expiration_time))
                        defaults = {
                            "token": token,
                            "expiration_time": expiration_time
                        }
                        User_token.objects.update_or_create(user=db_search, defaults=defaults)
                        print("登录成功")
                        print(str(token))
                        result = {}
                        result["token"] = token
                        result["msg"] = "登陆成功"
                        user = User_info.objects.filter(uid=uid).first()
                        path = os.path.join('http://120.24.164.113:8080/', user.uimage)
                        result["uimage"] = path
                        return Response(status=status.HTTP_200_OK, data=json.dumps(result))
                except Exception as e:
                    print(str(e))
                    print("用户不存在")
                    return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "用户不存在"}))
            else:
                print("密码为空")
                return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        else:
            print("号码为空")
            return  Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))


@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        print(request.data)
        user = request.data.get('user',None)
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        uname = user.get('uname',None)
        upassword = user.get('upassword', None)
        uphone = user.get('uphone', None)
        print(uname)
        print(uphone)
        print(upassword)
        if uname != "":
            if uphone != "":
                if upassword != "":
                    try:
                        db_search = User_info.objects.filter(uphone=uphone)
                        if not db_search:
                            new_db = User_info()
                            new_db.uname = uname
                            new_db.uphone = uphone
                            new_db.upassword = upassword
                            new_db.save() 
                            print(new_db.uid)
                            token = md5(str(new_db.uid))
                            print(token)
                            expiration_time = datetime.now() + dateutil.relativedelta.relativedelta(weeks=1)
                            print(expiration_time, type(expiration_time))
                            defaults = {
                                "token": token,
                                "expiration_time": expiration_time
                            }
                            User_token.objects.update_or_create(user=new_db, defaults=defaults)
                            print("登录成功")
                            print(str(token))
                            print("注册成功")
                            return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "注册成功","token":token}))
                        else:
                            print("该手机号已存在")
                            return Response(status=status.HTTP_300_MULTIPLE_CHOICES, data=json.dumps({"msg": "该用户已存在"}))
                    except Exception as e:
                        print(str(e))
                        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
                else:
                    print("密码为空")
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
            else:
                print("号码为空")
                return  Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
        else:
            print("用户名为空")
            return  Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))

@api_view(['POST'])
def user_change(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
        #print(request.data)
        uname = request.data.get('uname',None)
        upassword = request.data.get('upassword', None)
        data = request.data.get('uimage', None)
        print(uname)
        print(upassword)
        if uname != "":
            try:
                db_search = User_info.objects.filter(uid=uid).first()
                if db_search:
                    db_search.uname = uname
                    db_search.save() 
                    print("修改成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "修改成功"}))
                else:
                    print("该用户不存在")
                    return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "该用户不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        if upassword != "":
            try:
                db_search = User_info.objects.filter(uid=uid).first()
                if db_search:
                    db_search.upassword = upassword
                    db_search.save() 
                    print("修改成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "修改成功"}))
                else:
                    print("该用户不存在")
                    return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "该用户不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        if data != "":
            strs = data.split(",")[1]
            image_data = base64.b64decode(strs)
            s = str(uid)
            imname = 'static/user_md/'+str(s)+'.jpg'
            file = open(imname,'wb')
            file.write(image_data)
            file.close()
            uimage = imname
            try:
                db_search = User_info.objects.filter(uid=uid).first()
                if db_search:
                    db_search.uimage = uimage
                    db_search.save() 
                    print("修改成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "修改成功"}))
                else:
                    print("该用户不存在")
                    return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "该用户不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))   
        else:
            print("信息不完整")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg": "信息不完整"}))
          
          
import pytz          
@api_view(['POST'])
def add_receiveinfo(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
         
        print(request.data)
        rname = request.data.get('rname', None)
        raddress = request.data.get('raddress', None)
        rphone = request.data.get('rphone', None)
        print(rname)
        print(raddress)
        print(rphone)
        if all([uid, rname, raddress, rphone]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                db_search = Receiveinfo.objects.filter(uid=user,rname=rname,raddress=raddress,rphone=rphone)
                if not db_search:
                    new_db = Receiveinfo()
                    new_db.uid = user
                    new_db.rname = rname
                    new_db.raddress = raddress
                    new_db.rphone = rphone
                    new_db.save() 
                    print("添加成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "添加成功"}))
                else:
                    print("该收获信息已存在")
                    return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "该收获信息已存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("信息不完整")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))


import pytz          
@api_view(['POST'])
def delete_receiveinfo(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
         
        print(request.data)
        rid = request.data.get('rid', None)
        print(rid)
        if all([uid, rid]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                print(user)
                db_search = Receiveinfo.objects.filter(uid=user,rid=rid)
                print(db_search)
                if db_search:
                    db_search.delete() 
                    print("删除成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "删除成功"}))
                else:
                    print("该收获信息不存在")
                    return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "该收获信息不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("请返回rid")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"请返回rid"}))

import pytz          
@api_view(['POST'])
def change_receiveinfo(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))         
        print(request.data)
        rid = request.data.get('rid', None)
        rname = request.data.get('rname', None)
        raddress = request.data.get('raddress', None)
        rphone = request.data.get('rphone', None)
        print(rid)
        if all([uid, rid, rname, raddress, rphone]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                print(user)
                db_search = Receiveinfo.objects.filter(uid=user,rid=rid).first()
                print(db_search)
                if db_search:
                    db_search.rname = rname
                    db_search.raddress = raddress
                    db_search.rphone = rphone
                    db_search.save() 
                    print("修改成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "修改成功"}))
                else:
                    print("该收获信息不存在")
                    return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "该收获信息不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("信息不完整")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))

          

@api_view(['GET','POST'])
def get_receiveinfo(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
                receiveinfo = Receiveinfo.objects.filter(uid=uid)
                print(receiveinfo)
                if receiveinfo:
                    serializer = ReceiveinfoSerializer(receiveinfo, many=True)
                    print(serializer.data)
                    return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"当前用户无收货信息"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))

         
@api_view(['POST'])
def add_cart(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
         
        print(request.data)
        pid = request.data.get('pid', None)
        psum = request.data.get('psum', None)
        print(pid)
        print(psum)
        if all([uid, pid, psum]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                print(user)
                product = Pro_info.objects.filter(pid=pid).first()
                db_search = Cart.objects.filter(uid=user, pid=pid).first()
                if not db_search:
                    new_db = Cart()
                    new_db.uid = user
                    new_db.pid = product
                    new_db.psum = psum
                    new_db.save() 
                    print("添加成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "添加成功"}))
                else:
                    db_search.psum += int(psum)
                    db_search.save()
                    print("添加成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "添加成功"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("信息不完整")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))


@api_view(['POST'])
def reduce_cart(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
         
        print(request.data)
        pid = request.data.get('pid', None)
        print(pid)
        if all([uid, pid]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                print(user)
                product = Pro_info.objects.filter(pid=pid).first()
                db_search = Cart.objects.filter(uid=user, pid=pid).first()
                if db_search:
                    db_search.psum -= 1
                    if db_search.psum == 0:
                        db_search.delete()
                        return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "减少成功"}))
                    else:
                        db_search.save() 
                        print("减少成功")
                        return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "减少成功"}))
                else:
                    print("该购物车商品不存在")
                    return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "该购物车商品不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("请返回pid")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"请返回pid"}))
          
import pytz          
@api_view(['POST'])
def delete_cart(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
         
        print(request.data)
        pid = request.data.get('pid', None)
        print(pid)
        if all([uid, pid]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                print(user)
                db_search = Cart.objects.filter(uid=user,pid=pid)
                print(db_search)
                if db_search:
                    db_search.delete() 
                    print("删除成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "删除成功"}))
                else:
                    print("该商品不存在")
                    return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "该商品不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("请返回pid")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"请返回pid"}))
          
          
@api_view(['GET','POST'])
def get_cart(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                #print(token_user.user_id)
                uid = token_user.user_id
                cart = Cart.objects.filter(uid=uid)
                #print(cart)
                if cart:
                    serializer = CartSerializer(cart, many=True)
                    for item in serializer.data:
                        p = item["pid"]
                        pro = Pro_info.objects.filter(pid=p).first()
                        item["pname"] = pro.pname
                        item["price"] = pro.price
                        item["sid"] = pro.sid.sid
                        path = os.path.join('http://120.24.164.113:8080/', pro.p_picture)
                        item["p_picture"] = path
                        print(item)
                        s = pro.sid.sid
                        print(s)
                        sup = Sup_info.objects.filter(sid=s).first()
                        item["sname"] = sup.sname
                    #print(serializer.data)
                    return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"当前用户无购物车信息"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))

#用户关注店铺         
@api_view(['POST'])
def add_likestores(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
         
        print(request.data)
        sid = request.data.get('sid', None)
        print(sid)
        if all([uid, sid]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                sup = Sup_info.objects.filter(sid=sid).first()
                
                db_search = Likestores.objects.filter(uid=uid, sid=sid).first()
                db_1 = Sup_info.objects.filter(sid=sid).first()
                if not db_search:
                    new_db = Likestores()
                    new_db.uid = user
                    new_db.sid = sup
                    db_1.likesum += 1
                    new_db.save() 
                    db_1.save()
                    print("关注成功")
                    
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "关注成功"}))
                    print("sss")
                else:
                    print("已在关注列表")
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg": "已在关注列表"}))
                    print("444")
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("信息不完整")

          
import pytz          
@api_view(['POST'])
def delete_likestores(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
         
        print(request.data)
        sid = request.data.get('sid', None)
        print(sid)
        if all([uid, sid]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                print(user)
                db_search = Likestores.objects.filter(uid=user,sid=sid)
                print(db_search)
                db_1 = Sup_info.objects.filter(sid=sid).first()
                print(db_1)
                if db_search:
                    db_search.delete()
                    db_1.likesum -= 1
                    db_1.save()
                    print("取消关注成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "取消关注成功"}))
                else:
                    print("您未关注该店铺")
                    return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "您未关注该店铺"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("请返回sid")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"请返回sid"}))          
 
 
@api_view(['GET','POST'])
def get_likestores(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
                stores = Likestores.objects.filter(uid=uid)
                print(stores)
                if stores:
                    serializer = LikestoresSerializer(stores, many=True)
                    for item in serializer.data:
                        s = item["sid"]
                        sup = Sup_info.objects.filter(sid=s).first()
                        item["sname"] = sup.sname
                        path = os.path.join('http://120.24.164.113:8080/', sup.logo)
                        item["logo"] = path
                    print(serializer.data)
                    return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"当前用户无收货信息"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
 
 
@api_view(['POST'])
def click_pro(request):
    if request.method == 'POST':
        pid = request.data.get('pid',None)
        print(pid)
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token:
            print(token)
            token_user = User_token.objects.filter(token=token).first()
            print(token_user)
            if token_user:
                datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
                if token_user.expiration_time < datetime_now:
                    return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
                else:
                    print(token_user.user_id)
                    uid = token_user.user_id
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            try:
                pro1 = Pro_info.objects.filter(pid=pid).first()
                new_db = Records()
                new_db.uid = token_user.user
                new_db.pid = pro1
                new_db.save() 
                print("记录成功")                     
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))

        pro = Pro_info.objects.filter(pid=pid)
        if pro:
            serializer = Pro_clickSerializer(pro, many=True)
            for item in serializer.data:
                s = item["sid"]
                sup = Sup_info.objects.filter(sid=s).first()
                item["sname"] = sup.sname
                p = Pro_info.objects.filter(pid=item["pid"]).first()
                path1 = os.path.join('http://120.24.164.113:8080/',p.p_picture)
                item["p_picture"] = path1
            print(serializer.data)
            return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"无商品详情"}))

        
@api_view(['POST'])
def click_sup(request):
    if request.method == 'POST':
        sid = request.data.get('sid',None)
        print(sid)
        sup = Sup_info.objects.filter(sid=sid)
        if sup:
            serializer1 = Sup_clickSerializer(sup, many=True)
            pro = Pro_info.objects.filter(sid=sid)
            for item in serializer1.data:
                print(item)
                s = Sup_info.objects.filter(sid=sid).first()
                print(s)
                path = os.path.join('http://120.24.164.113:8080/', s.logo)
                print(path)
                path2 = os.path.join('http://120.24.164.113:8080/',s.sprove)
                item["logo"] = path
                item["sprove"] = path2
                if pro:
                    serializer2 = Pro_searchSerializer(pro, many=True)
                    for i in serializer2.data:
                        p = Pro_info.objects.filter(pid=i["pid"]).first()
                        print(p.p_picture)
                        path3 = os.path.join('http://120.24.164.113:8080/',p.p_picture)
                        i["p_picture"] = path3
                    item["pro"] = serializer2.data
            print(serializer1.data)
            return Response(status=status.HTTP_200_OK,data=json.dumps(serializer1.data))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"无此商家"}))


@api_view(['GET','POST'])
def get_records(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        #print(token)
        token_user = User_token.objects.filter(token=token).first()
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                #print(token_user.user)
                uid = token_user.user
                print(uid)
                records = Records.objects.filter(uid=uid)
                print(records)
                if records:
                    serializer = RecordsSerializer(records, many=True)
                    for item in serializer.data:
                        p = item["pid"]
                        pro = Pro_info.objects.filter(pid=p).first()
                        pname = pro.pname
                        sup = pro.sid
                        item["pname"] = pname
                        item["sname"] = sup.sname
                        path = os.path.join('http://120.24.164.113:8080/', pro.p_picture)
                        item["p_picture"] = path
                    print(serializer.data)
                    return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"当前用户无收货信息"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))

'''
@api_view(['GET','POST'])
def delete(request):
    if request.method == 'GET':
        pro = Pro_info.objects.all()
        for item in pro:
            item.delete()
        print("chenggong")
        sup = Sup_info.objects.all()
        for i in sup:
            i.delete()
        print("chenggong")
        return Response(status=status.HTTP_200_OK,data=json.dumps({"msg":"chenggong"}))
'''