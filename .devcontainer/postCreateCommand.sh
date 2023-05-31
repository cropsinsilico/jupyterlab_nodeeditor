#!/bin/bash

# Install Python dependencies
pip install pyyaml
pip install jupyter-packaging
pip install yggdrasil-framework

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