import ipywidgets
import traitlets

from ._version import __version__

EXTENSION_VERSION = "~" + __version__

@ipywidgets.register
class NodeEditorModel(ipywidgets.DOMWidget):
    _model_name = traitlets.Unicode('ReteEditorModel').tag(sync=True)
    _model_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    _view_name = traitlets.Unicode('ReteEditorView').tag(sync=True)
    _view_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _view_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)