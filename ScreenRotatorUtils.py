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

class ScreenRotatorUtils(object):
    def __init__(self):
        print ("test utils constructor")

    def test():
         print ("test")

    def currentOrientation(self):
        cmdpipe = subprocess.Popen("xrandr --query --verbose | grep 'primary' | cut -d ' ' -f 6", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result = cmdpipe.stdout.readline()  
        result = result.decode()
        result = re.sub(r'[^a-zA-Z0-9--]', '', result)
        return result
    
    def readConfigreturnAttribute(self, attribute):
        filename = os.path.join(os.path.dirname(__file__), 'autoRotation.config') 
        with open(filename) as f:
            file_content = f.readlines()
            for line in file_content:
                attributeFile = re.sub(r'[^a-zA-Z0-9--]', '', re.sub('\:.*$',"",line) )
                if attribute == attributeFile:
                    data = re.sub('^[^:]*',"", line).split(':')
        return re.sub('\n','', data[1]) #Return value minus new line characters 

    def RotateScreen(self, DevicesList, TargetCordinateMatrix, direction):
        DevicesList.QueryDeviceAddressing()
        #DevicesList.DebugPrintDeviceIDS()
        #get current screen orientaion
        result = self.currentOrientation()
        if direction != result:
            #print (TargetCordinateMatrix + " direction target " + direction)
            call(["xrandr", "-o", direction])                      
            if DevicesList.DigitiserDeviceID and (not DevicesList.DigitiserDeviceID.isspace()):                                                            # Execute screen rotation to the desired orientation
                command = "xinput set-prop " + DevicesList.DigitiserDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix  # The method above inverts the Pen/Digitiser calibration
                os.system(command)
            if DevicesList.TouchScreenDeviceID and (not DevicesList.TouchScreenDeviceID.isspace()):                                                        # Execute the Pen/Digitiser inversion command
                command = "xinput set-prop " + DevicesList.TouchScreenDeviceID + " 'Coordinate Transformation Matrix' " + TargetCordinateMatrix
                #print ("this will be the command - " +command ) # DEBUG
                os.system(command) 
           # NotificationToasty ("Screen Auto Rotation", "Switching rotating " + direction)

    def ReadConfigFile(self, filename):
        lineCount = 0
        with open(filename) as f:
            file_content = f.readlines()
        return file_content

    def writeConfig(self, attribute, value, lines):
        lineCount = 0
        filename = os.path.join(os.path.dirname(__file__), 'autoRotation.config') 
        #lines = self.ReadConfigFile(self, filename)
        for line in lines:
                attributeFile = re.sub(r'[^a-zA-Z0-9--]', '', re.sub('\:.*$',"",line) )
                if attributeFile == attribute:
                    lines[lineCount] = attribute +":" + value +"\n"
                lineCount = lineCount + 1
        f = open(filename, "w")
        f.writelines(lines)
        f.close()