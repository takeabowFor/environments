"""oursite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from user_md import views
from sup_med import sup_views
from pro_up import pro_up_views
from order_md import order_views
from pl_rev import pl_views
from doc_ch import doc_views

#router = routers.DefaultRouter()
#router.register(r'^api/pro_up/up/$',pro_up_views.pro_upload,basename='api/pro_up/up/$')


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('admin/', include(router.urls)),
    re_path(r'^api/user_md/login/$',views.user_login),
    re_path(r'^api/user_md/register/$',views.user_register),
    re_path(r'^api/user_md/changeinfo/$',views.user_change),
    re_path(r'^api/user_md/addreceiveinfo/$',views.add_receiveinfo),
    re_path(r'^api/user_md/deletereceiveinfo/$',views.delete_receiveinfo), 
    re_path(r'^api/user_md/changereceiveinfo/$',views.change_receiveinfo),
    re_path(r'^api/user_md/getreceiveinfo/$',views.get_receiveinfo),
    re_path(r'^api/user_md/addcart/$',views.add_cart),
    re_path(r'^api/user_md/reducecart/$',views.reduce_cart),
    re_path(r'^api/user_md/deletecart/$',views.delete_cart),
    re_path(r'^api/user_md/getcart/$',views.get_cart),
    re_path(r'^api/user_md/addlikestores/$',views.add_likestores),
    re_path(r'^api/user_md/deletelikestores/$',views.delete_likestores),
    re_path(r'^api/user_md/getlikestores/$',views.get_likestores),
    re_path(r'^api/user_md/getrecords/$',views.get_records),
    re_path(r'^api/user_md/clickpro/$',views.click_pro),
    re_path(r'^api/user_md/clicksup/$',views.click_sup),
    re_path(r'^api/pro_up/search/$',pro_up_views.search_pro),
    re_path(r'^api/pro_up/index/$',pro_up_views.index_pro),
    re_path(r'^api/sup_med/search/$',sup_views.search_sup), 
    re_path(r'^api/order_md/addorder/$',order_views.add_order),
    re_path(r'^api/order_md/addRx/$',order_views.add_Rx),
    re_path(r'^api/order_md/showRx/$',order_views.show_Rx),
    re_path(r'^api/order_md/checkRx/$',order_views.check_Rx),
    re_path(r'^api/order_md/changestatus/$',order_views.change_status),
    re_path(r'^api/order_md/expinfo/$',order_views.get_expinfo),
    re_path(r'^api/order_md/deleteorder/$',order_views.delete_order),
    re_path(r'^api/order_md/getorder/$',order_views.get_orderinfo),
    re_path(r'^api/order_md/clickorder/$',order_views.click_order),
    re_path(r'^api/order_md/confirmorder/$',order_views.confirm_order),
    re_path(r'^api/order_md/commentorder/$',order_views.comment_order),
    re_path(r'^api/order_md/getcomment/$',order_views.get_comment), 
#    re_path(r'^api/order_md/test/$',order_views.test_view),
#    re_path(r'^api/user_md/delete/$',views.delete),
    
    re_path(r'^api/sup_med/register/$',sup_views.sup_register),
    re_path(r'^api/sup_med/login/$',sup_views.sup_login),
    re_path(r'^api/sup_med/sinfo_edit/$',sup_views.sinfo_edit),
    re_path(r'^api/sup_med/sinfo_show/$',sup_views.sinfo_show),
    re_path(r'^api/pro_up/pro_down/$',pro_up_views.pro_down),
    re_path(r'^api/pro_up/new_pro_show/$',pro_up_views.new_pro_show),
    re_path(r'^api/pro_up/up/$',pro_up_views.pro_upload),
    re_path(r'^api/sup_med/sup_pro_man/$',sup_views.sup_pro_man),
    re_path(r'^api/sup_med/sup_check_order/$',sup_views.sup_check_order),
 
    re_path(r'^api/pl_rev/login/$',pl_views.plmanager_login),
    re_path(r'^api/pl_rev/register/$',pl_views.plmanager_register),
    re_path(r'^api/pl_rev/showSupAuth/$',pl_views.show_supAuth),
    re_path(r'^api/pl_rev/checkSupAuth/$',pl_views.check_supAuth),
 
    re_path(r'^api/doc_ch/login/$',doc_views.doc_login),
    re_path(r'^api/doc_ch/register/$',doc_views.doc_register),
]
