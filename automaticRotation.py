#!/usr/bin/python
import sys 
from time import sleep
from os import path as op
from subprocess import check_call, check_output
from glob import glob
import os                                                                       # Libary used for making system calls
import signal                                                                   # enables us to use signal handlers so that we can perform custom tasks whenever a signal is received.
import time                                                                     # Used for access to the process sleep libary
import subprocess                                                               # Libary used to call the commands from the operating system
import gi                                                                       # PyGObject GTK3 Library
import re                                                                       # Regular expressions library
gi.require_version('AppIndicator3', '0.1')                                      # Versonioning checks
gi.require_version('Notify', '0.7')                                             # Versonioning checks
from gi.repository import Notify                                                # Notification libary
from subprocess import call                                                     # Subprocess libary for making system calls
from gi.repository import AppIndicator3 as AppIndicator                         # Indicator libary for task bar
from gi.repository import Notify, GdkPixbuf                                     # notification libary import
from string import digits                                                       # String libary used for rege functions and string manipulation
from time import sleep                                                          # Required to add easy pause into while loop that samples from acceleromoeter
from DevicesClass import DevicesClass
from ScreenRotatorUtils import ScreenRotatorUtils

###############################################################################################################################
def NotificationToasty (title,message):
    if ReadConfigFile("notifications") == "enabled":
        notifications.update(title, message)
        notifications.show()

def ReadConfigFile(attribute):
    filename = os.path.join(os.path.dirname(__file__), 'autoRotation.config') 
    with open(filename) as f:
        file_content = f.readlines()
        for line in file_content:
            attributeFile = re.sub(r'[^a-zA-Z0-9--]', '', re.sub('\:.*$',"",line) )
            if attribute == attributeFile:
                data = re.sub('^[^:]*',"", line).split(':')
    return re.sub('\n','', data[1]) #Return value minus new line characters 


###############################################################################################################################
global applicationMode
APPINDICATOR_ID = "screenrotator"
orientation = "normal"                                        # The Default startip state is assumed to be in laptop configuration
NotificationIconPath = ReadConfigFile("NotificationIconPath")        
Notify.init(ReadConfigFile("Notify"))                         # Initialise the notification object with the applications title, This will appear in bold on the notification toatsy
applicationMode = "auto"
##################### Set the tranformation matrix variables ##################################################################
stringInvertedTransform = "-1 0 1 0 -1 1 0 0 1"
stringNormalTransform   = "1 0 0 0 1 0 0 0 1"
stringLeftTransform     = "0 -1 1 1 0 0 0 0 1"
stringRightTransform    = "0 1 0 -1 0 1 0 0 1"

################################################################################################################################
notifications = Notify.Notification.new("Screen Rotation", "Auto Rotation Service Started")                     # Create the Notification Object and set it with the start up values ready for display
image = GdkPixbuf.Pixbuf.new_from_file(NotificationIconPath)                                                    # Intialise the image object to be used bu the notification system using GdkPixbuf to create the proper image type
notifications.set_icon_from_pixbuf(image)                                                                       # Set the icon Image for the notifications popup   
notifications.set_image_from_pixbuf(image)                                                                      # Set the image to be used by the notification popup
utilsLibrary = ScreenRotatorUtils()                                                                             # Intialise utilslibary object from screen rotator utils class
NotificationToasty ("Screen Auto Rotation", "Auto rotation Service starting ")                                  # Display the first notification stating that the application has started
#TouchScreenName = utilsLibrary.readConfigreturnAttribute("TouchScreen")
DevicesList = DevicesClass( utilsLibrary.readConfigreturnAttribute("TouchScreen") )

while applicationMode != "quit":
    # monitor for acceleometer changes. Then parse the output to get the direction state change
    cmdpipe = subprocess.Popen("'monitor-sensor'  ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #for stdout_line in iter(cmdpipe.stdout.readline,""):
    for stdout_line in iter(cmdpipe.stdout.readline,""):
        mode = re.sub(r'[^a-zA-Z0-9--]', '', ReadConfigFile("mode") )
        acceleromoeterReading =  re.sub(r'[^a-zA-Z0-9--]', '', re.sub(' ','', re.sub('[:]','', re.sub('^[^:]*',"", stdout_line.decode("utf-8") ))))
        if mode == "auto" or mode =="Auto":
            if stdout_line and (not stdout_line.isspace()): 
                #print ("test acceleromoeterReading " + acceleromoeterReading)
                if acceleromoeterReading == "right-up":
                    #RotateScreen (stringRightTransform, "right") 
                    utilsLibrary.RotateScreen (DevicesList, stringNormalTransform, "right")  
                elif acceleromoeterReading == "left-up":
                    #RotateScreen (stringLeftTransform, "left") 
                    utilsLibrary.RotateScreen (DevicesList, stringNormalTransform, "left")   
                elif acceleromoeterReading == "normal":
                    #RotateScreen (stringNormalTransform, "normal") 
                    utilsLibrary.RotateScreen (DevicesList, stringNormalTransform, "normal")    
                elif acceleromoeterReading == "bottom-up":
                    #RotateScreen (stringInvertedTransform, "inverted")
                    utilsLibrary.RotateScreen (DevicesList, stringInvertedTransform, "inverted")     
        elif mode =="quit":
            break
        acceleromoeterReading = utilsLibrary.currentOrientation()
        #print (" finish " + acceleromoeterReading)
    pass


