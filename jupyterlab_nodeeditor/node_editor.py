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
    _model_name = traitlets.Unicode('ReteInputModel').tag(sync=True)
    _model_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)

    key = traitlets.Unicode().tag(sync=True)
    title = traitlets.Unicode().tag(sync=True)
    socket_type = traitlets.Unicode().tag(sync=True)
    sockets = traitlets.Instance(SocketCollection).tag(
        sync=True, **ipywidgets.widget_serialization)

@ipywidgets.register
class OutputSlot(ipywidgets.Widget):
    _model_name = traitlets.Unicode('ReteOutputModel').tag(sync=True)
    _model_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)

    key = traitlets.Unicode().tag(sync=True)
    title = traitlets.Unicode().tag(sync=True)
    socket_type = traitlets.Unicode().tag(sync=True)
    sockets = traitlets.Instance(SocketCollection).tag(
        sync=True, **ipywidgets.widget_serialization)

@ipywidgets.register
class Component(ipywidgets.Widget):
    _model_name = traitlets.Unicode('ReteComponentModel').tag(sync=True)
    _model_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    title = traitlets.Unicode('Title').tag(sync=True)
    inputs = traitlets.List(traitlets.Instance(InputSlot)).tag(
        sync=True, **ipywidgets.widget_serialization)
    outputs = traitlets.List(traitlets.Instance(OutputSlot)).tag(
        sync=True, **ipywidgets.widget_serialization)
    sockets = traitlets.Instance(SocketCollection).tag(
        sync=True, **ipywidgets.widget_serialization)

@ipywidgets.register
class NodeEditorModel(ipywidgets.DOMWidget):
    _model_name = traitlets.Unicode('ReteEditorModel').tag(sync=True)
    _model_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    _view_name = traitlets.Unicode('ReteEditorView').tag(sync=True)
    _view_module = traitlets.Unicode('jupyterlab_nodeeditor').tag(sync=True)
    _view_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)