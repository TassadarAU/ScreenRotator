#!/usr/bin/env python3
######################################################################################################################################
# Maintainer - Domenic.
# 
# Requirements - gnome based interface 
#
#
# Originaly forked from ScreenRotator http://
# Modifications made ahve been to support devices such as the HP x360 convertable systems. This allows the system to be inverted or 
# put into tent mode and flip the screen which requires the touch screen cor-ordinate system to also be inverted. Tablet mode was also
# added to disable the hardware keyboard and mouse to prevent unwanted keypress whilist holding the unit.
#
# https://askubuntu.com/questions/160945/is-there-a-way-to-disable-a-laptops-internal-keyboard
# https://unix.stackexchange.com/questions/229876/xinput-calibration-and-options
# https://houseofneruson.wordpress.com/2016/05/03/howto-enable-auto-screen-rotation-in-the-gnome-shell-for-2-in-1-convertible-laptops-solus-1-1/
# https://github.com/tegan-lamoureux/Rotate-Spectre/blob/master/rotate.py
# #####################################################################################################################################
# additional modules sudo apt-get install libnotify-bin http://www.devdungeon.com/content/desktop-notifications-python-libnotify
# sudo apt-get install python3-notify2
# sudo apt-get install iio-sensor-proxy inotify-tools https://linuxappfinder.com/blog/auto_screen_rotation_in_ubuntu
# sudo apt-get install xbacklight
# https://andym3.wordpress.com/2012/05/27/fixing-natural-scrolling-in-ubuntu-12-04/
# touch screen is fine, the mouse aka and stylus need the x and y axis switvhed in tablet mode
################################ Module inport section #######################################################################
import os                                                                       # Libary used for making system calls
import signal                                                                   # 
import time                                                                     # Used for access to the process sleep libary
import subprocess                                                               # Libary used to call the commands from the operating system
#import notify2
import gi                                                                       #
import re                                                                       #
gi.require_version("Notify", "0.7")                                             # Versioning checks for notify
gi.require_version("AppIndicator3", "0.1")                                      # Versioning checks for Appinidicator for unity
gi.require_version("Gtk", "3.0")                                                # Versonioning checks GTK graphics libary 
from gi.repository import Notify                                                # Notification libary
from subprocess import call                                                     # Subprocess libary for making system calls
from gi.repository import Gtk                                                   # Gtk libary for GUI shell objects
from gi.repository import AppIndicator3 as AppIndicator                         # Indicator libary for task bar
from gi.repository import Notify, GdkPixbuf                                     # notification libary import
from string import digits                                                       # String libary used for rege functions and string manipulation
from time import sleep                                                          # Required to add easy pause into while loop that samples from acceleromoeter
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
cmdpipe = subprocess.Popen("xinput --list | grep 'TouchPad' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)  # Grab the touchpad in preperation for regex functions 
result = cmdpipe.stdout.readline()                                                                   # Execute the above command to retreive the touchpad ID string                       
TouchPadDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])         # Strip out the device ID from the returned String
TouchPadSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                    # String the Slave ID from the original returned string 
# Grab the TouchScreen device Numbers
cmdpipe = subprocess.Popen("xinput --list | grep 'ELAN0732:00' | grep -v 'Pen'  ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
result = cmdpipe.stdout.readline()                                                                   # Execute the above command and return the raw touch screen ID as the PEN/Stylus will have a similar ID the grep -v will remove the any line with PEN in the string
TouchScreenDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])      # Strip the device ID from the returned string by removing anything before the = 
TouchPadSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                    # Strip the device salve id by removing anything betweem the brackets
# Grab the Digitiser/Pen device Numbers     
cmdpipe = subprocess.Popen("xinput --list | grep 'Pen' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
result = cmdpipe.stdout.readline()                                                                   # Execute the command and store the output 
DigitiserDeviceID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])        # Strip out the device ID number is regex looking for a numeric charcters after the an =
DigitiserSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]                   # Strip out the slave ID looking for numeric characters between brackets

######################## DEBUG ###########################
print "Keyboard ID       - "     + KeyboardDeviceID                                                                               # Debug
print "Keyboard Slave id - "     + KeyboardSlaveID                                                                                # Debug
print "Touch Pad ID      - "     + TouchPadDeviceID                                                                               # Debug
print "Touch Pad Slave ID - "    + TouchPadSlaveID                                                                                # Debug
print "Pen Device ID - "         + DigitiserDeviceID                                                                              # Debug 
print "Pen Slave ID - "          + DigitiserSlaveID                                                                               # Debug
print "Touch Screen - "          + TouchScreenDeviceID                                                                            # Debug
print "touch Screen Slave ID - " + TouchPadSlaveID                                                                                # Debug
######################## DEBUG ###########################

def main():
    indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(IndicatorIconPath), AppIndicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    Gtk.main()
    
def build_menu():
    menu = Gtk.Menu()
    #brightness
    item_brightness_up = Gtk.MenuItem('Increase Brightness')
    item_brightness_up.connect('activate', increase_brightness)
    menu.append(item_brightness_up)
    item_brightness_down = Gtk.MenuItem("Decrease Brightness")
    item_brightness_down.connect('activate', decrease_brightness)
    menu.append(item_brightness_down)

    #seperator
    seperator = Gtk.SeparatorMenuItem()
    menu.append(seperator)

    #rotate
    item_rotate = Gtk.MenuItem('Rotate')
    item_rotate.connect('activate', rotate_screen)
    menu.append(item_rotate)

    #Portrait
    item_Portrait = Gtk.MenuItem('Portrait')
    item_Portrait.connect('activate', Portrait)
    menu.append(item_Portrait)

    #flip
    item_flip = Gtk.MenuItem('Flip')
    item_flip.connect('activate', flip_screen)
    menu.append(item_flip)

    #seperator
    seperator = Gtk.SeparatorMenuItem()
    menu.append(seperator)

    #NoteBookMode 
    item_NoteBookMode = Gtk.MenuItem('Notebook Mode')
    item_NoteBookMode.connect('activate', notebook_mode)
    menu.append(item_NoteBookMode)

    #TabletMode 14 and 13 from xinput -list
    item_TabletMode = Gtk.MenuItem('Tablet Mode')
    item_TabletMode.connect('activate', tablet_mode)
    menu.append(item_TabletMode)

    #seperator
    seperator = Gtk.SeparatorMenuItem()
    menu.append(seperator)


    #Automatic application mode menu item
    item_auto = Gtk.MenuItem('Automatic Rotation')
    item_auto.connect('activate', auto_screen)
    menu.append(item_auto)

    #Automatic application mode menu item
    item_man = Gtk.MenuItem('Manual Rotation')
    item_man.connect('activate', man_screen)
    menu.append(item_man)

    #quit
    item_quit = Gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    
    #seperator
    seperator = Gtk.SeparatorMenuItem()
    menu.append(seperator)

    
    return menu

def man_screen(source):
    global applicationMode
    mode = "manualReset"
    applicationMode = mode
    print "Manual mode invoked " + applicationMode

def auto_screen(source):
    global applicationMode
    mode = 'auto"'
    applicationMode = mode

    while applicationMode != "man":
        print "This is where the automatic code is "  +applicationMode# Debug
        pass
        sleep(1)
    

def rotate_screen(source):
    global orientation                          # Global variable for orientation
    global TargetCordinateMatrix                # Blogal variable for the Cordinate Matrix used for screen calbibration
    command = ""                                # Null out the command string just incase
    if orientation == "normal":
        direction = "left"
        TargetCordinateMatrix = stringLeftTransform
        notifications.update("Screen Rotation Enchanced", "Rotating screen left")
    elif orientation == "left":
        direction = "inverted"
        TargetCordinateMatrix = stringInvertedTransform
        notifications.update("Screen Rotation Enchanced", "Rotating screen inverted")
    elif orientation == "inverted":
        direction = "right"
        TargetCordinateMatrix = stringRightTransform
        notifications.update("Screen Rotation Enchanced", "Rotating screen right")
    elif orientation == "right":
        direction = "normal"
        TargetCordinateMatrix = stringNormalTransform
        notifications.update("Screen Rotation Enchanced", "Rotating screen normal")
    
    notifications.show()                                                    # Show notification based on which orientation is to be displayed
    call(["xrandr", "-o", direction])                                       # Call the screen rotation
    command = "xinput set-prop " + DigitiserDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix  #The method above inverts the Pen/Digitiser calibration
    print "this will be the command - " +command                            # DEBUG
    os.system(command)                                                      # Execute the screen transformation
    orientation = direction                                                 # Update the orientation global tracking variable to equal the new adjusted orientation

def automaticMode(source):
    global applicationMode
    notifications.update("Screen Rotation Enchanced", "Rotating screen normal")
    notifications.show()

def flip_screen(source):
    global orientation
    global TargetCordinateMatrix
    command = ""
    if orientation == "normal":
        direction = "inverted"
        notifications.update("Screen Rotation Enchanced", "Inverting screen orientation")
        TargetCordinateMatrix = stringInvertedTransform
    elif orientation == "inverted":
        direction ="normal"
        notifications.update("Screen Rotation Enchanced", "Restoring screen orientation")                              # Update the notification string
        TargetCordinateMatrix = stringNormalTransform                                                                  # Set the transformation matrix variable to normal
    notifications.show()                                                                                               # Show updated notification pannel 
    call(["xrandr", "-o", direction])                                                                                  # Execute screen rotation to the desired orientation
    print "targeted Matrix = " + TargetCordinateMatrix                                                                 # Debug
    orientation = direction
    command = "xinput set-prop " + DigitiserDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix  #The method above inverts the Pen/Digitiser calibration
    print "this will be the command - " +command  # DEBUG
    os.system(command)                                                                                                 # Execute the Pen/Digitiser inversion command
    #natrual Scrolling next here if required
    #touchscreen as well? work out if its necessary

def Portrait(source):
    global orientation                          # Global variable for orientation
    global TargetCordinateMatrix                # Blogal variable for the Cordinate Matrix used for screen calbibration
    command = ""                                # Null out the command string just incase
    # Check what our current state is
    if  orientation == "normal":
        # Change summary and body
        direction = "right"
        notifications.update("Screen Rotation Enchanced", "Switching to Protrait")
        TargetCordinateMatrix = stringRightTransform                                       # Set targeted tranform variable to be right portrait tranformation to match the screen rotation
    else:
        direction ="normal"                                                                # Set the screen direction variable to normal                                  
        notifications.update("Screen Rotation Enchanced", "Switching back to normal from portait")
        #enable the keyboard and mouse inputs
        TargetCordinateMatrix = stringNormalTransform                                      # Set tranformation variable to normal screen orientation
    # Show again
    notifications.show()  
    command = "xinput set-prop " + DigitiserDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix  #The method above inverts the Pen/Digitiser calibration
    print "this will be the command - " +command                                           # DEBUG
    os.system(command)                                                                     # Execute the command       
    call(["xrandr", "-o", direction])                                                      # Execute the screen reorientation
    orientation = direction                                                                # Set the global variable with the current adjusted screen orientation value     

def tablet_mode(source):
    global orientation                          # Global variable for orientation
    global TargetCordinateMatrix                # Blogal variable for the Cordinate Matrix used for screen calbibration
    command = ""                                # Null out the command string just incase
    # Check what our current state is
    if orientation == "normal":
         # Change summary and body
        notifications.update("Screen Rotation Enchanced", "Switching to tablet mode")      # Set Notificationcontent
        notifications.show()                                                               # Show again
        direction = "inverted"                                                             # Set rotation direction to be inverted ready for execution at the end of the function          
        TargetCordinateMatrix = stringInvertedTransform                                    # Set the transformation set to be inverted ready for execution
        #disable the keyboard and mouse inputs inputs
        call(["xinput", "float", KeyboardDeviceID])                                        # Detach the keybvoard
        call(["xinput", "float", TouchPadDeviceID])                                        # Detach the Touch Pad
    elif orientation == "inverted":
        notifications.update("Screen Rotation Enchanced", "The Device is already in tablet mode, reverting")
        TargetCordinateMatrix = stringNormalTransform                                      # Set Transformation Matrix to the normal           
        direction = "normal"                                                               # Set the rotation direction to be altered to normal
    #print "targeted Matrix = " + TargetCordinateMatrix                                    # Debug
    command = "xinput set-prop " + DigitiserDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix  #The method above inverts the Pen/Digitiser calibration
    #print "this will be the command - " +command                                          # DEBUG
    os.system(command)                                                                     # Execute the command       
    call(["xrandr", "-o", direction])                                                      # Execute the screen rotation command
    orientation = direction                                                                # Set the global screen position to equal the adjustment


# 
def notebook_mode(source):
    global orientation                          # Global variable for orientation
    global TargetCordinateMatrix                # Blogal variable for the Cordinate Matrix used for screen calbibration
    command = ""                                # Null out the command string just incase
    TargetCordinateMatrix = stringNormalTransform
    # Check what our current state is
    if orientation == "normal":
         # Change summary and body
        notifications.update("Screen Rotation Enchanced", "The Device is already in notebook mode")
        #enable the keyboard and mouse inputs inputs
    elif orientation == "inverted":
        notifications.update("Screen Rotation Enchanced", "Switching to notebook mode")    # Set the notification
        direction ="normal"                                                                # Set the global screen position to equal the adjustment
    #####################################  Reattach devices ###################################################
    notifications.show()                                                                   # Show notification
    call(["xinput", "reattach", KeyboardDeviceID, KeyboardSlaveID])                        # Reattach the keyboard
    call(["xinput", "reattach", TouchPadDeviceID, TouchPadSlaveID])                        # Reattach the keyboard
    call(["xrandr", "-o", direction])                                                      # Ensure Screen orientation is normal    
    command = "xinput set-prop " + DigitiserDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix  #The method above inverts the Pen/Digitiser calibration
    print "this will be the command - " +command                                           # DEBUG
    os.system(command)                                                                     # Execute the transform matrix command
    #############################################################################################################
    print "targeted Matrix = " + TargetCordinateMatrix                                     # Debug
    orientation = direction                                                                # Set the global variable to be the reset screen orientation
                             

def increase_brightness(source):
    call(["xbacklight", "-inc", "20"])                                                     # Increase the screen brightness using xbacklight

def decrease_brightness(source):
    call(["xbacklight", "-dec", "20"])                                                     # Decrease the screen brightness using xbacklight

#def hmiTransform (orientation):
#    #use the matrix to set the transform
#    print "test " + stringInvertedTransform                                               # Debug


if __name__ == "__main__":
    #make sure the screen is in normal orientation when the script starts
    call(["xrandr", "-o", orientation])
    #keyboard interrupt handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
    