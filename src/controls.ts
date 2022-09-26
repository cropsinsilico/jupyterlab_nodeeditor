import * as Rete from 'rete';
import { DOMWidgetModel } from '@jupyter-widgets/base';
import { MODULE_NAME, MODULE_VERSION } from './version';
import type { EventsTypes } from 'rete/types/events';
import type { ISerializers } from '@jupyter-widgets/base';
import { unpack_models } from '@jupyter-widgets/base';

import {
  NumberInputControl,
  DropDownInputControl,
  TextInputControl
} from 'nodeeditor-controls';
import { ReteEditorModel } from './widget';

//numcontrol
interface IVueNumControlProps {
  initialValue: number;
  ikey: string;
  reteEmitter?: Rete.Emitter<EventsTypes> | undefined;
  reteGetData?: (ikey: string) => number;
  retePutData?: (ikey: string, value: number) => void;
}

class NumControl extends Rete.Control {
  constructor(emitter: Rete.Emitter<EventsTypes>, key: string) {
    super(key);
    this.component = NumberInputControl;
    this.props = {
      initialValue: 0,
      ikey: key,
      reteEmitter: emitter,
      reteGetData: this.getData.bind(this) as (ikey: string) => number,
      retePutData: this.putData.bind(this)
    };
    (this.data as any).render = 'vue';
  }

  setValue(val: number) {
    this.vueContext.value = val;
  }

  component: any;
  vueContext: any;
  props: IVueNumControlProps;
}

//textcontrol
interface IVueTextControlProps {
  initialValue: string;
  ikey: string;
  reteEmitter?: Rete.Emitter<EventsTypes> | undefined;
  reteGetData?: (ikey: string) => number;
  retePutData?: (ikey: string, value: number) => void;
}

class TextControl extends Rete.Control {
  constructor(emitter: Rete.Emitter<EventsTypes>, key: string) {
    super(key);
    this.component = TextInputControl;
    this.props = {
      initialValue: '',
      ikey: key,
      reteEmitter: emitter,
      reteGetData: this.getData.bind(this) as (ikey: string) => number,
      retePutData: this.putData.bind(this)
    };
    (this.data as any).render = 'vue';
  }

  setValue(val: number) {
    this.vueContext.value = val;
  }

  component: any;
  vueContext: any;
  props: IVueTextControlProps;
}

//dropdowncontrol
interface IVueDropDownControlProps {
  ikey: string;
  options?: { text: string; value: string }[];
  reteEmitter?: Rete.Emitter<EventsTypes> | undefined;
  reteGetData?: (ikey: string) => number;
  retePutData?: (ikey: string, value: number) => void;
}

class DropDownControl extends Rete.Control {
  constructor(emitter: Rete.Emitter<EventsTypes>, key: string) {
    super(key);
    this.component = DropDownInputControl;
    this.props = {
      ikey: key,
      reteEmitter: emitter,
      reteGetData: this.getData.bind(this) as (ikey: string) => number,
      retePutData: this.putData.bind(this)
    };
    (this.data as any).render = 'vue';
  }

  setValue(val: number) {
    this.vueContext.value = val;
  }

  component: any;
  vueContext: any;
  props: IVueDropDownControlProps;
}

export class ReteControlModel extends DOMWidgetModel {
  defaults(): any {
    return {
      ...super.defaults(),
      key: undefined,
      editor: undefined,
      _model_name: ReteControlModel.model_name,
      _model_module: ReteControlModel.model_module,
      _model_module_version: ReteControlModel.model_module_version
    };
  }

  async initialize(attributes: any, options: any): Promise<void> {
    super.initialize(attributes, options);
    this.key = this.get('key');
    this.editor = this.get('editor');
  }

  getInstance(): Rete.Control {
    return undefined;
  }

  key: string;
  editor: ReteEditorModel;
  static model_name = 'ReteControlModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    editor: { deserialize: unpack_models }
  };
}

export class ReteNumControlModel extends ReteControlModel {
  getInstance(): NumControl {
    return new NumControl(this.editor.engine, this.key);
  }
  static model_name = 'ReteNumControlModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}

export class ReteTextControlModel extends ReteControlModel {
  getInstance(): TextControl {
    return new TextControl(this.editor.engine, this.key);
  }
  static model_name = 'ReteTextControlModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}

export class ReteDropDownControlModel extends ReteControlModel {
  getInstance(): DropDownControl {
    return new DropDownControl(this.editor.engine, this.key);
  }
  static model_name = 'ReteDropDownControlModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}
