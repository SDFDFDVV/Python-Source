#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot
from telebot import types
from telebot import util
import sys
import json
import os
import random
import base64
import urllib
import urllib2
import redis
import requests as req
reload(sys)
sys.setdefaultencoding("utf-8")

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)
is_sudo = '142141024'
rediss = redis.StrictRedis(host='localhost', port=6379, db=0)
#################################################################################################################################################################################################

@bot.message_handler(commands=['shorten'])
def send_pic(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.replace("/shorten ","")
        res = urllib.urlopen("http://yeo.ir/api.php?url={}".format(text)).read()
        bot.send_message(m.chat.id, "*Your Short Link :* {}".format(res), parse_mode="Markdown", disable_web_page_preview=True)

#################################################################################################################################################################################################

@bot.message_handler(commands=['pic'])
def send_pic(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        urllib.urlretrieve("https://source.unsplash.com/random", "img.jpg")
        bot.send_photo(m.chat.id, open('img.jpg'))

#################################################################################################################################################################################################

@bot.message_handler(commands=['start'])
def welcome(m):
    cid = m.chat.id
    markup = types.InlineKeyboardMarkup()
    b = types.InlineKeyboardButton("Help",callback_data='help')
    c = types.InlineKeyboardButton("About",callback_data='pouria')
    markup.add(b,c)
    nn = types.InlineKeyboardButton("Inline Mode", switch_inline_query='')
    oo = types.InlineKeyboardButton("Channel", url='https://telegram.me/CyberCH')
    markup.add(nn,oo)
    id = m.from_user.id
    rediss.sadd('memberspy',id)
    bot.send_message(cid, "Hi \n\nWelcome To CyberBot \n\nPlease Choose One :)", disable_notification=True, reply_markup=markup)

#################################################################################################################################################################################################

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
     if call.message:
        if call.data == "help":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Comming Soon!")
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
        ids = m.text.split()[1]
        rediss.sadd('banlist',int(ids))
        bot.send_message(int(ids), '<b>You Are Banned!</b>',parse_mode='HTML')
        bot.send_message(m.chat.id, 'Banned!')

#################################################################################################################################################################################################

@bot.message_handler(commands=['unban'])
def send_stats(m):
    if m.from_user.id == 142141024:
        ids = m.text.split()[1]
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
        text = message.text.replace("/tex ","")
        urllib.urlretrieve('https://assets.imgix.net/sandbox/sandboxlogo.ai?blur=500&fit=crop&w=1200&h=600&txtclr=black&txt={}&txtalign=middle%2C%20center&txtsize=150&txtline=3'.format(text), 'time.jpg')
        bot.send_sticker(message.chat.id, open('time.jpg'))

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
        text = m.text.split()[1]
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
def test_handler(m):
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

@bot.message_handler(commands=['getme'])
def answer(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = bot.get_chat_members_count(m.chat.id).status
        bot.send_message(m.chat.id,text)

#################################################################################################################################################################################################

@bot.message_handler(commands=['imdb'])
def gif(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.replace("/imdb ","")
        r = requests.get('http://www.omdbapi.com/?t={}'.format(text))
        json_data = r.json()
        Year = json_data['Year']
        Title = json_data['Title']
        Released = json_data['Released']
        Runtime = json_data['Runtime']
        Genre = json_data['Genre']
        Director = json_data['Director']
        Language = json_data['Language']
        Poster = json_data['Poster']
        urllib.urlretrieve("{}".format(Poster), "imdb.png")
        bot.send_sticker(m.chat.id, open('imdb.png'))
        bot.send_message(m.chat.id, "*Title* : ``` {}``` \n *Year* : ``` {}```\n *Published* : ``` {}``` \n *Runtime* : ``` {}``` \n *Genre* : ``` {}``` \n *Director* : ``` {}``` \n *Language* : ```{}```".format(Title,Year,Released,Runtime,Genre,Director,Language), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['song'])
def music(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.replace("/song ","")
        opener = urllib2.build_opener()
        f = opener.open('https://api.spotify.com/v1/search?limit=1&type=track&q={}'.format(text))
        parsed_json = json.loads(f.read())
        Artist = parsed_json['tracks']['items'][0]['artists'][0]['name']
        name = parsed_json['tracks']['items'][0]['name']
        music = parsed_json['tracks']['items'][0]['preview_url']
        urllib.urlretrieve("{}".format(music), "song.ogg")
        image = parsed_json['tracks']['items'][0]['album']['images'][0]['url']
        urllib.urlretrieve("{}".format(image), "song.png")
        bot.send_message(m.chat.id, "*Artist* : ```{}``` \n *Name* : ```{}```".format(Artist,name), parse_mode="Markdown")
        bot.send_sticker(m.chat.id, open('song.png'))
        bot.send_document(m.chat.id, open('song.ogg'), caption=" @CyberCH")

#################################################################################################################################################################################################

@bot.message_handler(regexp='^(/ip) (.*)')
def ip(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.split()[1]
        r = requests.get('http://ip-api.com/json/{}?fields=262143'.format(text))
        json_data = r.json()
        country = json_data['country']
        city = json_data['city']
        isp = json_data['isp']
        timezone = json_data['timezone']
        lon = json_data['lon']
        lat = json_data['lat']
        bot.send_location(m.chat.id, lat, lon)
        bot.send_message(m.chat.id, "*Country* : ```{}``` \n *City* : ```{}``` \n *Isp* : ```{}``` \n *Timezone* : ```{}```".format(country,city,isp,timezone), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['food'])
def send_sports(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':    
        urllib.urlretrieve("http://lorempixel.com/400/200/food/OffLiNeTeam", "food.jpg")
        bot.send_sticker(m.chat.id, open('food.jpg'))

#################################################################################################################################################################################################

@bot.message_handler(commands=['key'])
def keyboardHide(m):
        markup = types.ReplyKeyboardHide(selective=False)
        bot.send_message(m.chat.id, 'KeyBoard Cleaned', reply_markup=markup)

#################################################################################################################################################################################################

@bot.message_handler(commands=['logo'])
def logo(message):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = message.text.split()[1]
        urllib.urlretrieve('http://logo.clearbit.com/{}?size=800'.format(text), 'logo.jpg')
        bot.send_sticker(message.chat.id, open('logo.jpg'))

#################################################################################################################################################################################################

@bot.inline_handler(lambda query: len(query.query) is 0)
def query_text(query):
    user = query.from_user.username
    name = query.from_user.first_name
    lname = query.from_user.last_name
    uid = query.from_user.id
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('{}'.format(lname), url="https://telegram.me/{}".format(user)))
    thumb_url = 'http://uupload.ir/files/7d23_download.png'
    info = types.InlineQueryResultArticle('1',
                                          'Your Info',
                                          types.InputTextMessageContent('*Username* : @{} \n*Your First Name* : *{}* \n*Your LastName* : *{}* \n*Your ID* : *{}*'.format(user,name,lname,uid), parse_mode="Markdown"),
                                          reply_markup=markup,
                                          thumb_url=thumb_url)

    text = urllib.urlopen("http://vip.opload.ir/vipdl/94/11/amirhmz/joke.db").read()
    text1 = text.split(",")
    last = random.choice(text1)
    joke = types.InlineQueryResultArticle('4', 'Joke', types.InputTextMessageContent('{}'.format(last)),thumb_url='http://uupload.ir/files/sfxc_download.jpg')
    
    
    url = req.get('http://api.gpmod.ir/time/')
    data = url.json()
    FAdate = data['FAdate']
    FAtime = data['FAtime']
    ENdate = data['ENdate']
    ENtime = data['ENtime']
    time_tmp = 'http://uupload.ir/files/zneb_download_(1).png'
    timesend = types.InlineQueryResultArticle('2', 'Time', types.InputTextMessageContent('`{}` : *ساعت* `{}` \n\n `{}` *Time* : `{}`'.format(FAdate,FAtime,ENdate,ENtime), parse_mode='Markdown'), thumb_url=time_tmp)
    bot.answer_inline_query(query.id, [info, dollar, joke, timesend], cache_time=5, switch_pm_text='Start bot')

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

@bot.message_handler(regexp='^(/git) (.*)')
def gif(m):
    text = m.text.split()[1]
    r = requests.get('https://api.github.com/users/{}'.format(text))
    json_data = r.json()
    if 'id' in json_data:
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
        urllib.urlretrieve("{}".format(avatar_url), "git.png")
        bot.send_sticker(m.chat.id, open('git.png'))
        bot.send_message(m.chat.id, 'Name : <b>{}</b>\nType : <b>{}</b>\nCompany : <b>{}</b>\nblog : <code>{}</code>\nlocation : <b>{}</b>\nbio : <i>{}</i>\n\nUrl : <code>{}</code>\nfollowers : <code>{}</code>\nfollowing : <code>{}</code>\nRepos : <code>{}</code>\n\xE2\x97\xBC \xE2\x97\xBB \xE2\x97\xBC \xE2\x97\xBB \xE2\x97\xBC \xE2\x97\xBB \xE2\x97\xBC \n@taylor_team'.format(name,typee,company,blog,location,bio,url_html,followers,following,public_repos), parse_mode='HTML')
        print 'bot send git command'
    if 'message' in json_data:
        bot.send_message(m.chat.id, 'Error \n/git [username]')
        return

#################################################################################################################################################################################################

@bot.inline_handler(lambda query: len(query.query.split()) == 1)
def qq(q):
    text = q.query
    r = requests.get('https://api.github.com/users/{}'.format(text))
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
        tmp = 'http://ericsteinborn.com/github-for-cats/img/ironcat.png'
        gitss = types.InlineQueryResultArticle('1', 'Git username\xE2\x9C\x8F\xEF\xB8\x8F', types.InputTextMessageContent('Name : <b>{}</b>\nUrl : <b>{}</b>\nBlog : <b>{}</b>\nLocation : <b>{}</b>\nBio : <i>{}</i>\n\nRepos : <code>{}</code>\nfollowers : <code>{}</code>\nfollowing : <code>{}</code>'.format(name,url_html,blog,location,bio,public_repos,followers,following), parse_mode="HTML"), thumb_url=tmp)
        avatarr = types.InlineQueryResultPhoto('2', '{}'.format(avatar_url), '{}'.format(avatar_url), description='avatar', caption='Name : {}\nUrl : {}\nBlog : {}\nLocation : {}\nBio : {}\n\nRepos : {}'.format(name,url_html,blog,location,bio,public_repos))
        bot.answer_inline_query(q.id, [gitss, avatarr], cache_time=1)

#################################################################################################################################################################################################

@bot.message_handler(regexp='^(/mean) (.*)')
def mean(m):
    banlist = rediss.sismember('banlist_arrow', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        text = m.text.split()[1]
        r = req.get('http://api.vajehyab.com/v2/public/?q={}'.format(text))
        json_data = r.json()
        textx = json_data['data']['text']
        bot.send_message(m.chat.id, textx)
        
#################################################################################################################################################################################################

@bot.message_handler(commands=['gif'])
def aparat(m):
    text = m.text.replace('/gif ','')
    url = "http://www.flamingtext.com/net-fu/image_output.cgi?_comBuyRedirect=false&script=blue-fire&text={}&symbol_tagname=popular&fontsize=70&fontname=futura_poster&fontname_tagname=cool&textBorder=15&growSize=0&antialias=on&hinting=on&justify=2&letterSpacing=0&lineSpacing=0&textSlant=0&textVerticalSlant=0&textAngle=0&textOutline=off&textOutline=false&textOutlineSize=2&textColor=%230000CC&angle=0&blueFlame=on&blueFlame=false&framerate=75&frames=5&pframes=5&oframes=4&distance=2&transparent=off&transparent=false&extAnim=gif&animLoop=on&animLoop=false&defaultFrameRate=75&doScale=off&scaleWidth=240&scaleHeight=120&&_=1469943010141".format(text)
    res = urllib.urlopen(url)
    parsed_json = json.loads(res.read())
    gif = parsed_json['src']
    link = parsed_json['gimpHost']
    urllib.urlretrieve("{}".format(gif), "aaa.gif")
    bot.send_document(m.chat.id, open('aaa.gif'), caption="@CyberCH")

#################################################################################################################################################################################################
    
@bot.message_handler(commands=['stickerpro'])
def aparat(m):
    text = m.text.replace('/stickerpro ','')
    url = "https://assets.imgix.net/examples/clouds.jpg?blur=150&w=150&h=150&fit=crop&txt={}&txtsize=50&txtclr=blue&txtalign=middle,center&txtfont=Futura%20Condensed%20Medium&mono=ff6598cc".format(text)
    res = urllib.urlopen(url)
    urllib.urlretrieve("{}".format(url), "aaa.png")
    bot.send_sticker(m.chat.id, open('aaa.jpg'))

#################################################################################################################################################################################################

@bot.message_handler(commands=['qr'])
def code(message):
    text = message.text.split()[1]
    urllib.urlretrieve("https://chart.googleapis.com/chart?chs=150x150&cht=qr&chl={}".format(text), 'qr.jpg')
    bot.send_photo(message.chat.id, open('qr.jpg'))

#################################################################################################################################################################################################

@bot.message_handler(commands=['imagepro'])
def aparat(m):
    text = m.text.replace('/imagepro ','')
    url = "https://assets.imgix.net/examples/clouds.jpg?blur=150&w=150&h=150&fit=crop&txt={}&txtsize=50&txtclr=blue&txtalign=middle,center&txtfont=Futura%20Condensed%20Medium&mono=ff6598cc".format(text)
    res = urllib.urlopen(url)
    urllib.urlretrieve("{}".format(url), "aaa.png")
    bot.send_photo(m.chat.id, open('aaa.jpg'), caption="@CyberCH")
    
#################################################################################################################################################################################################

@bot.message_handler(commands=['sport'])
def sport(message):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False':
        urllib.urlretrieve('http://lorempixel.com/400/200/sports/OffLiNewTeam/', 'sport.jpg')
        bot.send_sticker(message.chat.id, open('sport.jpg'))

#################################################################################################################################################################################################


#################################################################################################################################################################################################

@bot.message_handler(commands=['calc'])
def clac(m):
    banlist = rediss.sismember('banlist', '{}'.format(m.from_user.id))
    if str(banlist) == 'False': 
        text = m.text.replace("/calc ","")
        res = urllib.urlopen("http://api.mathjs.org/v1/?expr={}".format(text)).read()
        bot.send_message(m.chat.id, "_{}_ = `{}`".format(text,res), parse_mode="Markdown", disable_web_page_preview=True)

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
    senderid = m.chat.id
    first = m.from_user.first_name
    usr = m.from_user.username
    str = m.text
    txt = str.replace('/feedback', '')
    bot.send_message(senderid, "_Thank Your Msg Posted admin_", parse_mode="Markdown")
    bot.send_message(142141024, "Msg : {}\nID : {}\nName : {}\nUsername : @{}".format(txt,senderid,first,usr))

#################################################################################################################################################################################################

@bot.message_handler(commands=['uptime'])
def uptime(m):
    if m.from_user.id == config.is_sudo:
        cc = os.popen("uptime").read()
        bot.send_message(m.chat.id, '{}'.format(cc))

#################################################################################################################################################################################################

@bot.message_handler(commands=['md'])
def time(m):
        pouria = m.text.replace("/md ","")
        bot.send_message(m.chat.id, "{}".format(pouria), parse_mode="Markdown")

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
        x = m.text.replace("/number ","")
        a = len(x)
        bot.send_message(m.chat.id, "*Number Of Your Text :* {}".format(a), parse_mode="Markdown")

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

#################################################################################################################################################################################################

@bot.message_handler(commands=['clac'])
def clac(m):
    text = m.text.replace("/calc ","")
    res = urllib.urlopen("http://api.mathjs.org/v1/?expr={}".format(text)).read()
    bot.send_message(m.chat.id, "{}".format(res), parse_mode="Markdown", disable_web_page_preview=True)

#################################################################################################################################################################################################

@bot.message_handler(commands=['photo'])
def tostick(m):
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
    id = m.text.replace("/rank ","")
    rank = rediss.hget("user:rank","{}".format(id))
    bot.send_message(m.chat.id, "{}".format(rank), parse_mode="Markdown")

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
      if message.reply_to_message:
        if message.reply_to_message.sticker:
          token = TOKEN
          file_id = message.reply_to_message.sticker.file_id
          id = message.from_user.id
          rediss.hset('stickers',id,file_id)
          bot.send_message(message.chat.id, '<b>Sticker Has Been Set!</b>',parse_mode='HTML')

#################################################################################################################################################################################################

@bot.message_handler(content_types=['photo','sticker','document','video','audio','voice'])
def send_photo_id(message):
  text = m.text.replace("/fileid")
  if message.reply_to_message:
    if message.photo:
        bot.send_message(message.chat.id, "File ID :\n" + message.photo[1].file_id)
    if message.sticker:
        bot.send_message(message.chat.id, "File ID :\n" + message.sticker.file_id)
    if message.document:
        bot.send_message(message.chat.id, "File ID :\n" + message.document.file_id)
    if message.voice:
        bot.send_message(message.chat.id, "File ID :\n" + message.voice.file_id)
    if message.audio:
        bot.send_message(message.chat.id, "File ID :\n" + message.audio.file_id)
    if message.video:
        bot.send_message(message.chat.id, "File ID :\n" + message.video.file_id)

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
      if message.reply_to_message:
        if message.reply_to_message.photo:
          token = TOKEN
          file_id = message.reply_to_message.photo[1].file_id
          id = message.from_user.id
          text = message.text.replace("/cap ","")
          rediss.hset('caption',id,file_id)
          photo = rediss.hget('caption',id)
          bot.send_photo(message.chat.id,photo,caption="{}".format(text))

#################################################################################################################################################################################################

@bot.message_handler(commands=['sethelp'])
def clac(m):
    if m.from_user.id == 142141024:
        text = m.text.replace("/sethelp","")
        rediss.hset("help","{}".format(text))
        bot.send_message(m.chat.id, "`New Help Has Been Set!` {}".format(text), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['help'])
def clac(m):
    text = m.text.replace("/get","")
    link = rediss.get("help")
    bot.send_message(m.chat.id, "{}".format(link), parse_mode="Markdown")

#################################################################################################################################################################################################

@bot.message_handler(commands=['aparat'])
def aparat(m):
    import urllib
    import json
    import os
    text = m.text.split(' ',1)[1]
    url = urllib.urlopen('http://www.aparat.com/etc/api/videoBySearch/text/'+text)
    data = url.read()
    js = json.loads(data)
    title1 = js['videobysearch'][0]['title']
    poster1 = js['videobysearch'][0]['big_poster']
    uid1 = js['videobysearch'][0]['uid']
    urllib.urlretrieve(poster1,'poster.png')
    bot.send_photo(m.chat.id, open('poster.png'), caption='Title : '+title1+'\nLink : http://www.aparat.com/v/'+uid1)
    os.remove('poster.png')

#################################################################################################################################################################################################

@bot.message_handler(commands=['gpinfo'])
def welcome(m):
    cid = m.chat.id
    id = m.from_user.id
    ids = m.chat.id
    type = m.chat.type
    name = m.chat.title
    admin = bot.get_chat_administrators(cid)
    member = bot.get_chat_members_count(cid)
    user = bot.get_chat_member(m.chat.id, cid)
    if m.chat.type == 'group':
      bot.send_message(m.chat.id, "*Group Name* : *{}* \n*Group ID* : *{}* \n*Group Type* : *{}* \n*Admin* : *{}* \n*Member* : *{}* \n*Users* : *{}*".format(name,cid,type,admin,member,user), parse_mode='Markdown')

#################################################################################################################################################################################################

@bot.message_handler(commands=['setphone'])
def clac(m):
    text = m.text.replace("/setphone","")
    rediss.hset("user:phone","{}".format(m.from_user.id),"{}".format(text))
    bot.send_message(m.chat.id, "`This phone` *{}* `Seted For` {}".format(text,m.from_user.username), parse_mode="Markdown")

#################################################################################################################################################################################################
@bot.message_handler(commands=['myphone'])
def clac(m):
    number = rediss.hget("user:phone","{}".format(m.from_user.id))
    bot.send_contact(m.chat.id, phone_number="{}".format(number), first_name="{}".format(m.from_user.first_name))

#################################################################################################################################################################################################
@bot.message_handler(commands=['download'])
def image(m):
    text = m.text.split()[1]
    urllib.urlretrieve('{}'.format(text), 'image.jpg')
    bot.send_photo(m.chat.id, open('image.jpg'), caption="@CyberCH")
    
#################################################################################################################################################################################################
@bot.message_handler(commands=['download'])
def video(m):
    text = m.text.split()[1]
    urllib.urlretrieve('{}'.format(text), 'video.mp4')
    bot.send_video(m.chat.id, open('video.mp4'), caption="@CyberCH")
    
#################################################################################################################################################################################################
@bot.message_handler(commands=['download'])
def file(m):
    text = m.text.split()[1]
    urllib.urlretrieve('{}'.format(text), 'file.zip')
    bot.send_document(m.chat.id, open('file.zip'), caption="@CyberCH")
    
#################################################################################################################################################################################################
@bot.message_handler(commands=['download'])
def music(m):
    text = m.text.split()[1]
    urllib.urlretrieve('{}'.format(text), 'music.mp3')
    bot.send_document(m.chat.id, open('music.mp3'), caption="@CyberCH")
    
#################################################################################################################################################################################################
@bot.message_handler(commands=['download'])
def picture(m):
    text = m.text.split()[1]
    urllib.urlretrieve('{}'.format(text), 'picture.png')
    bot.send_photo(m.chat.id, open('picture.png'), caption="@CyberCH")
    
#################################################################################################################################################################################################
@bot.message_handler(commands=['download'])
def sticker(m):
    text = m.text.split()[1]
    urllib.urlretrieve('{}'.format(text), 'sticker.webp')
    bot.send_sticker(m.chat.id, open('sticker.webp'), caption="@CyberCH")
    
#################################################################################################################################################################################################
@bot.message_handler(commands=['download'])
def apk(m):
    text = m.text.split()[1]
    urllib.urlretrieve('{}'.format(text), 'apk.apk')
    bot.send_document(m.chat.id, open('apk.apk'), caption="@CyberCH")
    
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
