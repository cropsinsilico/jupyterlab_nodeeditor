import json

import ipywidgets
import traitlets
from IPython.display import display

from ._version import __version__

EXTENSION_VERSION = "~" + __version__


@ipywidgets.register
class SocketCollection(ipywidgets.Widget):
    _model_name = traitlets.Unicode("ReteSocketCollectionModel").tag(sync=True)
    _model_module = traitlets.Unicode("jupyterlab_nodeeditor").tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    socket_types = traitlets.Tuple().tag(sync=True)


@ipywidgets.register
class InputSlot(ipywidgets.Widget):
    _model_name = traitlets.Unicode("ReteInputModel").tag(sync=True)
    _model_module = traitlets.Unicode("jupyterlab_nodeeditor").tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)

    key = traitlets.Unicode().tag(sync=True)
    title = traitlets.Unicode().tag(sync=True)
    multi_connection = traitlets.Bool().tag(sync=True)
    socket_type = traitlets.Unicode().tag(sync=True)
    sockets = traitlets.Instance(SocketCollection).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    def _ipython_display_(self):
        display(ipywidgets.HBox(self.widget()))

    def widget(self):
        # We're going to return this as columns -- left and right.
        name = ipywidgets.HTML(
            f"<b><tt>{self.key}</tt>: {self.title}</b> ({self.socket_type})"
        )
        val = ipywidgets.HTML("")
        return name, val


class InputSlotTrait(traitlets.TraitType):
    default_value = None
    info_text = "A slot type"

    def validate(self, obj, value):
        if isinstance(value, InputSlot):
            return value
        elif not isinstance(value, dict):
            self.error(type(obj), value)
        value.setdefault("sockets", obj.sockets)
        new_obj = InputSlot(**value)
        return new_obj


@ipywidgets.register
class OutputSlot(ipywidgets.Widget):
    _model_name = traitlets.Unicode("ReteOutputModel").tag(sync=True)
    _model_module = traitlets.Unicode("jupyterlab_nodeeditor").tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)

    key = traitlets.Unicode().tag(sync=True)
    title = traitlets.Unicode().tag(sync=True)
    multi_connection = traitlets.Bool().tag(sync=True)
    socket_type = traitlets.Unicode().tag(sync=True)
    sockets = traitlets.Instance(SocketCollection).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    def _ipython_display_(self):
        display(ipywidgets.HBox(self.widget()))

    def widget(self):
        # We're going to return this as columns -- left and right.
        name = ipywidgets.HTML(
            f"<b><tt>{self.key}</tt>: {self.title}</b> ({self.socket_type})"
        )
        val = ipywidgets.HTML("")
        return name, val


class OutputSlotTrait(traitlets.TraitType):
    default_value = None
    info_text = "A slot type"

    def validate(self, obj, value):
        if isinstance(value, OutputSlot):
            return value
        elif not isinstance(value, dict):
            self.error(type(obj), value)
        value.setdefault("sockets", obj.sockets)
        new_obj = OutputSlot(**value)
        return new_obj


# We don't register this, as it is the base class.
class InputControlModel(ipywidgets.Widget):
    key = traitlets.Unicode().tag(sync=True)
    editor = traitlets.ForwardDeclaredInstance("NodeEditorModel").tag(
        sync=True, **ipywidgets.widget_serialization
    )
    _model_module = traitlets.Unicode("jupyterlab_nodeeditor").tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)


@ipywidgets.register
class DropDownInputControlModel(InputControlModel):
    _model_name = traitlets.Unicode("ReteDropDownControlModel").tag(sync=True)
    options = traitlets.List(
        trait=traitlets.Dict(
            value_trait=traitlets.Unicode(), key_trait=traitlets.Unicode()
        )
    ).tag(sync=True)


@ipywidgets.register
class NumberInputControlModel(InputControlModel):
    _model_name = traitlets.Unicode("ReteNumControlModel").tag(sync=True)
    value = traitlets.CInt().tag(sync=True)


@ipywidgets.register
class TextInputControlModel(InputControlModel):
    _model_name = traitlets.Unicode("ReteTextControlModel").tag(sync=True)
    value = traitlets.Unicode().tag(sync=True)


@ipywidgets.register
class Component(ipywidgets.Widget):
    _model_name = traitlets.Unicode("ReteComponentModel").tag(sync=True)
    _model_module = traitlets.Unicode("jupyterlab_nodeeditor").tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    title = traitlets.Unicode("Title").tag(sync=True)
    # We distinguish between name and title because one is displayed on all
    # instances and the other is the name of the component type
    type_name = traitlets.Unicode().tag(sync=True)
    sockets = traitlets.Instance(SocketCollection).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    inputs = traitlets.List(InputSlotTrait()).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    controls = traitlets.List(traitlets.Instance(InputControlModel)).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    outputs = traitlets.List(OutputSlotTrait()).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    @traitlets.default("type_name")
    def _default_type_name(self):
        # slugize the title
        name = "component_" + self.title.replace(" ", "_").lower()
        return name


@ipywidgets.register
class NodeInstanceModel(ipywidgets.Widget):
    _model_name = traitlets.Unicode("ReteNodeModel").tag(sync=True)
    _model_module = traitlets.Unicode("jupyterlab_nodeeditor").tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    _view_name = traitlets.Unicode("ReteNodeView").tag(sync=True)
    _view_module = traitlets.Unicode("jupyterlab_nodeeditor").tag(sync=True)
    _view_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    title = traitlets.Unicode("Title").tag(sync=True)
    # We distinguish between name and title because one is displayed on all
    # instances and the other is the name of the component type
    type_name = traitlets.Unicode("DefaultComponent", allow_none=False).tag(sync=True)
    inputs = traitlets.List(InputSlotTrait()).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    controls = traitlets.List(traitlets.Instance(InputControlModel)).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    outputs = traitlets.List(OutputSlotTrait()).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    display_element = traitlets.Instance(ipywidgets.VBox)

    @traitlets.default("display_element")
    def _default_display_element(self):
        title = ipywidgets.Text()
        traitlets.link((self, "title"), (title, "value"))
        input_grid = ipywidgets.GridspecLayout(len(self.inputs) + 1, 2)
        output_grid = ipywidgets.GridspecLayout(len(self.outputs) + 1, 2)
        box = ipywidgets.VBox([title, input_grid, output_grid])

        def _update_inputs(event):
            input_grid = ipywidgets.GridspecLayout(len(self.inputs) + 1, 2)
            input_grid[0, :] = ipywidgets.Label("Inputs")
            for i, slot in enumerate(self.inputs):
                input_grid[i + 1, 0], input_grid[i + 1, 1] = slot.widget()
            box.children = box.children[:1] + (input_grid,) + box.children[2:]

        def _update_outputs(event):
            output_grid = ipywidgets.GridspecLayout(len(self.outputs) + 1, 2)
            output_grid[0, :] = ipywidgets.Label("Outputs")
            for i, slot in enumerate(self.outputs):
                output_grid[i + 1, 0], output_grid[i + 1, 1] = slot.widget()
            box.children = box.children[:2] + (output_grid,)

        self.observe(_update_inputs, ["inputs"])
        self.observe(_update_outputs, ["outputs"])
        return box


@ipywidgets.register
class NodeEditorModel(ipywidgets.DOMWidget):
    _model_name = traitlets.Unicode("ReteEditorModel").tag(sync=True)
    _model_module = traitlets.Unicode("jupyterlab_nodeeditor").tag(sync=True)
    _model_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    _view_name = traitlets.Unicode("ReteEditorView").tag(sync=True)
    _view_module = traitlets.Unicode("jupyterlab_nodeeditor").tag(sync=True)
    _view_module_version = traitlets.Unicode(EXTENSION_VERSION).tag(sync=True)
    _components = traitlets.List(traitlets.Instance(Component)).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    editorConfig = traitlets.Dict().tag(sync=True)
    selected_node = traitlets.Instance(NodeInstanceModel, allow_none=True).tag(
        sync=True, **ipywidgets.widget_serialization
    )
    nodes = traitlets.List(traitlets.Instance(NodeInstanceModel), default_value=[]).tag(
        sync=True, **ipywidgets.widget_serialization
    )

    def add_component(self, component):
        self._components = self._components + [component]

    def send_config(self, config):
        if isinstance(config, str):
            config = json.loads(config)
        self.send({"name": "setConfig", "args": [config]})

    def sync_config(self):
        self.send({"name": "getConfig", "args": []})


class NodeEditor(traitlets.HasTraits):
    node_editor = traitlets.Instance(NodeEditorModel)
    socket_collection = traitlets.Instance(SocketCollection)
    socket_types = traitlets.Tuple()

    def add_component(self, component):
        if isinstance(component, dict):
            new_component = {"sockets": self.socket_collection}
            new_component.update(component)
            component = Component(**new_component)
        self.node_editor.add_component(component)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        traitlets.link((self, "socket_types"), (self.socket_collection, "socket_types"))

    @traitlets.default("node_editor")
    def _default_node_editor(self):
        return NodeEditorModel()

    @traitlets.default("socket_collection")
    def _default_socket_collection(self):
        return SocketCollection()

    def _ipython_display_(self):
        accordion = ipywidgets.Accordion()

        def update_nodes(change):
            accordion.children = [node.display_element for node in change["new"]]
            for i, node in enumerate(change["new"]):
                accordion.set_title(i, f"Node {i+1} - {node.title}")

        def update_selected(change):
            accordion.selected_index = self.node_editor.nodes.index(change["new"])

        update_nodes({"new": self.node_editor.nodes})
        self.node_editor.observe(update_nodes, ["nodes"])
        self.node_editor.observe(update_selected, ["selected_node"])
        app_layout = ipywidgets.AppLayout(
            header=ipywidgets.Label("Node Editor"),
            left_sidebar=None,
            center=self.node_editor,
            right_sidebar=accordion,
            footer=None,
            pane_heights=[1, "500px", 1],
            pane_widths=[1, 10, "300px"],
        )
        display(app_layout)
