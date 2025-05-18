#!/bin/bash

# Update package list
sudo apt update

# Install Node.js and npm
sudo apt install -y nodejs npm

# Install Xvfb
sudo apt install -y xvfb

# Install Chromium
sudo apt install -y chromium-browser

# Install Puppeteer
npm install puppeteer
