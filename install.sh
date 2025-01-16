#!/bin/sh

# Web Script Waring
echo "Please be sure to never run a script from a website without checking it first!"
echo ""
echo "This script will install the terminal-colorpicker on your system."
echo ""
echo "Please make sure you have git and python3 installed."
echo ""
echo "Are you sure you want to continue? (y/n)"
read -r -n 1 response
echo ""
if [ "$response" != "y" ]; then
    echo "Installation aborted."
    exit 1
fi

cd ~

# Choose InstallPath
INSTALL_PATH=/opt/terminal-colorpicker
echo "Install Path: $INSTALL_PATH"

# Create app directory in home folder
sudo mkdir -v -p $INSTALL_PATH

# Clone repository
git clone https://github.com/derDere/terminal-colorpicker.git ~/.TMP_TERMINAL_COLORPICKER

# Go to the cloned repository
cd ~/.TMP_TERMINAL_COLORPICKER

# Install submodules
git submodule update --init --recursive

# Go back to the original path
cd ~

# Move files to app directory
sudo mv -v ~/.TMP_TERMINAL_COLORPICKER/* $INSTALL_PATH

# Remove TMP_TERMINAL_COLORPICKER
sudo rm -rvf ~/.TMP_TERMINAL_COLORPICKER

# Goto the app directory
cd $INSTALL_PATH

# Install Unicurses
sudo ./unicguard/install_unicurses.sh

# Allow execution
sudo chmod +x $INSTALL_PATH/ncolorpicker.sh

# Create symbolic link
USR_BIN=/usr/bin
sudo ln -s $INSTALL_PATH/ncolorpicker.sh $USR_BIN/ncolorpicker

# Go back to the app directory
cd ~
