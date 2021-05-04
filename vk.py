# -*- coding: utf-8 -*-
import vk_api
import bs4
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from bot_vk import*

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id':0})

token = "52a012744a2cae90394c97e810fb3e2d7ea89ce24a2c50db31014215e7e69874017945543d7f88cc79887"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)



print("Server started")
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            bot = VkBot(event.user_id)
            print('For me by:', 'https://vk.com/'+str(event.user_id), end='')
            write_msg(event.user_id, bot.new_message(event.text))
            print('Text: ', event.text)
