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


from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework import generics
from rest_framework import filters
from django.http import FileResponse

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ZJTAutoTestingPlatform.settings")
import django
django.setup()

from user_md.models import User_info, User_token, Receiveinfo, Cart, Likestores, Records
from pro_up.models import Pro_info
from sup_med.models import Sup_info, Sup_token
from .models import Order_info, Ordproducts, Ordpay, Ordrec, Ordcom, test, Rx_order
from oursite.settings import SECRET_KEY
from user_md.serializers import User_infoSerializer, ReceiveinfoSerializer, CartSerializer, LikestoresSerializer, RecordsSerializer
from pro_up.serializers import Pro_clickSerializer,Pro_searchSerializer
from sup_med.serializers import Sup_infoSerializer, Sup_clickSerializer
from .serializers import Order_infoSerializer, Order_proSerializer, Order_clickSerializer, OrdcomSerializer, TestSerializer, Order_expSerializer

import base64
import cv2
import numpy as np

import pytz          
@api_view(['POST'])
def add_order(request):
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
        pro = request.data.get('pro', None)
        rid = request.data.get('rid', None)
        unotes = request.data.get('unotes', None)
        sid = request.data.get('sid', None)
        ordprice = request.data.get('ordprice', None)
        print(pro)
        print(unotes)
        print(sid)
        print(ordprice)
        if all([uid, sid, pro, rid, ordprice]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                sup = Sup_info.objects.filter(sid=sid).first()
                if all([user, sup]):
                    new_db = Order_info()
                    new_db.uid = user
                    new_db.sid = sup
                    new_db.unotes = unotes
                    new_db.ordprice = ordprice 
                    new_db.save()
                    print(new_db.ordno)
                    
                    for item in pro:
                        print(item)
                        new_ordpro = Ordproducts()
                        new_ordpro.ordno = new_db
                        p = Pro_info.objects.filter(pid=item["pid"]).first()
                        print(p)
                        if p:
                            psum = int(item["psum"])
                            if p.stock < psum:
                                order = Order_info.objects.filter(ordno=new_db.ordno).first()
                                order.delete()
                                return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg": "库存不足"}))
                            else:
                                new_ordpro.pid = p
                                new_ordpro.psum = psum
                                p.stock -= psum
                                p.save()
                                new_ordpro.save()
                        else:
                            order = Order_info.objects.filter(ordno=new_db.ordno).first()
                            order.delete()
                            print("查无此药品")
                            return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "查无此药品"}))
                    
                    r = Receiveinfo.objects.filter(rid=rid).first()
                    if r:
                        newrec = Ordrec()
                        newrec.ordno = new_db
                        newrec.uid = user
                        newrec.rid = r
                        newrec.save()
                    else:
                        order = Order_info.objects.filter(ordno=new_db.ordno).first()
                        order.delete()
                        print("查无此收货地址")
                        return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "查无此收货地址"}))
                   
                    newpay = Ordpay()
                    newpay.ordno = new_db
                    newpay.save()
                   
                    print("下单成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "下单成功"}))
                else:
                    print("用户或商家不存在")
                    return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "用户或商家不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("信息不完整")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))


import pytz          
@api_view(['POST'])
def add_Rx(request):
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
         
        pro = request.data.get('pro', None)
        rid = request.data.get('rid', None)
        unotes = request.data.get('unotes', None)
        sid = request.data.get('sid', None)
        ordprice = request.data.get('ordprice', None)
        print(unotes)
        print(sid)
        print(ordprice)
        p = request.data.get("Rx",None)
        strs = p.split(",")[1]
        image_data = base64.b64decode(strs)
        s = str(uid)+"_"+str(token)+"_"+str(sid)
        imname = 'static/order_md/'+str(s)+'.jpg'
        file = open(imname,'wb')
        file.write(image_data)
        file.close()
        Rx = imname
        if all([uid, sid, pro, rid, ordprice, Rx]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                sup = Sup_info.objects.filter(sid=sid).first()
                if all([user, sup]):
                    new_db = Order_info()
                    new_db.uid = user
                    new_db.sid = sup
                    new_db.unotes = unotes
                    new_db.ordprice = ordprice
                    new_db.ordstatus = '待审核'
                    new_db.save()
                    
                    Rx_db = Rx_order()
                    order = Order_info.objects.filter(ordno=new_db.ordno).first()
                    Rx_db.ordno = order
                    Rx_db.uid = user
                    Rx_db.Rx = Rx
                    Rx_db.save()                    
                    print(new_db.ordno)                   
                    for item in pro:
                        print(item)
                        new_ordpro = Ordproducts()
                        new_ordpro.ordno = new_db
                        p = Pro_info.objects.filter(pid=item["pid"]).first()
                        if p:
                            psum = int(item["psum"])
                            if p.stock < psum:
                                order = Order_info.objects.filter(new_db.ordno).first()
                                order.delete()
                                return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg": "库存不足"}))
                            else:
                                new_ordpro.pid = p
                                new_ordpro.psum = psum
                                p.stock -= psum
                                p.save()
                                new_ordpro.save()
                        else:
                            order = Order_info.objects.filter(ordno=new_db.ordno).first()
                            order.delete()
                            print("查无此药品")
                            return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "查无此药品"})) 
                    r = Receiveinfo.objects.filter(rid=rid).first()
                    if r:
                        newrec = Ordrec()
                        newrec.ordno = new_db
                        newrec.uid = user
                        newrec.rid = r
                        newrec.save()
                    else:
                        order = Order_info.objects.filter(ordno=new_db.ordno).first()
                        order.delete()
                        print("查无此收货地址")
                        return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "查无此收货地址"}))
                   
                    newpay = Ordpay()
                    newpay.ordno = new_db
                    newpay.save()
                   
                    print("下单成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "下单成功"}))
                else:
                    print("用户或商家不存在")
                    return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "用户或商家不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("信息不完整")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))


import pytz          
@api_view(['GET'])
def show_Rx(request):
    if request.method == 'GET':
        result = []
        order = Order_info.objects.filter(ordstatus='待审核')
        #print(order)
        for item in order:
            print(item)
            re = {}
            pro=[]
            ord_pro = Ordproducts.objects.filter(ordno=item)
            print(ord_pro)
            for i in ord_pro:
                p = Pro_info.objects.filter(pid=i.pid.pid).first()
                p_dict={}
                p_dict["pid"] = p.pid
                p_dict["pname"] = p.pname
                pro.append(p_dict)
            Rx = Rx_order.objects.filter(ordno=item).first()
            print(Rx)
            path = os.path.join('http://120.24.164.113:8080/', Rx.Rx)
            re["ordno"] = item.ordno
            re["pro"] = pro
            re["image"] = str(path)
            result.append(re)
        return Response(status=status.HTTP_200_OK, data=json.dumps(result))

import pytz          
@api_view(['POST'])
def check_Rx(request):
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
        image = request.FILES.get('image',None)
        print(image.name)
        print(image.size)
        new_db = test()
        new_db.image = image
        new_db.save()
        db = test.objects.filter(pk=1).first()
        print(db.image.name)
        path = os.path.join('http://120.24.164.113:8080/', db.image.name)
        return FileResponse(status=status.HTTP_200_OK, data=json.dumps(res))
'''
       
         

import pytz          
@api_view(['POST'])
def change_status(request):
    if request.method == 'POST':
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
        ordno = request.data.get('ordno', None)
        expno = request.data.get('expno', None)
        print(ordno)
        if all([sid, ordno, expno]):
            try:
                sup = Sup_info.objects.filter(sid=sid).first()
                print(sup)
                db_search = Order_info.objects.filter(sid=sup,ordno=ordno).first()
                print(db_search)
                if db_search and db_search.ordstatus=='未发货':
                    db_search.ordstatus = '商家已发货'
                    db_search.expno = expno
                    db_search.save() 
                    print("发货成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "发货成功"}))
                else:
                    print("该订单不存在")
                    return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "该订单不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("信息不完整")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))          

@api_view(['POST'])
def get_expinfo(request):
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
                ordno = request.data.get("ordno",None)
                if ordno:
                    order = Order_info.objects.filter(ordno=ordno).first()
                    result = {}
                    result["ordno"] = ordno
                    result["expno"] = order.expno
                    r = Ordrec.objects.filter(ordno=ordno).first()
                    re = Receiveinfo.objects.filter(rid=r.rid.rid).first()
                    result["rname"] = re.rname
                    result["raddress"] = re.raddress
                    result["rphone"] = re.rphone
                    print(result)
                    return Response(status=status.HTTP_200_OK,data=json.dumps(result))
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"当前用户无订单信息"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
          
import pytz          
@api_view(['POST'])
def delete_order(request):
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
        ordno = request.data.get('ordno', None)
        print(ordno)
        if all([uid, ordno]):
            try:
                user = User_info.objects.filter(uid=uid).first()
                print(user)
                db_search = Order_info.objects.filter(ordno=ordno).first()
                print(db_search)
                if db_search:
                    if db_search.ordstatus=="未发货":
                        pros = Ordproducts.objects.filter(ordno=ordno)
                        for pro in pros:
                            p = Pro_info.objects.filter(pid=pro.pid.pid).first()
                            p.stock += pro.psum
                            p.save()
                        db_search.delete() 
                        print("删除成功")
                        return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "删除成功"}))
                    else:
                        print("该商品已发货")
                        return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "该商品已发货"}))
                else:
                    print("该收获信息不存在")
                    return Response(status=status.HTTP_403_FORBIDDEN, data=json.dumps({"msg": "该收获信息不存在"}))
            except Exception as e:
                print(str(e))
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
        else:
            print("请返回ordno")
            return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"请返回ordno"}))

          
@api_view(['GET'])
def get_orderinfo(request):
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
                orders = Order_info.objects.filter(uid=uid)
                print(orders)
                if orders:
                    serializer = Order_infoSerializer(orders, many=True)
                    print(serializer.data)
                    for item in serializer.data:
                        pros = Ordproducts.objects.filter(ordno=item["ordno"])
                        #print(pros)
                        if pros:
                            proser = Order_proSerializer(pros, many=True)                        
                            print(proser.data)
                            sup = Sup_info.objects.filter(sid=item["sid"]).first()
                            item["sname"] = sup.sname
                            item["pro"] = []                       
                            for i in proser.data:
                                p = Pro_info.objects.filter(pid=i["pid"]).first()
                                i["pname"] = p.pname
                                i["price"] = p.price
                                path = os.path.join('http://120.24.164.113:8080/', p.p_picture)
                                i["p_picture"] = path
                                item["pro"].append(i)
                    return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"当前用户无订单信息"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))

@api_view(['POST'])
def click_order(request):
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
                user = User_info.objects.filter(uid=uid).first()
                ordno = request.data.get('ordno', None)
                print(ordno)
                if ordno:
                    order = Order_info.objects.filter(ordno=ordno,uid=user)
                    print(order)
                    if order:
                        serializer = Order_clickSerializer(order,many=True)
                        print(serializer.data)
                        for item in serializer.data:
                            sup = Sup_info.objects.filter(sid=item["sid"]).first()
                            item["sname"] = sup.sname
                            ordrec = Ordrec.objects.filter(ordno=item["ordno"]).first()
                            receive = Receiveinfo.objects.filter(rid=ordrec.rid.rid).first()
                            item["rname"] = receive.rname
                            item["raddress"] = receive.raddress
                            item["rphone"] = receive.rphone
                            item["pro"] = []
                            pros = Ordproducts.objects.filter(ordno=item["ordno"])
                            proser = Order_proSerializer(pros, many=True)                        
                            print(proser.data)
                            for i in proser.data:
                                p = Pro_info.objects.filter(pid=i["pid"]).first()
                                print(p)
                                i["pname"] = p.pname
                                i["price"] = p.price
                                print(p.p_picture)
                                path = ''
                                path = os.path.join('http://120.24.164.113:8080/',str(p.p_picture))
                                #print(path)
                                i["p_picture"] = path
                                item["pro"].append(i)
                        print("查找成功")
                        return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
                    else:
                        return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"查无此订单信息"}))
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"请返回ordno"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))

@api_view(['POST'])
def confirm_order(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                print("登录过期")
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
                ordno = request.data.get("ordno", None)
                order = Order_info.objects.filter(ordno=ordno).first()
                print(order)
                if order:
                    if order.ordstatus == '商家已发货':
                        order.ordstatus = '交易成功'
                        order.save()
                        pros = Ordproducts.objects.filter(ordno=ordno)
                        for pro in pros:
                            p = Pro_info.objects.filter(pid=pro.pid.pid).first()
                            p.sales += pro.psum
                            p.save()
                        print("交易成功")
                        return Response(status=status.HTTP_200_OK,data=json.dumps({"msg":"交易成功"}))
                    else:
                        print("该订单不可确认收货")
                        return Response(status=status.HTTP_200_OK,data=json.dumps({"msg":"该订单不可确认收货"}))
                else:
                    print("无此订单信息")
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"无此订单信息"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))


@api_view(['POST'])
def comment_order(request):
    if request.method == 'POST':
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        token_user = User_token.objects.filter(token=token).first()
        print(token_user)
        if token_user:
            datetime_now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
            if token_user.expiration_time < datetime_now:
                print("登录过期")
                return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))
            else:
                print(token_user.user_id)
                uid = token_user.user_id
                user = User_info.objects.filter(uid=uid).first()
                ordno = request.data.get("ordno", None)
                pro_com = request.data.get("pro_com", None)
                order = Order_info.objects.filter(ordno=ordno).first()
                print(order)
                if ([order, user, ordno, pro_com]):
                    if order.ordstatus == '交易成功':
                        for item in pro_com:
                            if item["comment"]:
                                pro = Pro_info.objects.filter(pid=item["pid"]).first()
                                new_db = Ordcom()
                                new_db.uid = user
                                new_db.ordno = order
                                new_db.pid = pro
                                new_db.comment = item["comment"]
                                new_db.save()
                        print("评价成功")
                        return Response(status=status.HTTP_200_OK,data=json.dumps({"msg":"评价成功"}))
                    else:
                        print("该订单不可评价")
                        return Response(status=status.HTTP_200_OK,data=json.dumps({"msg":"该订单不可评价"}))
                else:
                    print("无此订单信息")
                    return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"无此订单信息"}))
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"登录过期"}))


         
@api_view(['POST'])
def get_comment(request):
    if request.method == 'POST':
        pid = request.data.get('pid',None)
        print(pid)
        if pid:
            pro = Pro_info.objects.filter(pid=pid).first()
            comment = Ordcom.objects.filter(pid=pro)
            if comment:
                serializer = OrdcomSerializer(comment, many=True)
                for item in serializer.data:
                    user = User_info.objects.filter(uid=item["uid"]).first()
                    item["uname"] = user.uname
                print(serializer.data)
                return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
            else:
                return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"该商品无评价"}))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"未找到此商品"}))