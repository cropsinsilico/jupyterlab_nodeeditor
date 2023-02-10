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


def _initialize_hotfix():
    """
    This is a gross monkeypatch to address
    https://github.com/ipython/ipykernel/issues/1090
    """
    import ipywidgets

    ipywidgets.Widget.class_traits()["comm"].klass = "ipykernel.comm.comm.BaseComm"


from .node_editor import (
    Component,
    ConnectionModel,
    DropDownInputControlModel,
    InputSlot,
    NodeEditor,
    NodeEditorModel,
    NumberInputControlModel,
    OutputSlot,
    SocketCollection,
    TextInputControlModel,
)
