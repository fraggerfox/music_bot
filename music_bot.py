#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import sys
import signal
import datetime
import time
import commands
import thread
import ConfigParser

import wmp
import mpd
import amarok

global player_backend_type
global irc_network
global irc_port
global irc_nick
global irc_channel
global irc_speaker

# Handle the Ctrl + C and gracefully exit
def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


# Notifies the music track to IRC channel
# This runs in a separate thread
def notify_music_track(player_backend_type):
    global sock,connected

    if(player_backend_type == 'wmp'):
        player_backend = wmp;
    elif(player_backend_type == 'mpd'):
        player_backend = mpd
    elif(player_backend_type == 'amarok'):
        player_backend = amarok

    while 1:
        if (connected == True) :       
            player_backend.init()            
            duration = int(player_backend.get_track_duration())
            previous_player_state = player_backend.get_player_state()
            artist = player_backend.get_artist()

            time.sleep(duration * 0.05)
            if ((player_backend.get_player_state() != 'paused') and (previous_player_state != 'paused')):
                # Do we use ACTION or PRIVMSG or NOTICE this needs to be decided
                sock.send('NOTICE ' + irc_channel + ' :d(-_-)b ' + irc_speaker + ' is listening to '+ player_backend.get_title() +' by '+ player_backend.get_artist() +' \r\n')
                time.sleep(20) #sleep for a specified amount of time.

            time.sleep(1) #sleep for a specified amount of time.

# Function to join the IRC Channel
def join(irc_network,irc_port,irc_bot_nick,irc_channel):
    global sock,connected

    try:
	print 'Connecting....'
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((irc_network,irc_port))

	#send irc_bot_nick, user info to irc_network
	sock.send('NICK ' + irc_bot_nick + '\r\n')
	sock.send('USER ' + irc_bot_nick + ' ' + irc_bot_nick + ' '+ irc_bot_nick + ' :' + 'localhost\r\n')
  
	#join irc_channel
	sock.send('JOIN ' + irc_channel + '\r\n')
#	sock.setblocking(0)
	connected = True
	print 'Connected to ' + irc_channel + ' on ' + irc_network + ' as ' + irc_bot_nick
    except socket.error,(value,msg):
	print msg

# Function to connect to the IRC Network
def connectToIRC():
    global sock,connected

    connected = False
    #Loops only if bot is not connected
    while connected == False:
	#connect
	join(irc_network,irc_port,irc_bot_nick,irc_channel)

	#initialize checkpoint
	checkpoint = time.time()
	heloflag=False
        
	#Loop to keep listening
	while connected == True:
	    try:
                # This captures the data from IRC
		data = sock.recv(5120)
                print data

		#check for PING from server and reply with PONG if found
		if data.find('PING')!= -1 :
		    sock.send('PONG ' + data.split()[1] + '\r\n')
		    checkpoint=time.time()
            
		#check for message in irc_channel 
		if data.find('PRIVMSG ' + irc_channel) != -1:
		    speaker = data.split('!')[0].replace(':','')
		    message = ''.join(data.split(':')[2:])
                    print speaker
                    print message
		    checkpoint=time.time()
            
		#check for HELO msg and reset checkpoint
		if data.find('PRIVMSG ' + irc_bot_nick) != -1 and data.find('HELO'):
		    print 'Received HELO. Resetting idle counter....'
		    checkpoint=time.time()

		heloflag=True

	    except socket.error,(value,msg):
		#join again in case of error
		if value != 11:
		    print msg
		    sock.shutdown(2)
		    sock.close()	
		    sock=""
		    connected = False
		else:
		  #get current time and calculate idletime
		  now=time.time()
		  idletime = (int)(now-checkpoint)
		  #if idle time is above 90 secs send helo message
		  if(idletime == 90 and heloflag == False):
		    sock.send('PRIVMSG ' + irc_bot_nick + ' :HELO\r\n')
		    print 'Sending HELO due to inactivity'
		    heloflag=True
		  #if idle time has gone above 120 secs reconnect
		  if(idletime > 120):
		    sock.shutdown(2)
		    sock.close()	
		    sock=""
		    connected  = False
		    

# Reads the configuration settings from music_bot.ini file
def readConfigSettings():
    global player_backend_type
    global irc_network
    global irc_port
    global irc_bot_nick
    global irc_channel
    global irc_speaker

    config = ConfigParser.ConfigParser()
    config.read("music_bot.ini")
    
    player_backend_type = config.get('Player_Config', 'player_backend')

    irc_network = config.get('IRC_Config', 'network')
    irc_port = int(config.get('IRC_Config', 'port'))
    irc_bot_nick = config.get('IRC_Config', 'nick')
    irc_channel = config.get('IRC_Config', 'channel')
    irc_speaker = config.get('IRC_Config', 'speaker')

# Entry point of the application
def main():
    # Capture Ctrl-C and exit gracefully
    signal.signal(signal.SIGINT, signal_handler)

    # Read the configuration file
    readConfigSettings()
 
    # Create the background poll and notify thread
    try:
        thread.start_new_thread( notify_music_track, (player_backend_type,) )
    except thread.error, (value, msg):
        print value + ": " + msg

    # Establish connection to IRC
    connectToIRC()

if __name__=="__main__":
    main()

    while 1:
        pass
