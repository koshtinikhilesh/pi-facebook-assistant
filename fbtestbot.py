"""
fbtestbot.py


# date: 23 june 2018
# author: Koshti Nikhilesh

This script is used to developed a Home Automation using Raspberry PI
   and Facebook messenger.
This home assistant is Artificial Intelligence integrated which
   uses natural language processing to extract inten
   from the user's actions.
"""

# important imports
from flask import Flask, request
import requests
import sys
import os
import json
import vlc
import datetime
import random
import pandas as pd
import pyowm
import netifaces as ni

import Credentials

# Raspberry PI GPIO imports
# import RPi.GPIO as GPIO
# GPIO.cleanup(21)
# GPIO.cleanup(12)
# The script as below using BCM GPIO 00..nn numbers
# GPIO.setmode(GPIO.BCM)
# Set relay pins as output
# GPIO.setup(7,   GPIO.OUT)


# Constant variables
images = []
videos = []
app = Flask(__name__)
APIKEY = "<API KEY>"
github_link = "<GITHUB LINK>"

valid_month = ['january', 'febuary', 'march',
               'april', 'may', 'june', 'july',
               'august', 'september', 'october',
               'november', 'december', 'jan', 'feb',
               'mar', 'apr', 'may', 'aug', 'sep',
               'sept', 'octo', 'nov', 'dec']

address = ni.ifaddresses('eth0')[2][0]['addr']
address = 'http://' + str(address) + '/'
# Used to play a single song on http server of current pc
c = vlc.MediaPlayer(address)


# **************** reminder module ***************
def reminder_details(current_greeting):
    """
    This methods is used
    e.g:-- good morning,  hey its morning,  good night.

    :param current_greeting: Greeting as per current time
    :return listq: Reminders for current date
    """
    # check for the csv files for reminder if any reminder is stored
    mess1 = None
    try:
        remindcsv = pd.read_csv('remind.csv')
    except Exception:
        mess = 'Invalid remind csv file'
        return mess, mess1

    # return reminder to the user every morning when asked
    if current_greeting[5:] == 'morning':
        todays_date = datetime.datetime.now().day
        todays_month = datetime.datetime.now().strftime('%B')
        todays_month = todays_month.lower()
        valid_date = list(remindcsv['date'])
        print str(valid_date)
        print todays_date
        print todays_month

        listq = []

        for j in range(len(valid_date)):
            if valid_date[j] == todays_date:
                # check for the current date
                dateindex = j
                print 'dateindex' + str(dateindex)
                month_value = remindcsv.loc[dateindex]['month']
                print month_value
                if month_value == todays_month:
                    # check for current month
                    qwe = ''
                    remind_message = (str(remindcsv.loc[dateindex]['reminder']))
                    # reminder message for current date and month
                    print remind_message

                    remind_time = remindcsv.loc[dateindex]['time_info_data']
                    print remind_time
                    remind_min = remindcsv.loc[dateindex]['time_info_min']
                    print remind_min
                    remind_min_data = remindcsv.loc[dateindex]['time_info_time']

                    qwe = str(remind_message) + ' at ' + str(remind_time) + '\
                     ' + str(remind_min) + ' ' + str(remind_min_data)
                    print qwe
                    listq.append(qwe)

        return listq

    else:
        return None


# **************************** weather module ****************************
def weatherinfo(placesinfo):
    """
    This method is used to give the weather information using pyown module
    of the city asked by the user.

    :param placesinfo: Name of the city asked by user
    :param mess: Message containing the weather information of the city
    """
    try:
        owm = pyowm.OWM(APIKEY)
        observation = owm.weather_at_place(placesinfo)
        w = observation.get_weather()
        temp_details = w.get_temperature('celsius')

        mess = placesinfo + '\n' + 'Weather informations are as folllow:--' + '\n' + str(w) + '\n' + \
              'Temerature details are:--   ' + str(temp_details['temp_max']) + ' celsius'
    except Exception:
        mess = 'Sorry no places available'
    return mess

##################################### for checking time format ##############################################################
def check_time(hours):
    """
    Check the time and return greetings accrodingly
    :param hours: current time
    :return greetings: Greetings based on time format
    """
    if 0 <= hours <= 12:
        return 'good morning'
    elif 13 <= hours <= 15:
        return 'good afternoon'
    elif 16 <= hours <= 18:
        return 'good evening'
    elif 19 <= hours <= 24:
        return 'good night'
    else:
        return 'Sorry'


####creating a localhost webpage and verfication of access_token from facebook ###

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args.get('hub.verify_token', '') == Credentials.VERIFY_TOKEN:
        return request.args.get('hub.challenge', 200)
    else:
        return 'Error,  wrong validation token'

################################# action for different input##############################################################################
start = 0
end = 0
mlplayer = vlc.MediaListPlayer()
pl = vlc.MediaPlayer()

def returnmessage(message, sender_id):
    """
    Act accordingly based on the action asked by user

    :param message: action asked by user
    :param sender_id: sender id
    :return message: text message to send
    :return message1: flag for image send
    """
    # flush the std output
    sys.stdout.flush()

    bkmessage = message
    message = message.split(' ')

    # contant value saved in the variables
    mess = 'Sorry ask again'
    mess1 = None
    message = [i.lower() for i in message]
    print "sender id is ", sender_id
    if 'song' in message:   # for playing song related to artist and album
        # check for the playlist for specific artist
        if 'artist' in message:

            # check if the song is playing
            # if player is in play status,  stop the song and play the new song based on artist playlist
            if mlplayer.is_playing():
                mlplayer.stop()
            # read the csv file in which the songs and artist and album names are saved
            try:
                df = pd.read_csv('songs.csv')
            except Exception:
                mess = 'invalid csv file'

                return mess, mess1
            try:
                df1 = df.set_index('artist')
                of_index = message.index('artist')
                artist_name = message[of_index + 1]
                mess = artist_name
                artist_namelist = list(df.loc[:]['artist'])

                # check for the artist name in list of artists
                if artist_name in artist_namelist:
                    # create a playlist of songs for speicific artist
                    artist_songs = []
                    artist_songlist = list(df1.get_value(artist_name, 'songs'))
                    for i in artist_songlist:
                        new1 = address + i
                        artist_songs.append(new1)

                    # python-vlc plugin used to play the song
                    medialist = vlc.MediaList(artist_songs)
                    mlplayer.set_media_list(medialist)
                    mlplayer.set_media_player(pl)
                    mlplayer.play()
                    mess = 'Playing list song'

                else:
                    mess = "Sorry, artist is not available"

            except Exception:
                mess = 'something went wrong'

        if 'album' in message:
            # check for the playlist for specific album
            if mlplayer.is_playing():
                mlplayer.stop()

            try:
                # read the csv file of songs
                df = pd.read_csv('songs.csv')
            except Exception:
                mess = 'invalid csv file'
                return mess, mess1

            try:
                df11 = df.set_index('album')
                of_index1 = message.index('album')
                album_name = message[of_index1 + 1]
                mess = album_name
                album_namelist = list(df.loc[:]['album'])
                mess = album_namelist[0]

                # check for album name in list
                if album_name in album_namelist:
                    # create a playlist for specific album name
                    album_songs = []
                    album_songlist = list(df11.get_value(album_name, 'songs'))
                    mess = 'in for loop'
                    mess = album_songlist[0]

                    for i in album_songlist:
                        new1 = address + i
                        album_songs.append(new1)

                    mess = album_songs[0]
                    medialist1 = vlc.MediaList(album_songs)
                    mlplayer.set_media_list(medialist1)
                    mlplayer.set_media_player(pl)
                    mlplayer.play()
                    mess = 'Playing album list song'

                else:
                    mess = "Sorry, album is not available"

            except Exception:
                mess = 'something wrong album is performed'

    elif 'next' in message:			# for next song
        if mlplayer.is_playing():
            # play the next song in playlist
            mlplayer.next()
            mess = 'playing the next song'

        else:
            mess = 'No song is playing yet'

    elif 'previous' in message:     # for previous song
        if mlplayer.is_playing():
            # play the previous song in playlist
            mlplayer.previous()
            mess = 'playing the previous song'

        else:
            mess = 'previous song is not performed'



    elif 'pause' in message:         # for pausing song
        if mlplayer.is_playing():
            # pause the current song
            mlplayer.pause()
            mess = 'pausing the song'

        else:
            mess = 'pausing song is not performed'

    elif 'title' in message or 'name' in message:   # title of song
        if mlplayer.is_playing():
            # get the title of the current song
            media = pl.get_media()
            title_song = media.get_meta(vlc.Meta.Title)
            mess = title_song

        else:
            mess = 'no song is played yet'

    elif 'play' in message:  # play the song
        if mlplayer.is_playing():
            mess = 'already playing'

        else:
            mlplayer.play()
            mess = 'Playing song'

    elif 'stop' in message: # stop the song
        if mlplayer.is_playing():
            mlplayer.stop()
            mess = 'Stopping the recent song'

        else:
            mess = 'No song is played yet'

    elif 'volume' in message:  # increase or decrease the volume of song
        if 'increase' in message:
            try:
                if mlplayer.is_playing():
                    # increase the volume of song by 10
                    print str(pl.audio_get_volume())
                    mess = '\nCurrent volume is  ' + str(pl.audio_get_volume())
                    volume = pl.audio_get_volume() + 10
                    print volume
                    if volume > 100:
                        mess = mess + '\n\nWarning:--  Volume above 100 may cause problem\n\n'
                    pl.audio_set_volume(volume)
                    mess = mess + '\nVolume increased to value  ' + str(volume)

            except Exception:
                mess = mess + '\n  Error:--- Increased volume is not performed\n'

        elif 'decrease' in message:
            try:
                if mlplayer.is_playing():
                    # decrease the volume of song by 10
                    mess = '\nCurrent volume is  ' + str(pl.audio_get_volume())
                    volume = pl.audio_get_volume() - 10
                    if volume > 100:
                        mess = mess + '\n\nWarning:--  Volume above 100 may cause problem\n\n'
                pl.audio_set_volume(volume)
                mess = mess + '\nVolume decreased to value  ' + str(volume)
            except Exception:
                mess = mess +  '\n   Error:--- Decreased volume is not performed\n'


    elif 'change' in message:  # change the volume of song to any number
        try:
            to_index = message.index('to')
            if mlplayer.is_playing():
                data_vol_index = int(message[to_index +1])
                print data_vol_index
                pl.audio_set_volume(data_vol_index)

                # warn user for max volume
                if data_vol_index > 100:
                    mess = "Warning:-- Volume above 100 may cause problem \
                            ..\n\n Changed the volume to %d " %(data_vol_index)
        except Exception:
            print "Error:-- Changing volume cannot ber performed"


    elif 'time' in message and len(message) < 5:   # for asking time related info.
        mess = datetime.datetime.now().strftime('%I %M  %p %d %B %Y %A ')


    elif 'morning' in message  or 'afternoon' in message  or 'night' in message or 'evening' in message or 'noon' in message:  # greeting
        # Check for reminders for the user
        current_hour = datetime.datetime.now().hour
        current_greeting = check_time(current_hour)

        # return the current greeting to the user
        mess = 'Hey its ' + current_greeting[5:] + ' ,  ' + current_greeting

        # check for reminders for the current day
        reminders = reminder_details(current_greeting)
        if reminders:
            mess = 'Your reminder for todays is :--\n'

        for reminder in reminders:
            mess = mess + ' ' + reminder + '\n'

        else:
            mess = 'No reminder for today'


    elif 'hey' in message or 'hi' in message or 'hello' in message: # greeting to user
        # regular greetings to the user
        greet_message = random.choice(['Hi,  good to see you', 'Hello,  good to see you', 'Hey,   nice to see you'])
        mess = greet_message + ' ' + u'\U0001f600'.encode('utf8')

    elif 'die' in message:		# rolling a die
        # roll a die and generate the number between 0 and 6
        mess = random.randint(0, 7)

    elif 'flip'in message and 'coin' in message: # flip a coin
        mess = u'\U0001F604'

    elif 'you' in message or 'your' in message or 'yourself' in message or 'yourselves' in message:  # assistant info
        # get the assistant informations
        if 'are' in message  or 'know' in message or 'explain' in message or 'name' in message:
            mess = 'I am your Pi Assistant, How can I help You'

    elif 'date' in message and len(message) <= 5:

        if 'tomorrow' in message:
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            mess = tomorrow.strftime("%B %d %Y %A")

        elif 'yesterday' in message:
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            mess = yesterday.strftime("%B %d %Y %A")

        else:
            today = datetime.date.today()
            mess = today.strftime("%B %d %Y %A")

    elif 'weather' in message: # weather informations
        # check for weather for any city using pyown weather spi
        placesinfo = bkmessage[11:].upper()
        mess = weatherinfo(placesinfo)

    elif 'today' in message and 'reminder' in message or 'todays' in message: # check for greetings
        # check for greetings
        dateq = 'good morning'
        reminders = greetings(dateq)
        if reminders:
            mess = 'Your reminder for todays is :--\n'
            for reminder in reminders:
                mess = mess + ' ' + reminder + '\n'
        else:
            mess = 'No reminder for today'

    elif 'camera' in message: # took a picture though camera
        try:
            # capture a image and upload it to cloud/git
            images_name = datetime.datetime.now().strftime('%I%M%S%p')
            images_name = images_name + '.jpeg'

            # command to capture image
            cmd = 'fswebcam -r 1920x1080 --set brightness=50%  '
            cmd = cmd + images_name
            print 'cmd is ' + str(cmd)
            os.system(cmd)

            # upload pic to git
            os.system('git add -A')
            os.system("git commit -m 'latest comit' ")
            os.system('git push  -f origin master')

            imageslink = github_link + images_name +'?raw=true'
            print imageslink
            mess = imageslink
            images.append(mess)
            mess = 'Images is captured\n\n The Captured image is at location:--' + imageslink

        except Exception:
            mess = 'no image available'


    elif 'capture' in message:
        # capturing a images
        if 'image' in message:
            lastimages = images[-1]
            mess = lastimages
        mess1 = 'images'

    elif 'video' in message: # capturing a videos
        try:
            if len(videos) >= 1:

                lastvideo = videos[-1]
                mess = 'The Videos is captured\n and locations is at:-- \n\n '
                os.system('git add -A')
                os.system('git commit -m "videos commit" ')
                os.system('git push origin master')
                mess = lastvideo
            else:
                mess = 'Sorry, no video is captured'
        except Exception:
            mess = 'Sorry video is not available'


    elif 'video' in message:
        try:
            # capture a videos
            s = datetime.datetime.now().strftime('%I%M%S%p')
            s = s + '.mp4'
            cmd = 'ffmpeg -t 10  -f v4l2 -framerate 25 -video_size 640x800 -i /dev/video0   '
            cmd = cmd + s
            print 'cmd is ' + str(cmd)
            os.system(cmd)

            mess = ' Videos of 10 second is captured\n '
            imageslink1 = github_link + s +'?raw=true'
            videos.append(imageslink1)

        except Exception:
            mess = 'no video available'

    elif 'list' in message: #  get a list of artist and album
        try:
            df1 = pd.read_csv('songs.csv')
        except Exception:
            mess = 'invalid csv file '
            return mess, mess1

        if 'artist' in message:
            artistlistname = set(list(df1.loc[:]['artist']))
            l1 = ''
            for j in artistlistname:
                l1 = l1 + j + '\n'
            mess = 'The available artist  are:--\n' + l1
            print artistlistname
        elif 'album' in message:
            albumlistname = set(list(df1.loc[:]['album']))
            l1 = ''
            for j in albumlistname:
                l1 = l1 + j + '\n'
            mess = 'The available album  are:--\n' + l1
            print albumlistname

    elif 'lights' in message or 'light' in message:  # light on/off
        if 'off' in message:
           # GPIO.output(26,  GPIO.LOW)
            mess = 'Lights off'
        elif 'on' in message:
           # GPIO.output(26,  GPIO.HIGH)
            mess = 'Lights on'


        elif 'fan' in message:
            if 'off' in message:
            #    GPIO.output(12,  GPIO.LOW)
                mess = 'fan off'
            elif 'on' in message:
             #   GPIO.output(12,  GPIO.HIGH)
                mess = 'fan on'

    elif 'remind' in message and 'me' in message:  # remind the messsage for user
        if not os.path.exists('remind.csv'):
            file('remind.csv', 'w').close()
            fdremind = pd.DataFrame(columns=['date', 'month', 'time_info_data',
                                   'time_info_min', 'time_info_time', 'reminder'])
            fdremind.to_csv('remind.csv', index=False)

        try:
            remindcsv = pd.read_csv('remind.csv')
        except Exception:
            mess = 'Invalid remind csv file'
            return mess, mess1


###########################   remind module   ###########################################################
#remind me <message_data> at  4 pm dec 31
#remind me <message_data> at 4 pm dec
#remind me <message_data> at 4 dec 31
#remind me <message_data> at 4 pm 31


    elif 'remind' in message and 'me' in message:
        if not os.path.exists('remind.csv'):
            file('remind.csv', 'w').close()
            fdremind = pd.DataFrame(columns=['date', 'month', 'time_info_data',
                                             'time_info_min', 'time_info_time', 'reminder'])
            fdremind.to_csv('remind.csv', index=False)

        try:
            remindcsv = pd.read_csv('remind.csv')
        except Exception:
            mess = 'Invalid remind csv file'
            return mess, mess1


        if len(message) == 2:
            mess = 'Invalid format\n\nremind me < message data> at < time >  < date>        \n'
            return mess, mess1

        elif 'at' in message:
            start = message.index('me')
            stop = message.index('at')
            if (stop - start) <= 1:
                mess = 'No message  received'
            else:
                timedata_min = 0
                count = 0
                message_data = message[start+1:stop]
                message1 = message[stop+1:len(message)]
                print message1
                print len(message1)
                message2 = filter(None, message1)
                print message2
                if len(message2) == 4: # remidn me for call at dec 12 4 pm
                    for i in message2:
                        if i in valid_month:
                            print i
                            month = i
                            monthindex = message.index(i)
                            count = 1
                    if count == 0:
                        mess = 'Invalid month entered'
                        return mess, mess1
                    datemonth = message[monthindex - 1]
                    try:
                        date1 = int(datemonth)
                        # print date1
                        mess = date1
                        if date1 not in range(0, 32):
                            mess = 'Error:- Invalid Date entered'
                            return mess, mess1
                    except Exception:
                        try:
                            date1 = int(message[monthindex + 1])
                            # print date1
                            mess = date1
                            if date1 not in range(0, 32):
                                mess = 'Error:-- invalid date entered'
                                return mess, mess1
                        except Exception:
                            mess = '\nMonth is missing.please try again\n'
                            return mess, mess1

                    print 'date is {date}and month is {month}'.format(date=date1, month=month)

                    if 'am' in message2:
                        amindex = message.index('am')
                        v_time = message[amindex]
                        amdata = message[amindex - 1]
                        try:
                            timedata = int(amdata)
                            print timedata
                        except Exception:
                            try:
                                timedata = int(message[amindex + 1])
                                print timedata
                            except Exception:
                                print 'Time is missing'
                                mess = 'Time is missing'
                                return mess, mess1
                    elif 'pm' in message2:
                        pmindex = message.index('pm')
                        v_time = message[pmindex]
                        pmdata = message[pmindex - 1]
                        try:
                            timedata = int(pmdata)
                            #mess = mess + pmdata1
                        except Exception:
                            try:
                                timedata = int(message[pmindex + 1])

                            except Exception:
                                print 'Time is missing'
                                mess = 'Time is missing'
                                return mess, mess1
                    else:
                        mess = 'Invalid time format'
                        return mess, mess1
                    mess = 'Message reminded for {date}{month}'.format(date=date1, month=month)

                    if timedata not in range(0, 13) or timedata_min not in range(0, 61):
                        mess = 'Invalid time and month'
                        return mess, mess1

                    else:         # remind me for call a freind at 4 30 pm dec 12
                        for i in message2:
                            if i in valid_month:
                                print i
                                month = i
                                monthindex = message.index(i)
                                count = 1
                        if count == 0:
                            mess = 'Invalid month entered'
                            return mess, mess1
                        datemonth = message[monthindex - 1]
                        try:
                            date1 = int(datemonth)
                            # print date1
                            mess = date1
                            if date1 not in range(0, 32):
                                mess = 'Error:- Invalid Date entered'
                                return mess, mess1
                        except Exception:
                            try:
                                date1 = int(message[monthindex + 1])
                                # print date1
                                mess = date1
                                if date1 not in range(0, 32):
                                    mess = 'Error:-- invalid date entered'
                                    return mess, mess1
                            except Exception:
                                mess = '\nMonth is missing.please try again\n'
                                return mess, mess1
                            print 'datetttttttttt is {date}and month is {month}'.format(date=date1, month=month)


                            if 'am' in message2:
                                amindex = message.index('am')
                                v_time = message[amindex]
                                amdata = message[amindex - 1]
                                print 'amdata is {am}'.format(am=amdata)
                                try:
                                    timedata_min = int(amdata)
                                    timedata = int(message[amindex - 2])
                                    print timedata
                                    print timedata_min
                                except Exception:
                                    try:
                                        timedata = int(message[amindex + 1])
                                        timedata_min = int(message[amindex + 2])
                                        print timedata
                                        print timedata_min
                                    except Exception:
                                        print 'Time is missing'
                                        mess = 'Time is missing'
                                        return mess, mess1
                            elif 'pm' in message2:
                                pmindex = message.index('pm')
                                v_time = message[pmindex]
                                pmdata = message[pmindex - 1]

                                try:

                                    timedata = int(message[pmindex-2])
                                    print timedata
                                    print timedata_min
                                    #			mess = mess + pmdata1
                                except Exception:
                                    try:
                                        timedata = int(message[pmindex + 1])
                                        timedata_min = int(message[pmindex + 2])

                                    except Exception:
                                        print 'Time is missing'
                                        mess = 'Time is missing'
                                        return mess, mess1
                            else:
                                mess = 'Invalid time format'
                                return mess, mess1
                            mess = 'Message reminded for {date}{month}'.format(date=date1, month=month)
                            if timedata not in range(0, 13) or timedata_min not in range(0, 61):
                                mess = 'Invalid time and month'
                                return mess, mess1

                        remindcsv.loc[len(remindcsv) + 1] = [date1, month, timedata, timedata_min, v_time, message_data]
                        remindcsv.to_csv('remind.csv', index=False)

    return mess, mess1

 ########################## POST request handler function ##################################################################
@app.route('/', methods=['POST'])
def handle_messages():
    """
    Main method which is used to act when POST requests to the flask server
    """
    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                try:
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        recipient_id = messaging_event["recipient"]["id"]
                        print "receipeint id is ", recipient_id
                        message_text = messaging_event["message"]["text"]
                        message_text, message_text1 = returnmessage(message_text, sender_id)
                        send_message(sender_id, message_text, message_text1)
                except Exception:
                    try:
                        urlqq = 'https://www.dropbox.com/s/fmdm0559r55ixtc/IMG_20170227_114753227.jpg?dl=0?raw=true'

                        send_message(sender_id, urlqq, message_text1)
                    except Exception:
                        urlqq = 'Sorry no attachment'
                        message_text1 = None
                        send_message(sender_id, urlqq, message_text1)

    return "ok", 200



##################sending message to facebook page using graph api #########################################################

def send_message(recipient_id, message_text, datay):
    """
    THis method is used to send structured data back to facebook page of user

    :param recipient_id: id of receiver
    :param message_text: json formatted data to be send
    :param datay: flag for images data
    """
    images_data1 = datay
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))


    params = {
        "access_token": Credentials.PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })

    data1 = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
        "attachment": {
        "type": "image",
        "payload": {
        "url": message_text

      }
    }
        }
    })


    if images_data1 == None:
        send_requests = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    else:
        send_requests = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data1)
    log("status code is {status}".format(status=send_requests.status_code))
    log(send_requests.status_code)
    if send_requests.status_code != 200:
        log(send_requests.status_code)
    log(send_requests.text)

############# for printing message into stdout in terminal ####

def log(message):
    """
    simple wrapper for logging to stdout on heroku
    :param message:-- message to log
    :return None
    """
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=PORT)
