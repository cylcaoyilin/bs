from django.conf.urls import url
from . import views

app_name='TuiJian'
urlpatterns = [
    url(r'user_based/',views.user_based_recommend),
    url(r'item_based/',views.item_based_recommend),
    url(r'index$',views.index,name='index'),
    url(r'^$',views.index,name='index'),
    url(r'itype_s/(.*)/',views.itype_s,name='itype_s'),
    url(r'sousuo/',views.sousuo,name='sousuo'),
    url(r'case_item/([0-9]+)/',views.case_item,name='case_item'),
    url(r'add_pinglun/([0-9]+)/',views.add_pinglun,name='add_pinglun'),
    url(r'add_dianzan$', views.add_dianzan, name='add_dianzan'),
]