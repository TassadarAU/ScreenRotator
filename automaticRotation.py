#!/usr/bin/python
import os                                                                       # Libary used for making system calls
import subprocess                                                               # Libary used to call the commands from the operating system
import gi                                                                       # PyGObject GTK3 Library
import re                                                                       # Regular expressions library
gi.require_version('AppIndicator3', '0.1')                                      # Versonioning checks
gi.require_version('Notify', '0.7')                                             # Versonioning checks
from gi.repository import Notify                                                # Notification libary
from subprocess import call                                                     # Subprocess libary for making system calls
from gi.repository import Notify, GdkPixbuf                                     # notification libary import
from DevicesClass import DevicesClass
from ScreenRotatorUtils import ScreenRotatorUtils
###############################################################################################################################
def NotificationToasty (title,message):
    if utilsLibrary.readConfigreturnAttribute("notifications") == "enabled":
        notifications.update(title, message)
        notifications.show()

###############################################################################################################################
global applicationMode
utilsLibrary = ScreenRotatorUtils()
APPINDICATOR_ID = "screenrotator"
orientation = "normal"                                        # The Default startip state is assumed to be in laptop configuration
NotificationIconPath = utilsLibrary.readConfigreturnAttribute("NotificationIconPath")        
Notify.init(utilsLibrary.readConfigreturnAttribute("Notify"))                       
applicationMode = "auto"
##################### Set the tranformation matrix variables ##################################################################
stringInvertedTransform = "-1 0 1 0 -1 1 0 0 1"
stringNormalTransform   = "1 0 0 0 1 0 0 0 1"
stringLeftTransform     = "0 -1 1 1 0 0 0 0 1"
stringRightTransform    = "0 1 0 -1 0 1 0 0 1"

################################################################################################################################
notifications = Notify.Notification.new("Screen Rotation", "Auto Rotation Service Started")          # Create the Notification Object and set it with the start up values ready for display
image = GdkPixbuf.Pixbuf.new_from_file(NotificationIconPath)                                         # Intialise the image object to be used bu the notification system using GdkPixbuf to create the proper image type
notifications.set_icon_from_pixbuf(image)                                                            # Set the icon Image for the notifications popup   
notifications.set_image_from_pixbuf(image)                                                           # Set the image to be used by the notification popup
NotificationToasty ("Screen Auto Rotation", "Auto rotation Service starting ")                       # Display the first notification stating that the application has started
#TouchScreenName = utilsLibrary.readConfigreturnAttribute("TouchScreen")
DevicesList = DevicesClass(utilsLibrary.readConfigreturnAttribute("TouchScreen"))
TouchScreenName = DevicesList.DiscoverTouchScreenName(utilsLibrary.readConfigreturnAttribute("TouchScreen"))
print ("TouchScreenName returned is " +TouchScreenName)
DevicesList.QueryDeviceAddressing()
DevicesList.DebugPrintDeviceIDS()
mode = re.sub(r'[^a-zA-Z0-9--]', '', utilsLibrary.readConfigreturnAttribute("mode"))
NotificationToasty ("Screen Auto Rotation", "Current mode is " + mode)
while applicationMode != "quit":
    acceleromoeterReading = ""
    # Grab the TouchScreen device Numbers
    cmdpipe = subprocess.Popen("'monitor-sensor'  ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    for stdout_line in iter(cmdpipe.stdout.readline,""):
        mode = re.sub(r'[^a-zA-Z0-9--]', '', utilsLibrary.readConfigreturnAttribute("mode"))
        direction = ""
        if mode == "auto" or mode =="Auto":
            if stdout_line and (not stdout_line.isspace()): 
                acceleromoeterReading = re.sub(r'[^a-zA-Z0-9--]', '', re.sub(' ','', re.sub('[:]','', re.sub('^[^:]*',"", stdout_line.decode()))))
            if acceleromoeterReading != utilsLibrary.currentOrientation():
                if acceleromoeterReading == "right-up":
                    utilsLibrary.RotateScreen (DevicesList, stringRightTransform, "right") 
                    direction = "right"
                    NotificationToasty ("Screen Auto Rotation", "Switching rotating " + direction)
                elif acceleromoeterReading == "left-up":
                    utilsLibrary.RotateScreen (DevicesList, stringLeftTransform, "left") 
                    direction = "left"
                    NotificationToasty ("Screen Auto Rotation", "Switching rotating " + direction)
                elif acceleromoeterReading == "normal":
                    utilsLibrary.RotateScreen (DevicesList, stringNormalTransform, "normal") 
                    direction = "normal"
                    NotificationToasty ("Screen Auto Rotation", "Switching rotating " + direction)
                elif acceleromoeterReading == "bottom-up":
                    direction = "inverted" 
                    utilsLibrary.RotateScreen (DevicesList, stringInvertedTransform, direction)
                    NotificationToasty ("Screen Auto Rotation", "Switching rotating " + direction)
        elif mode =="quit":
            break
    pass


