#!/bin/sh

# Web Script Waring
echo ""
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo " Please be sure to never run a script from a website without checking it first!"
echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
echo ""
echo "This script will install the terminal-colorpicker on your system."
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
echo "Creating app directory..."
sudo mkdir -v -p $INSTALL_PATH

# Clone repository
echo "Cloning repository..."
git clone https://github.com/derDere/terminal-colorpicker.git ~/.TMP_TERMINAL_COLORPICKER

# Go to the cloned repository
echo "Going to the cloned repository..."
cd ~/.TMP_TERMINAL_COLORPICKER

# Install submodules
echo "Installing submodules..."
git submodule update --init --recursive

# Go back to the original path
echo "Going back to the original path..."
cd ~

# Move files to app directory
echo "Moving files to app directory..."
sudo mv -v ~/.TMP_TERMINAL_COLORPICKER/* $INSTALL_PATH

# Remove TMP_TERMINAL_COLORPICKER
echo "Removing TMP_TERMINAL_COLORPICKER..."
sudo rm -rvf ~/.TMP_TERMINAL_COLORPICKER

# Goto the app directory
echo "Going to the app directory..."
cd $INSTALL_PATH

# Install Unicurses
echo "Installing Unicurses..."
sudo ./unicguard/install_unicurses.sh

# Allow execution
echo "Allowing execution..."
sudo chmod +x $INSTALL_PATH/ncolorpicker.sh

# Create symbolic link
echo "Creating symbolic link..."
USR_BIN=/usr/bin
sudo ln -s $INSTALL_PATH/ncolorpicker.sh $USR_BIN/ncolorpicker

# Go back to the app directory
echo "Going back to the app directory..."
cd ~

# Finished
echo "Installation finished."
echo "You can now use the terminal-colorpicker by typing 'ncolorpicker' in your terminal."
echo ""
