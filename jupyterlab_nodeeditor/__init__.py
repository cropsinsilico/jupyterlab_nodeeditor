import json
from pathlib import Path

from ._version import __version__

HERE = Path(__file__).parent.resolve()
fn = HERE / "labextension" / "package.json"

with fn.open() as fid:
    data = json.load(fid)


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": data["name"]}]


from .handlers import setup_handlers


def _jupyter_server_extension_points():
    return [{"module": "jupyterlab_nodeeditor"}]


def _load_jupyter_server_extension(server_app):
    """Registers the API handler to receive HTTP requests from the frontend extension.

    Parameters
    ----------
    server_app: jupyterlab.labapp.LabApp
        JupyterLab application instance
    """
    setup_handlers(server_app.web_app)
    server_app.log.info(
        "Registered HelloWorld extension at URL path /jupyterlab_nodeeditor"
    )


from .node_editor import (
    Component,
    InputSlot,
    NodeEditor,
    NodeEditorModel,
    OutputSlot,
    SocketCollection,
    DropDownInputControlModel,
    NumberInputControlModel,
    TextInputControlModel,
)
from .yggdrasil_to_editor import yml_trans
