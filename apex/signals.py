

from re import S, sub
from typing import Counter
from django.db.models.signals import post_save,post_delete,pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import *
import datetime
import calendar
from .helper import alertmessages, logsave, scrapsave, channel_alert
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

# this signal create groups
@receiver(post_save,sender=User)
def user_profile(sender,instance,created, **kwargs):
    if created:
        # current_date = str(datetime.date.today()).replace('-',' ')
        # today_date = datetime.datetime.strptime(current_date, '%Y %m %d').weekday()
        # current_day = calendar.day_name[today_date]
        group = Group.objects.get(name='employes')
        instance.groups.add(group)
# this signal create active inactive and delete access       
@receiver(post_save, sender=Register)  
def register(sender,instance,created, **kwargs):
    if created:
        rg = Register.objects.get(id = instance.id)       
        time = Timmer.objects.filter().last()
        a_time = str(time.active_time)
        d_time = str(time.inactive_time)
        a_hour = int(a_time[0:2])
        a_min = a_time.replace(":",'')[2::]
        d_hour = int(d_time[0:2])
        d_min = d_time.replace(":","")[2::]
        a_t = int(str(a_hour)+str(a_min))
        d_t = int(str(d_hour)+str(d_min))
        
        my_time = str(datetime.datetime.now())[10:16].replace(":",'')
        
        hour = int(my_time[0:2])
       
        min = my_time[2::]
        
        t = int(str(hour)+str(min))

        if t >= a_t and t <= d_t:
            rg.status = 'Pending'
            rg.userRole = 'Active'
            rg.save()
            print('active')
        elif t > d_t:
            rg.status = 'Pending'
            rg.userRole = 'In-Active'
            rg.save()
            print('deactivate')
        elif t < a_t:
            rg.status = 'Pending'
            rg.userRole = 'In-Active'
            rg.save()
            print('deactivate')
    else:
        channel_layer = get_channel_layer()
        data = {}
        us = str(User.objects.get(username= instance.user).username)
        print(us,'######')
        data['delete_access'] = instance.delete_access
        data['userRole'] = instance.userRole  
        async_to_sync(channel_layer.group_send)(
            "room_%s" % us,{
                'type':'send_alert_user',
                'value': json.dumps(data)
            }
        )     

#this is raw material page signal saves scrap data
@receiver(post_save,sender=rawMaterial)
def rawmaterial(sender,created,instance,**kwargs):
    if created:
        rm = rawMaterial.objects.filter(id__exact=instance.id)
        rm_count = rawMaterial.objects.filter().count()
        alertmessages.rmalert(rmm=rm_count, stock_count=rm_count)
        rm_data = rm.values()
        print(rm_data)
        
        print(rm_data,'rm_data created')
        rm_dic = rm_data[0]
        rm_id = int(rm_dic['id'])
        rm_scrapWeight = rm_dic['RM_scrapWeight']
        scrapsave.scrap_rm(id = rm_id,weight=rm_scrapWeight)
        rm_register_id = int(rm_dic['register_id'])
        logsave.logg(regid=rm_register_id,tbid=rm_id,operation='Entry Created',tname='Raw Material')

@receiver(post_save, sender= FMstock)
def fmstock_raw(sender,instance,created,**kwargs):
    if created:
        fm = FMstock.objects.filter(id__exact=instance.id)
        fm_data= fm.values()
        #######################################
        # check_fm_weight
        fm = FMstock.objects.values()
        size = []
        weight = []

        for i in fm:
            size.append(i['FM_Size'])
            weight.append(i['FM_Weight'])
        res = {key: [] for key in size}
        for key, val in zip(size, weight):
            res[key].append(int(val))
        keys = []
        values = []
        for i in res.values():
            values.append(sum(i))
        for i in res.keys():
            keys.append(i)
        res2 = {key: 0 for key in keys}
        for key, val in zip(keys, values):
            res2[key] = val
        for key, value in res2.items():
            # print(key,value)
            if 1000 >= value:
                alertmessages.empty(subject='Finish Material Alert',text='FM stock of size {} is Low get New Stock'.format(key),
                stock_count=value)
                # ms = Messages.objects.create()

                # ms.subject = 'Finish Material Alert'
                # ms.text = 'FM stock of size {} is Low get New Stock'.format(key)
                # ms.date = str(datetime.date.today())
                # ms.seen = 'False'
                # ms.stock_count = value
                # channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
                # ms.save()
                # print(key)
        


########################################################################
        # print(fm_data)
        fm_dic = fm_data[0]
        fm_id = int(fm_dic['id'])
        rawMaterial_id = int(fm_dic['coilUID_id'])
        ufm_register_id = int(fm_dic['register_id'])
        ufm_weight = fm_dic['UF_Weight']
        ufm_quantiy = int(fm_dic['UF_Quantity'])
        ufm_type = fm_dic['materialType']
        fm_size = fm_dic['FM_Size']              
        fm_weight= int(fm_dic['coilWeight'])
        # f_weight
        fm_scrapweight = fm_dic['FM_scrapWeight']
        scrapsave.scrap_fm(id=fm_id,weight=fm_scrapweight)
        # alertmessages.msale(weightt=fm_weight,id=fm_id,stock_count=fm_weight)
        logsave.logg(regid=ufm_register_id,tbid=fm_id,operation='Entry Created',tname='Finished Material Stock')
        rw = rawMaterial.objects.filter(id__exact=rawMaterial_id)
        rw_data = rw.values()
        rw_dic = rw_data[0]
        rw_size = rw_dic['RM_Size']
        rw_weight = int(rw_dic['RM_coilWeight'])
        # size = rw_size - fm_size
        weight = rw_weight - fm_weight
        # if rw_size < fm_size:
        #     print('not enough size in raw material')
        if rw_weight < fm_weight:
            print('not enough weight in raw material')
        else:
            raw = rawMaterial.objects.get(id=rawMaterial_id)
            # raw.RM_Thickness = 0
            # raw.RM_Size = size
            raw.RM_coilWeight = weight
            raw.save()
            logsave.logg(regid=ufm_register_id,tbid=rawMaterial_id,operation='Entry Updated',tname='Raw Material')

        ufmstock = UFMstock.objects.create()
        ufmstock.register = User.objects.get(id=ufm_register_id)
        ufmstock.UFM_Weight = ufm_weight
        ufmstock.UFM_Quantity = ufm_quantiy
        ufmstock.UFM_type = ufm_type
        ufmstock.FMid = FMstock.objects.get(id=instance.id)
        ufmstock.UFM_date = str(datetime.date.today())
        ufmstock.save()
        logsave.logg(regid=ufm_register_id,tbid=ufmstock.pk,operation='Entry Created',tname='Un-Finished Material Stock')


@receiver(post_save, sender= Sale)
def sale(sender,instance,created,**kwargs):
    if created:
        s = Sale.objects.filter(id__exact=instance.id)
        s_data= s.values()
        print(s_data)
        s_dic = s_data[0]
        s_idd = int(s_dic['id'])
        s_register_id = int(s_dic['register_id'])
        s_quantity= int(s_dic['Sale_Quantity'])
        FM_id = s_dic['FMcoilUID_id']
        logsave.logg(regid=s_register_id,tbid=s_idd,operation='Entry Created',tname='Sales')
        if FM_id == None:
            fm_id = 0
        else:
            fm_id = 1
        UF_id = s_dic['UFcoilID_id']
        if UF_id == None:
            uf_id = 0  
        else:
            uf_id = 1         
        s_weight= int(s_dic['Sale_Weight'])
        if fm_id == 1:
            fm = FMstock.objects.filter(id__exact=FM_id)
            fm_data = fm.values()
            fm_dic = fm_data[0]
            fm_weight = int(fm_dic['FM_Weight'])
            fm_quantity = int(fm_dic['FM_Quantity'])
            weight = fm_weight - s_weight
            quantity = fm_quantity - s_quantity
            if fm_weight < s_weight:
                print('not enough weight in stock')
            elif fm_quantity < s_quantity:
                print('not enough quantity in stock')
            else:
                fms = FMstock.objects.get(id=int(FM_id))
                fms.FM_Quantity = quantity
                fms.FM_Weight = weight
                fms.save()
                fm_check = FMstock.objects.values()
                size = []
                weight = []

                for i in fm_check:
                    size.append(i['FM_Size'])
                    weight.append(i['FM_Weight'])
                res = {key: [] for key in size}
                for key, val in zip(size, weight):
                    res[key].append(int(val))
                keys = []
                values = []
                for i in res.values():
                    values.append(sum(i))
                for i in res.keys():
                    keys.append(i)
                res2 = {key: 0 for key in keys}
                for key, val in zip(keys, values):
                    res2[key] = val
                for key, value in res2.items():
                    if 1000 >= value:
                        alertmessages.empty(subject='Finish Material Alert',text='FM stock of size {} is Low get New Stock'.format(key),
                        stock_count=value)
                        # ms = Messages.objects.create()
                        # ms.subject = 'Finish Material Alert'
                        # ms.text = 'FM stock of size {} is Low get New Stock'.format(key)
                        # ms.date = str(datetime.date.today())
                        # ms.seen = 'False'
                        # ms.stock_count = value
                        # channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
                        # ms.save()
                # alertmessages.msale(weightt=weight,id=FM_id,stock_count=0)
                logsave.logg(regid=s_register_id,tbid=FM_id,operation='Entry Updated',tname='Finished Material Stock')
        elif uf_id == 1:
            uf = UFMstock.objects.filter(id__exact=UF_id)
            uf_data = uf.values()
            uf_dic = uf_data[0]
            uf_weight = int(uf_dic['UFM_Weight'])
            uf_quantity = int(uf_dic['UFM_Quantity'])
            weight = uf_weight - s_weight
            quantity = uf_quantity - s_quantity
            if uf_weight < s_weight:
                print('not enough weight in stock')
            elif uf_quantity < s_quantity:
                print('not enough quantity in stock')
            else:
                print('ufid:',UF_id,uf_dic,)
                ufs = UFMstock.objects.get(id=UF_id)
                print(ufs)
                ufs.UFM_Quantity = quantity
                ufs.UFM_Weight = weight
                ufs.save()
                
                logsave.logg(regid=s_register_id,tbid=UF_id,operation='Entry Updated',tname='Un-Finished Material Stock')

@receiver(post_save, sender= EssentialItemUsePerDay)
def essentialitem(sender,instance,created,**kwargs):

    if created:
        es = EssentialItemUsePerDay.objects.filter(id__exact=instance.id)
        es_data= es.values()
        es_dic = es_data[0]
        es_idd = int(es_dic['id'])
        es_register_id = int(es_dic['register_id'])
        es_type = str(es_dic['EPD_Type'])
        es_id = es_dic['EPD_UID_id']   
        es_size = es_dic['EPD_Size']            
        es_quantity = int(es_dic['EPD_Quantity'])
        logsave.logg(regid=es_register_id,tbid=es_idd,operation='Entry Created', tname='Essential Item use per day Stock')
        upd = essentialitemStock.objects.filter(id__exact=es_id)
        upd_data = upd.values()
        upd_dic = upd_data[0]     
        # upd_size = int(upd_dic['ES_Size'])                 
        fm_Type= str(upd_dic['Type'])
        upd_quantity = int(upd_dic['ES_Quantity'])
        # size = upd_size - es_size
        quantity = upd_quantity - es_quantity 

        # if upd_size < es_size:
        #     print('not enough size in stock')
        if upd_quantity < es_quantity:
            print('not enough quantity in stock')
        else:
            estock = essentialitemStock.objects.get(id=es_id)
            estock.ES_Type = es_type
            # estock.ES_Size = size
            estock.ES_Quantity = quantity
            estock.save()
            alertmessages.esifelse(typee=fm_Type,quantityy=quantity,stock_count=quantity)
            logsave.logg(regid=es_register_id,tbid=es_id,operation='Entry Updated',tname='Essential Item Stock')
  

@receiver(post_save,sender=essentialitemStock)
def es_stock(sender,instance,created,**kwargs):
    if created:
        es = essentialitemStock.objects.filter(id__exact=instance.id)
        es_data = es.values()
        es_dic = es_data[0]
        es_id = int(es_dic['id'])
        es_quantity = int(es_dic['ES_Quantity'])
        es_type = str(es_dic['Type'])
        alertmessages.esifelse(typee=es_type,quantityy=es_quantity,stock_count=es_quantity)
        es_register_id = int(es_dic['register_id'])
        logsave.logg(regid=es_register_id,tbid=es_id,operation='Entry Created', tname='Essential Item Stock') 


@receiver(post_delete,sender=rawMaterial)
def raw_post(sender,instance,**kwargs):
    rm =rawMaterial.objects.filter().count()
    alertmessages.rmalert(rmm=rm,stock_count=rm)

# @receiver(post_delete,sender=FMstock)
# def fm_post(sender,instance,**kwargs):
#     fm = FMstock.objects.filter(id=instance.id)
#     alertmessages.rmalert(rmm=fm,stock_count=fm)
@receiver(post_delete,sender=essentialitemStock)
def es_post(sender,instance,**kwargs):
    es = essentialitemStock.objects.filter().count()
    if es == 0:
        alertmessages.empty(subject='Essential Stock Alert',text='essential item stock is empty',stock_count=0)

@receiver(pre_delete,sender=rawMaterial)
def raw_del(sender,instance,**kwargs):
    # rm = rawMaterial.objects.filter().count()
    # alertmessages.rmalert(rmm=rm,stock_count=rm)
    rm1 = rawMaterial.objects.filter(id=instance.id) 
    print(rm1.values())
    rm_dic = rm1.values()[0]
    table_name = 'Raw Material'
    m_id = rm_dic['id']
    date = rm_dic['RM_Date']
    size = rm_dic['RM_Size']
    weight = rm_dic['RM_coilWeight']
    type = 'Raw Material'
    quantity= 'Na'
    dt = Deleted_tables(table_name=table_name,material_id = m_id,date =date,size = size,type=type
            ,quantity=quantity,weight= weight)
    dt.save()

@receiver(pre_delete,sender=FMstock)
def FM_delete(sender,instance,**kwargs):
    # rm = FMstock.objects.filter().count()
    # alertmessages.rmalert(rmm=rm)
    fm = FMstock.objects.filter(id=instance.id) 
    rm_dic = fm.values()[0]
    table_name = 'Finished Material Stock'
    m_id = rm_dic['id']
    date = rm_dic['FM_Date']
    size = rm_dic['FM_Size']
    weight = rm_dic['FM_Weight']
    type = rm_dic['materialType'] +' FM'
    quantity= rm_dic['FM_Quantity']
    dt = Deleted_tables(table_name=table_name,material_id = m_id,date =date,size = size,type=type
            ,quantity=quantity,weight= weight)
    dt.save()
    # sc = Scrape.objects.get(t_id = m_id)
    # sc.delete()

@receiver(pre_delete,sender=UFMstock)
def UFM_delete(sender,instance,**kwargs):
    # rm = FMstock.objects.filter().count()
    # alertmessages.rmalert(rmm=rm)
    fm = UFMstock.objects.filter(id=instance.id) 
    rm_dic = fm.values()[0]
    table_name = 'Un-Finished Material Stock'
    m_id = rm_dic['id']
    date = rm_dic['UFM_date']
    size = 'Na'
    weight = rm_dic['UFM_Weight']
    type = 'UFM stock'
    quantity= rm_dic['UFM_Quantity']
    dt = Deleted_tables(table_name=table_name,material_id = m_id,date =date,size = size,type=type
            ,quantity=quantity,weight= weight)
    dt.save()

@receiver(pre_delete,sender=Sale)
def FM_delete(sender,instance,**kwargs):
    # rm = FMstock.objects.filter().count()
    # alertmessages.rmalert(rmm=rm)
    fm = Sale.objects.filter(id=instance.id) 
    rm_dic = fm.values()[0]
    table_name = 'Sales Table'
    m_id = rm_dic['id']
    date = rm_dic['Sale_date']
    size = 'Na'
    weight = rm_dic['Sale_Weight']
    type = rm_dic['Stock'] + ' Sales'
    quantity= rm_dic['Sale_Quantity']
    dt = Deleted_tables(table_name=table_name,material_id = m_id,date =date,size = size,type=type
            ,quantity=quantity,weight= weight)
    dt.save()

@receiver(post_delete,sender=FMstock)
def FM_delete_alert(sender,instance,**kwargs):
    fm = FMstock.objects.values()
    try:
        check = fm[0]

        size = []
        weight = []
        for i in fm:
            size.append(i['FM_Size'])
            weight.append(i['FM_Weight'])
        res = {key: [] for key in size}
        for key, val in zip(size, weight):
            res[key].append(int(val))
        keys = []
        values = []
        for i in res.values():
            values.append(sum(i))
        for i in res.keys():
            keys.append(i)
        res2 = {key: 0 for key in keys}
        for key, val in zip(keys, values):
            res2[key] = val
        print(res2)
        for key, value in res2.items():
            if 1000 >= value:
                alertmessages.empty(subject='Finish Material Alert',text='FM stock of size {} is Low get New Stock'.format(key)
                    ,stock_count=value,)
                # ms = Messages.objects.create()
                # ms.subject = 'Finish Material Alert'
                # ms.text = 'FM stock of size {} is Low get New Stock'.format(key)
                # ms.date = str(datetime.date.today())
                # ms.stock_count = value
                # ms.seen = 'False'
                # channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
                # ms.save()
                # print(key)
    except:
        alertmessages.empty(subject='Finish Material Alert',text='FM Stock is Empty',stock_count=0)
        # ms = Messages.objects.create()
        # ms.subject = 'Finish Material Alert'
        # ms.text = 'FM Stock is Empty'
        # ms.date = str(datetime.date.today())
        # ms.stock_count = 0
        # ms.seen= 'False'
        # channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
        # ms.save()



@receiver(pre_delete,sender=essentialitemStock)
def FM_delete(sender,instance,**kwargs):
    # rm = FMstock.objects.filter().count()
    # alertmessages.rmalert(rmm=rm)
    
    #######################################################################3
    fm = essentialitemStock.objects.filter(id=instance.id) 
    rm_dic = fm.values()[0]
    table_name = 'Essential Item Stock'
    m_id = rm_dic['id']
    date = rm_dic['ES_Date']
    size = rm_dic['ES_Size']
    weight = 'Na'
    type = 'Essential item stock'
    quantity= rm_dic['ES_Quantity']
    dt = Deleted_tables(table_name=table_name,material_id = m_id,date =date,size = size,type=type
            ,quantity=quantity,weight= weight)
    dt.save()

@receiver(pre_delete,sender=EssentialItemUsePerDay)
def FM_delete(sender,instance,**kwargs):
    # rm = FMstock.objects.filter().count()
    # alertmessages.rmalert(rmm=rm)
    fm = EssentialItemUsePerDay.objects.filter(id=instance.id) 
    rm_dic = fm.values()[0]
    table_name = 'Essential Item use per day'
    m_id = rm_dic['id']
    date = rm_dic['EPD_Date']
    size = rm_dic['EPD_Size']
    weight = 'Na'
    # type = rm_dic['EPD_Type']
    type = 'Essential User per Day'
    quantity= rm_dic['EPD_Quantity']
    dt = Deleted_tables(table_name=table_name,material_id = m_id,date =date,size = size,type=type
            ,quantity=quantity,weight= weight)
    dt.save()



# @receiver(post_save,sender=Messages)
# def msg_channel(sender,created,instance,**kwargs):
#     if created:
#         print(instance.id,'id################')
#         ms = Messages.objects.filter(id__exact = instance.id).values()
#         print(ms,'post_save ########')

