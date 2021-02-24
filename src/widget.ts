import * as Rete from 'rete';
//import Data from 'rete/types/core/data';
//import ConnectionPlugin from 'rete-connection-plugin';
import ReactRenderPlugin from 'rete-vue-render-plugin';
import { DOMWidgetModel, DOMWidgetView, uuid } from '@jupyter-widgets/base';
import { MODULE_NAME, MODULE_VERSION } from './version';

export class ReteEditorComponents extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      _model_name: ReteEditorComponents.model_name,
      _model_module: ReteEditorComponents.model_module,
      _model_module_version: ReteEditorComponents.model_module_version,
      _view_name: ReteEditorComponents.view_name,
      _view_module: ReteEditorComponents.view_module,
      _view_module_version: ReteEditorComponents.view_module_version
    };
  }

  // eslinct-disable-next-line @typescript-eslint/explicit-module-boundary-types
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
  async render(): Promise<void> {
    this.div = document.createElement('div');
    this.divId = 'rete-editor-' + uuid();
    this.div.setAttribute('id', this.divId);
    this.el.classList.add('retejseditor');
    this.el.appendChild(this.div);
    this.editor = new Rete.NodeEditor(
      `${MODULE_NAME}@${MODULE_VERSION}`,
      this.div
    );
    this.editor.use(ReactRenderPlugin);
    //await this.editor.fromJSON(editorData as any);
  }

  div: HTMLDivElement;
  divId: string;
  editor: Rete.NodeEditor;
}
