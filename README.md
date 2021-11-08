# ScreenRotator
Small applet for rotating the screen for the linux Desktop forked from https://github.com/frecel/ScreenRotator

![Updated Icon](https://github.com/TassadarAU/ScreenRotator/blob/Enhanced/ScreenCapture20.04.jpg)

ScreenRotator has several dependencies. You can install it by running the following commands: 
```
sudo apt install python3-gi
sudo apt-get install python3-notify2
sudo apt-get install iio-sensor-proxy inotify-tools
sudo apt-get install xbacklight
sudo apt-get install libnotify-bin

```
Files: 
* AutomaticRotation.py - This is the service that controls auto rotation of the screen by using your acceleromoter. It uses a common config file to control manual and automated operations from the system tray applet
* ScreenRotatorEnhanced - Creats a system tray applet. Toggles manual and autmated screen rotation functionality.
* autoRotation.config - Contains the configurable parameters of the software:
    * TouchScreen:Your touch screen ID
    * mode: Auto or manual operations can be hand crafted or the app indicator can be used to set this value on the fly
    * NotificationIconPath:image for notification toasty/popup
    * IndicatorIconPath: image for application tray icon
    * notifications:enabled - Supress pops and toasty, software runs does its thing doesn't bother you in any way. Other wise screen changes and mode changes have toasty notification


Installation Instructions:
1. Copy the scripts and config files to your /usr/sbin/ Directory (this part is optional you can run the script from anywhere you choose)
2. Create the folder for images for example /usr/share/ScreenRotationIndicator Copy the icon and notification graphics files to that location (this part is required         unless you alter the graphics variables to your desired location) 
3. Add an auto start item in your system to execute the following: python ScreenRotatorEnhanced.py
4. Edit the config file and change the device to that of your screen. use xinput --list to Identify it. All other hardware items such as Pens, touchpad and     keybaords are automaticly identified by the script. The script will use regex to determine the hardware id's. Pens and stylus ids will be rescanned prior to the sreen rotation to ensure the correct cordinate transform is applied

Notes:
I have done alot of recent upgrades and tweaking to this script. It is alot leaner and cleaner than before. Please feel free to use modify this software to your hearts content. 
happt to have any feedback good and bad.

The icon is from Google's Material Desing icon pack (https://materialdesignicons.com/)

This version includes tablet mode, portrait, lanscape modes and complete automation.
