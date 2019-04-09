#!/bin/bash

# DO NOT MODIFY THIS FILE

# User's Wallpaper's directory.
#homedir=$( getent passwd "$USER" | cut -d: -f6 )
#dir="$homedir/Pictures/BingWallpapers/"
fl=$(find /proc -maxdepth 2 -user "$(whoami)" -name environ -print -quit)
for i in {1..5}
do
  fl=$(find /proc -maxdepth 2 -user "$(whoami)" -name environ -newer "$fl" -print -quit)
done

export DBUS_SESSION_BUS_ADDRESS
DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS "$fl" | cut -d= -f2-)

python3 ~/BingImagify/image_loader.py
