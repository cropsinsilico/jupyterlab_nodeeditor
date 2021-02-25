import ipywidgets
import traitlets

from ._version import __version__

EXTENSION_VERSION = "~" + __version__

@ipywidgets.register
class SocketCollection(ipywidgets.Widget):
    _model_name = traitlets.Unicode('ReteSocketCollectionModel').tag(sync=True)
    _model_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    socket_types = traitlets.Tuple().tag(sync=True)

@ipywidgets.register
class InputSlot(ipywidgets.Widget):
    _model_name = traitlets.Unicode('InputSlotModel').tag(sync=True)
    _model_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)

    key = traitlets.Unicode().tag(sync=True)
    title = traitlets.Unicode().tag(sync=True)
    socket_type = traitlets.Unicode().tag(sync=True)

@ipywidgets.register
class OutputSlot(ipywidgets.Widget):
    _model_name = traitlets.Unicode('InputSlotModel').tag(sync=True)
    _model_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)

    key = traitlets.Unicode().tag(sync=True)
    title = traitlets.Unicode().tag(sync=True)
    socket_type = traitlets.Unicode().tag(sync=True)

@ipywidgets.register
class Component(ipywidgets.Widget):
    _model_name = traitlets.Unicode('ReteComponentModel').tag(sync=True)
    _model_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    title = traitlets.Unicode('Title').tag(sync=True)
    inputs = traitlets.List(values = traitlets.Instance(InputSlot))
    outputs = traitlets.List(values = traitlets.Instance(OutputSlot))
    sockets = traitlets.Instance(SocketCollection)

@ipywidgets.register
class NodeEditorModel(ipywidgets.DOMWidget):
    _model_name = traitlets.Unicode('ReteEditorModel').tag(sync=True)
    _model_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    _view_name = traitlets.Unicode('ReteEditorView').tag(sync=True)
    _view_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _view_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)