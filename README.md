# ScreenRotator
Small applet for rotating the screen on Unity Desktop forked from https://github.com/frecel/ScreenRotator

![Updated Icon](https://github.com/TassadarAU/ScreenRotator/blob/Enhanced/ScreenCapture.jpg)

ScreenRotator requires python3-gi to work. You can install it by running:
```
sudo apt install python3-gi
sudo apt-get install python3-notify2
sudo apt-get install iio-sensor-proxy inotify-tools
sudo apt-get install xbacklight
sudo apt-get install libnotify-bin

```

Installation Instructions:
1. Copy the script to your /usr/sbin/ Directory (this part is optional you can run the script from anywhere you choose)
2. Create the folder /usr/share/ScreenRotationIndicator Copy the icon and notification graphics files to that location (this part is required         unless you alter the graphics variables to your desired location) 
3. Add an auto start item in your system to execute the following: python ScreenRotatorEnhanced.py
4. Edit the script and change the device if of your screen. use xinput --list to Identify it. All other hardware items such as Pens, touchpad and     keybaords are automaticly identified by the script

Notes:
If you are autostarting ScreenRotator and the icon does not show up in your
system tray change the path to the icon in line 13 of ScreenRotator.py to an
absolute path.

The icon is from Google's Material Desing icon pack (https://materialdesignicons.com/)

This version includes tablet mode, portrait and lanscape modes.
