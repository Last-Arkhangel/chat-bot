#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

# если выкладываем на heroku
WEBHOOK_HOST = ''

# телеграм может работать с портами 443, 80, 88 или 8443
WEBHOOK_PORT = '88'

# In some VPS you may need to put here the IP addr
WEBHOOK_LISTEN = '192.168.1.1'  

# Path to the ssl certificate
WEBHOOK_SSL_CERT = 'server.crt'  

# Path to the ssl private key
WEBHOOK_SSL_PRIV = 'server.key'  

# Path that telegram sends updates
WEBHOOK_PATH = "/cbv/"

# Debug 'True sets False'
WEBHOOK_DEBUG = False

# Interval to polling telegram servers
POLLING_INTERVAL = 2

# Timeout to polling telegram servers
POLLING_TIMEOUT = 25

# Bot version
VERSION = '1.1.1 від 03.01.2021'

#bot token
TOKEN = ''

#id without quotescan be group id
MAIN_ID = -11111111111

# Admin id: my
ADMINS_ID = 222222222

# Database name
DATABASE = 'users.db'

#start command
START = "Вітаю, {}! Версія бота {} р.\n"

#help command
HELP = "Графік роботи \n"

#answering_text to user
TEXT_MESSAGE = "Ви відправили запитання ↗️ відповімо"

#answering_text to admin
TEXT_ADMINS = "Ви не вибрали користувача ↖️ для відповіді."

#message that would be displayed if user has blocked you
BLOCKED = "🤖Бот був 📵заблокований📵 користувачем💩"

#ban message
BAN = "Ви були 🚫заблоковані🚫 адміністратором!"

#unban message
UNBAN = "Ви були ✅розблоковані✅ адміністратором."

#if admin has blocked a user
BANNED = "Вас 🚫заблокували🚫"

#not admin
NO_ADMIN = "Ви не адміністратор 👿!"

#not admin
Y_BAN = "Ви 🚫заблокували 👤користувача з id:"

#not admin
Y_UNBAN = "Ви ✅розблокували 👤користувача з id:"

#not admin
Y_ADMIN = "Ваше повідомлення буде відправлено: "

