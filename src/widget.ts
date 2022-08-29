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
import {
  DOMWidgetModel,
  DOMWidgetView,
  uuid,
  unpack_models,
  ManagerBase
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
    return new Rete.Input(
      this.key,
      this.title,
      this.sockets.getSocket(this.socket_type),
      this.multi_connection
    );
  }

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
    return new Rete.Output(
      this.key,
      this.title,
      this.sockets.getSocket(this.socket_type),
      this.multi_connection
    );
  }

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
    this.type_name = this.get('type_name');
    await this.createComponent();
  }

  createComponent(): void {
    const thisTypeName = this.type_name;
    const title = this.title;
    const inputs = this.inputs;
    const outputs = this.outputs;
    this._rete_component = new (class ThisComponent extends Rete.Component {
      constructor(_title: string) {
        super(title);
      }
      async builder(node: Rete.Node): Promise<void> {
        node.meta.componentType = thisTypeName;
        node.meta.inputSlots = inputs;
        node.meta.outputSlots = outputs;
        inputs.forEach((e: ReteInputModel) => {
          node.addInput(e.getInstance());
        });
        outputs.forEach((e: ReteOutputModel) => {
          node.addOutput(e.getInstance());
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
    outputs: { deserialize: unpack_models }
  };

  // the inputs and outputs will need serializers and deserializers
  _rete_component: Rete.Component;
  sockets: ReteSocketCollectionModel;
  title: string;
  type_name: string;
  inputs: ReteInputModel[];
  outputs: ReteOutputModel[];
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

  declare model: ReteNodeModel;
}

export class ReteEditorModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      editorConfig: {},
      _components: [],
      selected_node: undefined,
      nodes: [],
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
    this.on('msg:custom', this.onCommand.bind(this));
    this.addNewComponent();
  }

  async updateViews(): Promise<void> {
    for (const viewId of Object.keys(this.views)) {
      await this.views[viewId].then(v => {
        (v as ReteEditorView).editor.view.area.update();
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
    nodes: { deserialize: unpack_models }
  };

  _components: ReteComponentModel[];
  nodes: ReteNodeModel[];
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
    this.div = document.createElement('div');
    this.divId = 'rete-editor-' + uuid();
    this.div.setAttribute('id', this.divId);
    this.el.classList.add('retejseditor');
    this.el.appendChild(this.div);
    //await this.editor.fromJSON(editorData as any);
    this.setupListeners();
    this.displayed.then(() => this.setupEditor());
  }

  setupListeners(): void {
    this.model.on('change:_components', this.addNewComponent, this);
    this.model.on('change:nodes', this.updateNodes, this);
  }

  addNewComponent(): void {
    const components: ReteComponentModel[] = this.model.get('_components');
    console.log(components);
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
    this.editor.register(defaultComponent);
    this.editor.on(['noderemoved'], async () => {
      this.model.updateViews();
    });
    this.editor.on(['nodeselected'], async (node: Rete.Node) => {
      // Figure out which NodeModel it corresponds to
      console.log('selected', node.meta.nodeModel);
      this.model.set('selected_node', node.meta.nodeModel);
      this.model.save_changes();
    });
    this.editor.on(['nodecreated'], async (node: Rete.Node) => {
      await this.createNewNode(node);
      this.model.updateViews();
    });
    this.editor.on(
      ['connectioncreated', 'connectionremoved'],
      // Note that I *believe* that the connectionremoved function is called
      // whenever a connection is clicked on.  That's not super ideal, since
      // we really only want to sync when the connection has been deleted.
      // We may actually eventually want to explore using connectiondrop, which
      // may fire only when the mouse is lifted.
      async (connection: Rete.Connection) => this.updateConnection(connection)
    );
    this.editor.view.resize();
    this.addNewComponent();
  }

  async updateNodes(model: ReteEditorModel): Promise<void> {
    const oldNodes: ReteNodeModel[] = model.previous('nodes');
    const newNodes: ReteNodeModel[] = model.get('nodes');
    console.log('oldNodes', this.divId, oldNodes);
    for (const remNode of oldNodes.filter(_ => !newNodes.includes(_))) {
      // These are instances, so we match based on keys
      this.editor.removeNode(remNode._node);
    }
    for (const newNode of newNodes.filter(_ => !oldNodes.includes(_))) {
      console.log('newnode', this.divId, newNode);
      if (newNode._node === undefined) {
        newNode._node = new Rete.Node(newNode.get('type_name'));
        newNode._node.meta.nodeModel = newNode;
        newNode.changeInputs();
        newNode.changeOutputs();
      }
      if (!this.editor.nodes.includes(newNode._node)) {
        this.editor.addNode(newNode._node);
      }
      console.log(this.divId, newNode._node);
    }
  }

  async updateConnection(connection: Rete.Connection): Promise<void> {
    console.log('Updated ', connection);
  }

  async createNewNode(node: Rete.Node): Promise<void> {
    if (node.meta.nodeModel) {
      return;
    }
    const manager: ManagerBase<any> = this.model.widget_manager;
    const newNode: ReteNodeModel = (await manager.new_widget({
      model_name: ReteNodeModel.model_name,
      model_module: ReteNodeModel.model_module,
      model_module_version: ReteNodeModel.model_module_version,
      view_name: ReteNodeModel.view_name,
      view_module: ReteNodeModel.view_module,
      view_module_version: ReteNodeModel.view_module_version
    })) as ReteNodeModel;
    newNode._node = node;
    newNode.set('title', node.name);
    newNode.set('inputs', node.meta.inputSlots || []);
    newNode.set('outputs', node.meta.outputSlots || []);
    newNode.save_changes();
    node.meta.nodeModel = newNode;
    const newNodes: ReteNodeModel[] = (
      this.model.get('nodes') as ReteNodeModel[]
    ).concat([newNode]);
    this.model.set('nodes', newNodes);
    this.model.save_changes();
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
