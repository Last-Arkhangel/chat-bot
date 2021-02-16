#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import flask
import datetime
import settings
import core
import telebot
import sqlite3
import time
import requests
from core import create_db_new, blocked, unblocked, text, other, start, help, message_everyone
from flask import Flask, request
from flask_sslify import SSLify

WEBHOOK_URL_BASE = "https://{}:{}".format(settings.WEBHOOK_HOST, settings.WEBHOOK_PORT)

bot = telebot.TeleBot(settings.TOKEN, threaded=True)

# удаляем предыдущие вебхуки, если они были
bot.remove_webhook()

# ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
bot.set_webhook(url=WEBHOOK_URL_BASE + settings.WEBHOOK_PATH)

app = flask.Flask(__name__)
sslify = SSLify(app)

@bot.message_handler(commands=['start'])
def start2(message):
    start(message)

@bot.message_handler(commands=['help'])
def get_text_messages(message):
    help(message)

@bot.message_handler(commands=["ban"])
def bloc(message):
    blocked(message)

@bot.message_handler(commands=["unban"])
def some(message):
    unblocked(message)

@bot.message_handler(commands=["admin_message"])
def reklama(message):
    if message.chat.id == settings.ADMINS_ID:
        bot.send_message(message.chat.id, settings.Y_ADMIN)
        bot.register_next_step_handler(message, textrek)
    else:
        pass
def textrek(message):
    message_everyone(message)

@bot.message_handler(commands=['log'])
def logs(message):
    if message.chat.id == settings.ADMINS_ID:
        file = open(settings.DATABASE, 'rb')
        bot.send_document(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, settings.NO_ADMIN)

@bot.message_handler(content_types=['text'])
def tex(message):    
    text(message)

#photo #stikeri #video        
@bot.message_handler(content_types=['photo','sticker','video','audio','voice','location','animation','contact','document','dice','poll'])
def other2(message):    
    other(message)


# пустая главная страничка для проверки
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм 
@app.route(settings.WEBHOOK_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

# Start polling server
#bot.polling(interval=settings.POLLING_INTERVAL, timeout=settings.POLLING_TIMEOUT, none_stop=True)

# Start flask server
app.run(host=settings.WEBHOOK_LISTEN,
        port=settings.WEBHOOK_PORT,
        ssl_context=(settings.WEBHOOK_SSL_CERT, settings.WEBHOOK_SSL_PRIV),
        debug=settings.WEBHOOK_DEBUG)