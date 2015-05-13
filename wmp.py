import os
import win32file
import win32con
from xml.dom import minidom

global now_playing_xmldoc

def init():
    global now_playing_xmldoc
    ACTIONS = {
        1 : "Created",
        2 : "Deleted",
        3 : "Updated",
        4 : "Renamed from something",
        5 : "Renamed to something"
    }
    # Thanks to Claudio Grondi for the correct set of numbers
    FILE_LIST_DIRECTORY = 0x0001

    path_to_watch = "D:\\"
    hDir = win32file.CreateFile (
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    #
    # ReadDirectoryChangesW takes a previously-created
    # handle to a directory, a buffer size for results,
    # a flag to indicate whether to watch subtrees and
    # a filter of what changes to notify.
    #
    # NB Tim Juchcinski reports that he needed to up
    # the buffer size to be sure of picking up all
    # events when a large number of files were
    # deleted at once.
    #
    results = win32file.ReadDirectoryChangesW (
        hDir,
        1024,
        False,
        win32con.FILE_NOTIFY_CHANGE_LAST_WRITE,
        None,
        None
    )
        
    for action, file in results:
        full_filename = os.path.join (path_to_watch, file)            
        if(file == "now_playing_track.xml"):
            now_playing_xmldoc = minidom.parse(full_filename)
            
def get_title():
    title = now_playing_xmldoc.getElementsByTagName('title')[0].childNodes[0].data
    return title

def get_artist():
    artist = ''
    if(len(now_playing_xmldoc.getElementsByTagName('artist')[0].childNodes) > 0):
        artist = now_playing_xmldoc.getElementsByTagName('artist')[0].childNodes[0].data
    return artist

def get_album():
    album = ''
    if(len(now_playing_xmldoc.getElementsByTagName('album')[0].childNodes) > 0):
        album = now_playing_xmldoc.getElementsByTagName('album')[0].childNodes[0].data
    return album

def get_player_state():
    player_state = now_playing_xmldoc.getElementsByTagName('player_state')[0].childNodes[0].data
    return player_state

def get_track_duration():
    track_duration = now_playing_xmldoc.getElementsByTagName('duration')[0].childNodes[0].data
    return track_duration

