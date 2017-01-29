# -*- coding: UTF-8 -*-

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import requests
from bs4 import BeautifulSoup

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
taiwan=['臺北市','新北市','桃園市','臺中市','臺南市','高雄市','基隆市','新竹縣','新竹市','苗栗縣','彰化縣','南投縣','雲林縣','嘉義縣','嘉義市','屏東縣','宜蘭縣','花蓮縣','臺東縣','澎湖縣','金門縣','連江縣']
weather_url=settings.WEATHER_URL

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    final_reply = event.message.text  #if not searching for weather,echo it
    for country in taiwan:
        if country in event.message.text: #if there is city that match input string
            website=requests.get(weather_url)
            soup = BeautifulSoup(website.text,"html.parser")
            str_pointer=soup.find(string=country) #find where the tag is
            str_pointer=str_pointer.find_parents("location")
            for fragment in str_pointer:
                weather=fragment.find('parametername').string  #find the first weather
            final_reply=country + weather #concat with country name
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=final_reply) #reply
    )

@handler.default()
def default(event):
    print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='講中文啦!') #if is not text message,like stickers
    )

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()