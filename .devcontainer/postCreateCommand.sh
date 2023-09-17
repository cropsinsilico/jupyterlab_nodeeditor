#!/bin/bash

sudo apt update

#install node and npm
sudo apt install nodejs npm --yes

#update node to the latest
nvm install node
nvm use node
nvm alias default node

# update several packages exist in the original image
pip install --upgrade spyder spyder-kernels conda-repo-cli

