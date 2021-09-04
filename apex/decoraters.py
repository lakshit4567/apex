import datetime
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *
import pandas as pd
from django.contrib.auth import authenticate, logout, login
from .tests import PDF, Fetch_Data
from django_celery_beat.models import PeriodicTask, PeriodicTasks, IntervalSchedule
# this decorator checks for authenticated users
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_raw_material')
        else:
            return view_func(request,*args, **kwargs)
    return wrapper_func
# def admin_access(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         us = request.user.groups.all()[0].name
#         print(us)
#         return view_func(request, *args, **kwargs)
#     return wrapper_func
# this decorator is for access functionality of groups
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            # print('working',allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(group)
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('user_raw_material')
        return wrapper_func
    return decorator

# this decorator checks for active users
def unautherized_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            user_id = request.user
            rg = Register.objects.filter(user__exact=user_id)
        except:
            redirect('login')
        # rs = rg.values()[0]
        try:
            rs = rg.values()[0]
            rs_status = rs['userRole']
            if rs_status == 'Active':
                return view_func(request,*args, **kwargs)
            else:
                # return view_func(request,*args, **kwargs)
                # print('nothing')
                return 'nothing'
        except:
            return view_func(request,*args, **kwargs)
    return wrapper_func
        
# this decorator checks for delete access
def del_access(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            user_id = request.user
            rg = Register.objects.filter(user__exact=user_id)
        except:
            redirect('login')
        # rs = rg.values()[0]
        try:
            rs = rg.values()[0]
            rs_del = rs['delete_access']
            if rs_del == 'Yes':
                return view_func(request,*args, **kwargs)
            else:
                # return view_func(request,*args, **kwargs)
                # print('nothing')
                return 'nothing'
        except:
            return view_func(request,*args, **kwargs)
    return wrapper_func

def test(view_func):
    def wrapper_func(request, *args, **kwargs):
        
        # current_date = datetime.date.today()
        # raw_dic = Fetch_Data.raw_material(rm_data=rawMaterial.objects.filter(RM_Date__exact=current_date))   
        # Es_dic = Fetch_Data.EssentialitemUserperDay(es_data=EssentialItemUsePerDay.objects.filter(EPD_Date__exact=current_date))
        # df_rm = pd.DataFrame(raw_dic)
        # df_es = pd.DataFrame(Es_dic)
        # rm_csv_path = 'dailyReports/DailyReport RM {}.csv'.format(str(datetime.date.today()))
        # es_csv_path = 'dailyReports/DailyReport ES {}.csv'.format(str(datetime.date.today()))
        # pdf_path = 'dailyReports/DailyReport {}.pdf'.format(str(datetime.date.today()))
        # df_rm.to_csv(rm_csv_path, index=False)
        # df_es.to_csv(es_csv_path,index=False)
        # pdf = PDF()
        # pdf.alias_nb_pages()
        # pdf.set_auto_page_break(auto=True,margin=15)
        # pdf.add_page()
        # pdf.print_page('Raw Material',rm_csv_path)
        # pdf.print_page('Essential item user per day',es_csv_path)
        # pdf.print_page('Finsihed material Stock',rm_csv_path)
        # pdf.output(pdf_path, 'F')
        from datetime import date
        today = date.today()
        # d = essentialitemStock.objects.filter(ES_Date__year=today.year,
        #                                ES_Date__month=today.month,).values()
        # d = EssentialItemUsePerDay.objects.filter(EPD_Date__year=today.year,
        #                                EPD_Date__month=today.month,
        #                                EPD_Date=today).values()
        # # # d = rawMaterial.objects.values()
        # print(d)
        return view_func(request,*args,**kwargs)
    return wrapper_func

