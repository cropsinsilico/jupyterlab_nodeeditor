try:
    from ._version import __version__
except ImportError:
    # Fallback when using the package in dev mode without installing
    # in editable mode with pip. It is highly recommended to install
    # the package from a stable release or in editable mode:
    # https://pip.pypa.io/en/stable/topics/local-project-installs/
    import warnings

    warnings.warn("Importing 'jupyterlab_nodeeditor' outside a proper installation.")
    __version__ = "dev"
from .handlers import setup_handlers


def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": "jupyterlab_nodeeditor"}]


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
from .yggdrasil_to_editor import editor_yaml, yml_trans
