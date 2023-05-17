import json
import traceback

from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,HttpResponseRedirect,HttpResponse
from . import models
from django.db.models import Q
import uuid
import os
from .user_based_xietong import UserCf
from .item_based_xietong import ItemCf
# Create your views here.



#这个是搜索函数，搜索提交的值跟名称做模糊搜索后返回用户
@login_required
def sousuo(request):
    if request.method == 'POST':
        error = {}
        data = request.POST
        name = data.get('name', '')
        list_data = models.Case_item.objects.filter(name__icontains=name)

        return render(request, 'test/itype_all.html', locals())

#做基于用户协同过滤的过程和提交的数据做处理。
def Recommend1(name_a):
    try:
        user_list = []
        dicts = {}
        Biaoqians1 = models.Biaoqian.objects.filter(user=get_object_or_404(models.Users,username=name_a)).order_by('-fenshu')[:100]#取出自己关注热度前面的标签
        Biaoqians = list(set([resu.biaoqian for resu in Biaoqians1]))
        dttas3 = models.Pinfen.objects.filter(user=get_object_or_404(models.Users,username=name_a))
        dicts[name_a] = {}
        for resu1 in dttas3:
            case_item1 = resu1.case
            dicts[name_a][str(case_item1.id)] = 4
            li1 = models.Pinfen.objects.filter(case=case_item1.id)
            for resu2 in li1:
                user_list.append(resu2.user.username)
        user_set = list(set(user_list))
        for resu in user_set:
            dicts[resu] = {}
            results = models.Pinfen.objects.filter(user=get_object_or_404(models.Users,username=resu))
            for resu1 in results:
                dicts[resu][resu1.case.id] = 4
        print("所有用户点赞的视频：",dicts)

        userCf = UserCf(data=dicts)
        recommendations = userCf.recommend(name_a)
        print("recommendations:",recommendations)

        listz = []
        if recommendations != []:
            for resu in recommendations:
                case = models.Case_item.objects.get(pk=resu[0])
                biaoqians = case.biaoqian.split(',')
                for resu1 in biaoqians:
                    if resu1 in Biaoqians:
                        listz.append(case)
                        break
            if not listz:
                for resu in recommendations[:8]:
                    case = models.Case_item.objects.get(pk=resu[0])
                    listz.append(case)
            elif len(listz) < 8:
                for resu in recommendations:
                    case = models.Case_item.objects.get(pk=resu[0])
                    if case not in listz:
                        listz.append(case)
                        if len(listz) >= 8:
                            break

            return listz, 1
        else:
            return '', 0
    except Exception as e:
        print(traceback.format_exc())
        return '', 0

def Recommend2(name_a):
    try:
        user_list = []
        dicts = {}
        Biaoqians1 = models.Biaoqian.objects.filter(user=get_object_or_404(models.Users,username=name_a)).order_by('-fenshu')[:100]#取出自己关注热度前面的标签
        Biaoqians = list(set([resu.biaoqian for resu in Biaoqians1]))
        dttas3 = models.Pinfen.objects.filter(user=get_object_or_404(models.Users,username=name_a))
        dicts[name_a] = {}
        for resu1 in dttas3:
            case_item1 = resu1.case
            dicts[name_a][str(case_item1.id)] = 4
            li1 = models.Pinfen.objects.filter(case=case_item1.id)
            for resu2 in li1:
                user_list.append(resu2.user.username)
        user_set = list(set(user_list))
        for resu in user_set:
            dicts[resu] = {}
            results = models.Pinfen.objects.filter(user=get_object_or_404(models.Users,username=resu))
            for resu1 in results:
                dicts[resu][resu1.case.id] = 4
        print("所有用户评分的视频：",dicts)

        itemCf = ItemCf(data=dicts)
        recommendations = itemCf.recommend(name_a)
        print("recommendations:",recommendations)

        listz = []
        if recommendations != []:
            for resu in recommendations:
                case = models.Case_item.objects.get(pk=resu[0])
                biaoqians = case.biaoqian.split(',')
                for resu1 in biaoqians:
                    if resu1 in Biaoqians:
                        listz.append(case)
                        break
            if not listz:
                for resu in recommendations[:8]:
                    case = models.Case_item.objects.get(pk=resu[0])
                    listz.append(case)
            elif len(listz) < 8:
                for resu in recommendations:
                    case = models.Case_item.objects.get(pk=resu[0])
                    if case not in listz:
                        listz.append(case)
                        if len(listz) >= 8:
                            break

            return listz, 1
        else:
            return '', 0
    except Exception as e:
        print(traceback.format_exc())
        return '', 0



#主页，推荐数据
@login_required
def index(request):
    if request.method == 'GET':
        username = request.user.username
        wheelsList1, it1 = Recommend1(username)
        print("wheelsList1:",wheelsList1)
        print("it1:",it1)

        types = list(set([resu.itype  for resu in models.Case_item.objects.all()]))
        types.sort()
        data2 = models.Case_item.objects.all().order_by('id')[:50]
        if it1 == 1:
            data3 = wheelsList1
        else:
            data3 = models.Case_item.objects.all().order_by('id')[:8]
        # print("data3:",data3)

        return render(request,'test/index.html',locals())




#分类
@login_required
def itype_s(request,td):
    types = list(set([resu.itype for resu in models.Case_item.objects.all()]))
    types.sort()
    if request.method=='GET':
        list_data = models.Case_item.objects.filter(itype=td).order_by('-id')
        return render(request,'test/itype_all.html',locals())

#详细信息
import random
@login_required
def case_item(request,id):
    types = list(set([resu.itype for resu in models.Case_item.objects.all()]))
    types.sort()
    if request.method == 'GET':
        data = get_object_or_404(models.Case_item,pk=id)
        datas = models.PinLun.objects.filter(case=data)
        dianzhan = models.Pinfen.objects.filter(case=data).filter(user=request.user)

        return render(request,'test/carts.html',locals())

#评论
@login_required
def add_pinglun(request,id):
    if request.method == 'POST':
        data = get_object_or_404(models.Case_item,pk=id)
        content = request.POST.get('content')
        models.PinLun.objects.create(
            user = request.user,
            case = data,
            content = content
        )
        return redirect("/case_item/{}".format(id))


@login_required
def add_dianzan(request):
    if request.method == 'GET':
        tid = request.GET.get('tid')
        data = get_object_or_404(models.Case_item,pk=tid)
        if not models.Pinfen.objects.filter(case=data).filter(user=request.user):
            models.Pinfen.objects.create(
                user = request.user,
                case = data
            )
            for resu in data.biaoqian.split(','):
                if not models.Biaoqian.objects.filter(Q(biaoqian=resu)&Q(user= request.user)):
                    models.Biaoqian.objects.create(
                        user = request.user,
                        biaoqian = resu,
                        fenshu = 1
                    )
                else:
                    da = models.Biaoqian.objects.filter(Q(biaoqian=resu)&Q(user= request.user))
                    da[0].fenshu = da[0].fenshu + 1
                    da[0].save()
            json_info = {
                "status":True,
                "content":"点赞成功"
            }




        else:
            models.Pinfen.objects.filter(case=data).filter(user=request.user)[0].delete()
            json_info = {
                "status": True,
                "content": "取消点赞成功"
            }

        return HttpResponse(json.dumps(json_info))


# 基于用户推荐
def user_based_recommend(request):
    if request.method == 'GET':
        username = request.user.username
        wheelsList1, it1 = Recommend1(username)
        print("wheelsList1:",wheelsList1)
        print("it1:",it1)

        types = list(set([resu.itype  for resu in models.Case_item.objects.all()]))
        types.sort()
        data2 = models.Case_item.objects.all().order_by('id')[:50]
        if it1 == 1:
            data3 = wheelsList1
        else:
            data3 = models.Case_item.objects.all().order_by('id')[:8]
        # print("data3:",data3)

        return render(request,'test/user_based_recommend.html',locals())

#首先看URL：/user_based  对应  views中的user_based_recommend函数 这个函数返回一个页面user_based_recommend.html

# 基于物品推荐
def item_based_recommend(request):
    if request.method == 'GET':
        username = request.user.username
        wheelsList1, it1 = Recommend2(username)
        # print("wheelsList1:",wheelsList1)
        print("it1:",it1)

        types = list(set([resu.itype  for resu in models.Case_item.objects.all()]))
        types.sort()
        data2 = models.Case_item.objects.all().order_by('id')[:50]
        if it1 == 1:
            data3 = wheelsList1
        else:
            data3 = models.Case_item.objects.all().order_by('id')[:8]
        # print("data3:",data3)

        return render(request,'test/item_based_recommend.html',locals())