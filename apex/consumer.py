# channels              2.4.0
# channels-redis        2.4.2


import datetime
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from .models import *
# this is admin notification system
class AlertSystem(WebsocketConsumer):
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({'status':'connected from django channels'}))
    #{'user_id':1, 'message':'hi'} thats how we'll send data from front end
    def receive(self, text_data):
        # print(text_data,'this is text data')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type': 'run',
                'payload': text_data
            }
        )
        # data = text_data

        # d = data['status']
        # print(d,'this is out data')        
        # self.send(text_data=json.dumps({'status':'we got you'}))


    def disconnect(self, *args , **kwargs):
        print('disconnected')

    def send_notification(self, event):
        # print(event)

        data = json.loads(event.get('value'))
        print(data,'@@@@@@@@@@@@@')
        # print(f'data in consumer {data}')
        self.send(text_data=json.dumps({'payload':data}))
        print('alert notification')
    

    # def run(self,event):
    #     data = event['payload']
    #     print(data)

    #     data1 = json.loads(data)
    #     print(data1)
    #     d = data1['status']
    #     users = Register.objects.all()
    #     user_list = users.values()
    #     if d == 'Active':
    #         for i in user_list:
    #             user_name = i['UserName']
    #             status = i['userRole']
    #             user_id = i['user_id']
    #             get_user = Register.objects.get(user_id=user_id)
    #             get_user.userRole = 'Active'
    #             get_user.save()
    #     elif d == 'time up':
    #         for i in user_list:
    #             user_name = i['UserName']
    #             status = i['userRole']
    #             user_id = i['user_id']
    #             get_user = Register.objects.get(user_id=user_id)
    #             if user_name == 'admin@gmail.com':
    #                 get_user.userRole = 'Active'
    #                 get_user.save()
    #             else:
    #                 get_user.userRole = 'Not_Active'
    #             # print(get_user.userRole,get_user.UserName,'working hours over')
    #                 get_user.save()
    #     self.send(text_data=json.dumps({'payload':data1}))
# this is user alert notification system
class UserAlert(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_code']
        self.room_group_name = "room_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        try:
            reg = Register.give_noti_detail(self.room_name)
            print(reg)
            self.accept()
            # self.send(text_data=json.dumps({'payload':reg}))
        except:
            # print(reg)
            self.accept()
            self.send(text_data=json.dumps({'payload':'sdsdd'}))
    def receive(self,text_data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_alert_user',
                'payload': text_data
            }
        )
        

    def disconnect(self,close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print('disconnected')

    def send_alert_user(self, event):
        print('alert notification')
        # print(event['value'],'@@@@')
        try:
            print(event.get('value'),'sdksdkd')
            data = json.loads(event.get('value'))
            # print(f'data in consumer {data}')
            self.send(text_data=json.dumps({'payload':data}))
            print('alert notification')
        except:
            pass