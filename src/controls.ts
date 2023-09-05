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
} from '@data-exp-lab/nodeeditor-controls';
import { ReteEditorModel } from './widget';
type DropDownOption = {
  text: string;
  value: string;
};
//numcontrol
interface IVueNumControlProps {
  initialValue?: number;
  ikey: string;
  reteEmitter?: Rete.Emitter<EventsTypes> | undefined;
  reteGetData?: (ikey: string) => number;
  retePutData?: (ikey: string, value: number) => void;
}

export interface IVueControlWidget extends Rete.Control {
  setValue(val: any): void;
}

class NumControl extends Rete.Control implements IVueControlWidget {
  constructor(
    emitter: Rete.Emitter<EventsTypes>,
    key: string,
    initialValue: number,
    control: ReteNumControlModel
  ) {
    super(key);
    this.component = NumberInputControl;
    this.control = control;
    this.props = {
      initialValue: initialValue || undefined,
      ikey: key,
      reteEmitter: emitter,
      reteGetData: this.getData.bind(this) as (ikey: string) => number,
      retePutData: this.putData.bind(this)
    };

    (this.data as any).render = 'vue';
  }
  setValue(val: any) {
    this.vueContext.currentValue = val;
  }

  putData(key: string, data: unknown): void {
    console.log('Putting', key, data);
    super.putData(key, data);
    if (key === this.props.ikey) {
      console.log('Setting value', data);
      this.control.set('value', data);
      this.control.save_changes();
    }
  }

  component: any;
  vueContext: any;
  props: IVueNumControlProps;
  control: ReteNumControlModel;
}

//textcontrol
interface IVueTextControlProps {
  initialValue?: string;
  ikey: string;
  reteEmitter?: Rete.Emitter<EventsTypes> | undefined;
  reteGetData?: (ikey: string) => number;
  retePutData?: (ikey: string, value: number) => void;
}

class TextControl extends Rete.Control implements IVueControlWidget {
  constructor(
    emitter: Rete.Emitter<EventsTypes>,
    key: string,
    initialValue: string,
    control: ReteTextControlModel
  ) {
    super(key);
    this.component = TextInputControl;
    this.control = control;
    this.props = {
      initialValue: initialValue || undefined,
      ikey: key,
      reteEmitter: emitter,
      reteGetData: this.getData.bind(this) as (ikey: string) => number,
      retePutData: this.putData.bind(this)
    };
    (this.data as any).render = 'vue';
  }

  setValue(val: any) {
    this.vueContext.value = val;
  }

  putData(key: string, data: unknown): void {
    super.putData(key, data);
    if (key === this.props.ikey) {
      this.control.set('value', data);
    }
  }
  component: any;
  vueContext: any;
  props: IVueTextControlProps;
  control: ReteTextControlModel;
}

//dropdowncontrol
interface IVueDropDownControlProps {
  ikey: string;
  options?: DropDownOption[];
  reteEmitter?: Rete.Emitter<EventsTypes> | undefined;
  reteGetData?: (ikey: string) => number;
  retePutData?: (ikey: string, value: number) => void;
}

class DropDownControl extends Rete.Control implements IVueControlWidget {
  constructor(
    emitter: Rete.Emitter<EventsTypes>,
    key: string,
    options: DropDownOption[],
    control: ReteDropDownControlModel
  ) {
    super(key);
    this.component = DropDownInputControl;
    this.control = control;
    this.props = {
      ikey: key,
      reteEmitter: emitter,
      options: options || undefined,
      reteGetData: this.getData.bind(this) as (ikey: string) => number,
      retePutData: this.putData.bind(this)
    };
    (this.data as any).render = 'vue';
  }

  setValue(val: any) {
    this.vueContext.value = val;
  }

  putData(key: string, data: unknown): void {
    super.putData(key, data);
    if (key === this.props.ikey) {
      this.control.set('value', data);
    }
  }
  component: any;
  vueContext: any;
  props: IVueDropDownControlProps;
  control: ReteDropDownControlModel;
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
  defaults(): any {
    return {
      ...super.defaults(),
      value: 0
    };
  }

  async initialize(attributes: any, options: any): Promise<void> {
    super.initialize(attributes, options);
    this.value = this.get('value');
  }

  getInstance(): NumControl {
    return new NumControl(this.editor.engine, this.key, this.value, this);
  }
  value: number | undefined;
  static model_name = 'ReteNumControlModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}

export class ReteTextControlModel extends ReteControlModel {
  defaults(): any {
    return {
      ...super.defaults(),
      value: ''
    };
  }
  async initialize(attributes: any, options: any): Promise<void> {
    super.initialize(attributes, options);
    this.value = this.get('value');
    // console.log('this is a:', this.initialValue);
  }
  getInstance(): TextControl {
    return new TextControl(this.editor.engine, this.key, this.value, this);
  }
  value: string | undefined;
  static model_name = 'ReteTextControlModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}

export class ReteDropDownControlModel extends ReteControlModel {
  defaults(): any {
    return {
      ...super.defaults(),
      options: []
    };
  }
  async initialize(attributes: any, options: any): Promise<void> {
    super.initialize(attributes, options);
    this.options = this.get('options');
    // console.log('Options!', this.options);
    if (this.options.length === 0) {
      this.options = undefined;
    }
    this.editor = this.get('editor');
  }
  getInstance(): DropDownControl {
    return new DropDownControl(
      this.editor.engine,
      this.key,
      this.options,
      this
    );
  }
  options: DropDownOption[] | undefined;
  static model_name = 'ReteDropDownControlModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
}
