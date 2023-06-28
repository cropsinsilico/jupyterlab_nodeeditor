#!/bin/bash

# Install Python dependencies
pip install pyyaml==6.0
pip install jupyter-packaging==0.12.3
pip install yggdrasil-framework==1.10.0

# Set up Jupyter notebook kernel
python -m ipykernel install --name jlne_env --user

# Install local package in editable mode
pip install -e .

# Install JavaScript dependencies
jlpm install

# Develop a JupyterLab extension
jupyter labextension develop . --overwrite

# Run a build
jlpm run build