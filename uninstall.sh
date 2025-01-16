#!/bin/sh

# Choose InstallPath
INSTALL_PATH=/opt/terminal-colorpicker

# Remove app directory
sudo rm -rvf $INSTALL_PATH

# Remove symbolic link
USR_BIN=/usr/bin
sudo rm -v $USR_BIN/ncolorpicker
