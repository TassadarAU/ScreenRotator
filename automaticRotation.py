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

def QueryDeviceAddressing():
    global TouchScreenName         # system firendly name as displayed in xinput
    global KeyboardDeviceID        # This will be used in later functions to disable the hardware keyboard when in tablet mode
    global KeyboardSlaveID         # Slave id for the onboard keyboard
    global TouchScreenDeviceID     # This will be used to flip the screem inputs whe in tablet mode.
    global TouchScreenSlaveID      # This will beused 
    global TouchPadDeviceID        # This will be used to disable the touchpad in tablet mode
    global TouchPadSlaveID         # This will be used to disable the touchpad in tablet mode
    global DigitiserDeviceID       # Pen/Stylus/Digitiser Device ID
    global DigitiserSlaveID        # Pen/Stylus/Digitiser Slave ID
    TouchScreenName = ReadConfigFile("TouchScreen") # read value from config file to make sure we query the correct device

    cmdpipe = subprocess.Popen("xinput --list | grep 'AT Translated' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = cmdpipe.stdout.readline()                                                                      # Result from the xinput command filtered to show the current keyboard
    if result and (not result.isspace()): 
        KeyboardDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])         # Regex filtering to cut the numeric value for the ID
        KeyboardSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                    # Regex filtering to cut the numeric value for the slave id
    # Grab the touch pad device numbers
    cmdpipe = subprocess.Popen("xinput --list | grep 'Synaptics' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)  # Grab the touchpad in preperation for regex functions 
    result = cmdpipe.stdout.readline()      
    if result and (not result.isspace()):                                                                    # Execute the above command to retreive the touchpad ID string                       
        TouchPadDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])         # Strip out the device ID from the returned String
        TouchPadSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                    # String the Slave ID from the original returned string 
    # Grab the TouchScreen device Numbers
    cmdpipe = subprocess.Popen("xinput --list | grep '" + TouchScreenName + "' | grep -v 'keyboard'  ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = cmdpipe.stdout.readline()
    if result and (not result.isspace()):                                                                    # Execute the above command and return the raw touch screen ID as the PEN/Stylus will have a similar ID the grep -v will remove the any line with PEN in the string
        TouchScreenDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])      # Strip the device ID from the returned string by removing anything before the = 
        TouchPadSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                    # Strip the device salve id by removing anything betweem the brackets
    # Grab the Digitiser/Pen device Numbers     
    cmdpipe = subprocess.Popen("xinput --list | grep 'pointer' | grep 'Stylus' | grep 'Pen'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = cmdpipe.stdout.readline()  
    if result and (not result.isspace()): 
        DigitiserDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])        # Strip out the device ID number is regex looking for a numeric charcters after the an =
        DigitiserSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                   # Strip out the slave ID looking for numeric characters between brackets
    else:
        DigitiserDeviceID = ""       
        DigitiserSlaveID = ""

def RotateScreen(TargetCordinateMatrix, direction):
    QueryDeviceAddressing()
    #get current screen orientaion
    cmdpipe = subprocess.Popen("xrandr --query --verbose | grep 'primary' | cut -d ' ' -f 6", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = cmdpipe.stdout.readline()  
    result = re.sub(r'[^a-zA-Z0-9--]', '', result)
    if direction != result:
        #print (TargetCordinateMatrix + "direction target" + direction)
        call(["xrandr", "-o", direction])                      
        if DigitiserDeviceID and (not DigitiserDeviceID.isspace()):                                                            # Execute screen rotation to the desired orientation
            command = "xinput set-prop " + DigitiserDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix  # The method above inverts the Pen/Digitiser calibration
            os.system(command)
        if TouchScreenDeviceID and (not TouchScreenDeviceID.isspace()):                                                        # Execute the Pen/Digitiser inversion command
            command = "xinput set-prop " + TouchScreenDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix
            #print ("this will be the command - " +command ) # DEBUG
            os.system(command) 
        NotificationToasty ("Screen Auto Rotation", "Switching rotating " + direction)

def DebugPrintDeviceIDS():
    ######################## DEBUG ###########################
    print ("Keyboard ID       - "     + KeyboardDeviceID    )
    print ("Keyboard Slave id - "     + KeyboardSlaveID     )
    print ("Touch Pad ID      - "     + TouchPadDeviceID    )
    print ("Touch Pad Slave ID - "    + TouchPadSlaveID     )
    print ("Pen Device ID - "         + DigitiserDeviceID   )
    print ("Pen Slave ID - "          + DigitiserSlaveID    )
    print ("Touch Screen - "          + TouchScreenDeviceID ) 
    print ("touch Screen Slave ID - " + TouchPadSlaveID     ) 
    ######################## DEBUG ########################### 


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
notifications = Notify.Notification.new("Screen Rotation", "Auto Rotation Service Started")          # Create the Notification Object and set it with the start up values ready for display
image = GdkPixbuf.Pixbuf.new_from_file(NotificationIconPath)                                         # Intialise the image object to be used bu the notification system using GdkPixbuf to create the proper image type
notifications.set_icon_from_pixbuf(image)                                                            # Set the icon Image for the notifications popup   
notifications.set_image_from_pixbuf(image)                                                           # Set the image to be used by the notification popup
NotificationToasty ("Screen Auto Rotation", "Auto rotation Service starting ")                                                                              # Display the first notification stating that the application has started
QueryDeviceAddressing()                                                                              # Retreive device IDs to be used later 

while applicationMode != "quit":
    acceleromoeterReading = ""
    # Grab the TouchScreen device Numbers
    cmdpipe = subprocess.Popen("'monitor-sensor'  ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    for stdout_line in iter(cmdpipe.stdout.readline,""):
        mode = re.sub(r'[^a-zA-Z0-9--]', '', ReadConfigFile("mode") )
        if mode == "auto" or mode =="Auto":
            if stdout_line and (not stdout_line.isspace()): 
                acceleromoeterReading = re.sub(r'[^a-zA-Z0-9--]', '', re.sub(' ','', re.sub('[:]','', re.sub('^[^:]*',"", stdout_line))))
            if acceleromoeterReading == "right-up":
                RotateScreen (stringRightTransform, "right") 
            elif acceleromoeterReading == "left-up":
                RotateScreen (stringLeftTransform, "left") 
            elif acceleromoeterReading == "normal":
                RotateScreen (stringNormalTransform, "normal") 
            elif acceleromoeterReading == "bottom-up":
                RotateScreen (stringInvertedTransform, "inverted") 
        elif mode =="quit":
            break
    pass


