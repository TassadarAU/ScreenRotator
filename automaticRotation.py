#!/usr/bin/python
# demo.py - CMD Args Demo By nixCraft
import sys 
from time import sleep
from os import path as op
from subprocess import check_call, check_output
from glob import glob
import os                                                                       # Libary used for making system calls
import signal                                                                   # 
import time                                                                     # Used for access to the process sleep libary
import subprocess                                                               # Libary used to call the commands from the operating system
#import notify2
import gi                                                                       #
import re                                                                       #
gi.require_version("Notify", "0.7")                                             # Versioning checks for notify
gi.require_version("Gtk", "3.0")                                                # Versonioning checks GTK graphics libary 
from gi.repository import Notify                                                # Notification libary
from subprocess import call                                                     # Subprocess libary for making system calls
from gi.repository import Gtk                                                   # Gtk libary for GUI shell objects
from gi.repository import AppIndicator3 as AppIndicator                         # Indicator libary for task bar
from gi.repository import Notify, GdkPixbuf                                     # notification libary import
from string import digits                                                       # String libary used for rege functions and string manipulation
from time import sleep                                                          # Required to add easy pause into while loop that samples from acceleromoeter
###############################################################################################################################



# Get the total number of args passed to the demo.py
total = len(sys.argv)
 
# Get the arguments list 
cmdargs = str(sys.argv)
 
# Print it
print ("The total numbers of args passed to the script: %d " % total)
print ("Args list: %s " % cmdargs)


###############################################################################################################################

APPINDICATOR_ID = "screenrotator"
orientation = "normal"                                                                               # The Default startip state is assumed to be in laptop configuration
NotificationIconPath = "/usr/share/ScreenRotationIndicator/notifications.png"                        # require to configure the applications notification icon
KeyboardDeviceID = ""                                                                                # This will be used in later functions to disable the hardware keyboard when in tablet mode
KeyboardSlaveID  = ""                                                                                # Slave id for the onboard keyboard
TouchScreenDeviceID = ""                                                                             # This will be used to flip the screem inputs whe in tablet mode.
TouchScreenSlaveID = ""                                                                              # This will beused 
TouchPadDeviceID = ""                                                                                # This will be used to disable the touchpad in tablet mode
TouchPadSlaveID = ""                                                                                 # This will be used to disable the touchpad in tablet mode
DigitiserDeviceID = ""                                                                               # Pen/Stylus/Digitiser Device ID
DigitiserSlaveID = ""                                                                                # Pen/Stylus/Digitiser Slave ID
MonitorDeviceName = "ELAN0732:00"                                                                    # This is the screens name as per the output of xrandr -q this will be used to try alter the screen state
IndicatorIconPath = "/usr/share/ScreenRotationIndicator/icon.svg"                                    # Indicator icon location path, This will be programaticly set later
Notify.init("Screen Rotiation")                                                                      # Initialise the notification object with the applications title, This will appear in bold on the notification toatsy
applicationMode = "Manual"
###############################################################################################################################
#set the tranformation matrix variables
########## Transforms #####################
stringInvertedTransform = "-1 0 1 0 -1 1 0 0 1"
stringNormalTransform = "1 0 0 0 1 0 0 0 1"
stringLeftTransform = "0 -1 1 1 0 0 0 0 1"
stringRightTransform = "0 1 0 -1 0 1 0 0 1"

################################################################################################################################
# Use GdkPixbuf to create the proper image type
notifications = Notify.Notification.new("Screen Rotation Enchanced", "Application Started")          # Create the Notification Object and set it with the start up values ready for display
image = GdkPixbuf.Pixbuf.new_from_file(NotificationIconPath)                                         # Intialise the image object to be used bu the notification system
# Use the GdkPixbuf image
notifications.set_icon_from_pixbuf(image)                                                            # Set the icon Image for the notifications popup   
notifications.set_image_from_pixbuf(image)                                                           # Set the image to be used by the notification popup
notifications.show()                                                                                 # Display the first notification stating that the application has started
# Grab the keyboard device numbers in preperation
cmdpipe = subprocess.Popen("xinput --list | grep 'AT Translated' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
result = cmdpipe.stdout.readline()                                                                   # Result from the xinput command filtered to show the current keyboard
KeyboardDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])         # Regex filtering to cut the numeric value for the ID
KeyboardSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                    # Regex filtering to cut the numeric value for the slave id
# Grab the touch pad device numbers
cmdpipe = subprocess.Popen("xinput --list | grep 'Synaptics' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)  # Grab the touchpad in preperation for regex functions 
result = cmdpipe.stdout.readline()                                                                   # Execute the above command to retreive the touchpad ID string                       
TouchPadDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])         # Strip out the device ID from the returned String
TouchPadSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                    # String the Slave ID from the original returned string 
# Grab the TouchScreen device Numbers
cmdpipe = subprocess.Popen("xinput --list | grep 'ELAN0732:00' | grep -v 'keyboard'  ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
result = cmdpipe.stdout.readline()                                                                   # Execute the above command and return the raw touch screen ID as the PEN/Stylus will have a similar ID the grep -v will remove the any line with PEN in the string
TouchScreenDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])      # Strip the device ID from the returned string by removing anything before the = 
TouchPadSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                    # Strip the device salve id by removing anything betweem the brackets
# Grab the Digitiser/Pen device Numbers     
cmdpipe = subprocess.Popen("xinput --list | grep 'pointer' | grep 'Stylus' | grep 'Pen'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
result = cmdpipe.stdout.readline()                                                                   # Execute the command and store the output 
DigitiserDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])        # Strip out the device ID number is regex looking for a numeric charcters after the an =
DigitiserSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                   # Strip out the slave ID looking for numeric characters between brackets

######################## DEBUG ###########################
print ("Keyboard ID       - "     + KeyboardDeviceID   )                                                                            # Debug
print ("Keyboard Slave id - "     + KeyboardSlaveID  )                                                                              # Debug
print ("Touch Pad ID      - "     + TouchPadDeviceID   )                                                                            # Debug
print ("Touch Pad Slave ID - "    + TouchPadSlaveID )                                                                               # Debug
print ("Pen Device ID - "         + DigitiserDeviceID )                                                                             # Debug 
print ("Pen Slave ID - "          + DigitiserSlaveID  )                                                                             # Debug
print ("Touch Screen - "          + TouchScreenDeviceID )                                                                           # Debug
print ("touch Screen Slave ID - " + TouchPadSlaveID )                                                                               # Debug
######################## DEBUG ###########################

def RotateScreen(TargetCordinateMatrix, direction):
    #get current screen orientaion
    cmdpipe = subprocess.Popen("xrandr --query --verbose | grep 'primary' | cut -d ' ' -f 6", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = cmdpipe.stdout.readline()  
    result = re.sub(r'[^a-zA-Z0-9--]', '', result)
    if direction == result:
        print ("directions is the same there is nothing to do here")
    else:
        #print (TargetCordinateMatrix + "direction target" + direction)
        call(["xrandr", "-o", direction])                                                                                  # Execute screen rotation to the desired orientation
        command = "xinput set-prop " + DigitiserDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix  #The method above inverts the Pen/Digitiser calibration
        #print ("this will be the command - " +command ) # DEBUG
        os.system(command)                                                                                                 # Execute the Pen/Digitiser inversion command
        command = "xinput set-prop " + TouchScreenDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix
        #print ("this will be the command - " +command ) # DEBUG
        os.system(command) 
        notifications.update("Screen Auto Rotation", "Switching rotating " + direction)
        notifications.show()

global applicationMode
mode = "auto"
applicationMode = mode
print ("starting auto mode")
while applicationMode != "man":
    acceleromoeterReading = ""
    # Grab the TouchScreen device Numbers
    cmdpipe = subprocess.Popen("'monitor-sensor'  ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    for stdout_line in iter(cmdpipe.stdout.readline,""):
        #yield stdout_line
        acceleromoeterReading = re.sub('^[^:]*',"", stdout_line) 
        acceleromoeterReading = re.sub('[:]','', acceleromoeterReading)
        acceleromoeterReading = re.sub(' ','', acceleromoeterReading)
        acceleromoeterReading = re.sub(r'[^a-zA-Z0-9--]', '', acceleromoeterReading)
        if acceleromoeterReading == "right-up":
            #print ("Right UP")   #debug
            RotateScreen (stringRightTransform, "right") 
        elif acceleromoeterReading == "left-up":
            #print ("Left-Up")
            RotateScreen (stringLeftTransform, "left") 
        elif acceleromoeterReading == "normal":
            #print ("Normal")
            RotateScreen (stringNormalTransform, "normal") 
        elif acceleromoeterReading == "bottom-up":
            #print ("bottom-Up")
            RotateScreen (stringInvertedTransform, "inverted") 
        #print (acceleromoeterReading)
    pass


