/* eslint-disable @typescript-eslint/no-unused-vars */
import regeneratorRuntime from 'regenerator-runtime';
require('regenerator-runtime/runtime');
(window as any).regeneratorRuntime = regeneratorRuntime;

import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';
import { MODULE_NAME, MODULE_VERSION } from './version';

import * as nodeeditorExports from './widgetexports';

/**
 * Initialization data for the jupyterlab_nodeeditor extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_nodeeditor:plugin',
  description: 'Edit nodes with Rete and jupyterlab',
  autoStart: true,
  requires: [IJupyterWidgetRegistry],
  activate: (app: JupyterFrontEnd, registry: IJupyterWidgetRegistry) => {
    console.log('JupyterLab extension jupyterlab_nodeeditor is activated!');
    registry.registerWidget({
      name: MODULE_NAME,
      version: MODULE_VERSION,
      exports: nodeeditorExports
    });
  }
};

export default plugin;
