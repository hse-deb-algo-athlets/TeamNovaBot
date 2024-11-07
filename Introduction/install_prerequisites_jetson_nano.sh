#!/bin/bash

# Update & cleanup the system
echo "Updating and cleaning up the system..."
sudo apt-get update 
sudo dpkg --configure -a
sudo apt-get upgrade -y
sudo apt-get autoremove -y

# Install required tools if not already installed
install_if_not_installed() {
    if ! command -v $1 &> /dev/null; then
        echo "Installing $2..."
        sudo apt-get install -y $2
    else
        echo "$2 is already installed."
    fi
}

# Firefox installation
install_if_not_installed firefox firefox

# Git installation
install_if_not_installed git git

# Python installation
install_if_not_installed python3 python3

# Pip installation
install_if_not_installed pip3 python3-pip

# Install VSCode if not installed
if ! command -v code &> /dev/null; then
    echo "Installing Visual Studio Code..."
    wget -N -O vscode-linux-deb.arm64.deb https://update.code.visualstudio.com/latest/linux-deb-arm64/stable
    sudo apt install ./vscode-linux-deb.arm64.deb
else
    echo "Visual Studio Code is already installed."
fi

# Install Jtop for Jetson system monitoring
if ! command -v jtop &> /dev/null; then
    echo "Installing Jtop..."
    sudo -H pip3 install -U jetson-stats
else
    echo "Jtop is already installed."
fi

# Ensure Docker is installed and set up permissions
if ! command -v docker &> /dev/null; then
    echo "Docker is already installed."
else
    echo "Setting up Docker permissions for user..."
    sudo groupadd docker
    sudo usermod -aG docker $USER
    sudo chmod 666 /var/run/docker.sock
fi

# Install Rye (Python Toolchain Manager)
if ! command -v rye &> /dev/null; then
    echo "Installing Rye..."
    curl -sSf https://rye.astral.sh/get | bash
    echo 'source "$HOME/.rye/env"' >> ~/.bashrc
    source ~/.bashrc
else
    echo "Rye is already installed."
fi

# Clone the project repository
DEV_DIR="/home/johbaum8/DEV"
REPO_URL="<repo-url>"

if [ ! -d "$DEV_DIR" ]; then
    echo "Creating development directory..."
    mkdir -p $DEV_DIR
fi

cd $DEV_DIR

if [ ! -d "$DEV_DIR/build-your-own-chatbot" ]; then
    echo "Cloning the project repository..."
    git clone $REPO_URL
else
    echo "Repository already cloned."
fi

# VSCode recommended extensions setup
echo "Setting up VSCode recommended extensions..."
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension esbenp.prettier-vscode
code --install-extension foxundermoon.shell-format
code --install-extension ms-azuretools.vscode-docker
code --install-extension rangav.vscode-thunder-client
code --install-extension mhutchie.git-graph
code --install-extension ms-vscode-remote.remote-containers
code --install-extension ms-python.isort
code --install-extension ms-toolsai.jupyter

# Set up project environment and synchronize dependencies
PROJECT_DIR="$DEV_DIR/build-your-own-chatbot"

if [ -d "$PROJECT_DIR" ]; then
    echo "Navigating to the project directory..."
    cd $PROJECT_DIR
    echo "Synchronizing dependencies with Rye..."
    rye sync
else
    echo "Project directory not found. Ensure the repository was cloned correctly."
fi

# Final reboot
echo "Rebooting system to apply changes..."
sudo reboot