import subprocess                                                               # Libary used to call the commands from the operating system
import re                                                                       # Regular expressions library

class DevicesClass(object):
    def __init__(self, screen):
        self.screen = screen 
       # print ("Test Class" + self.DiscoverTouchScreenName () )
        #self.DiscoverTouchScreenName (screen)
        if (self.screen =="auto"):
           # print ("attempting to discover touch screen name") #debug
            self.TouchScreenName      = self.DiscoverTouchScreenName (screen)
        else:
            #print ("using passed in value" + screen) #debug
            self.TouchScreenName      = screen  # system firendly name as displayed in xinput
        #initialise the attributes of the device class
        
        self.KeyboardDeviceID     = " "     # This will be used in later functions to disable the hardware keyboard when in tablet mode
        self.KeyboardSlaveID      = " "     # Slave id for the onboard keyboard
        self.TouchScreenDeviceID  = " "     # This will be used to flip the screem inputs whe in tablet mode.
        self.TouchScreenSlaveID   = " "     # This will beused 
        self.TouchPadDeviceID     = " "     # This will be used to disable the touchpad in tablet mode
        self.TouchPadSlaveID      = " "     # This will be used to disable the touchpad in tablet mode
        self.DigitiserDeviceID    = " "     # Pen/Stylus/Digitiser Device ID
        self.DigitiserSlaveID     = " "     # Pen/Stylus/Digitiser Slave ID

    def RetreiveDeviceID (self, inputValue):
        inputValue  = str(inputValue)
        value = re.sub("[^0-9]", "", inputValue.join(inputValue.split('=')[1:]).split(" ",1 )[0])
        return value

    def RetreiveSlaveID (self, inputValue):
        inputValue  = str(inputValue)
        value = inputValue.join(inputValue.split('=')[1:]).split("(")[1].rsplit(")")[0]   
        return value
    def DiscoverTouchScreenName(self, screen):
        if (screen =="auto" ):
            cmdpipe = subprocess.Popen("xinput --list | grep 'Stylus' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            result = cmdpipe.stdout.readline()
            result = result.decode()
            #print(result) # Debug
            value = re.sub('[^A-Za-z0-9: ]+', '', result.join(result.split()[1:]).split(" ",1 )[0])
            #value = re.sub('[^A-Za-z0-9]+', '', re.sub('\:.*$',"",value))
            #print("Discovering screen device name " + value)  #Debug
            return value
        else:
            return screen
    def QueryDeviceAddressing(self):
        
        #TouchScreenName = self.screen
        cmdpipe = subprocess.Popen("xinput --list | grep 'AT Translated' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result = cmdpipe.stdout.readline()                                                                     
        if result and (not result.isspace()): 
            self.KeyboardDeviceID = self.RetreiveDeviceID(result)
            self.KeyboardSlaveID = self.RetreiveSlaveID(result)
        # Grab the touch pad device numbers
        cmdpipe = subprocess.Popen("xinput --list | grep 'Synaptics' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)  # Grab the touchpad in preperation for regex functions 
        result = cmdpipe.stdout.readline()      
        if result and (not result.isspace()):                                      
            self.TouchPadDeviceID =  self.RetreiveDeviceID(result) 
            self.TouchPadSlaveID = self.RetreiveSlaveID(result) 
        # Grab the TouchScreen device Numbers
        #print ("the touch screen name in query is " + self.TouchScreenName)
        cmdpipe = subprocess.Popen("xinput --list | grep '" + self.TouchScreenName + "' | grep -v 'keyboard'  ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result = cmdpipe.stdout.readline()
        if result and (not result.isspace()):
            self.TouchScreenDeviceID = self.RetreiveDeviceID(result)    
            self.TouchPadSlaveID = self.RetreiveSlaveID(result)                  
        # Grab the Digitiser/Pen device Numbers     
        cmdpipe = subprocess.Popen("xinput --list | grep 'pointer' | grep 'Stylus' | grep 'Pen'", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        result = cmdpipe.stdout.readline()  
        if result and (not result.isspace()): 
            self.DigitiserDeviceID = self.RetreiveDeviceID(result)
            self.DigitiserSlaveID = self.RetreiveSlaveID(result)
        else:
            self.DigitiserDeviceID = ""       
            self.DigitiserSlaveID = ""


    def DebugPrintDeviceIDS(self):
        ######################## DEBUG ###########################
        print ("Keyboard ID       - "    + self.KeyboardDeviceID    )
        print ("Keyboard Slave id - "     + self.KeyboardSlaveID     )
        print ("Touch Pad ID      - "     + self.TouchPadDeviceID    )
        print ("Touch Pad Slave ID - "    + self.TouchPadSlaveID     )
        print ("Pen Device ID - "         + self.DigitiserDeviceID   )
        print ("Pen Slave ID - "          + self.DigitiserSlaveID    )
        print ("Touch Screen - "          + self.TouchScreenDeviceID ) 
        print ("touch Screen Slave ID - " + self.TouchPadSlaveID     ) 
        ######################## DEBUG ########################### 
    #QueryDeviceAddressing()
    #DebugPrintDeviceIDS()s