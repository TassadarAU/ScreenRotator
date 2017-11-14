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
# added to disable the hardware keyboard to prevent unwanted keypress whilist holding the unit.
#
# https://askubuntu.com/questions/160945/is-there-a-way-to-disable-a-laptops-internal-keyboard
#
######################################################################################################################################
# additional modules sudo apt-get install libnotify-bin http://www.devdungeon.com/content/desktop-notifications-python-libnotify
#sudo apt install python3-notify2
# sudo apt install iio-sensor-proxy inotify-tools https://linuxappfinder.com/blog/auto_screen_rotation_in_ubuntu


################################ Module inport section #######################################################################
import os
import signal
import time
#import notify2
import gi 
gi.require_version("Notify", "0.7")
gi.require_version("AppIndicator3", "0.1")
gi.require_version("Gtk", "3.0")
from gi.repository import Notify                                                # Notification libary
from subprocess import call                                                     # Subprocess libary for making system calls
from gi.repository import Gtk                                                   # Gtk libary for GUI shell objects
from gi.repository import AppIndicator3 as AppIndicator                         # Indicator libary for task bar
from gi.repository import Notify, GdkPixbuf                                     # notification libary import
###############################################################################################################################

APPINDICATOR_ID = "screenrotator"
orientation = "normal"                                                                               # The Default startip state is assumed to be in laptop configuration
ScriptPath = "/home/tassadar/Documents/Projects/ScreenRotator-master/"                               # Required to constrict some commands
NotificationIconPath = "/home/tassadar/Documents/Projects/ScreenRotator-master/notifications.png"    # require to configure the applications notification icon
KeyboardDeviceID = ""                                                                                # This will be used in later functions to disable the hardware keyboard when in tablet mode
TouchScreenDeviceID = ""                                                                             # This will be used to flip the screem inputs whe in tablet mode.
MonitorDeviceName = "eDP-1"                                                                          # This is the screens name as per the output of xrandr -q this will be used to try alter the screen state
IndicatorIconPath = "/home/tassadar/Documents/Projects/ScreenRotator-master/icon.svg"                # Indicator icon location path, This will be programaticly set later
Notify.init("Screen Rotiation")                                                                      # Initialise the notification object with the applications title, This will appear in bold on the notification toatsy
# Use GdkPixbuf to create the proper image type
notifications = Notify.Notification.new("Screen Rotation Enchanced", "Application Started")          # Create the Notification Object and set it with the start up values ready for display
image = GdkPixbuf.Pixbuf.new_from_file(NotificationIconPath)                                         # Intialise the image object to be used bu the notification system
# Use the GdkPixbuf image
notifications.set_icon_from_pixbuf(image)                                                            # Set the icon Image for the notifications popup   
notifications.set_image_from_pixbuf(image)                                                           # Set the image to be used by the notification popup
notifications.show()                                                                                 # Display the first notification stating that the application has started


def main():
    indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(IndicatorIconPath), AppIndicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    Gtk.main()
    #notification = Notify.Notification.new("Screen Rotator Started")
    #notification.show()

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

    #quit
    item_quit = Gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def rotate_screen(source):
    global orientation
    if orientation == "normal":
        direction = "left"
    elif orientation == "left":
        direction ="normal"
    call(["xrandr", "-o", direction])
    orientation = direction

def flip_screen(source):
    global orientation
    if orientation == "normal":
        direction = "inverted"
        notifications.update("Screen Rotation Enchanced", "Inverting screen orientation")
        # Show again
        notifications.show()
    elif orientation == "inverted":
        direction ="normal"
        notifications.update("Screen Rotation Enchanced", "Restoring screen orientation")
        # Show again
        notifications.show()
    call(["xrandr", "-o", direction])
    orientation = direction
    #The method above inverts the touch screen calibration  

def Portrait(source):
    global orientation
    # Check what our current state is
    if orientation == "normal":
        # Change summary and body
        call("xrandr --output LVDS1 --rotate right")
        notifications.update("Screen Rotation Enchanced", "Switching to Protrait")
        # Show again
        notifications.show()  
        #direction = "inverted"
        #now adjust the tranform matrix for the touch screen to account for the inverted screen orientation 
        #call([ "xinput set-prop 'Your Touchscreens Name' --type=float 'Coordinate Transformation Matrix' -1 0 1 0 -1 1 0 0 1"])
    else:
        notifications.update("Screen Rotation Enchanced", "The Device is already in portrait")
        # Show again
        notifications.show()
        #enable the keyboard and mouse inputs

def tablet_mode(source):
    global orientation
    # Check what our current state is
    if orientation == "normal":
         # Change summary and body
        notifications.update("Screen Rotation Enchanced", "Switching to tablet mode")
        # Show again
        notifications.show()
        #call(["ls", "-l"])   
        direction = "inverted"
        #disable the keyboard and mouse inputs inputs
        #call([xinput float 13])

    elif orientation == "inverted":
        notifications.update("Screen Rotation Enchanced", "The Device is already in tablet mode")
        # Show again
        notifications.show()
        direction ="normal"
        #enable the keyboard and mouse inputs
        call(["xrandr", "-o", direction])
        call(["xinput", reattach, 13, 3])
   # orientation = direction

# 
def notebook_mode(source):
    global orientation
    # Check what our current state is
    if orientation == "normal":
         # Change summary and body
        notifications.update("Screen Rotation Enchanced", "The Device is already in notebook mode")
        # Show again
        notifications.show()
        #disable the keyboard and mouse inputs inputs
    elif orientation == "inverted":
        notifications.update("Screen Rotation Enchanced", "Switching to notebook mode")
        notifications.show()
        direction ="normal"
        #xinput reattach 10 3                                                   #re-enable the keyboard
    call(["xrandr", "-o", direction])
    orientation = direction


def increase_brightness(source):
    call(["xbacklight", "-inc", "20"])

def decrease_brightness(source):
    call(["xbacklight", "-dec", "20"])

if __name__ == "__main__":
    #make sure the screen is in normal orientation when the script starts
    call(["xrandr", "-o", orientation])
    #keyboard interrupt handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
