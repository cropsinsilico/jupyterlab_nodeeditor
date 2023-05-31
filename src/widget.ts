/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import * as Rete from 'rete';
import type {
  NodeData,
  WorkerInputs,
  WorkerOutputs,
  Data
} from 'rete/types/core/data';
import ConnectionPlugin from 'rete-connection-plugin';
import ContextMenuPlugin from 'rete-context-menu-plugin';
import VueRenderPlugin from 'rete-vue-render-plugin';
import AutoArrangePlugin from 'rete-auto-arrange-plugin';
import {
  DOMWidgetModel,
  DOMWidgetView,
  uuid,
  unpack_models
} from '@jupyter-widgets/base';
import type { ISerializers } from '@jupyter-widgets/base';
import { MODULE_NAME, MODULE_VERSION } from './version';
import { ReteControlModel } from './controls';

export class ReteSocketCollectionModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      _model_name: ReteSocketCollectionModel.model_name,
      _model_module: ReteSocketCollectionModel.model_module,
      _model_module_version: ReteSocketCollectionModel.model_module_version,
      socket_types: ['number', 'string']
    };
  }

  async initialize(attributes: any, options: any): Promise<void> {
    this.socket_instances = new Map<string, Rete.Socket>();
    await super.initialize(attributes, options);
    this.on('change:socket_types', this.socketTypesChanged, this);
    this.socketTypesChanged();
  }

  socketTypesChanged(): void {
    this.socket_types = this.get('socket_types');
    this.socket_types = [
      ...new Set([...this.socket_types, ...this.get('socket_types')])
    ];
    this.socket_types.forEach(e => this.getSocket(e));
  }

  getSocket(socketName: string): Rete.Socket {
    if (this.socket_instances.get(socketName) === undefined) {
      this.socket_instances.set(socketName, new Rete.Socket(socketName));
    }
    return this.socket_instances.get(socketName);
  }

  socket_types: string[];
  socket_instances: Map<string, Rete.Socket>;
  static model_name = 'ReteSocketCollectionModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}

export class ReteConnectionModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      source_node: null,
      source_key: null,
      destination_node: null,
      destination_key: null,
      _model_name: ReteConnectionModel.model_name,
      _model_module: ReteConnectionModel.model_module,
      _model_module_version: ReteConnectionModel.model_module_version,
      _view_name: ReteConnectionModel.view_name,
      _view_module: ReteConnectionModel.view_module,
      _view_module_version: ReteConnectionModel.view_module_version
    };
  }

  async initialize(attributes: any, options: any): Promise<void> {
    super.initialize(attributes, options);
    this.source_node = this.get('source_node');
    this.source_key = this.get('source_key');
    this.destination_node = this.get('destination_node');
    this.destination_key = this.get('destination_key');
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    source_node: { deserialize: unpack_models },
    destination_node: { deserialize: unpack_models }
  };

  _connection: Rete.Connection;
  source_node: ReteNodeModel;
  source_key: string;
  destination_node: ReteNodeModel;
  destination_key: string;
  static model_name = 'ReteConnectionModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ReteConnectionView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export class ReteConnectionView extends DOMWidgetView {
  async render(): Promise<void> {
    super.render();
    return this.setupEventListeners();
  }

  async setupEventListeners(): Promise<void> {
    return;
  }

  declare model: ReteConnectionModel;
}

abstract class ReteIOModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      key: undefined,
      title: undefined,
      multi_connection: undefined,
      socket_type: undefined,
      _model_name: ReteIOModel.model_name,
      _model_module: ReteIOModel.model_module,
      _model_module_version: ReteIOModel.model_module_version
    };
  }

  async initialize(attributes: any, options: any): Promise<void> {
    super.initialize(attributes, options);
    this.key = this.get('key');
    this.title = this.get('title');
    this.multi_connection = this.get('multi_connection');
    this.socket_type = this.get('socket_type');
    this.sockets = this.get('sockets');
  }

  // Probably a better way to do this with generics, etc, but.
  public abstract getInstance(): Rete.Input | Rete.Output;

  key: string;
  title: string;
  multi_connection: boolean;
  socket_type: string;
  sockets: ReteSocketCollectionModel;
  static model_name = 'ReteIOModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    sockets: { deserialize: unpack_models }
  };
}

export class ReteInputModel extends ReteIOModel {
  defaults(): any {
    return {
      ...super.defaults(),
      _model_name: ReteInputModel.model_name
    };
  }

  getInstance(): Rete.Input {
    // Disabled for time being
    if (!this._instance) {
      return new Rete.Input(
        this.key,
        this.title,
        this.sockets.getSocket(this.socket_type),
        this.multi_connection
      );
    }
    return this._instance;
  }

  _instance: Rete.Input;
  static model_name = 'ReteInputModel';
}

export class ReteOutputModel extends ReteIOModel {
  defaults(): any {
    return {
      ...super.defaults(),
      _model_name: ReteOutputModel.model_name
    };
  }

  getInstance(): Rete.Output {
    // Disabled for time being
    if (!this._instance) {
      return new Rete.Output(
        this.key,
        this.title,
        this.sockets.getSocket(this.socket_type),
        this.multi_connection
      );
    }
    return this._instance;
  }

  _instance: Rete.Output;
  static model_name = 'ReteOutputModel';
}

export class ReteComponentModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      sockets: undefined,
      _model_name: ReteComponentModel.model_name,
      _model_module: ReteComponentModel.model_module,
      _model_module_version: ReteComponentModel.model_module_version
    };
  }

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  async initialize(attributes: any, options: any): Promise<void> {
    super.initialize(attributes, options);
    this.sockets = this.get('sockets');
    this.title = this.get('title');
    this.inputs = this.get('inputs');
    this.outputs = this.get('outputs');
    this.controls = this.get('controls');
    this.type_name = this.get('type_name');
    await this.createComponent();
  }

  createComponent(): void {
    const thisTypeName = this.type_name;
    const title = this.title;
    const inputs = this.inputs;
    const outputs = this.outputs;
    const controls = this.controls;
    this._rete_component = new (class ThisComponent extends Rete.Component {
      constructor(_title: string) {
        super(title);
      }
      async builder(node: Rete.Node): Promise<void> {
        node.meta.componentType = thisTypeName;
        node.meta.inputSlots = inputs;
        node.meta.outputSlots = outputs;
        node.meta.controls = controls;
        inputs.forEach((e: ReteInputModel) => {
          node.addInput(e.getInstance());
        });
        outputs.forEach((e: ReteOutputModel) => {
          node.addOutput(e.getInstance());
        });
        controls.forEach((e: ReteControlModel) => {
          node.addControl(e.getInstance());
        });
      }
      worker(
        node: NodeData,
        inputs: WorkerInputs,
        outputs: WorkerOutputs,
        ...args: unknown[]
      ): void {
        return;
      }
      componentId: string;
    })('');
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    sockets: { deserialize: unpack_models },
    inputs: { deserialize: unpack_models },
    outputs: { deserialize: unpack_models },
    controls: { deserialize: unpack_models }
  };

  // the inputs and outputs will need serializers and deserializers
  _rete_component: Rete.Component;
  sockets: ReteSocketCollectionModel;
  title: string;
  type_name: string;
  inputs: ReteInputModel[];
  outputs: ReteOutputModel[];
  controls: ReteControlModel[];
  static model_name = 'ReteComponentModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}

export class ReteNodeModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      title: 'Empty Title',
      type_name: 'DefaultComponent',
      inputs: [],
      outputs: [],
      controls: [],
      _model_name: ReteNodeModel.model_name,
      _model_module: ReteNodeModel.model_module,
      _model_module_version: ReteNodeModel.model_module_version,
      _view_name: ReteNodeModel.view_name,
      _view_module: ReteNodeModel.view_module,
      _view_module_version: ReteNodeModel.view_module_version
    };
  }

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  async initialize(attributes: any, options: any): Promise<void> {
    super.initialize(attributes, options);
    this.on('change:title', this.changeTitle, this);
    this.on('change:inputs', this.changeInputs, this);
    this.on('change:outputs', this.changeOutputs, this);
    this.on('change:controls', this.changeControls, this);
  }

  changeTitle(): void {
    this._node.name = this.get('title');
    this.title = this.get('title');
    this._node.update();
  }

  changeInputs(): void {
    const newInputs: ReteInputModel[] = this.get('inputs') || [];
    const oldInputs: ReteInputModel[] = this.previous('inputs') || [];
    for (const remEl of oldInputs.filter(_ => !newInputs.includes(_))) {
      // These are instances, so we match based on keys
      this._node.removeInput(this._node.inputs.get(remEl.key));
    }
    for (const newEl of newInputs.filter(_ => !oldInputs.includes(_))) {
      if (!this._node.inputs.has(newEl.getInstance().key)) {
        this._node.addInput(newEl.getInstance());
      }
    }
    this._node?.update();
    this.inputs = this.get('inputs');
  }

  changeOutputs(): void {
    const newOutputs: ReteOutputModel[] = this.get('outputs') || [];
    const oldOutputs: ReteOutputModel[] = this.previous('outputs') || [];
    for (const remEl of oldOutputs.filter(_ => !newOutputs.includes(_))) {
      // These are instances, so we match based on keys
      this._node?.removeOutput(this._node.outputs.get(remEl.key));
    }
    for (const newEl of newOutputs.filter(_ => !oldOutputs.includes(_))) {
      if (!this._node.outputs.has(newEl.getInstance().key)) {
        this._node?.addOutput(newEl.getInstance());
      }
    }
    this._node?.update();
    this.outputs = this.get('outputs');
  }

  changeControls(): void {
    const newControls: ReteControlModel[] = this.get('controls') || [];
    const oldControls: ReteControlModel[] = this.previous('controls') || [];
    for (const remEl of oldControls.filter(_ => !newControls.includes(_))) {
      // These are instances, so we match based on keys
      this._node?.removeControl(this._node.controls.get(remEl.key));
    }
    for (const newEl of newControls.filter(_ => !oldControls.includes(_))) {
      if (!this._node.controls.has(newEl.getInstance().key)) {
        this._node?.addControl(newEl.getInstance());
      }
    }
    this.controls = this.get('controls');
    this._node?.update();
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    inputs: { deserialize: unpack_models },
    outputs: { deserialize: unpack_models },
    controls: { deserialize: unpack_models }
  };

  // the inputs and outputs will need serializers and deserializers
  title: string;
  type_name: string;
  _node?: Rete.Node;
  inputs: ReteInputModel[] = [];
  outputs: ReteOutputModel[] = [];
  controls: ReteControlModel[] = [];
  static model_name = 'ReteNodeModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ReteNodeView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export class ReteNodeView extends DOMWidgetView {
  async render(): Promise<void> {
    super.render();
    return this.setupEventListeners();
  }

  async setupEventListeners(): Promise<void> {
    return;
  }

  model: ReteNodeModel;
}

export class ReteEditorModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      editorConfig: {},
      _components: [],
      selected_node: undefined,
      nodes: [],
      connections: [],
      _model_name: ReteEditorModel.model_name,
      _model_module: ReteEditorModel.model_module,
      _model_module_version: ReteEditorModel.model_module_version,
      _view_name: ReteEditorModel.view_name,
      _view_module: ReteEditorModel.view_module,
      _view_module_version: ReteEditorModel.view_module_version
    };
  }

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  async initialize(attributes: any, options: any): Promise<void> {
    super.initialize(attributes, options);
    this.engine = new Rete.Engine(`${MODULE_NAME}@${MODULE_VERSION}`);
    this.on('change:_components', this.addNewComponent, this);
    this.on('change:nodes', () => (this.nodes = this.get('nodes')));
    this.on('msg:custom', this.onCommand.bind(this));
    this.addNewComponent();
  }

  async updateViews(): Promise<void> {
    for (const viewId of Object.keys(this.views)) {
      await this.views[viewId].then(_v => {
        const v = _v as ReteEditorView;
        v.editor.view.area.update();
        for (const [node, nodeView] of v.editor.view.nodes) {
          node.update();
          nodeView.update();
        }
      });
    }
  }

  private async onCommand(command: any, buffers: any) {
    let newConfig: Data;
    const myConfig: { [key: string]: any } = {};
    switch (command.name) {
      case 'setConfig':
        newConfig = command.args[0] as Data;
        this.updateViews();
        for await (const viewId of Object.keys(this.views)) {
          const view = await this.views[viewId];
          (view as ReteEditorView).editor.fromJSON(newConfig);
        }
        break;
      case 'getConfig':
        for await (const viewId of Object.keys(this.views)) {
          const view = await this.views[viewId];
          myConfig[viewId] = (view as ReteEditorView).editor.toJSON() as any;
        }
        this.editorConfig = myConfig;
        this.set('editorConfig', this.editorConfig);
        this.save();
        break;
      case 'arrangeNodes':
        for await (const viewId of Object.keys(this.views)) {
          const view = (await this.views[viewId]) as ReteEditorView;
          for (const node of view.editor.nodes) {
            view.editor.trigger('arrange' as any, { node });
          }
        }
        break;
      default:
        break;
    }
  }
  addNewComponent(): void {
    this._components = this.get('_components');
    this._components.forEach(v => {
      if (this.engine.components.get(v.title) === undefined) {
        this.engine.register(v._rete_component);
      }
    });
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    _components: { deserialize: unpack_models },
    nodes: { deserialize: unpack_models },
    selected_node: { deserialize: unpack_models },
    connections: { deserialize: unpack_models }
  };

  _components: ReteComponentModel[];
  nodes: ReteNodeModel[];
  connections: ReteConnectionModel[];
  engine: Rete.Engine;
  editorConfig: { [key: string]: any };
  static model_name = 'ReteEditorModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ReteEditorView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}
export class ReteEditorView extends DOMWidgetView {
  render(): void {
    this.el.classList.add('retejseditor');
    this.div = document.createElement('div');
    this.divId = 'rete-editor-' + uuid();
    this.div.classList.add('retejseditorDiv');
    this.div.setAttribute('id', this.divId);
    this.el.appendChild(this.div);
    //await this.editor.fromJSON(editorData as any);
    this.setupListeners();
    this.displayed.then(() => this.setupEditor());
  }

  setupListeners(): void {
    this.model.on('change:_components', this.addNewComponent, this);
    this.model.on('change:nodes', this.updateNodes, this);
    this.model.on('change:connections', this.updateConnections, this);
  }

  addNewComponent(): void {
    const components: ReteComponentModel[] = this.model.get('_components');
    components.forEach(v => {
      if (this.editor.components.get(v.title) === undefined) {
        this.editor.register(v._rete_component);
      }
    });
  }

  async setupEditor(): Promise<void> {
    this.editor = new Rete.NodeEditor(
      `${MODULE_NAME}@${MODULE_VERSION}`,
      this.div
    );
    this.editor.use(VueRenderPlugin);
    this.editor.use(ConnectionPlugin);
    this.editor.use(ContextMenuPlugin);
    this.editor.use(AutoArrangePlugin, { margin: { x: 25, y: 25 }, depth: 0 });
    this.editor.register(defaultComponent);
    this.editor.on(['nodetranslated'], async () => {
      this.model.updateViews();
    });
    this.editor.on(['noderemoved'], async (node: Rete.Node) => {
      await this.removeNode(node);
      this.model.updateViews();
    });
    this.editor.on(['nodeselected'], async (node: Rete.Node) => {
      // Figure out which NodeModel it corresponds to
      this.model.set('selected_node', node.meta.nodeModel);
      this.model.save_changes();
    });
    this.editor.on(['nodecreated'], async (node: Rete.Node) => {
      await this.createNewNode(node);
      this.model.updateViews();
    });
    this.editor.on(
      ['connectionremoved'],
      // Note that I *believe* that the connectionremoved function is called
      // whenever a connection is clicked on.  That's not super ideal, since
      // we really only want to sync when the connection has been deleted.
      // We may actually eventually want to explore using connectiondrop, which
      // may fire only when the mouse is lifted.
      async (connection: Rete.Connection) => this.removeConnection(connection)
    );
    this.editor.on(['connectioncreated'], async (connection: Rete.Connection) =>
      this.createConnection(connection)
    );
    this.editor.on(
      [
        'connectioncreated',
        'connectionremoved',
        'nodecreated',
        'noderemoved',
        'componentregister'
      ],
      async () => this.updateConfig()
    );
    this.editor.view.resize();
    this.div.style.height = null;
    this.addNewComponent();
    return this.addInitialNodes(), this.addInitialConns();
  }

  private async addInitialConns(): Promise<void> {
    const conns: ReteConnectionModel[] = this.model.get('connections');
    console.log('hahaha');
    for (const newConn of conns) {
      console.log('Found a new connection', newConn);
      if (newConn._connection === undefined) {
        // We need to get our connections list and then look at the difference.

        const connData: { [key: string]: unknown } = {};
        connData['connectionModel'] = newConn;
        const sourceNode = newConn.source_node._node;
        const destNode = newConn.destination_node._node;
        const initialConnections: Rete.Connection[] =
          sourceNode.getConnections();
        this.editor.connect(
          sourceNode.outputs.get(newConn.source_key),
          destNode.inputs.get(newConn.destination_key),
          connData
        );
        const finalConnections: Rete.Connection[] = sourceNode.getConnections();
        const newlyAdded = finalConnections.filter(
          x => !initialConnections.includes(x)
        );
        if (newlyAdded.length !== 1) {
          // console.log('Initial:', initialConnections);
          // console.log('Final:', finalConnections);
          // console.log('Intersection:', newlyAdded);
        }
        newConn._connection = newlyAdded[0];
      }
    }
  }
  private async addInitialNodes(): Promise<void> {
    const nodes: ReteNodeModel[] = this.model.get('nodes');
    for (const newNode of nodes) {
      if (newNode._node === undefined) {
        // console.log('Adding new node', newNode);
        newNode._node = new Rete.Node(newNode.get('title'));
        newNode._node.meta.nodeModel = newNode;
        newNode.changeInputs();
        newNode.changeOutputs();
        newNode.changeControls();
      }
      if (!this.editor.nodes.includes(newNode._node)) {
        this.editor.addNode(newNode._node);
      }
    }
  }

  async updateConfig(): Promise<void> {
    this.model.editorConfig = this.editor.toJSON();
    // console.log('Updating config', this.model.editorConfig);
    this.model.set('editorConfig', this.model.editorConfig);
    this.model.save();
  }

  async updateNodes(model: ReteEditorModel): Promise<void> {
    const oldNodes: ReteNodeModel[] = model.previous('nodes');
    const newNodes: ReteNodeModel[] = model.get('nodes');
    for (const remNode of oldNodes.filter(_ => !newNodes.includes(_))) {
      // These are instances, so we match based on keys
      if (this.editor.nodes.includes(remNode._node)) {
        this.editor.removeNode(remNode._node);
      }
    }
    for (const newNode of newNodes.filter(_ => !oldNodes.includes(_))) {
      if (newNode._node === undefined) {
        newNode._node = new Rete.Node(newNode.get('title'));
        newNode._node.meta.nodeModel = newNode;
        newNode.changeInputs();
        newNode.changeOutputs();
        newNode.changeControls();
      }
      if (!this.editor.nodes.includes(newNode._node)) {
        this.editor.addNode(newNode._node);
        //(this.editor as any).arrange(newNode._node);
        const node = newNode._node;
        (this.editor as any).trigger('arrange', { node });
      }
    }
  }

  async updateConnections(model: ReteConnectionModel): Promise<void> {
    const oldConns: ReteConnectionModel[] = model.previous('connections');
    const newConns: ReteConnectionModel[] = model.get('connections');
    for (const remConn of oldConns.filter(_ => !newConns.includes(_))) {
      // These are instances, so we match based on keys
      // console.log('Removing old connection', remConn);
      this.editor.removeConnection(remConn._connection);
    }
    for (const newConn of newConns.filter(_ => !oldConns.includes(_))) {
      // console.log('Found a new connection', newConn);
      if (newConn._connection === undefined) {
        // We need to get our connections list and then look at the difference.

        const connData: { [key: string]: unknown } = {};
        connData['connectionModel'] = newConn;
        const sourceNode = newConn.source_node._node;
        const destNode = newConn.destination_node._node;
        const initialConnections: Rete.Connection[] =
          sourceNode.getConnections();
        this.editor.connect(
          sourceNode.outputs.get(newConn.source_key),
          destNode.inputs.get(newConn.destination_key),
          connData
        );
        const finalConnections: Rete.Connection[] = sourceNode.getConnections();
        const newlyAdded = finalConnections.filter(
          x => !initialConnections.includes(x)
        );
        if (newlyAdded.length !== 1) {
          console.log('Initial:', initialConnections);
          console.log('Final:', finalConnections);
          console.log('Intersection:', newlyAdded);
        }
        newConn._connection = newlyAdded[0];
      }
    }
  }

  async createConnection(connection: Rete.Connection): Promise<void> {
    if (
      (connection.data as { [key: string]: unknown })['connectionModel'] !==
      undefined
    ) {
      // console.log('This connection has already been mirrored.');
      return;
    }
    // console.log('Created_Connection ', connection); //this will return value
    // console.log('Create_Connection_Input ', connection.input);
    const manager = this.model.widget_manager;
    const newConnection: ReteConnectionModel = (await manager.new_widget({
      model_name: ReteConnectionModel.model_name,
      model_module: ReteConnectionModel.model_module,
      model_module_version: ReteConnectionModel.model_module_version,
      view_name: ReteConnectionModel.view_name,
      view_module: ReteConnectionModel.view_module,
      view_module_version: ReteConnectionModel.view_module_version
    })) as ReteConnectionModel;
    newConnection._connection = connection;
    (connection.data as { [key: string]: unknown }) = {
      connectionModel: newConnection
    };
    // console.log('Created_Connection ', connection); //this will not return value
    // console.log('Create_Connection_Input ', connection.input);
    // console.log('output', connection.output.node.meta);
    const sourceNode: ReteNodeModel = connection.output.node.meta
      .nodeModel as ReteNodeModel;
    // console.log('input', connection.input.node.meta);
    const destNode: ReteNodeModel = connection.input.node.meta
      .nodeModel as ReteNodeModel;
    // We need to get the slots
    newConnection.set('source_node', sourceNode);
    newConnection.source_node = sourceNode;
    newConnection.set('source_key', connection.output.key);
    newConnection.source_key = connection.output.key;
    newConnection.set('destination_node', destNode);
    newConnection.destination_node = destNode;
    newConnection.set('destination_key', connection.input.key);
    newConnection.destination_key = connection.input.key;
    newConnection.save_changes();
    // console.log(newConnection);
    const newConnections: ReteConnectionModel[] = (
      this.model.get('connections') as ReteConnectionModel[]
    ).concat([newConnection]);
    this.model.set('connections', newConnections);
    this.model.save_changes();
    // console.log('Saved connections', this.model.get('connections'));
  }
  async removeConnection(connection: Rete.Connection): Promise<void> {
    // console.log('Removed ', connection);
  }

  async createNewNode(node: Rete.Node): Promise<void> {
    if (node.meta.nodeModel) {
      return;
    }
    const manager = this.model.widget_manager;
    const newNode: ReteNodeModel = (await manager.new_widget(
      {
        model_name: ReteNodeModel.model_name,
        model_module: ReteNodeModel.model_module,
        model_module_version: ReteNodeModel.model_module_version,
        view_name: ReteNodeModel.view_name,
        view_module: ReteNodeModel.view_module,
        view_module_version: ReteNodeModel.view_module_version
      },
      {
        title: node.name,
        type_name: 'Type Name',
        inputs: [],
        outputs: [],
        controls: []
      }
    )) as ReteNodeModel;
    newNode._node = node;
    node.meta.nodeModel = newNode;
    newNode.set('inputs', node.meta.inputSlots);
    newNode.set('outputs', node.meta.outputSlots);
    newNode.set('controls', node.meta.controls);
    newNode.save();
    const newNodes: ReteNodeModel[] = (
      this.model.get('nodes') as ReteNodeModel[]
    ).concat([newNode]);
    this.model.set('nodes', newNodes);
    await this.model.save();
  }

  async removeNode(node: Rete.Node): Promise<void> {
    if (!node.meta.nodeModel) {
      return;
    }
    const nModel: ReteNodeModel = node.meta.nodeModel as ReteNodeModel;
    const oldNodes: ReteNodeModel[] = this.model.get(
      'nodes'
    ) as ReteNodeModel[];
    const newNodes = oldNodes.filter(n => n.model_id !== nModel.model_id);
    this.model.set('nodes', newNodes);
    await this.model.save();
  }

  declare model: ReteEditorModel;
  div: HTMLDivElement;
  divId: string;
  editor: Rete.NodeEditor;
  engine: Rete.Engine;
}

class DefaultComponent extends Rete.Component {
  constructor() {
    super('DefaultComponent');
  }

  async builder(node: Rete.Node): Promise<void> {
    // Nominally, this is where we would build things, but we don't need to at
    // this point.
  }

  async worker(
    node: NodeData,
    inputs: WorkerInputs,
    outputs: WorkerOutputs
  ): Promise<void> {
    // Because we don't have any inputs or outputs by default,
    // this too will be empty.
  }
}

const defaultComponent = new DefaultComponent();
