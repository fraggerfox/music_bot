##########################################
# Amarok Back-end for Music Bot
##########################################
import os
import sys
import commands

global status_lines

def init():
    global status_lines
    
    track_data = ''

    amarok_status_output = commands.getoutput('qdbus org.kde.amarok /Player org.freedesktop.MediaPlayer.GetMetadata');
    status_lines = amarok_status_output.split('\n')

            
def get_title():
    title = ''

    for status_line in status_lines:
        if status_line.find('title') != -1:
            title = status_line.split(":")[1].strip()

    return title

def get_artist():
    artist = ''

    for status_line in status_lines:
        if status_line.find('artist') != -1:
            artist = status_line.split(":")[1].strip()

    print artist
    return artist

def get_album():
    album = ''

    for status_line in status_lines:
        if status_line.find('album') != -1:
            album = status_line.split(":")[1].strip()

    return album

def get_duration():
    total_duration = 0
    
    for status_line in status_lines:
        if status_line.find('time') != -1:
            total_duration = status_line.split(":")[1].strip()
       
    return total_duration

# TODO: Implement this
def get_player_state():
    player_state = 'stopped'

    return player_state


#		    if cmp(speaker, 'fragger_fox') == 0 and message.startswith(irc_nick): #bad..get boss from command line
#			
#			#Modify the command passed to commands.getoutput to suit player of wish
#			if message.find('artist') != -1:
#			    #artist = commands.getoutput('qdbus org.kde.amarok /Player GetMetadata | grep \'artist\' | cut -d ":" -f 2 | cut -c 2-')
#			    #sock.send('PRIVMSG ' + irc_channel + ' :' + speaker + ' d(-_-)b ' + artist +'\r\n')
#                            artist = 'sample text'
#                            sock.send('ACTION ' + irc_channel + ' :' + speaker + ' d(-_-)b ' + artist +'\r\n')
#                            
#                            sock.send('NOTICE ' + irc_channel + ' :' + speaker + ' d(-_-)b ' + artist +'\r\n')
##			if message.find('track') != -1:
##			    track = commands.getoutput('qdbus org.kde.amarok /Player GetMetadata | grep \'title\' | cut -d ":" -f 2 | cut -c 2-')
##			    sock.send('PRIVMSG ' + irc_channel + ' :' + speaker + ' d(-_-)b ' + track +'\r\n')
##			if message.find('song') != -1:
##			    artist = commands.getoutput('qdbus org.kde.amarok /Player GetMetadata | grep \'artist\' | cut -d ":" -f 2 | cut -c 2-')
##			    track = commands.getoutput('qdbus org.kde.amarok /Player GetMetadata | grep \'title\' | cut -d ":" -f 2 | cut -c 2-')
##			    sock.send('PRIVMSG ' + irc_channel + ' :' + speaker + ' d(-_-)b ' + track + ' by ' + artist + '\r\n')
