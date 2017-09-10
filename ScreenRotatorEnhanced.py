#!/usr/bin/env python3
# additional modules sudo apt-get install libnotify-bin http://www.devdungeon.com/content/desktop-notifications-python-libnotify
#sudo apt install python3-notify2
#test
import os
import signal
import time
#import notify2
import gi # Test
gi.require_version("Notify", "0.7")
gi.require_version("AppIndicator3", "0.1")
gi.require_version("Gtk", "3.0")
from gi.repository import Notify
from subprocess import call
from gi.repository import Gtk
from gi.repository import AppIndicator3 as AppIndicator
from gi.repository import Notify, GdkPixbuf # notification libary import

APPINDICATOR_ID = "screenrotator"
orientation = "normal"                                                                      # The Default startip state is assumed to be in laptop configuration
ScriptPath = "/home/tassadar/Downloads/ScreenRotator-master/"                               # Required to constrict some commands
NotificationIconPath = "/home/tassadar/Downloads/ScreenRotator-master/notifications.png"    # require to configure the applications notification icon
KeyboardDeviceID = ""                                                                       # This will be used in later functions to disable the hardware keyboard when in tablet mode
TouchScreenDeviceID = ""                                                                    # This will be used to flip the screem inputs whe in tablet mode.
MonitorDeviceName = "eDP-1"                                                                 # This is the screens name as per the output of xrandr -q this will be used to try alter the screen state

Notify.init("Screen Rotiation")
# Use GdkPixbuf to create the proper image type
notifications = Notify.Notification.new("Screen Rotation Enchanced", "Application Started") # Create the Notification Object and set it with the start up values ready for display
image = GdkPixbuf.Pixbuf.new_from_file(NotificationIconPath)                                # Intialise the image object to be used bu the notification system
# Use the GdkPixbuf image
notifications.set_icon_from_pixbuf(image)                                                   # Set the icon Image for the notifications popup   
notifications.set_image_from_pixbuf(image)                                                  # Set the image to be used by the notification popup
notifications.show()                                                                        # Display the first notification stating that the application has started


def main():
    indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('/usr/bin/icon.svg'), AppIndicator.IndicatorCategory.SYSTEM_SERVICES)
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
    elif orientation == "inverted":
        direction ="normal"
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
        call(["ls", "-l"])   
        #direction = "inverted"
        #now adjust the tranform matrix for the touch screen to account for the inverted screen orientation 
        #call([ "xinput set-prop 'Your Touchscreens Name' --type=float 'Coordinate Transformation Matrix' -1 0 1 0 -1 1 0 0 1"])
    
        #disable the keyboard and mouse inputs inputs
    elif orientation == "inverted":
        notifications.update("Screen Rotation Enchanced", "The Device is already in tablet mode")
        # Show again
        notifications.show()
        #direction ="normal"
        #enable the keyboard and mouse inputs
   # call(["xrandr", "-o", direction])
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
        call(["ls", "-l"])   
        #disable the keyboard and mouse inputs inputs
    elif orientation == "inverted":
        notifications.update("Screen Rotation Enchanced", "Switching to notebook mode")
        notifications.show()
        direction ="normal"
        #enable the keyboard and mouse inputs inputs
        #call([ "xinput set-prop 'Your Touchscreens Name' --type=float 'Coordinate Transformation Matrix' 1 0 0 0 1 0 0 0 1"])
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
