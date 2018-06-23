from flask import Flask, request
import requests,sys,os,json,vlc,datetime,random
import pandas as pd
from Credentials import *
import pyowm
import sys,time
import netifaces as ni
#import RPi.GPIO as GPIO
#GPIO.cleanup(21)
#GPIO.cleanup(12)
from time import sleep
# The script as below using BCM GPIO 00..nn numbers
#GPIO.setmode(GPIO.BCM)
# Set relay pins as output
#GPIO.setup(7, GPIO.OUT)

a = 0
images = []
videos = []
app = Flask(__name__)
APIKEY = '8a7bc3e088eacc7f179bfa3561815da2'
github_link = 'https://github.com/koshtinikhilesh/hello_world/blob/master/'

valid_month = ['january','febuary','march','april','may','june','july','august','september','october','november','december','jan','feb','mar','apr','may','aug','sep','sept','octo','nov','dec']

'''

 fswebcam -r 1920x1080 --set brightness=50% images.jpg
ffmpeg -t 20  -f v4l2 -framerate 25 -video_size 640x800 -i /dev/video0 output1.mkv

ip addr show eth0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1

    ip addr show eth0 shows information about eth0
    grep "inet\b" only shows the line that has the IPv4 address (if you wanted the IPv6 address, change it to "inet6\b")
    awk '{print $2}' prints on the second field, which has the ipaddress/mask, example 172.20.20.15/25
    cut -d/ -f1 only takes the IP address portion.


espeak -v mb-en1 "hey,nice to see you" -a 250
{u'entry': [{u'messaging': [{u'delivery': {u'mids': [u'mid.1486981403176:35fddc5141'], u'seq': 0, u'watermark': 1486981403176}, u'timestamp': 1486981403619, u'recipient': {u'id': u'255389034497244'}, u'sender': {u'id': u'1655714677778768'}}], u'id': u'255389034497244', u'time': 1486981403621}], u'object': u'page'}
127.0.0.1 - - [13/Feb/2017 15:53:25] "POST / HTTP/1.1" 200 -


{u'entry': [{u'messaging': [{u'timestamp': 1487139962833, u'message': {u'attachments': [{u'type': u'image', u'payload': {u'url': u'https://scontent.xx.fbcdn.net/v/t39.1997-6/851557_369239266556155_759568595_n.png?_nc_ad=z-m&oh=85e24066ebe64f04d457b242e22e7054&oe=5939B5DC', u'sticker_id': 369239263222822}}], u'mid': u'mid.1487139962833:e74149e302', u'seq': 5113, u'sticker_id': 369239263222822}, u'recipient': {u'id': u'255389034497244'}, u'sender': {u'id': u'1655714677778768'}}], u'id': u'255389034497244', u'time': 1487143026155}], u'object': u'page'}

{u'entry': [{u'messaging': [{u'timestamp': 1487152691073, u'message': {u'text': u'Next song', u'mid': u'mid.1487152691073:be2a4b7483', u'seq': 5257}, u'recipient': {u'id': u'255389034497244'}, u'sender': {u'id': u'1655714677778768'}}], u'id': u'255389034497244', u'time': 1487152691142}], u'object': u'page'}
sending message to 1655714677778768: playing the next song
{"recipient_id":"1655714677778768","message_id":"mid.1487152693070:9547bd7282"}
127.0.0.1 - - [15/Feb/2017 15:28:13] "POST / HTTP/1.1" 200 -
{u'entry': [{u'messaging': [{u'timestamp': 1487152693070, u'message': {u'text': u'playing the next song', u'is_echo': True, u'app_id': 1603566436336994, u'seq': 5258, u'mid': u'mid.1487152693070:9547bd7282'}, u'recipient': {u'id': u'1655714677778768'}, u'sender': {u'id': u'255389034497244'}}], u'id': u'255389034497244', u'time': 1487152693475}], u'object': u'page'}
sending message to 255389034497244: playing the next song


Verification Token - A secret value that will be sent to your bot, in order to verify the request is coming from Facebook.

incase of emoji message:--

{u'entry': [{u'messaging': [{u'timestamp': 1487239667910, u'message': {u'text': u'\U0001f600', u'mid': u'mid.1487239667910:1f6765e107', u'seq': 6360}, u'recipient': {u'id': u'255389034497244'}, u'sender': {u'id': u'1655714677778768'}}], u'id': u'255389034497244', u'time': 1487239667971}], u'object': u'page'}
sending message to 1655714677778768: something images is received

'''
address = ni.ifaddresses('eth0')[2][0]['addr']
address = 'http://' + str(address) + '/'
songs_path = address
songs_path = songs_path
c = vlc.MediaPlayer('http://10.107.3.134/Afghan%20Jalebi%20-%20Pritam%20Feat.%20Nakash%20Aziz%20-%20MTV%20Unplugged%20Season%205(mp3rule.com).mp3')


'''
def vlcfunctions(songlist):
    pl = vlc.MediaPlayer() 
    medialist = vlc.MediaList(songlist)
    mlplayer.set_media_list(medialist)
    mlplayer.set_media_player(pl)    
    return mlplayer,pl
'''

def remind_function(dateq):

    try:
	remindcsv = pd.read_csv('remind.csv')
    except:
	mess = 'Invalid remind csv file'
	return mess,mess1
    list1 = []
    print dateq

    if dateq[5:] == 'morning':

   

	todays_date = datetime.datetime.now().day
	todays_month = datetime.datetime.now().strftime('%B')
	todays_month = todays_month.lower()
	valid_date = list(remindcsv['date'])	
	print str(valid_date)
	print todays_date
	print todays_month
	listq = []
	for j in range(len(valid_date)):
            print 'jjjj is ' + str(j)
	    if valid_date[j] == todays_date:
	 
	        dateindex = j
	        print 'dateindex' + str(dateindex)
	        month_value = remindcsv.loc[dateindex]['month']
	            
	        print month_value
		if month_value == todays_month:
		    qwe = ''
		    remind_message = (str(remindcsv.loc[dateindex]['reminder']))
		    #remind_message= remind_message.split(',')
		    print remind_message
 
		    remind_time = remindcsv.loc[dateindex]['time_info_data']
		    print remind_time		            
		    remind_min = remindcsv.loc[dateindex]['time_info_min']
		    print remind_min
		    remind_min_data = remindcsv.loc[dateindex]['time_info_time']

		    qwe =  str(remind_message) + ' at ' + str(remind_time) + ' ' + str(remind_min) + ' ' + str(remind_min_data)
		    print qwe
		    listq.append(qwe) 
			
        print listq 
	return listq  


    else:
	return None







def weatherinfo(placesinfo):
    try:
        owm = pyowm.OWM(APIKEY)
	observation = owm.weather_at_place(placesinfo)
	w = observation.get_weather()
	temp_details = w.get_temperature('celsius')

	mess = placesinfo + '\n' +  'Weather informations are as folllow:--'  + '\n' + str(w) + '\n' + 'Temerature details are:--   ' + str(temp_details['temp_max']) + ' celsius' 
	    

    except:
        mess = 'Sorry no places available'  
    return mess  
	    

##################################### for checking time format ##############################################################
def check_date(hours):
    if 0<=hours<=12:
        return 'good morning'
    elif 13 <= hours <= 15:
	return 'good afternoon'
    elif 16 <= hours <= 18:
	return 'good evening'
    elif 19 <= hours <= 24:
	return 'good night'
    else:
	return 'Sorry'



##########################creating a localhost webpageand verfication of access_token from facebook ############################

@app.route('/', methods=['GET'])
def handle_verification():
    if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
        return request.args.get('hub.challenge', 200)
    else:
        return 'Error, wrong validation token'

################################# action for different input##############################################################################
start = 0
end = 0
mlplayer = vlc.MediaListPlayer()
pl = vlc.MediaPlayer() 
def returnmessage(message,sender_id):
    sys.stdout.flush()
   
    bkmessage = message
    recess_id = sender_id
    message = message.split(' ')
    mess = 'Sorry ask again'
    mess1 = None
    message = [i.lower() for i in message]


    if 'song' in message:   # for playing song related to artist and album

        if 'artist' in message:
            if mlplayer.is_playing():
                mlplayer.stop()
            #df1 = df.set_index('artist')
	    try:
	        df = pd.read_csv('songs.csv')
            except:
		mess = 'invalid csv file'
		
		return mess,mess1
	    try:
                df1 = df.set_index('artist')
	        of_index = message.index('artist')
	        artist_name = message[of_index + 1]
	        mess = artist_name
                artist_namelist = list(df.loc[:]['artist'])
	        if artist_name in  artist_namelist:
	            artist_songs = []
		    artist_songlist = list(df1.get_value(artist_name,'songs'))
		    for i in artist_songlist:
		        new1 = songs_path + i
		        artist_songs.append(new1)
                
			
                
                    medialist = vlc.MediaList(artist_songs)
                    mlplayer.set_media_list(medialist)
                    mlplayer.set_media_player(pl)

	            mlplayer.play()
		    mess = 'Playing list song'
		    
		else:
		    mess = "Sorry,artist is not available"
		    

	    except:
	        mess = 'something wrong is performed'
		



	
        if 'album' in message:
            if mlplayer.is_playing():
                mlplayer.stop()
            
	    try:
	        df = pd.read_csv('songs.csv')
            except:
		mess = 'invalid csv file'
		
		return mess,mess1
	    try:
                df11 = df.set_index('album')
	        of_index1 = message.index('album')
	        album_name = message[of_index1 + 1]
	        mess = album_name
                album_namelist = list(df.loc[:]['album'])
		mess = album_namelist[0]
	        if album_name in  album_namelist:
	            album_songs = []
		    album_songlist = list(df11.get_value(album_name,'songs'))
		    mess = 'in for loop'
		    mess = album_songlist[0]
		    for i in album_songlist:
		        new1 = songs_path + i
		        album_songs.append(new1)
                    mess = album_songs[0]
                
			
                
                    medialist1 = vlc.MediaList(album_songs)
                    mlplayer.set_media_list(medialist1)
                    mlplayer.set_media_player(pl)

	            mlplayer.play()
		    mess = 'Playing album list song'
		    
		else:
		    mess = "Sorry,album is not available"
		    
	    except:
	        mess = 'something wrong album is performed'
		


        elif 'next' in message:			# for next song
	    if mlplayer.is_playing():
                mlplayer.next()
		mess = 'playing the next song'
		
	    else:
	        mess = 'No song is playing yet'
		


	elif 'previous' in message:               # for previous song
	    if mlplayer.is_playing():
                mlplayer.previous()
		mess = 'playing the previous song'
		
	    else:
		mess = 'previous song is not performed'   
		


	elif 'pause' in message:               # for pausing song
	    if mlplayer.is_playing():
	        mlplayer.pause()
		mess = 'pausing the song'
		
	    else:
	        mess = 'pausing song is not performed'
		
	elif 'title' in message or 'name' in message:   # title of song
	    if mlplayer.is_playing():
	        media = pl.get_media()
		title_song = media.get_meta(vlc.Meta.Title)
		mess = title_song
		
	    else:
		mess = 'no song is played yet'
		
	

    if 'play' in message:
        if mlplayer.is_playing():
            mess = 'already playing'
	    
	else:
	    mlplayer.play()
	    mess = 'Playing song'
	    
    elif 'stop' in message:
	if mlplayer.is_playing():
            mlplayer.stop()
	    mess = 'Stopping the recent song'
	    
	else:
	    mess = 'No song is played yet'
    
    elif 'volume' in message:
        if 'increase' in message:
	    try: 
	        if mlplayer.is_playing():
                 		 
		
		    print str(pl.audio_get_volume())
		    mess = '\nCurrent volume is  ' + str(pl.audio_get_volume())
		    volume = pl.audio_get_volume() + 10
		    print volume
		    if volume > 100:
		        mess = mess + '\n\nWarning:--  Volume above 100 may cause problem\n\n'
		    pl.audio_set_volume(volume)
		    mess = mess + '\nVolume increased to value  ' + str(volume)

	    except:
	        mess = mess +  '\n  Error:--- Increased volume is not performed\n'

	elif 'decrease' in message:
	    try:
	        if mlplayer.is_playing():

	            mess = '\nCurrent volume is  ' + str(pl.audio_get_volume())
		    volume = pl.audio_get_volume() - 10
		    if volume > 100:
		        mess = mess + '\n\nWarning:--  Volume above 100 may cause problem\n\n'
		    pl.audio_set_volume(volume)
		    mess = mess + '\nVolume decreased to value  ' + str(volume)
	    except:
	        mess = mess +  '\n   Error:--- Decreased volume is not performed\n' 


	elif 'change' in message:
	    try:
	        to_index = message.index('to')
	    	if mlplayer.is_playing():
		    data_vol_index = int(message[to_index +1])
		    print data_vol_index
		    pl.audio_set_volume(data_vol_index)
	            if data_vol_index > 100:
		        mess =  "Warning:-- Volume above 100 may cause problem..\n\n Changed the volume to %d " %(data_vol_index)
	    except:
	        print "Error:-- Changing volume cannot ber performed"

	   
    elif 'time' in message and len(message) < 5:                        # for asking time related info.
        mess = datetime.datetime.now().strftime('%I %M  %p %d %B %Y %A ')
	

    elif 'morning' in message  or 'afternoon' in message  or 'night' in message or 'evening' in message or 'noon' in message:  # greeting 
        date = datetime.datetime.now().hour
        dateq = check_date(date)
	list5 = remind_function(dateq)
	mess =  'Hey its ' + dateq[5:] + ' , ' + dateq 


        if list5:
	    mess = 'Your reminder for todays is :--\n'
	    for k in list5:
	        mess = mess + ' ' + k + '\n'
	else:
	    mess = 'No reminder for today'
	
        #print dataq

        
	print str(dateq)
    elif 'hey' in message or 'hi' in message or 'hello' in message:
        messig = random.choice(['Hi, good to see you','Hello, good to see you','Hey,  nice to see you'])
	mess = messig + ' ' + u'\U0001f600'.encode('utf8')
    elif 'die' in message:		# rolling a die
	    mess = random.randint(0,7)
	    
	    
    elif 'flip'in message and 'coin' in message: # flip a coin
	    #mess = random.choice(['head','tail'])
             mess =  u'\U0001F604'
	    
    elif  'you' in message or 'your' in message or 'yourself' in message or 'yourselves' in message:

        if 'are' in message  or 'know' in message or 'explain' in message or 'name' in message:
	    mess = 'I am your Pi Assistant,How can I help You'
	   
    elif 'date' in message and len(message) <= 5:
            if 'tomorrow' in message:
                tomorrow = datetime.date.today() + datetime.timedelta(days=1)
		mess =  tomorrow.strftime("%B %d %Y %A")
		
            elif 'yesterday' in message:
                yesterday = datetime.date.today() - datetime.timedelta(days=1)
		mess = yesterday.strftime("%B %d %Y %A")
		

	    
	    else:
                today = datetime.date.today()
		mess =  today.strftime("%B %d %Y %A")
		
    
    elif 'weather' in message:
######################### pyowm   weather map api for weather api ###############################


	placesinfo = bkmessage[11:].upper()
	mess = weatherinfo(placesinfo)
	'''
	try:
            owm = pyowm.OWM(APIKEY)
	    observation = owm.weather_at_place(placesinfo)
	    w = observation.get_weather()
	    temp_details = w.get_temperature('celsius')

	    mess = placesinfo + '\n' +  'Weather informations are as folllow:--'  + '\n' + str(w) + '\n' + 'Temerature details are:--   ' + str(temp_details['temp_max']) + ' celsius' 
	    

   	 
	except:
	    mess = 'Sorry no places available'    
	   ''' 
#    elif 'images' in message:
    elif 'today' in message and 'reminder' in message or 'todays' in message:
        dateq = 'good morning'
        list5 = remind_function(dateq)
        print list5
        if list5:
            mess = 'Your reminder for todays is :--\n'
	    for k in list5:
	        mess = mess + ' ' + k + '\n'
	else:
	    mess = 'No reminder for today'
	







    elif 'camera' in message:
	try:
	    start = int(datetime.datetime.now().strftime('%S'))
  	    s = datetime.datetime.now().strftime('%I%M%S%p')
	    s = s + '.jpeg'
	#s = 'downloads.jpeg'
	    script_commands = 'sh script2.sh'
	    script_commands = script_commands + ' ' + s 
	    cmd = 'fswebcam -r 1920x1080 --set brightness=50%  '
	    cmd = cmd + s
	    print 'cmd is ' + str( cmd)
	    os.system(cmd)
	    os.system('git add -A')
	    os.system("git commit -m 'latest comit' ")
	    
	    os.system('git push  -f origin master')
	   # os.system(script_commands)

	    imageslink = github_link + s +'?raw=true'
	    print imageslink
            mess = imageslink
	#mess = 'https://github.com/koshtinikhilesh/hello_world/blob/master/downloads.jpeg?raw=true'
	    images.append(mess)
            mess = 'Images is captured\n\n The Captured image is at location:--' + imageslink
        
	    
	   # mess1 = 'images'
	except:
	    mess = 'no image available'


    elif 'capture' in message:
        if 'image' in message:
            lastimages = images[-1]
            mess = lastimages
	    mess1 = 'images'

	elif 'video' in message:
	    try:
	        if len(videos) >= 1:
                
	            lastvideo = videos[-1]
	            mess = 'The Videos is captured\n and locations is at:-- \n\n '
	            os.system('git add -A')
	            os.system('git commit -m "videos commit" ')
	            os.system('git push origin master')
                    mess = lastvideo
                else:
	            mess = 'Sorry,no video is captured'
	    except:
	        mess = 'Sorry video is not available'


    elif 'video' in message:
	try:
	
	    start = int(datetime.datetime.now().strftime('%S'))
  	    s = datetime.datetime.now().strftime('%I%M%S%p')
	    s = s + '.mp4'
	    
	    cmd = 'ffmpeg -t 10  -f v4l2 -framerate 25 -video_size 640x800 -i /dev/video0   '
	    cmd = cmd + s
	    print 'cmd is ' + str( cmd)
	    os.system(cmd)
	    
            mess = ' Videos of 10 second is captured\n '
	    imageslink1 = github_link + s +'?raw=true'
            videos.append(imageslink1)
	   
	except:
	    mess = 'no video available'

    elif 'list' in message:
	try:
	    df1 = pd.read_csv('songs.csv')
	except:
	    mess = 'invalid csv file '
	    return mess,mess1
	
        if 'artist' in message:
	    artistlistname = set(list(df1.loc[:]['artist']))
	    l1 = ''
	    for j in artistlistname:
	        l1 = l1 + j + '\n'
	    mess = 'The available artist  are:--\n'  + l1
	    print artistlistname 
	elif 'album' in message:
	    albumlistname = set(list(df1.loc[:]['album']))
	    l1 = ''
	    for j in albumlistname:
	        l1 = l1 + j + '\n'
	    mess = 'The available album  are:--\n'  + l1
	    print albumlistname

    elif 'lights' in message or 'light' in message:
        if 'off' in message:
	    GPIO.output(26, GPIO.LOW)
	    mess = 'Lights off'
            
	elif 'on' in message:
	    GPIO.output(26, GPIO.HIGH)
	    mess = 'Lights on'

    
    elif 'fan' in message :
        if 'off' in message:
	    GPIO.output(12, GPIO.LOW)
	    mess = 'fan off'
	elif 'on' in message:
	    GPIO.output(12, GPIO.HIGH)
	    mess = 'fan on'



#    elif 'lights' in message or 'light' in message:
 #       if 'off' in message:
#	    GPIO.output(7, GPIO.LOW)
#	    mess = 'Lights off'
#	elif 'on' in message:
#	    GPIO.output(7, GPIO.HIGH)
#	    mess = 'Lights on'

###########################   remind module   ###########################################################
#remind me <message_data> at  4 pm dec 31
#remind me <message_data> at 4 pm dec
#remind me <message_data> at 4 dec 31
#remind me <message_data> at 4 pm 31


    elif 'remind' in message and 'me' in message:
        if not os.path.exists('remind.csv'):
	    file('remind.csv','w').close()
	    fdremind = pd.DataFrame(columns = ['date','month','time_info_data','time_info_min','time_info_time','reminder'])
	    fdremind.to_csv('remind.csv',index = False)

	try:
	    remindcsv = pd.read_csv('remind.csv')
	except:
	    mess = 'Invalid remind csv file'
	    return mess,mess1


#    elif 'lights' in message or 'light' in message:
 #       if 'off' in message:
#	    GPIO.output(7, GPIO.LOW)
#	    mess = 'Lights off'
#	elif 'on' in message:
#	    GPIO.output(7, GPIO.HIGH)
#	    mess = 'Lights on'

###########################   remind module   ###########################################################
#remind me <message_data> at  4 pm dec 31
#remind me <message_data> at 4 pm dec
#remind me <message_data> at 4 dec 31
#remind me <message_data> at 4 pm 31


    elif 'remind' in message and 'me' in message:
        if not os.path.exists('remind.csv'):
	    file('remind.csv','w').close()
	    fdremind = pd.DataFrame(columns = ['date','month','time_info_data','time_info_min','time_info_time','reminder'])
	    fdremind.to_csv('remind.csv',index = False)

	try:
	    remindcsv = pd.read_csv('remind.csv')
	except:
	    mess = 'Invalid remind csv file'
	    return mess,mess1


	if len(message) == 2:
	    mess = 'Invalid format\n\nremind me < message data> at < time >  < date>        \n'
	    return mess,mess1
	
        elif 'at' in message:
	    start = message.index('me')
	    stop = message.index('at')
	    if (stop -start) <= 1:
	        mess = 'No message  received'
	    else:
		timedata_min = 0
		count = 0
	        message_data = message[start+1:stop]
		#print message_data
		message1 = message[stop+1:len(message)]
	        print message1
		print len(message1)
		message2 = filter(None,message1)
		print message2
		if len(message2) == 4 : # remidn me for call at dec 12 4 pm
		    for i in message2:
		        if i in valid_month:
		            print i
			    month = i
		            monthindex = message.index(i)	
			    count = 1
		    if count == 0:
		        mess = 'Invalid month entered'
			return mess,mess1
	            datemonth = message[monthindex - 1]
		    try:
		        date1 = int(datemonth)
		   # print date1
		        mess =   date1
		        if date1 not in range(0,32):
		            mess =  'Error:- Invalid Date entered'
			    return mess,mess1
		    except:
		        try:
		            date1 = int(message[monthindex + 1])
		       # print date1
		            mess =  date1
		            if date1 not in range(0,32):
		                mess = 'Error:-- invalid date entered'
			        return mess,mess1
		        except:
		            mess = '\nMonth is missing.please try again\n'
			    return mess,mess1
		    	
                    print 'datetttttttttt is {date}and month is {month}'.format(date = date1,month = month)
                #message.remove(date1)
		#message.remove(month)
		    m = []
                    m = [i for i in message]
		    print m

		    if 'am' in message2:
		        amindex = message.index('am')
   		        v_time = message[amindex]
		        amdata = message[amindex - 1]
		        try:
		            timedata = int(amdata)
			    print timedata
		        except:
		            try:
			        timedata = int(message[amindex + 1])
			        print timedata
			    except:
			        print 'Time is missing'
			        mess = 'Time is missing'
			        return mess,mess1
		    elif 'pm' in message2:
		        pmindex = message.index('pm')
		        v_time = message[pmindex]
		        pmdata = message[pmindex - 1]
		        try:
		            timedata = int(pmdata)
#			mess = mess + pmdata1
		        except:
		            try:
			        timedata = int(message[pmindex + 1])
#			    mess = mess +  
			    except:
			        print 'Time is missing'
			        mess = 'Time is missing'
			        return mess,mess1
	            else:
		        mess = 'Invalid time format'
		        return mess,mess1
		    mess = 'Message reminded for {date}{month}'.format(date = date1,month = month)

		    if timedata not in range(0,13) or timedata_min not in range(0,61):
		        mess = 'Invalid time and month'
		    	return mess,mess1

                else:         # remind me for call a freind at 4 30 pm dec 12
	            for i in message2:
		        if i in valid_month:
		            print i
			    month = i
		            monthindex = message.index(i)
			    count = 1
		    if count == 0:
		        mess = 'Invalid month entered'
			return mess,mess1
	            datemonth = message[monthindex - 1]
		    try:
		        date1 = int(datemonth)
		   # print date1
		        mess =   date1
		        if date1 not in range(0,32):
		            mess =  'Error:- Invalid Date entered'
			    return mess,mess1
		    except:
		        try:
		            date1 = int(message[monthindex + 1])
		       # print date1
		            mess =  date1
		            if date1 not in range(0,32):
		                mess = 'Error:-- invalid date entered'
			        return mess,mess1
		        except:
		            mess = '\nMonth is missing.please try again\n'	
			    return mess,mess1
                    print 'datetttttttttt is {date}and month is {month}'.format(date = date1,month = month)
                #message.remove(date1)
		#message.remove(month)
		    

		    if 'am' in message2:
		        amindex = message.index('am')
   		        v_time = message[amindex]
		        amdata = message[amindex - 1]
		        print 'amdata is {am}'.format(am = amdata)
		        try:
		            timedata_min = int(amdata)
			    timedata =int(message[amindex - 2])
			    print timedata
			    print timedata_min
		        except:
		            try:
			        timedata = int(message[amindex + 1])
			        timedata_min = int(message[amindex + 2])
			        print timedata
			        print timedata_min
			    except:
			        print 'Time is missing'
			        mess = 'Time is missing'
			        return mess,mess1
		    elif 'pm' in message2:
		        pmindex = message.index('pm')
		        v_time = message[pmindex]
		        pmdata = message[pmindex - 1]

		        try:
		            timedata_min = int(pmdata)
                            timedata = int(message[pmindex-2])
			    print timedata
			    print timedata_min
#			mess = mess + pmdata1
		        except:
		            try:
			        timedata = int(message[pmindex + 1])
			        timedata_min = int(message[pmindex + 2])

#			    mess = mess +  
			    except:
			        print 'Time is missing'
			        mess = 'Time is missing'
			        return mess,mess1
	            else:
		        mess = 'Invalid time format'
		        return mess,mess1  
   		    mess = 'Message reminded for {date}{month}'.format(date = date1,month = month)  
		    if timedata not in range(0,13) or timedata_min not in range(0,61):
		        mess = 'Invalid time and month'
		    	return mess,mess1

		remindcsv.loc[len(remindcsv) +1] = [date1,month,timedata,timedata_min,v_time,message_data]
		remindcsv.to_csv('remind.csv',index=False)
		

		    




  
    return mess,mess1

 ########################## POST request handler function ##################################################################
#a = 0
@app.route('/', methods=['POST'])
#a = 0
def handle_messages():

    data = request.get_json()
    log(data)

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:


	        try:	
                    if messaging_event.get("message"):
                        sender_id = messaging_event["sender"]["id"]
                        recipient_id = messaging_event["recipient"]["id"]
                        message_text = messaging_event["message"]["text"]
                        message_text,message_text1 = returnmessage(message_text,sender_id)
                        send_message(sender_id, message_text,message_text1)
	        except:
		   
		    try:
			urlqq = 'https://www.dropbox.com/s/fmdm0559r55ixtc/IMG_20170227_114753227.jpg?dl=0?raw=true'
		       
			#message_text1 = 'images'
		        send_message_images(sender_id,urlqq,message_text1)
		    except:
			urlqq = 'Sorry no attachment'
			message_text1 = None
			send_message(sender_id,urlqq,message_text1)
               #  messaging_event["attachments"]["type"]

    return "ok", 200



##################sending message to facebook page using graph api #########################################################

def send_message(recipient_id, message_text,datay):
    images_data1 = datay
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
   # end = int(datetime.datetime.now().strftime('%S'))
   # log('Elapsed time is {end123} seconds'.format(end123 = (end - start)))

    params = {
        "access_token": PAGE_ACCESS_TOKEN
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

    data1 =   json.dumps({
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
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    else:
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data1)
    log("status code is {status}".format(status=r.status_code))
    log(r.status_code)
    if r.status_code != 200:
        log(r.status_code)
    log(r.text)
    #return True

############# for printing message into stdout in terminal ################################################################

def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
app.run(host='0.0.0.0', port=port)
