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


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework import generics
from rest_framework import filters
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from datetime import datetime,timedelta

import base64
import cv2
import numpy as np


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ZJTAutoTestingPlatform.settings")
import django
django.setup()

from .models import Pro_info,Pro_token
from sup_med.models import Sup_info,Sup_token
from oursite.settings import SECRET_KEY
from .serializers import *
from .serializers import Pro_searchSerializer
from .serializers import FileSerializer

class TokenAuthtication(BaseAuthentication):
    def authenticate(self, request):
        # 直接在请求头中获取token
        token = request._request.GET.get('token')
        token_obj = models.Pro_token.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("商品上架失败")
        else:
            datetime_now = datetime.now()
            if token_obj.expiration_time > datetime_now:
                # 在 rest framework 内部会将两个字段赋值给request，以供后续操作使用
                return (token_obj.pro, token_obj)
            else:
                raise exceptions.AuthenticationFailed("商品上架token过期,请重新录入")

    def authenticate_header(self, request):
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        pass


# 生成token
def md5(username):
    m = hashlib.md5(bytes(username, encoding='utf-8'))
    m.update(bytes(SECRET_KEY + str(time.time()), encoding='utf-8'))
    return m.hexdigest()
  

   

'''
class GoodsListViewSet(viewsets.GenericViewSet):
    """
    list: 商品列表
    """
#    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    serializer_class = Pro_searchSerializer
#    pagination_class = GoodsPagination
#    authentication_classes = [TokenAuthentication]
    queryset = Pro_info.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#    filter_class = GoodsFilter
    search_fields = ['pname', 'category','symptoms','pusage','pkeyword']
#    ordering_fields = ["sold_num", "shop_price"]
  
'''
import pytz
#商品上架界面
@api_view(['POST'])
def pro_upload(request):
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
        #print(request.data)
        #sid_state = Sup_info.objects.filter(sid=sid)
        sid_state = Sup_info.objects.get(sid=sid)
        sstate = sid_state.sstate
        print(sstate)
        if sstate == '待审核':
            return Response(status=status.HTTP_400_BAD_REQUEST,data=json.dumps({"msg":"待审核状态不能上架商品，请审核通过后操作"}))
        else:  
            #p_picture = request.FILES.get('p_picture',None)
            #p_picture = pro.get('p_picture',None)
            #file_path = os.path.join('./static',p_picture.name)
            #models.Img.objects.create(path=file_path)
            #print(p_picture)
            pro = request.data
            #print(request.data)
            #queryset = Pro_info.objects.all()
            #serializer_class = FileSerializer
            if not pro:
                return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))
            
            '''
            if(len(p)%3 ==1):
                p += "=="
            elif(len(p)%3 ==2):
                p += "="
            img_byte = base64.b64decode(p)
            #print(img_byte)
            img_np_arr = np.fromstring(img_byte, np.uint8)
            p_picture = cv2.imdecode(img_np_arr, cv2.IMREAD_COLOR)
            print("p_picture")
            print(p_picture)
            '''
            category = request.data.get('category',None)
            pname = request.data.get('pname',None)
            ptype = request.data.get('ptype',None)
            price = request.data.get('price', None)
            psize = request.data.get('psize',None)
            symptoms = request.data.get('symptoms',None)
            pusage = request.data.get('pusage',None)
            para = request.data.get('para',None)
            problems = request.data.get('problems',None)
            pkeyword = request.data.get('pkeyword',None)
            address = request.data.get('address',None)
            stock = request.data.get('stock',None)
            print(pname)
            print(price)
            print(ptype)
            p = request.data.get("p_picture")
            strs = p.split(",")[1]
            image_data = base64.b64decode(strs)
            s = str(sid)+"_"+str(pname)
            imname = 'static/pro_md/'+str(s)+'.jpg'
            file = open(imname,'wb')
            file.write(image_data)
            file.close()
            p_picture = imname
            
            #if all([sid,category,pname,ptype,price,psize,symptoms,pusage,para,problems,pkeyword,address,stock]):
            if all([sid,pname]):
                #file_name = './static/img/'+str(sid)+'/'+str(int(time.time()))+'.'+p_picture.name.split('.')[-1]
                #file_name = './static/img/'+str(sid)+'-'+'/'+p_picture.name.split('.')[-1]
                #file_name = 'static/'+p_picture.name
                #if p_picture.name.split('.')[-1] not in ['jpeg','jpg','png']:
                    #return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg": "输入文件有误"}))
                #try:
                db_search = Pro_info.objects.filter(sid=sid, pname=pname)
                if not db_search:
                    sup = Sup_info.objects.filter(sid=sid).first()
                    new_db = Pro_info()
                    new_db.sid = sup
                    new_db.p_picture = p_picture
                    #new_db.p_picture = file_name
                    new_db.category = category
                    new_db.pname = pname
                    new_db.ptype = ptype
                    new_db.price = price
                    new_db.psize = psize
                    new_db.symptoms = symptoms
                    new_db.pusage = pusage
                    new_db.para = para
                    new_db.problems = problems
                    new_db.pkeyword = pkeyword
                    new_db.address = address
                    new_db.stock = stock
                    new_db.save() 
                    print("1")
                    #f = open(file_name,'w')
                    #f.write(p_picture.read())
                    #f.close()
                    print("上架成功")
                    return Response(status=status.HTTP_200_OK, data=json.dumps({"msg": "上架成功"}))
                else:
                    print("该商品已上架")
                    return Response(status=status.HTTP_300_MULTIPLE_CHOICES, data=json.dumps({"msg": "商品已上架"}))
                '''except Exception as e:
                    print(str(e))
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))'''
            else:
                print("部分必填项为空")
                return Response(status=status.HTTP_400_BAD_REQUEST, data=json.dumps({"msg":"信息不完整"}))

import pytz
#商品下架
@api_view(['POST'])
def pro_down(request):
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
        try:
            pid = request.data["pid"]
            print(pid)
            db_delete = Pro_info.objects.filter(sid_id=sid,pid=pid).first()
            if not db_delete:
                return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"当前商品不存在"}))
            else:
                db_delete.delete()
                return Response(status=status.HTTP_200_OK,data=json.dumps({"msg":"下架成功"}))
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
          
#展示最新上架商品  
@api_view(['POST'])
def new_pro_show(request):
    if request.method == 'POST':
        sid = request.data.get('sid',None)
        print(sid)
        try:
            pro = Pro_info.objects.filter(sid=sid)
            print(type(pro))
            print("333")
            if not pro:
                return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"该商家还未上传任何商品"}))
            else:
                dic = pro.values()
                print(dic)
                #list = []
                list1 = []
                for item in dic:
                    pid = item["pid"]
                    print(pid)
                    ptime = item["ptime"]
                    print(ptime)
                    dt_s= datetime.now()
                    print(dt_s)
                    dt_e = (dt_s- timedelta(3))
                    print(dt_e)
                    #objs = Pro_info.objects.filter(ptime__range=[dt_s, dt_e]).filter(pid=pid)
                    #objs = Pro_info.objects.filter(Q(ptime__range=[dt_s, dt_e]) | Q(filter(pid=pid)))
                    #objs = Pro_info.objects.filter(pid=pid)
                    objs = Pro_info.objects.filter(ptime__range=[dt_e, dt_s]).filter(pid=pid)
                    print(objs)
                    if objs:   
                        #list.append(item["pname"]) 
                        list1.append(item["pid"])
                    else:
                        continue
                print(list1)
                len1 = len(list1)
                if len1==0:
                    return Response(status=status.HTTP_404_NOT_FOUND, data=json.dumps({"msg": "该商家不存在近三日新上架商品，请查看全部产品"}))
                else:
                    i = 0
                    #pro1 = Pro_info.objects.filter(pid=list[0])
                    #print(pro1)
                    print("222")
                    res = Pro_info.objects.none()
                    while i<len1:
                        pro1 = Pro_info.objects.filter(pid=list1[i])
                        res = res | pro1
                        print("333")
                        print("555")
                        i+=1
                    print(type(res))
                    serializer = Pro_newSerializer(res, many=True)
                    for item in serializer.data:
                        pro = Pro_info.objects.filter(pid=item["pid"]).first()
                        path = os.path.join('http://120.24.164.113:8080/', pro.p_picture)
                        item["p_picture"] = path  
                    print(serializer.data)
                    return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
                    #data = json.dumps(list(res))
                    #return Response(status=status.HTTP_200_OK,data=res.toJSON())
                
        except Exception as e:
            print(str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=json.dumps({"msg": "发生错误"}))
         
   

@api_view(['GET'])  
def search_pro(request):
    if request.method == 'GET':
        query = request.GET.get("search")
        result = Pro_info.objects.filter(Q(pname__icontains=query) | Q(category__icontains=query) | Q(symptoms__icontains=query) | Q(pusage__icontains=query) | Q(pkeyword__icontains=query))
        if result:
            serializer = Pro_searchSerializer(result, many=True)
            for item in serializer.data:
                s = item["sid"]
                sup = Sup_info.objects.filter(sid=s).first()
                item["sname"] = sup.sname
                pro = Pro_info.objects.filter(pid=item["pid"]).first()
                path = os.path.join('http://120.24.164.113:8080/', pro.p_picture)
                print(path)
                item["p_picture"] = path
            print(serializer.data)
            return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"检索结果为空"}))

@api_view(['GET'])  
def index_pro(request):
    if request.method == 'GET':
        result = Pro_info.objects.all().order_by('-sales')[:10]
        if result:
            serializer = Pro_searchSerializer(result, many=True)
            for item in serializer.data:
                s = item["sid"]
                sup = Sup_info.objects.filter(sid=s).first()
                item["sname"] = sup.sname
                pro = Pro_info.objects.filter(pid=item["pid"]).first()
                path = os.path.join('http://120.24.164.113:8080/', pro.p_picture)
                item["p_picture"] = path
            print(serializer.data)
            return Response(status=status.HTTP_200_OK,data=json.dumps(serializer.data))
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,data=json.dumps({"msg":"检索结果为空"}))
    

'''
class Myviewset(generics.ListAPIView):
    serializer_class = Pro_searchSerializer
    queryset = Pro_info.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['pname', 'category','symptoms','pusage','pkeyword']
'''
