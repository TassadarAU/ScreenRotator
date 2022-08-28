#!/usr/bin/env python3
######################################################################################################################################
# Maintainer - Domenic. aka TassadarAU
# 
# Requirements - X11 based interface tested on gnome and KDE.
#
#
# Originaly forked from ScreenRotator https://github.com/frecel/ScreenRotator
# Modifications made have been to support devices such as the HP x360 convertable systems. This allows the system to be inverted or 
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
# xrandr --query | grep -v dis | grep connected
################################ Module inport section #######################################################################
import os                                                                       # Libary used for making system calls
import signal                                                                   # 
import subprocess                                                               # Libary used to call the commands from the operating system
import gi                                                                       #
import re                                                                       # regular expression library
gi.require_version("Gtk", "3.0")                                                 
gi.require_version('AppIndicator3', '0.1')                                      
gi.require_version('Notify', '0.7')                                             
from gi.repository import Notify                                                # Notification libary
from subprocess import call                                                     # Subprocess libary for making system calls
from gi.repository import Gtk                                                   # Gtk libary for GUI shell objects
from gi.repository import AppIndicator3 as AppIndicator                         # Indicator libary for task bar
from gi.repository import Notify, GdkPixbuf                                     # notification libary import
from DevicesClass import DevicesClass
from ScreenRotatorUtils import ScreenRotatorUtils

def NotificationToasty (title,message):
    if utilsLibrary.readConfigreturnAttribute("notifications") == "enabled":
        notifications.update(title, message)
        notifications.show()

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
    applicationMode = "manual"
    utilsLibrary.writeConfig ("mode",applicationMode, utilsLibrary.ReadConfigFile('autoRotation.config') )
    NotificationToasty ("Screen Rotation Enchanced",  "Manual mode set")

def auto_screen(source):
    global applicationMode
    applicationMode = 'auto'
    utilsLibrary.writeConfig ("mode", applicationMode, utilsLibrary.ReadConfigFile('autoRotation.config') )
    NotificationToasty ("Screen Rotation Enchanced", "Auto mode set")

def rotate_screen(source):
    global orientation
    orientation = utilsLibrary.currentOrientation()
    mode = utilsLibrary.readConfigreturnAttribute("mode")
    if mode != "auto":
        if orientation == "normal":
            utilsLibrary.RotateScreen (DevicesList, stringLeftTransform, "left") 
            orientation = "left"
        elif orientation == "left":
            utilsLibrary.RotateScreen (DevicesList, stringInvertedTransform, "inverted") 
            orientation = "inverted"
        elif orientation == "inverted":
            utilsLibrary.RotateScreen (DevicesList, stringRightTransform, "right")
            orientation = "right"
        elif orientation == "right":
            utilsLibrary.RotateScreen (DevicesList, stringNormalTransform, "normal")
            orientation = "normal"         
    else:
        NotificationToasty ("Screen Rotation Enchanced",  "Rotation is in auto mode")
    
def flip_screen(source):
    global orientation
    orientation = utilsLibrary.currentOrientation()
    if orientation == "normal":
        utilsLibrary.RotateScreen (DevicesList, stringInvertedTransform, "inverted") 
    elif orientation == "inverted":
        utilsLibrary.RotateScreen (DevicesList, stringNormalTransform, "normal")

def Portrait(source):
    global orientation                          
    orientation = utilsLibrary.currentOrientation()
    # Check what our current state is
    if  orientation == "normal":
        utilsLibrary.RotateScreen (DevicesList, stringNormalTransform, "right")     
    else:
        utilsLibrary.RotateScreen (DevicesList, stringNormalTransform, "normal")   

def notebook_mode(source):
    global orientation                          
    orientation = utilsLibrary.currentOrientation()
    if orientation != "normal":
        utilsLibrary.RotateScreen (DevicesList, stringNormalTransform, "normal")                                                              # Set the global variable to be the reset screen orientation
                             
def increase_brightness(source):
    call(["xbacklight", "-inc", "20"])                                                     # Increase the screen brightness using xbacklight

def decrease_brightness(source):
    call(["xbacklight", "-dec", "20"])                                                     # Decrease the screen brightness using xbacklight

###############################################################################################################################
APPINDICATOR_ID = "screenrotator"
utilsLibrary = ScreenRotatorUtils()
global orientation 
orientation = utilsLibrary.currentOrientation()                                          # The Default startip state is assumed to be in laptop configuration
NotificationIconPath = utilsLibrary.readConfigreturnAttribute("NotificationIconPath")    # require to configure the applications notification icon
IndicatorIconPath = utilsLibrary.readConfigreturnAttribute("IndicatorIconPath")          # Indicator icon location path, This will be programaticly set later
Notify.init("Screen Rotiation")                                             # Initialise the notification object with the applications title, This will appear in bold on the notification toatsy
applicationMode = utilsLibrary.readConfigreturnAttribute("mode")
################################################  the tranformation matrix variables ###########################################
stringInvertedTransform = "-1 0 1 0 -1 1 0 0 1"
stringNormalTransform = "1 0 0 0 1 0 0 0 1"
stringLeftTransform = "0 -1 1 1 0 0 0 0 1"
stringRightTransform = "0 1 0 -1 0 1 0 0 1"
################################################  Start Up notification variables ##############################################
notifications = Notify.Notification.new("Screen Rotation Enchanced", "Application Started")          
image = GdkPixbuf.Pixbuf.new_from_file(NotificationIconPath)                                         
notifications.set_icon_from_pixbuf(image)                                                          
notifications.set_image_from_pixbuf(image)                                                         
NotificationToasty ("Screen Rotation Enchanced", "Application Started")                                                                           
TouchScreenName = utilsLibrary.readConfigreturnAttribute("TouchScreen")
DevicesList = DevicesClass( utilsLibrary.readConfigreturnAttribute("TouchScreen") )
TouchScreenName = DevicesList.DiscoverTouchScreenName( utilsLibrary.readConfigreturnAttribute("TouchScreen"))
DevicesList.QueryDeviceAddressing()
#DevicesList.DebugPrintDeviceIDS()

if __name__ == "__main__":
    #make sure the screen is in normal orientation when the script starts
    call(["xrandr", "-o", orientation])
    #keyboard interrupt handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
    