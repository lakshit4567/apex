from .models import *
import datetime
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# this notification alert system
class channel_alert:
    def save(subject,text,date,stock_count):
        print('save method called of messages')
        channel_layer = get_channel_layer()
        notification_objs = Messages.objects.filter(seen__exact = 'False').count()+1
        # print(notification_objs,'count#########')
        data = {
            'count': notification_objs,
            'Subject': subject,
            'text': text,
            'date':date,
            'stock_count': stock_count,
        }
        print(f'{data} ********************************************')
        async_to_sync(channel_layer.group_send)(
            'test_consumer_group' , {
                'type': 'send_notification',
                'value': json.dumps(data)

            }
        )




class alertmessages:
    def esifelse(typee,quantityy,stock_count):
        if typee == 'Belt' or 'Cylinder' or 'Fevil' or 'Cutter':
             if quantityy <= 20:        
                print('refile stock')
                ms = Messages.objects.create()
                ms.subject = 'Essential Stock Alert'
                ms.text = 'Essential Item ' + typee + ' is low please make new stock'
                ms.seen = 'False'
                ms.stock_count = stock_count
                ms.date = str(datetime.date.today())
                
                channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
                ms.save()
        elif typee == 'Cutting Oil':
            if quantityy <= 35:        
                print('refile stock')
                ms = Messages.objects.create()
                ms.subject = 'Essential Stock Alert'
                ms.text = 'Essential Item ' + typee + ' is low please make new stock'
                ms.date = str(datetime.date.today())
                ms.stock_count = stock_count
                ms.seen = 'False'
                channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
                ms.save()
        elif typee == 'Polish Wheel' or 'Conjuction Rod':
            if quantityy <= 2:        
                print('refile stock')
                ms = Messages.objects.create()
                ms.subject = 'Essential Stock Alert'
                ms.text = 'Essential Item ' + typee + ' is low please make new stock'
                ms.date = str(datetime.date.today())
                ms.stock_count = stock_count
                ms.seen = 'False'
                channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
                ms.save()
        elif typee == 'Matt Wheel' or 'Buff':
            if quantityy <= 10:        
                print('refile stock')
                ms = Messages.objects.create()
                ms.subject = 'Essential Stock Alert'
                ms.text = 'Essential Item ' + typee + ' is low please make new stock'
                ms.date = str(datetime.date.today())
                ms.stock_count = stock_count
                ms.seen = 'False'
                channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
                ms.save()
        elif typee == 'Plastic Roll' or 'Powder Box':
            if quantityy <= 1:        
                print('refile stock')
                ms = Messages.objects.create()
                ms.subject = 'Essential Stock Alert'
                ms.text = 'Essential Item ' + typee + ' is low please make new stock'
                ms.date = str(datetime.date.today())
                ms.stock_count = stock_count
                ms.seen = 'False'
                channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
                ms.save()
        elif typee == 'Big Carton':
            if quantityy <= 100:        
                print('refile stock')
                ms = Messages.objects.create()
                ms.subject = 'Essential Stock Alert' 
                ms.text = 'Essential Item ' + typee + ' is low please make new stock'
                ms.date = str(datetime.date.today())
                ms.stock_count = stock_count
                ms.seen = 'False'
                channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
                ms.save()
        elif typee == 'Small Plastic':
            if quantityy <= 5:        
                print('refile stock')
                ms = Messages.objects.create()
                ms.subject = 'Essential Stock Alert'
                ms.text = 'Essential Item ' + typee + ' is low please make new stock'
                ms.date = str(datetime.date.today())
                ms.stock_count = stock_count
                ms.seen = 'False'
                channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
                ms.save()

    def rmalert(rmm,stock_count):
        if rmm <= 1500:
            # print('refile stock')
            ms = Messages.objects.create()
            ms.subject = 'Raw Material Alert'
            ms.text = 'Coil stock is Low get New Stock'
            ms.date = str(datetime.date.today())
            ms.stock_count = stock_count
            ms.seen = 'False'
            channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
            ms.save()

    def empty(subject,text,stock_count):
        ms = Messages.objects.create()
        ms.subject = subject
        ms.text = text
        ms.date = str(datetime.date.today())
        ms.stock_count = stock_count
        ms.seen = 'False'
        channel_alert.save(subject=ms.subject,text=ms.text,stock_count=ms.stock_count,date=ms.date)
        ms.save()

    



class logsave():
    def logg(regid,tbid,operation,tname):
        log = LogTable.objects.create()
        use = User.objects.get(id=regid)
        log.register_id = str(regid)
        log.Username = str(use.username)
        log.CRUDoperation = operation
        log.Table_name = tname
        log.Table_id = str(tbid)
        log.Log_Date = str(datetime.date.today())
        log.save()

class scrapsave:
    def scrap_rm(id,weight):
        s = Scrape.objects.create()
        s.S_Type = 'Raw Material'
        s.t_id = id
        s.s_weight = weight
        s.S_date = str(datetime.date.today())
        s.save()
    def scrap_fm(id,weight):
        s = Scrape.objects.create()
        s.S_Type = 'Finish Material'
        s.t_id = id
        s.s_weight = weight
        s.S_date = str(datetime.date.today())
        s.save()

class dic_key_val:
    def dict(dic,key,value):
        type = []
        quantity = []
        
        for i in dic:
            type.append(i[key])
            quantity.append(i[value])
        # print(type,quantity)
        res = {key: [] for key in type}
        # print(res)
        for key, val in zip(type, quantity):
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
            
        return res2

    def dict_for_raw(dic,key,value):
        type = []
        quantity = []
        
        for i in dic:
            type.append(str(i[key])[8:])
            quantity.append(i[value])
        # print(type,quantity)
        res = {key: [] for key in type}
        # print(res)
        for key, val in zip(type, quantity):
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
            
        return res2

    def dict_for_fm(dic,key,value):
        type = []
        quantity = []
        
        for i in dic:
            type.append(str(i[key])[5:7])
            quantity.append(i[value])
        # print(type,quantity)
        res = {key: [] for key in type}
        # print(res)
        for key, val in zip(type, quantity):
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
            
        return res2


def check_for_null_values(d):
    try:
        total = int(list(d)[-1]) +1
        for i in range(1,total):
                # print(str(i))
                if str(i) not in d:
                    d[i]=0
    except:
        pass