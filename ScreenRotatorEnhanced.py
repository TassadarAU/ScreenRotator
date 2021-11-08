#!/usr/bin/env python3
######################################################################################################################################
# Maintainer - Domenic. aka TassadarAU
# 
# Requirements - gnome based interface 
#
#
# Originaly forked from ScreenRotator https://github.com/frecel/ScreenRotator
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
import gi                                                                       #
import re                                                                       # regular expression library
gi.require_version("Gtk", "3.0")                                                # Versonioning checks GTK graphics libary 
gi.require_version('AppIndicator3', '0.1')                                      # Versonioning checks
gi.require_version('Notify', '0.7')                                             # Versonioning checks
from gi.repository import Notify                                                # Notification libary
from subprocess import call                                                     # Subprocess libary for making system calls
from gi.repository import Gtk                                                   # Gtk libary for GUI shell objects
from gi.repository import AppIndicator3 as AppIndicator                         # Indicator libary for task bar
from gi.repository import Notify, GdkPixbuf                                     # notification libary import
from string import digits                                                       # String libary used for rege functions and string manipulation
from time import sleep                                                          # Required to add easy pause into while loop that samples from acceleromoeter

def NotificationToasty (title,message):
    if readConfigreturnAttribute("notifications") == "enabled":
        notifications.update(title, message)
        notifications.show()

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

def ReadConfigFile(filename):
    lineCount = 0
    with open(filename) as f:
        file_content = f.readlines()
    return file_content

def readConfigreturnAttribute(attribute):
    filename = os.path.join(os.path.dirname(__file__), 'autoRotation.config') 
    with open(filename) as f:
        file_content = f.readlines()
        for line in file_content:
            attributeFile = re.sub(r'[^a-zA-Z0-9--]', '', re.sub('\:.*$',"",line) )
            if attribute == attributeFile:
                data = re.sub('^[^:]*',"", line).split(':')
    return re.sub('\n','', data[1]) #Return value minus new line characters 

def writeConfig(attribute, value):
    lineCount = 0
    filename = os.path.join(os.path.dirname(__file__), 'autoRotation.config') 
    lines = ReadConfigFile(filename)
    for line in lines:
            attributeFile = re.sub(r'[^a-zA-Z0-9--]', '', re.sub('\:.*$',"",line) )
            if attributeFile == attribute:
                lines[lineCount] = attribute +":" + value +"\n"
            lineCount = lineCount + 1
    f = open(filename, "w")
    f.writelines(lines)
    f.close()

def man_screen(source):
    global applicationMode
    applicationMode = "manual"
    writeConfig ("mode",applicationMode)
    NotificationToasty ("Screen Rotation Enchanced",  "Manual mode set")

def auto_screen(source):
    global applicationMode
    applicationMode = 'auto'
    writeConfig ("mode", applicationMode)
    NotificationToasty ("Screen Rotation Enchanced", "Auto mode set")

def currentOrientation():
    cmdpipe = subprocess.Popen("xrandr --query --verbose | grep 'primary' | cut -d ' ' -f 6", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    result = cmdpipe.stdout.readline()  
    result = re.sub(r'[^a-zA-Z0-9--]', '', result)
    return result

def RotateScreen(TargetCordinateMatrix, direction):
    mode = readConfigreturnAttribute("mode")
    if mode != "auto":
        QueryDeviceAddressing()
        result = currentOrientation()
        if direction != result:
            call(["xrandr", "-o", direction])                      
            if DigitiserDeviceID and (not DigitiserDeviceID.isspace()):                                                            # Execute screen rotation to the desired orientation
                command = "xinput set-prop " + DigitiserDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix  # The method above inverts the Pen/Digitiser calibration
                os.system(command)
            if TouchScreenDeviceID and (not TouchScreenDeviceID.isspace()):                                                        # Execute the Pen/Digitiser inversion command
                command = "xinput set-prop " + TouchScreenDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix
                os.system(command) 
            NotificationToasty ("Screen Rotation Enchanced",  "Switching rotating " + direction)
    else:
        NotificationToasty ("Screen Rotation Enchanced",  "Rotation is in auto mode")

def rotate_screen(source):
    global orientation
    orientation = currentOrientation()
    if orientation == "normal":
        RotateScreen (stringLeftTransform, "left") 
        orientation = "left"
    elif orientation == "left":
        RotateScreen (stringInvertedTransform, "inverted") 
        orientation = "inverted"
    elif orientation == "inverted":
        RotateScreen (stringRightTransform, "right")
        orientation = "right"
    elif orientation == "right":
        RotateScreen (stringNormalTransform, "normal")
        orientation = "normal" 

def flip_screen(source):
    global orientation
    orientation = currentOrientation()
    if orientation == "normal":
        RotateScreen (stringInvertedTransform, "inverted") 
    elif orientation == "inverted":
        RotateScreen (stringNormalTransform, "normal")

def Portrait(source):
    global orientation                          
    orientation = currentOrientation()
    # Check what our current state is
    if  orientation == "normal":
        RotateScreen (stringNormalTransform, "right")     
    else:
        RotateScreen (stringNormalTransform, "normal")   

def notebook_mode(source):
    global orientation                          
    orientation = currentOrientation()
    if orientation != "normal":
        RotateScreen (stringNormalTransform, "normal")                                                              # Set the global variable to be the reset screen orientation
                             
def increase_brightness(source):
    call(["xbacklight", "-inc", "20"])                                                     # Increase the screen brightness using xbacklight

def decrease_brightness(source):
    call(["xbacklight", "-dec", "20"])                                                     # Decrease the screen brightness using xbacklight

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
    TouchScreenName = readConfigreturnAttribute("TouchScreen") # read value from config file to make sure we query the correct device

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


###############################################################################################################################
APPINDICATOR_ID = "screenrotator"
global orientation 
orientation = currentOrientation()                                          # The Default startip state is assumed to be in laptop configuration
NotificationIconPath = readConfigreturnAttribute("NotificationIconPath")    # require to configure the applications notification icon
IndicatorIconPath = readConfigreturnAttribute("IndicatorIconPath")          # Indicator icon location path, This will be programaticly set later
Notify.init("Screen Rotiation")                                             # Initialise the notification object with the applications title, This will appear in bold on the notification toatsy
applicationMode = readConfigreturnAttribute("mode")
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
QueryDeviceAddressing()                                                                       

if __name__ == "__main__":
    #make sure the screen is in normal orientation when the script starts
    call(["xrandr", "-o", orientation])
    #keyboard interrupt handler
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
    