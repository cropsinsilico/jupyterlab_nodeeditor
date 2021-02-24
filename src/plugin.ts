import regeneratorRuntime from 'regenerator-runtime';
require('regenerator-runtime/runtime');
(window as any).regeneratorRuntime = regeneratorRuntime;

import { IJupyterWidgetRegistry } from '@jupyter-widgets/base';
import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { MODULE_NAME, MODULE_VERSION } from './version';

import * as nodeeditorExports from './widget';

/**
 * Initialization data for the jupyterlab_nodeeditor extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_nodeeditor:plugin',
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

export default extension;
