/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
import * as Rete from 'rete';
import { NodeData, WorkerInputs, WorkerOutputs } from 'rete/types/core/data';
import ConnectionPlugin from 'rete-connection-plugin';
import ContextMenuPlugin from 'rete-context-menu-plugin';
//import Data from 'rete/types/core/data';
//import ConnectionPlugin from 'rete-connection-plugin';
import VueRenderPlugin from 'rete-react-render-plugin';
import {
  DOMWidgetModel,
  DOMWidgetView,
  uuid,
  unpack_models,
  ISerializers
} from '@jupyter-widgets/base';
import { MODULE_NAME, MODULE_VERSION } from './version';

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
    this.socket_type = this.get('socket_type');
    this.sockets = this.get('sockets');
    this.instance = this.getInstance();
  }

  // Probably a better way to do this with generics, etc, but.
  public abstract getInstance(): Rete.Input | Rete.Output;

  key: string;
  title: string;
  socket_type: string;
  instance: Rete.Input | Rete.Output;
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
      this.sockets.getSocket(this.socket_type)
    );
  }

  instance: Rete.Input;
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
      this.sockets.getSocket(this.socket_type)
    );
  }

  instance: Rete.Output;
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
    (window as any).comp = this;
  }

  createComponent(): void {
    const title = this.title;
    const inputs = this.inputs;
    const outputs = this.outputs;
    this._rete_component = class ThisComponent extends Rete.Component {
      constructor(_title: string) {
        super(title);
      }
      async builder(node: Rete.Node): Promise<void> {
        inputs.forEach((e: ReteInputModel) => {
          node.addInput(e.instance);
        });
        outputs.forEach((e: ReteOutputModel) => {
          node.addOutput(e.instance);
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
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    sockets: { deserialize: unpack_models },
    inputs: { deserialize: unpack_models },
    outputs: { deserialize: unpack_models }
  };

  // the inputs and outputs will need serializers and deserializers
  _rete_component: typeof Rete.Component;
  sockets: ReteSocketCollectionModel;
  title: string;
  inputs: ReteInputModel[];
  outputs: ReteOutputModel[];
  static model_name = 'ReteComponentModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}

export class ReteEditorModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
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
  }

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
    this.engine = new Rete.Engine(`${MODULE_NAME}@${MODULE_VERSION}`);
    this.engine.register(numComponent);
    this.displayed.then(() => this.setupEditor());
  }

  async setupEditor(): Promise<void> {
    this.editor = new Rete.NodeEditor(
      `${MODULE_NAME}@${MODULE_VERSION}`,
      this.div
    );
    this.editor.use(VueRenderPlugin);
    this.editor.use(ConnectionPlugin);
    this.editor.use(ContextMenuPlugin);
    this.editor.register(numComponent);
    //await this.editor.fromJSON(editorData as any);
    this.editor.on(
      [
        'process',
        'nodecreated',
        'noderemoved',
        'connectioncreated',
        'connectionremoved'
      ],
      async () => {
        await this.engine.abort();
        await this.engine.process(this.editor.toJSON());
      }
    );
    this.editor.view.resize();
  }

  div: HTMLDivElement;
  divId: string;
  editor: Rete.NodeEditor;
  engine: Rete.Engine;
}

const numSocket = new Rete.Socket('Number value');

class NumControl extends Rete.Control {
  constructor(key: string) {
    super(key);
  }

  setValue(val: any): void {
    this.setValue(val);
  }
}

class NumComponent extends Rete.Component {
  constructor() {
    super('Number');
  }

  async builder(node: Rete.Node): Promise<void> {
    const out = new Rete.Output('num', 'Number', numSocket);
    node.addOutput(out);
  }

  async worker(
    node: NodeData,
    inputs: WorkerInputs,
    outputs: WorkerOutputs
  ): Promise<void> {
    outputs['num'] = node.data.num;
  }
}

const numComponent = new NumComponent();
