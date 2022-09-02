import * as Rete from 'rete';
import { DOMWidgetModel } from '@jupyter-widgets/base';
import { MODULE_NAME, MODULE_VERSION } from './version';
import { DOMWidgetView, uuid } from '@jupyter-widgets/base';

import { NumberInputControl } from 'nodeeditor-controls';

interface IVueNumControlProps {
  initial: number;
  readonly: boolean;
  emitter: any;
  ikey: string;
  type: string;
  change?: (value: number | string) => void;
  getData?: (ikey: string) => number;
  putData?: (ikey: string, value: number | string) => void;
}

class NumControl extends Rete.Control {
  constructor(emitter: any, key: string, readonly: boolean) {
    super(key);
    this.component = NumberInputControl;
    this.props = { emitter, ikey: key, readonly, initial: 0, type: 'number' };
  }

  setValue(val: number) {
    this.vueContext.value = val;
  }

  component: any;
  vueContext: any;
  props: IVueNumControlProps;
}

export abstract class ReteControlModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      key: undefined,
      _model_name: ReteControlModel.model_name,
      _model_module: ReteControlModel.model_module,
      _model_module_version: ReteControlModel.model_module_version
    };
  }

  async initialize(attributes: any, options: any): Promise<void> {
    super.initialize(attributes, options);
  }

  abstract getInstance(): Rete.Control;

  key = '';
  static model_name = 'ReteControlModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}

export class ReteNumControlModel extends ReteControlModel {
  getInstance(): NumControl {
    return new NumControl(this, this.key, false);
  }
}

export class ReteControlView extends DOMWidgetView {
  async render(): Promise<void> {
    super.render();
    this.div = document.createElement('div');
    this.divId = 'rete-editor-' + uuid();
    this.div.setAttribute('id', this.divId);
    this.el.classList.add('retejseditor');
    this.el.appendChild(this.div);
    this.div.innerHTML = 'Hello there!  This is me.';
    //await this.editor.fromJSON(editorData as any);
  }
  div: HTMLDivElement;
  divId: string;
  declare model: ReteControlModel;
}
