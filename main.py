#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot import util
import re
import time
from time import sleep
import sys
import json
import os
import logging
import subprocess
import requests
import random
import base64
import urllib
from urllib import urlretrieve as dw
import urllib2
import redis
import requests as req
reload(sys)
sys.setdefaultencoding("utf-8")

TOKEN = '240545787:AAEwAOm2aKRcHVSYtLQ6gD-OBJFqCheA_OQ'
bot = telebot.TeleBot(TOKEN)
is_sudo = '142141024'
rediss = redis.StrictRedis(host='localhost', port=6379, db=0)
#################################################################################################################################################################################################

@bot.message_handler(commands=['short'])
def send_pic(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
      try:
        text = m.text.replace("/short ","")
        res = urllib.urlopen("http://yeo.ir/api.php?url={}".format(text)).read()
        bot.send_message(m.chat.id, "*Your Short Link :* {}".format(res), parse_mode="Markdown", disable_web_page_preview=True)
      except:
        bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['pic'])
def send_pic(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
      try:
        urllib.urlretrieve("https://source.unsplash.com/random", "img.jpg")
        bot.send_photo(m.chat.id, open('img.jpg'))
      except:
        bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################


@bot.message_handler(commands=['start'])
def welcome(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    c = types.InlineKeyboardButton("About",callback_data='pouria')
    markup.add(c)
    b = types.InlineKeyboardButton("Help",callback_data='help')
    markup.add(b)
    nn = types.InlineKeyboardButton("Inline Mode", switch_inline_query='')
    markup.add(nn)
    oo = types.InlineKeyboardButton("Channel", url='https://telegram.me/CyberCH')
    markup.add(oo)
    id = m.from_user.id
    rediss.sadd('memberspy',id)
    bot.send_message(cid, "*Hi*\n_Welcome To CyberBot_\n*Please Choose One*", disable_notification=True, reply_markup=markup, parse_mode='Markdown')

#################################################################################################################################################################################################

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
     if call.message:
        if call.data == "help":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Send /help Command!")
     if call.message:
        if call.data == "pouria":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="CyberBot Created By @This_Is_Pouria And Written In Python")
     if call.message:
        if call.data == "sticker":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            r = rediss.hget('file_id',call.message.chat.id)
            bot.send_sticker(call.message.chat.id, '{}'.format(r))
     if call.message:
        if call.data == "document":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            r = rediss.hget('file_id',call.message.chat.id)
            bot.send_document(call.message.chat.id, '{}'.format(r))
     if call.message:
        if call.data == "video":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            r = rediss.hget('file_id',call.message.chat.id)
            bot.send_video(call.message.chat.id, '{}'.format(r))
     if call.message:
        if call.data == "photo":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            r = rediss.hget('file_id',call.message.chat.id)
            bot.send_photo(call.message.chat.id, '{}'.format(r))
     if call.message:
        if call.data == "Audio":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=":D")
            r = rediss.hget('file_id',call.message.chat.id)
            bot.send_audio(call.message.chat.id, '{}'.format(r))

#################################################################################################################################################################################################

@bot.message_handler(commands=['stats'])
def send_stats(m):
    if m.from_user.id == 142141024:
        ban = str(rediss.scard('banlist'))
        usrs = str(rediss.scard('memberspy'))
        gps = str(rediss.scard('chats'))
        supergps = str(rediss.scard('supergroups'))
        text = '*Users* : *{}* \n\n*Groups* : *{}* \n\n*BanList* : *{}*'.format(usrs,gps,supergps,ban)
        bot.send_message(m.chat.id,text,parse_mode='Markdown')

#################################################################################################################################################################################################

@bot.message_handler(commands=['ban'])
def kick(m):
    if m.from_user.id == 142141024:
      if m.reply_to_message:
        ids = m.reply_to_message.from_user.id
        rediss.sadd('banlist',int(ids))
        bot.send_message(int(ids), '<b>You Are Banned!</b>',parse_mode='HTML')
        bot.send_message(m.chat.id, 'Banned!')

#################################################################################################################################################################################################

@bot.message_handler(commands=['unban'])
def send_stats(m):
    if m.from_user.id == 142141024:
      if m.reply_to_message:
        ids = m.reply_to_message.from_user.id
        rediss.srem('banlist',int(ids))
        bot.send_message(int(ids), '<b>You Are UnBanned!</b>',parse_mode='HTML')
        bot.send_message(m.chat.id, 'UnBanned!')

#################################################################################################################################################################################################

#@bot.message_handler(func=lambda message: True)
def set_stats(message):
    bot.reply_to(message, message.text)

#################################################################################################################################################################################################

@bot.message_handler(commands=['tex'])
def qr(message):
    banlist = rediss.sismember('banlist', '{}'.format(message.from_user.id))
    if str(banlist) == 'False':
      try:
        text = message.text.replace("/tex ","")
        urllib.urlretrieve('https://assets.imgix.net/sandbox/sandboxlogo.ai?blur=500&fit=crop&w=1200&h=600&txtclr=black&txt={}&txtalign=middle%2C%20center&txtsize=150&txtline=3'.format(text), 'time.jpg')
        bot.send_sticker(message.chat.id, open('time.jpg'))
      except:
        bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(content_types=['new_chat_member'])
def hi(m):
    name = m.new_chat_member.first_name
    title = m.chat.title
    id = m.new_chat_member.id
    if id == 142141024:
        rediss.sadd('chats',ids)
        bot.send_message(m.chat.id, 'Hi!\nPlease Start Me In Pravite', parse_mode='Markdown')
    else:
        bot.send_message(m.chat.id, '*Hi* `{}` *Welcome To* `{}`'.format(name,title), parse_mode='Markdown')

#################################################################################################################################################################################################

@bot.message_handler(commands=['cleanban'])
def kick(m):
    if m.from_user.id == 142141024:
        rediss.delete('banlist')
        bot.send_message(m.chat.id, '<b>Cleaned!</b>',parse_mode='HTML')

#################################################################################################################################################################################################

@bot.message_handler(content_types=['left_chat_member'])
def hi(m):
    name = m.left_chat_member.first_name
    bot.send_message(m.chat.id, '*GoodBye* `{}`'.format(name), parse_mode='Markdown')

#################################################################################################################################################################################################

@bot.message_handler(commands=['kick'])
def kick(m):
    if m.from_user.id == 142141024:
      if m.reply_to_message:
        text = m.reply_to_message.from_user.id
        bot.kick_chat_member(m.chat.id, text)
        bot.send_message(m.chat.id, '_User_ *{}* _has been kicked!_'.format(text), parse_mode='Markdown')
#################################################################################################################################################################################################

@bot.message_handler(commands=['kickme'])
def answer(m):
    bot.kick_chat_member(m.chat.id, m.from_user.id)

#################################################################################################################################################################################################

@bot.message_handler(regexp='^id')
def answer(m):
    if m.reply_to_message:
        id = m.reply_to_message.from_user.id
        bot.send_message(m.chat.id, id)

#################################################################################################################################################################################################

@bot.message_handler(commands=['id'])
def id_handler(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        cid = m.from_user.id
        fl = m.from_user.first_name
        bot.send_message(m.chat.id, "*{}*  Your ID = ```{}```".format(fl,cid), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['me'])
def answer(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        try:
          text = bot.get_chat_member(m.chat.id, m.from_user.id).status
          id = m.from_user.id
          rank = rediss.hget("user:rank","{}".format(id))
          msgs = rediss.get("{}".format(id))
          name = m.from_user.first_name
          user = m.from_user.username
          photo = rediss.hget('stickers',id)
          bot.send_message(m.chat.id, "*Name* : {} \n*UserName* = @{} \n*GlobalRank* : {} \n*Position In Group* : {} \n\n*Msgs* : {}".format(name,user,rank,text,msgs), parse_mode="Markdown")
          bot.send_sticker(m.chat.id,photo)
        except:
          bot.send_photo(m.chat.id, 'AgADBAADq6cxG3LsuA4NhfzrLPeDz-qCWBkABEgaS8eAZRQfsEkBAAEC',caption="Please Submit One Sticker For Your")
#################################################################################################################################################################################################

@bot.message_handler(commands=['leave'])
def leavehandler(m):
    if m.from_user.id == 142141024:
        bot.leave_chat(m.chat.id)

#################################################################################################################################################################################################

@bot.message_handler(commands=['food'])
def send_sports(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
      try:
        urllib.urlretrieve("http://lorempixel.com/400/200/food/OffLiNeTeam", "food.jpg")
        bot.send_sticker(m.chat.id, open('food.jpg'))
      except:
        bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['key'])
def keyboardHide(m):
        markup = types.ReplyKeyboardHide(selective=False)
        bot.send_message(m.chat.id, 'KeyBoard Cleaned', reply_markup=markup)

#################################################################################################################################################################################################

@bot.inline_handler(lambda query: len(query.query) is 0)
def query_text(query):
    user = query.from_user.username
    name = query.from_user.first_name
    lname = query.from_user.last_name
    uid = query.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('{}'.format(name), url="https://telegram.me/{}".format(user)))
    thumb_url = 'http://www.hopsten.de/assets/images/iNFO_LOGO.jpg'
    info = types.InlineQueryResultArticle('1','Your Info ',types.InputTextMessageContent('*Username : @{}\nYour First Name : {}\nYour Last Name : {}\nYour ID :  {}*'.format(user,name,lname,uid), parse_mode="Markdown"),reply_markup=markup,thumb_url=thumb_url)


    tumsss = 'http://images.clipartpanda.com/contact-clipart-contact-phone-md.png'
    random_text = random.randint(1, 100)
    tmpp = 'http://static.nautil.us/3006_5f268dfb0fbef44de0f668a022707b86.jpg'
    randowm = types.InlineQueryResultArticle('2', 'Random Nmber',types.InputTextMessageContent('random NUmber : {}'.format(random_text)), thumb_url=tmpp)


    req = urllib2.Request("http://umbrella.shayan-soft.ir/txt/joke.db")
    opener = urllib2.build_opener()
    f = opener.open(req)
    text = f.read()
    text1 = text.split(",")
    last = random.choice(text1)
    joke = types.InlineQueryResultArticle('3', 'Joke', types.InputTextMessageContent(last.replace('',"")),thumb_url='http://up.persianscript.ir/uploadsmedia/5b63-download-2-.png')
    
    
    reqa = urllib2.Request('http://api.gpmod.ir/time/')
    openera = urllib2.build_opener()
    fa = openera.open(reqa)
    parsed_jsona = json.loads(fa.read())
    ENtime = parsed_jsona['ENtime']
    FAtime = parsed_jsona['FAtime']
    ENdate = parsed_jsona['ENdate']
    FAdate = parsed_jsona['FAdate']
    time_tmp = 'http://a4.mzstatic.com/us/r30/Purple49/v4/c4/bf/0b/c4bf0bbe-f71c-12be-6017-818ab2594c98/icon128-2x.png'
    timesend = types.InlineQueryResultArticle('4', 'Time', types.InputTextMessageContent('`{}` : *ساعت* `{}` \n\n `{}` *Time* : `{}`'.format(FAdate,FAtime,ENdate,ENtime), parse_mode='Markdown'), thumb_url=time_tmp)
    
    
    req = urllib2.Request("http://umbrella.shayan-soft.ir/txt/danestani.db")
    opener = urllib2.build_opener()
    f = opener.open(req)
    text = f.read()
    text1 = text.split(",")
    last = random.choice(text1)
    logo = 'https://d2vvqscadf4c1f.cloudfront.net/R1H3Ms7QSQOwRpTbUImd_science.jpg'
    since = types.InlineQueryResultArticle('5', 'Danestani', types.InputTextMessageContent(last.replace('',"")),thumb_url=logo)

    bot.answer_inline_query(query.id, [info, randowm, joke, sinse, timesend], cache_time=5, switch_pm_text='Start bot')

#################################################################################################################################################################################################


@bot.inline_handler(lambda query: len(query.query.split()) == 1)
@bot.inline_handler(lambda query: len(query.query.split()) == 2)
@bot.inline_handler(lambda query: len(query.query.split()) == 3)
@bot.inline_handler(lambda query: len(query.query.split()) == 4)
@bot.inline_handler(lambda query: len(query.query.split()) == 5)
@bot.inline_handler(lambda query: len(query.query.split()) == 6)
@bot.inline_handler(lambda query: len(query.query.split()) == 7)
@bot.inline_handler(lambda query: len(query.query.split()) == 8)
@bot.inline_handler(lambda query: len(query.query.split()) == 9)
@bot.inline_handler(lambda query: len(query.query.split()) == 10)
def qq(q):
    l = q.query
    markdown = types.InlineQueryResultArticle('1', 'Markdown', types.InputTextMessageContent('{}'.format(l),parse_mode='Markdown'),thumb_url='http://uupload.ir/files/cd0k_m.jpg', description='Send Text With Markdown Styles')
    html = types.InlineQueryResultArticle('2', 'HTML', types.InputTextMessageContent('{}'.format(l),parse_mode='HTML'),thumb_url='http://uupload.ir/files/dc49_h.jpg', description='Send Text With HTML Styles')
    r = requests.get('https://api.github.com/users/{}'.format(l))
    json_data = r.json()
    if 'avatar_url' in json_data:
        url_html = json_data['html_url']
        typee = json_data['type']
        name = json_data['name']
        company = json_data['company']
        blog = json_data['blog']
        location = json_data['location']
        bio = json_data['bio']
        public_repos = json_data['public_repos']
        followers = json_data['followers']
        following = json_data['following']
        avatar_url = json_data['avatar_url']
        a = q.query
        avatar = types.InlineQueryResultPhoto('3', '{}'.format(avatar_url), '{}'.format(avatar_url), description='avatar', caption='Name : {}\nUrl : {}\nBlog : {}\nLocation : {}\nBio : {}\n\nRepos : {}\nFollowers : {}\nFollowing : {}'.format(name,url_html,blog,location,bio,public_repos,followers,following))
        avtar = types.InlineQueryResultPhoto('4', '{}'.format(a), '{}'.format(a), description='avatar', caption='aaa')
        bot.answer_inline_query(q.id, [markdown, html, avatar], cache_time=1)

#################################################################################################################################################################################################

@bot.message_handler(regexp='^(/mean) (.*)')
def mean(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
      try:
        text = m.text.split()[1]
        r = req.get('http://api.vajehyab.com/v2/public/?q={}'.format(text))
        json_data = r.json()
        textx = json_data['data']['text']
        bot.send_message(m.chat.id, textx)
      except:
        bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")
        
#################################################################################################################################################################################################

@bot.message_handler(content_types=['video','photo','sticker','document','audio','voice'])
def all(m):
        if m.chat.type == 'private':
            if m.photo :
                fileid = m.photo[1].file_id
            elif m.video :
                fileid = m.video.file_id
            elif m.sticker :
                fileid = m.sticker.file_id
            elif m.document :
                fileid = m.document.file_id
            elif m.audio :
                fileid = m.audio.file_id
            elif m.voice :
                fileid = m.voice.file_id
            e = m.from_user.username
            link = urllib2.Request("https://api.pwrtelegram.xyz/bot{}/getFile?file_id={}".format(TOKEN,fileid))
            open = urllib2.build_opener()
            f = open.open(link)
            link1 = f.read()
            jdat = json.loads(link1)
            patch = jdat['result']['file_path']
            send = 'https://storage.pwrtelegram.xyz/{}'.format(patch)
            bot.send_message(m.chat.id,'*File Id:*\n{}'.format(fileid),parse_mode='Markdown')
            bot.send_message(m.chat.id,'File Uploaded\nYour link: {}'.format(send))

#################################################################################################################################################################################################

@bot.message_handler(commands=['calc'])
def clac(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
      try:
        text = m.text.replace("/calc ","")
        res = urllib.urlopen("http://api.mathjs.org/v1/?expr={}".format(text)).read()
        bot.send_message(m.chat.id, "_{}_ = `{}`".format(text,res), parse_mode="Markdown", disable_web_page_preview=True)
      except:
        bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['msg'])
def send(m):
    user = m.from_user.username
    Msg = "Send Msg : "
    masg = m.text
    bot.send_message(142141024 , "TestMsg")
    print(user + Msg + masg )
#################################################################################################################################################################################################

@bot.message_handler(commands=['feedback'])
def feedback(m):    
  try:
    senderid = m.chat.id
    first = m.from_user.first_name
    usr = m.from_user.username
    str = m.text
    txt = str.replace('/feedback', '')
    bot.send_message(senderid, "_Thank Your Msg Posted admin_", parse_mode="Markdown")
    bot.send_message(142141024, "Msg : {}\nID : {}\nName : {}\nUsername : @{}".format(txt,senderid,first,usr))
  except:
    bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['uptime'])
def uptime(m):
    if m.from_user.id == 142141024:
        cc = os.popen("uptime").read()
        bot.send_message(m.chat.id, '{}'.format(cc))

#################################################################################################################################################################################################

@bot.message_handler(commands=['md'])
def time(m):
        pouria = m.text.replace("/md ","")
        bot.send_message(m.chat.id, "{}".format(pouria), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['bold'])
def time(m):
        pouria = m.text.replace("/bold ","")
        bot.send_message(m.chat.id, "*{}*".format(pouria), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['italic'])
def time(m):
        pouria = m.text.replace("/italic ","")
        bot.send_message(m.chat.id, "_{}_".format(pouria), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['code'])
def time(m):
        pouria = m.text.replace("/code ","")
        bot.send_message(m.chat.id, "`{}`".format(pouria), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['echo'])
def time(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        pouria = m.text.replace("/echo ","")
        bot.send_message(m.chat.id, "{}".format(pouria), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['ch'])
def time(m):
    pouria = m.text.replace("/send ","")
    bot.send_message(-1001052290909, "{}".format(pouria), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['num'])
def answer(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
      try:
        x = m.text.replace("/number ","")
        a = len(x)
        bot.send_message(m.chat.id, "*Number Of Your Text :* {}".format(a), parse_mode="Markdown")
      except:
        bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(content_types=['new_chat_participant'])
def send_message(m):
    cid = m.chat.id
    inviter = m.from_user.first_name
    userwhogotadded = m.new_chat_participant.first_name
    username = m.new_chat_participant.username
    groupname = m.chat.title
    groupid = m.chat.id
    rediss.sadd('group','{}'.format(m.chat.id))
    bot.send_message(-142141024, "New_chat \n\n name : {} id : {}".format(groupname,groupid), parse_mode="Markdown")
    bot.send_message(m.chat.id, "Hi all")

#################################################################################################################################################################################################

@bot.message_handler(commands=['sticker'])
def tostick(m):
  try:
    cid = m.chat.id
    if m.reply_to_message:
      if m.reply_to_message.photo:
        token = TOKEN
        fileid = m.reply_to_message.photo[1].file_id
        path1 = bot.get_file(fileid)
        path = path1.file_path
        link = "https://api.telegram.org/file/bot{}/{}".format(token,path)
        urllib.urlretrieve(link, "stick.png")
        file1 = open('stick.png', 'rb')
        bot.send_sticker(cid,file1)
  except:
        bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['clac'])
def clac(m):
  try:
    text = m.text.replace("/calc ","")
    res = urllib.urlopen("http://api.mathjs.org/v1/?expr={}".format(text)).read()
    bot.send_message(m.chat.id, "{}".format(res), parse_mode="Markdown", disable_web_page_preview=True)
  except:
    bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['photo'])
def tostick(m):
  try:
    cid = m.chat.id
    if m.reply_to_message:
      if m.reply_to_message.sticker:
        token = TOKEN
        fileid = m.reply_to_message.sticker.file_id
        path1 = bot.get_file(fileid)
        path = path1.file_path
        link = "https://api.telegram.org/file/bot{}/{}".format(token,path)
        urllib.urlretrieve(link, "stick1.png")
        file1 = open('stick1.png', 'rb')
        bot.send_photo(cid,file1)
  except:
        bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")
    
#################################################################################################################################################################################################

@bot.message_handler(regexp='^(/info)')
def info(m):
    if m.reply_to_message:
      id = m.reply_to_message.from_user.id
      user = m.reply_to_message.from_user.username
      first = m.reply_to_message.from_user.first_name
      last = m.reply_to_message.from_user.last_name
    else:
      id = m.from_user.id
      user = m.from_user.username
      first = m.from_user.first_name
      last = m.from_user.last_name
      profs = bot.get_user_profile_photos(id)
      count = profs.total_count
      url = req.get('http://api.gpmod.ir/time/')
      data = url.json()
      ENdate = data['ENdate']
      ENtime = data['ENtime']
      text = bot.get_chat_member(m.chat.id, m.from_user.id).status
      rank = rediss.hget("user:rank","{}".format(id))
      cap = 'First name : {}\nLast Name : {}\nUsername : @{}\nUser ID : {}\nDate : {}\nTime : {}\nGlobalRank : {}\nPost : {}'.format(first,last,user,id,ENdate,ENtime,rank,text)
    if int(count) == 0 :
      bot.send_photo(m.chat.id,open('personun.png'),caption='{}'.format(cap))
    else:
      fileid = profs.photos[0][2].file_id
      bot.send_photo(m.chat.id,fileid,caption='{}'.format(cap))
#################################################################################################################################################################################################

@bot.message_handler(commands=['setlink'])
def clac(m):
    if m.from_user.id == 142141024:
        text = m.text.replace("/setlink ","")
        rediss.hset("gp:link","{}".format(m.chat.id),"link: {}".format(text))
        bot.send_message(m.chat.id, "`This Link Seted` {}".format(text), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['link'])
def clac(m):
    link = rediss.hget("gp:link","{}".format(m.chat.id))
    bot.send_message(m.chat.id, "{}".format(link), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['setrank'])
def clac(m):
    if m.from_user.id == 142141024:
        text = m.text.split()[1]
        tezt = m.text.split()[2]
        rediss.hset("user:rank","{}".format(text),"{}".format(tezt))
        rank = rediss.hget("user:rank","{}".format(text))
        bot.send_message(m.chat.id, "`This Rank` *{}* `Seted For` {}".format(rank,text), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['rank'])
def clac(m):
  try:
    id = m.text.replace("/rank ","")
    rank = rediss.hget("user:rank","{}".format(id))
    bot.send_message(m.chat.id, "{}".format(rank), parse_mode="Markdown")
  except:
    bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['bc'])
def clac(m):
    if m.from_user.id == 142141024:
        text = m.text.replace("/bc ","")
        rd = rediss.smembers('memberspy')
        for id in rd:
            try:
                bot.send_message(id, "{}".format(text), parse_mode="Markdown")
            except:
                rediss.srem('memberspy', id)

#################################################################################################################################################################################################

@bot.message_handler(commands=['delrank'])
def kick(m):
    if m.from_user.id == 142141024:
        id = m.text.replace("/delrank ","")
        rank = rediss.hdel("user:rank","{}".format(id))
        bot.send_message(m.chat.id, '<code>Cleaned!</code>',parse_mode='HTML')

#################################################################################################################################################################################################

@bot.message_handler(commands=['setsticker'])
def tostick(message):
    cid = message.chat.id
    banlist = rediss.sismember('banlist', '{}'.format(message.from_user.id))
    if str(banlist) == 'False':
     try:
      if message.reply_to_message:
        if message.reply_to_message.sticker:
          token = TOKEN
          file_id = message.reply_to_message.sticker.file_id
          id = message.from_user.id
          rediss.hset('stickers',id,file_id)
          bot.send_message(message.chat.id, '<b>Sticker Has Been Set!</b>',parse_mode='HTML')
     except:
          bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['send']) 
def stats(message):
    id = message.text.replace("/send ","")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Sticker', callback_data='sticker'),types.InlineKeyboardButton('Document', callback_data='document'))
    markup.add(types.InlineKeyboardButton('Photo', callback_data='photo'),types.InlineKeyboardButton('Video', callback_data='video'))
    markup.add(types.InlineKeyboardButton('Audio', callback_data='Audio'))
    rediss.hset('file_id',message.chat.id,'{}'.format(id))
    bot.send_message(message.chat.id, 'Select _One_ of these `Items.:D` \n\n (Note: GIFs are Documents)', reply_markup=markup,parse_mode="Markdown")


#################################################################################################################################################################################################

@bot.message_handler(commands=['cap'])
def tostick(message):
    cid = message.chat.id
    banlist = rediss.sismember('banlist', '{}'.format(message.from_user.id))
    if str(banlist) == 'False':
     try:
      if message.reply_to_message:
        if message.reply_to_message.photo:
          token = TOKEN
          file_id = message.reply_to_message.photo[1].file_id
          id = message.from_user.id
          text = message.text.replace("/cap ","")
          rediss.hset('caption',id,file_id)
          photo = rediss.hget('caption',id)
          bot.send_photo(message.chat.id,photo,caption="{}".format(text))
     except:
          bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['help'])
def clac(m):
    text = m.text.replace("/help","")
    bot.send_message(m.chat.id, "*List Of Commands :*\n\n/short URL\n_Shorten Your Link_\n/pic\n_Sned Random Picture_\n/tex Text\n_Take Sticker From Text_\n/kickme\n_Exit From Group_\n/id\n_Get Your ID_\n/me\n_Show Your Information_\n/food\n_Get Food Sticker_\n/mean Text\n_Get The Meaning Of Texts_\n/feedback Text\n_Send PM To Admin_\n/bold Text\n_Bold The Text_\n/italic Text\n_Italic The Text_\n/code Text\n_Code The Text_\n/echo Text\n_Echo The Text_\n/sticker (reply to photo)\n_Convert Photo To Sticker_\n/photo (reply to sticker)\n_Convert Sticker To Photo_\n/info\n_Get Your Information_\n/link\n_Get Group Link_\n/rank\n_Show Your Rank_\n/setsticker (reply to sticker)\n_Set Sticker For Your Self_\n/cap Text (reply to photo)\n_Write Text Under The Photo_\n/setphone PhoneNumber\n_Set Your PhoneNumber In The Bot_\n/myphone\n_Show Your PhoneNumber_\n\n*Get Users ID:*\nid (reply to message)\n\n*Uploader Panel:*\n_Send Your File In Private To Upload!_".format(text), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['setphone'])
def clac(m):
  try:
    text = m.text.replace("/setphone","")
    rediss.hset("user:phone","{}".format(m.from_user.id),"{}".format(text))
    bot.send_message(m.chat.id, "`This phone` *{}* `Seted For` {}".format(text,m.from_user.username), parse_mode="Markdown")
  except:
    bot.send_message(m.chat.id, '*Error!*', parse_mode="Markdown")

#################################################################################################################################################################################################
@bot.message_handler(commands=['myphone'])
def clac(m):
    number = rediss.hget("user:phone","{}".format(m.from_user.id))
    bot.send_contact(m.chat.id, phone_number="{}".format(number), first_name="{}".format(m.from_user.first_name))

#################################################################################################################################################################################################

@bot.message_handler(commands=['fwd'])
def feed_back(message):
	markup = types.InlineKeyboardMarkup()
	b = types.InlineKeyboardButton("Cancel!",callback_data='cancel')
	msg = bot.send_message(message.chat.id, "Send Me Your Message Or Fwd Some Things", reply_markup=markup)
	bot.register_next_step_handler(msg, process_pm)
	
def process_pm(message):
	text = message.text
	bot.forward_message(142141024, message.from_user.id, message_id=message.message_id)

#################################################################################################################################################################################################
bot.polling(True)
#end
