#!/bin/bash

# This is a script to automate the installation process

# run jlpm install
jlpm install

# run jupyter labextension develop
jupyter labextension develop . --overwrite

# run jlpm build
jlpm run build

# run pip install
pip install -e .

# install yggdrasil-framework
pip install yggdrasil-framework