import os
import sys
import commands

global track_data
global status_lines

def init():
    global track_data
    global status_lines
    
    track_data = ''
    mpc_status_output = commands.getoutput('mpc status -f "[[%artist% / %title% / %album%]|[%file%]]"');

    status_lines = mpc_status_output.split(os.linesep)

    if(len(status_lines) > 1):
        track_data = status_lines[0].split("/")
    
            
def get_title():
    title = ''

    if(len(status_lines) > 1):
        if(len(track_data) == 3):
            title = track_data[1].strip()

        if(len(track_data) == 2):
            title = track_data[1].strip()

    return title

def get_artist():
    artist = ''

    if(len(status_lines) > 1):
        if(len(track_data) == 3):
            title = track_data[0].strip()

        if(len(track_data) == 2):
            title = track_data[0].strip()

    return artist

def get_album():
    album = ''

    if(len(status_lines) > 1):
        if(len(track_data) == 3):
            title = track_data[0].strip()

        if(len(track_data) == 2):
            title = track_data[0].strip()

    return album

def get_duration():
    total_duration = 0
    
    if(len(status_lines) > 1):
       player_details = status_lines[1].split(" ")
       track_duration = player_details[-2].split("/")[1]
       time_split = track_duration.split(":")

       if(len(time_split) == 2):
           total_duration = int(time_split[0]) * 60 + int(time_split[1])
       else:
           total_duration = int(time_split[0]) * 60 + int(time_split[1]) * 60 + int(time_split[2])
       
    return total_duration

def get_player_state():
    player_state = 'stopped'

    if(len(status_lines) > 1):
        player_details = status_lines[1].split(" ")
        player_state = player_details[0].strip("[]")

    return player_state
