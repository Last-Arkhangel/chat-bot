#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import telebot
import settings
import sqlite3

bot = telebot.TeleBot(settings.TOKEN)

def create_db_new():
    db = sqlite3.connect(settings.DATABASE, check_same_thread=False)
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS USERS(
        user_id INTEGER,
        first_name VARCHAR,
        messageid INT,
        message VARCHAR)''')
    sql.execute('''CREATE TABLE IF NOT EXISTS blocked(
        user_id INT)''')
    sql.execute('''CREATE TABLE IF NOT EXISTS user(
        user_id INT)''')
    sql.close()
    db.close()
create_db_new()


def blocked(message):
    try:
        db = sqlite3.connect(settings.DATABASE, check_same_thread=False)
        sql = db.cursor()
        if message.from_user.id == settings.ADMINS_ID:
            #fromm = str(message.from_user.id)
            #name = message.from_user.first_name
            sql.execute("SELECT user_id FROM USERS WHERE messageid = ?",(message.reply_to_message.message_id,))
            db.commit()
            Lusers = sql.fetchall()
            for i in Lusers:
                print(i[0])
                sql.execute("SELECT user_id FROM blocked WHERE user_id = ?",(i[0],))
                if sql.fetchone() is None:
                    bot.send_message(i[0],settings.BAN)
                    bot.send_message(message.chat.id, settings.Y_BAN + str(i[0]))
                    sql.execute("INSERT INTO blocked VALUES (?)",(i[0],))
                    db.commit()
        else:
            bot.send_message(message.chat.id, settings.NO_ADMIN)
        sql.close()
        db.close()
    except Exception as ee:
        print("error in block" + str(ee))


def text(message):
    try:
        db = sqlite3.connect(settings.DATABASE, check_same_thread=False)
        sql = db.cursor()
        sql.execute("SELECT user_id FROM blocked WHERE user_id = ?",(message.from_user.id,))
        db.commit()
        if sql.fetchone() is not None:
            bot.send_message(message.chat.id, settings.BANNED)
        else:
            if message.chat.id != settings.MAIN_ID:
                q = bot.forward_message(settings.MAIN_ID, message.chat.id, message.message_id)
                sql.execute("INSERT OR IGNORE INTO USERS VALUES(?,?,?,?)",(message.from_user.id,message.from_user.first_name, q.message_id, message.text))
                db.commit()
                bot.send_message(message.chat.id, settings.TEXT_MESSAGE)
                # mesenger id user consol
                print(message.message_id)
            elif message.chat.id == settings.MAIN_ID:
                if message.reply_to_message is None:
                    #bot.forward_message(settings.MAIN_ID, message.chat.id, message.message_id)
                    sql.execute("INSERT INTO USERS VALUES(?,?,?,?)",(message.from_user.id,message.from_user.first_name, message.message_id, message.text))
                    db.commit()
                    bot.send_message(message.chat.id, settings.TEXT_ADMINS)
                elif message.reply_to_message is not None:
                    # mesenger id admin consol
                    print(message.reply_to_message.message_id)
                    sql.execute("SELECT user_id FROM USERS WHERE messageid = ?",(message.reply_to_message.message_id,))
                    db.commit()
                    Lusers = sql.fetchall()
                    for i in Lusers:
                        # user id consol
                        print(i[0])
                        bot.send_message(i[0], message.text)
    except Exception as e:
        print(str(e))
        bot.send_message(message.chat.id, settings.BLOCKED)    


def unblocked(message):
    try:
        db = sqlite3.connect(settings.DATABASE, check_same_thread=False)
        sql = db.cursor()
        if message.from_user.id == settings.ADMINS_ID:
            sql.execute("SELECT user_id FROM USERS WHERE messageid = ?",(message.reply_to_message.message_id,))
            db.commit()
            Lusers = sql.fetchall()
            for i in Lusers:
                print(str(i[0]) + " mine")
                sql.execute("SELECT user_id FROM blocked WHERE user_id = ?",(i[0],))
                db.commit()
                print("unbanning")
                sql.execute("DELETE FROM blocked WHERE user_id = ?",(i[0],))
                db.commit()
                bot.send_message(i[0], settings.UNBAN)
                bot.send_message(message.chat.id, settings.Y_UNBAN + str(i[0]))
        else:
            bot.send_message(message.chat.id, settings.NO_ADMIN)
        sql.close()
        db.close()
    except Exception as ee:
        print("error in block" + str(ee))        


def start(message):
    try:
        db = sqlite3.connect(settings.DATABASE, check_same_thread=False)
        sql = db.cursor()
        bot.send_message(message.chat.id, settings.START.format(message.from_user.first_name + ' ' + ( message.from_user.last_name or ''), settings.VERSION), parse_mode='HTML')
        sql.execute("SELECT user_id FROM user WHERE user_id = ?",(message.from_user.id,))
        db.commit()
        if sql.fetchone() is None:
            sql.execute("INSERT INTO user VALUES(?)",(message.from_user.id,))
            db.commit()
        sql.close()
        db.close()
    except Exception as e:
        print(str(e))


def help(message):
    try:
        db = sqlite3.connect(settings.DATABASE, check_same_thread=False)
        sql = db.cursor()
        bot.send_message(message.chat.id, settings.HELP, parse_mode='HTML')
        sql.execute("SELECT user_id FROM user WHERE user_id = ?",(message.from_user.id,))
        db.commit()
        if sql.fetchone() is None:
            sql.execute("INSERT INTO user VALUES(?)",(message.from_user.id,))
            db.commit()
        sql.close()
        db.close()
    except Exception as e:
        print(str(e))

def other(message):
    try:
        db = sqlite3.connect(settings.DATABASE, check_same_thread=False)
        sql = db.cursor()
        sql.execute("SELECT user_id FROM blocked WHERE user_id = ?",(message.from_user.id,))
        db.commit()
        if sql.fetchone() is not None:
            bot.send_message(message.chat.id, settings.BANNED, parse_mode='HTML')
        else:
            if message.chat.id != settings.MAIN_ID:
                q = bot.forward_message(settings.MAIN_ID, message.chat.id, message.message_id)
                sql.execute("INSERT OR IGNORE INTO USERS VALUES(?,?,?,?)",(message.from_user.id,message.from_user.first_name, q.message_id, message.text))
                db.commit()
                bot.send_message(message.chat.id, settings.TEXT_MESSAGE)
                # mesenger id user consol
                print(message.message_id)
            elif message.chat.id == settings.MAIN_ID:
                if message.reply_to_message is None:
                    #bot.forward_message(settings.MAIN_ID, message.chat.id, message.message_id)
                    sql.execute("INSERT INTO USERS VALUES(?,?,?,?)",(message.from_user.id,message.from_user.first_name, message.message_id, message.text))
                    db.commit()
                    bot.send_message(message.chat.id, settings.TEXT_ADMINS)
                elif message.reply_to_message is not None:
                    # mesenger id admin consol
                    print(message.reply_to_message.message_id)
                    sql.execute("SELECT user_id FROM USERS WHERE messageid = ?",(message.reply_to_message.message_id,))
                    db.commit()
                    Lusers = sql.fetchall()
                    for i in Lusers:
                        # user id consol
                        print(i[0])
                        if message.content_type == "photo":
                            capt = message.caption
                            bot.send_photo(i[0], message.photo[-1].file_id, caption=capt)
                        elif message.content_type == "video":
                            capt = message.caption
                            bot.send_video(i[0], message.video.file_id, caption=capt)
                        elif message.content_type == "sticker":
                            bot.send_sticker(i[0], message.sticker.file_id)
                        elif message.content_type == "audio":
                            capt = message.caption
                            bot.send_audio(i[0], message.audio.file_id, caption=capt)
                        elif message.content_type == "voice":
                            capt = message.caption
                            bot.send_voice(i[0], message.voice.file_id, caption=capt)
                        elif message.content_type == "document":
                            capt = message.caption
                            bot.send_document(i[0], message.document.file_id, caption=capt)
                        elif message.content_type == "location":
                            bot.send_location(i[0], message.location.longitude, message.location.latitude)
                        elif message.content_type == "animation":
                            capt = message.caption
                            bot.send_animation(i[0], message.animation.file_id, caption=capt)
                        elif message.content_type == "contact":
                            bot.send_contact(i[0], message.contact.file_id)
        sql.close()
        db.close()
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, settings.BLOCKED)

def message_everyone(message):
    db = sqlite3.connect(settings.DATABASE, check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT user_id FROM user")
    Lusers = sql.fetchall()
    for i in Lusers:
        try:
            if message.content_type == "text":
                #text
                tex = message.text
                bot.send_message(i[0], tex)
            elif message.content_type == "photo":
                #photo
                capt = message.caption
                photo = message.photo[-1].file_id
                bot.send_photo(i[0], photo, caption=capt)
            elif message.content_type == "video":
                #video
                capt = message.caption
                photo = message.video.file_id
                bot.send_video(i[0], photo)
            elif message.content_type == "audio":
                #audio
                capt = message.caption
                photo = message.audio.file_id
                bot.send_audio(i[0], photo, caption=capt)
            elif message.content_type == "voice":
                #voice
                capt = message.caption
                photo = message.voice.file_id
                bot.send_voice(i[0], photo, caption=capt)
            elif message.content_type == "animation":
                #animation
                capt = message.caption
                photo = message.animation.file_id
                bot.send_animation(i[0], photo, caption=capt)
            elif message.content_type == "document":
                #document
                capt = message.caption
                photo = message.document.file_id
                bot.send_document(i[0], photo, caption=capt)
        except:
            print("error!!")
    sql.close()
    db.close()
    
