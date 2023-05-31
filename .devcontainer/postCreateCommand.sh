cd ..
git clone https://github.com/cropsinsilico/nodeeditor-controls
cd nodeeditor-controls/
npm install
npm run build
cd ..
cd jupyterlab_nodeeditor/
jlpm add /workspaces/nodeeditor-controls
jlpm install
jupyter labextension develop . --overwrite
jlpm run build
pip install -e .