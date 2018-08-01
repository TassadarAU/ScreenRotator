import subprocess
from string import digits
import re
from glob import glob       #rgex required for acceleroteter interface
from os import path as op   #required for the accelerpometer interface
import sys                  #required for accceleroteter portion
cmdpipe = subprocess.Popen("xinput --list | grep 'AT Translated' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#xinput --list | grep 'AT Translated' 
result = cmdpipe.stdout.readline()
res =  re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])
print "keyboard Id            - " + res

stage2 = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]
print "Keyboard Slave pointer - " + stage2

cmdpipe = subprocess.Popen("xinput --list | grep 'TouchPad' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#xinput --list | grep 'AT Translated' 
result = cmdpipe.stdout.readline()
touchPadID =  re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])
print "touchPad ID            - " + touchPadID
stringID = "xinput --list-props " + touchPadID + " | grep Matrix "
cmdpipe = subprocess.Popen(stringID, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
result = cmdpipe.stdout.readline()

print stringID 
print result

cmdpipe = subprocess.Popen("xinput --list | grep 'Pen' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
result = cmdpipe.stdout.readline()
StringDigitiserID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])
StringDigitiserSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]
print "Stylus/Digitser ID - " + StringDigitiserID
print "StylusDigitser Slave ID - " + StringDigitiserSlaveID

cmdpipe = subprocess.Popen("xinput --list | grep 'ELAN0732:00' | grep -v 'Pen'  ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
result = cmdpipe.stdout.readline()
StringTouchScreenID = re.sub("[^0-9]", "", result.join(result.split('=')[1:]).split(" ",1 )[0])
StringTouchScreenSlaveID = result.join(result.split('=')[1:]).split("(")[1].rsplit(")")[0]
print "Touch Screen ID - " + StringTouchScreenID
print "Touch Screen SlaveID - " +StringTouchScreenSlaveID

cmdpipe = subprocess.Popen("xinput --list-props " + touchPadID + " | grep 'Matrix' ", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#xinput --list | grep 'AT Translated' 
result = cmdpipe.stdout.readline()
print result
matrixPropertyID = result.split("(")[1].rsplit(")")[0]
print matrixPropertyID

########## Transforms #####################
stringInvertedTransform = "-1 0 1 0 -1 1 0 0 1"
stringNormalTransform = "1 0 0 0 1 0 0 0 1"
stringLeftTransform = "0 -1 1 1 0 0 0 0 1"
stringRightTransform = "0 1 0 -1 0 1 0 0 1"
#set the matrix property inverted:
stringInvertMatrixCMD = "xinput set-prop " + matrixPropertyID + " " + stringInvertedTransform
stringNormalMatrixCMD = "xinput set-prop " + matrixPropertyID + " " + stringNormalTransform
stringLeftMatrixCMD = "xinput set-prop " + matrixPropertyID + " " + stringLeftTransform
stringRightMatrixCMD = "xinput set-prop " + matrixPropertyID + " " + stringRightTransform
print "Inverted matrix        - " + stringInvertMatrixCMD
print "Normal Matrix          - " + stringNormalMatrixCMD
print "Left Matrix            - " + stringLeftMatrixCMD
print "Right Matrix           - " + stringRightMatrixCMD
#https://andym3.wordpress.com/2012/05/27/fixing-natural-scrolling-in-ubuntu-12-04/
#xinput set-prop 11 309 -113 -113
#xinput set-prop 14 309 113 113


def bdopen(fname):
    return open(op.join(basedir, fname))


def read(fname):
    return bdopen(fname).read()

for basedir in glob('/sys/bus/iio/devices/iio:device*'):
    if 'accel' in read('name'):
      stringAccel = read('name')
      print "accelerometer aquired  - " + stringAccel
      break
else:
    sys.stderr.write("Can't find an accellerator device!\n")
    sys.exit(1)




# Configure these to match your hardware (names taken from `xinput` output).
#TOUCHPAD='SynPS/2 Synaptics TouchPad'
#TOUCHSCREEN='Atmel Atmel maXTouch Digitizer'

#if [ -z "$1" ]; then
 # echo "Missing orientation."
 # echo "Usage: $0 [normal|inverted|left|right] [revert_seconds]"
 # echo
 # exit 1
#fi

#function do_rotate
#{
 # xrandr --output $1 --rotate $2

  #TRANSFORM='Coordinate Transformation Matrix'

  #case "$2" in
    #normal)
      #[ ! -z "$TOUCHPAD" ]    && xinput set-prop "$TOUCHPAD"    "$TRANSFORM" 1 0 0 0 1 0 0 0 1
     # [ ! -z "$TOUCHSCREEN" ] && xinput set-prop "$TOUCHSCREEN" "$TRANSFORM" 1 0 0 0 1 0 0 0 1
    #  ;;
   # inverted)
     # [ ! -z "$TOUCHPAD" ]    && xinput set-prop "$TOUCHPAD"    "$TRANSFORM" -1 0 1 0 -1 1 0 0 1
     # [ ! -z "$TOUCHSCREEN" ] && xinput set-prop "$TOUCHSCREEN" "$TRANSFORM" -1 0 1 0 -1 1 0 0 1
     # ;;
    #left)
     # [ ! -z "$TOUCHPAD" ]    && xinput set-prop "$TOUCHPAD"    "$TRANSFORM" 0 -1 1 1 0 0 0 0 1
     # [ ! -z "$TOUCHSCREEN" ] && xinput set-prop "$TOUCHSCREEN" "$TRANSFORM" 0 -1 1 1 0 0 0 0 1
     # ;;
    #right)
    #  [ ! -z "$TOUCHPAD" ]    && xinput set-prop "$TOUCHPAD"    "$TRANSFORM" 0 1 0 -1 0 1 0 0 1
   #   [ ! -z "$TOUCHSCREEN" ] && xinput set-prop "$TOUCHSCREEN" "$TRANSFORM" 0 1 0 -1 0 1 0 0 1
  #    ;;
 # esac
#}
