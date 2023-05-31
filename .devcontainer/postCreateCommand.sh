jlpm install
jupyter labextension develop . --overwrite
jlpm run build
pip install -e .
pip install yggdrasil-framework