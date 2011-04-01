# -*- coding: utf-8 -*-
import socket
import sys
import datetime
import time
import commands

def join(network,port,nick,channel):
    global sock,connected
    try:
	print 'Connecting....'
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((network,port))

	#send nick, user info to network
	sock.send('NICK ' + nick + '\r\n')
	sock.send('USER ' + nick + ' ' + nick + ' '+ nick + ' :' + 'localhost\r\n')
  
	#join channel
	sock.send('JOIN ' + channel + '\r\n')
	sock.setblocking(0)
	connected = True
	print 'Connected to ' + channel + ' on ' + network + ' as ' + nick
    except socket.error:
	print 'Could not open socket'

def main():
    global sock,connected
    try:
	#get stuff from command line
	network = sys.argv[1]
	port = 6667
	nick = sys.argv[2]
	channel = sys.argv[3]
    except IndexError:
	#Dsplay error and quit
	print 'Error: Missing required parameters'
	print 'Syntax is sakshi.py <network> <nickname> \'<channel>\''
	sys.exit()

    connected = False
    #Loops only if bot is not connected
    while connected == False:
	#connect
	join(network,port,nick,channel)

	#initialize checkpoint
	checkpoint = time.time()
	heloflag=0

	#Loop to keep listening
	while connected == True:
	    try:
		data = sock.recv(5120)
                print data
		#check for PING from server and reply with PONG if found
		if data.find('PING')!=-1 :
		    sock.send('PONG ' + data.split()[1] + '\r\n')
		    checkpoint=time.time()
            
		#check for message in channel 
		if data.find('PRIVMSG ' + channel) != -1:
		    speaker = data.split('!')[0].replace(':','')
		    message = ''.join(data.split(':')[2:])
                    print speaker
                    print message

		    if cmp(speaker, 'r2_d2') == 0 and message.startswith(nick): #bad..get boss from command line
			
			#Modify the command passed to commands.getoutput to suit player of wish
			if message.find('artist') != -1:
			    artist = commands.getoutput('qdbus org.kde.amarok /Player GetMetadata | grep \'artist\' | cut -d ":" -f 2 | cut -c 2-')
			    sock.send('PRIVMSG ' + channel + ' :' + speaker + ' d(-_-)b ' + artist +'\r\n')
			if message.find('track') != -1:
			    track = commands.getoutput('qdbus org.kde.amarok /Player GetMetadata | grep \'title\' | cut -d ":" -f 2 | cut -c 2-')
			    sock.send('PRIVMSG ' + channel + ' :' + speaker + ' d(-_-)b ' + track +'\r\n')
			if message.find('song') != -1:
			    artist = commands.getoutput('qdbus org.kde.amarok /Player GetMetadata | grep \'artist\' | cut -d ":" -f 2 | cut -c 2-')
			    track = commands.getoutput('qdbus org.kde.amarok /Player GetMetadata | grep \'title\' | cut -d ":" -f 2 | cut -c 2-')
			    sock.send('PRIVMSG ' + channel + ' :' + speaker + ' d(-_-)b ' + track + ' by ' + artist + '\r\n')
		    checkpoint=time.time()
            
		#check for HELO msg and reset checkpoint
		if data.find('PRIVMSG ' + nick) != -1 and data.find('HELO'):
		    print 'Received HELO. Resetting idle counter....'
		    checkpoint=time.time()
		heloflag=0
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
		  if(idletime == 90 and heloflag == 0):
		    sock.send('PRIVMSG ' + nick + ' :HELO\r\n')
		    print 'Sending HELO due to inactivity'
		    heloflag=1
		  #if idle time has gone above 100 secs reconnect
		  if(idletime > 120):
		    sock.shutdown(2)
		    sock.close()	
		    sock=""
		    connected  = False
		    
	      

if __name__=="__main__":
    main()
