#!/bin/bash
# setup_env.sh

echo "=== Updating and installing Chrome + Chromedriver ==="
apt update -qq
apt install chromium-chromedriver -qq

# Create folder if not exist
mkdir -p drivers

# Download Chrome .deb into folder
wget -O drivers/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install Chrome from that folder
apt install ./drivers/google-chrome-stable_current_amd64.deb -qq
