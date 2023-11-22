import os
import sys
import json
from dirsync import sync
from IPython.utils.capture import capture_output
from datetime import datetime

logfile = r'c:\temp\usb.log'
controlFile = r"D:\.sys\music_usb"

def checkValidUSB():
    #if a control file isnt found, quit

    if not os.path.isfile(controlFile):
        
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        msg = 'not a valid usb quitting'

        print (f'{msg}')

        with open(logfile, 'a') as file:
            file.write (f'{dt_string} - {msg}\n')
        sys.exit()

def checkValidPlaylists():
    
    #check the filepaths in each playlist link to an actual file

    playlist_list = []

    for root, dirs, files in os.walk('D:'): #walk will allow traversing sub dirs
        for file in files:
            if file.endswith(".m3u"): #play list extension
                playlist_list.append ((root,os.path.join(root, file)))

    #print (playlist_list)

    for playlist in playlist_list:
        root,playlist = playlist
        #print (playlist,root)

        with open(playlist, 'r') as file:
            lines = file.readlines()

            for line in lines:
                if not line.startswith('#') and line != '\n':
                    full_path = root + '\\' + line.replace('\n', '')
                    #print (full_path)
                    if not os.path.isfile(full_path):

                        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")    
                        msg = f'error - bad path - {full_path}'

                        print (msg)
                       
                        with open(logfile, 'a') as file:
                            file.write (f'{dt_string} - {msg}\n')

def syncfiles():

    #sync the destination with the source

    with open(controlFile) as input_file:
        line = [next(input_file) for _ in range(1)]
        #print(line)

    dict =json.loads(line[0]) #create a dictionary from a string

    usbLoc = dict['usbLoc'] 
    pcLoc = dict['pcLoc']
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with capture_output() as c:
        sync(pcLoc,usbLoc,'sync',purge=True,verbose=True)


    stdout = c.stdout.replace('\n\n', '')
    print (stdout.replace('\n\n', ''))

    with open(logfile, 'a') as file:
        file.write (f'{dt_string} - sync starting\n')   
        file.write (f'{stdout}\n')   
        file.write (f'{dt_string} - sync ended\n')            

checkValidUSB()
syncfiles()
checkValidPlaylists()