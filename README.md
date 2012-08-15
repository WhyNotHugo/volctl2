# Volume Control

A simple Volume Control application, mainly tailored for my Logitech MX Performance.  
I like to use the side buttons (identified as m10 and m13) to control my volume.

This simple application handles this, volume key on media keyboards, as well as showing a notification with the current volume, and controls to mute all sound from there.

This application has close to zero flexibility, but the source might help as a reference to others (how to globally bind a mouse button using Xlib, proper pynotify action handling, etc).

Feel free to use this as a reference for anything you like.  The design isn't the best I've dont, but it's quite understandable, efficient, and works.

## Installation

If you're running ArchLinux, download the PKGBUILD, and run "makepkg -sci".  Otherwise, download the source, and run `python2 setup.py install`.

## Usage

Run `volctld` to run the daemon.  Volume keys should work right away, and m10 and 13 control sound volume as well.

Copyright (c) 2012 Hugo Osvaldo Barrera &lt;hugo@osvaldobarrera.com.ar&gt;
