---
id: "g6-plugin-history-legend"
title: "G6 Undo/Redo (history) and Legend (legend)"
description: |
  history: Records the operation history of the graph, supports undo/redo, suitable for graph editing scenarios.
  legend: Automatically generates legends from node/edge data, supports click filtering.

library: "g6"
version: "5.x"
category: "plugins"
subcategory: "display"
tags:
  - "plugin"
  - "history"
  - "undo"
  - "legend"
  - "history"
  - "legend"

related:
  - "g6-plugin-contextmenu-toolbar"
  - "g6-state-overview"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Undo/Redo (history)

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'A' } },
       { id: 'n2', data: { label: 'B' } },
    ],
    edges: [{ source: 'n1', target: 'n2' }],
  },
  node: {
    type: 'circle',
    style: {
      size: 40,
      fill: '#1783FF',
      stroke: '#fff',
      labelText: (d) => d.data.label,
    },
  },
  layout: { type: 'circular' },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
  plugins: [
    {
      type: 'history',
      stackSize: 50,           // Maximum history size, 0 = unlimited
    },
  ],
});

graph.render();

// Register shortcuts Ctrl+Z / Ctrl+Y
document.addEventListener('keydown', (e) => {
  const plugin = graph.getPluginInstance('history');
  if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
    e.preventDefault();
    if (plugin.canUndo()) plugin.undo();
  }
  if ((e.ctrlKey || e.metaKey) && e.key === 'y') {
    e.preventDefault();
    if (plugin.canRedo()) plugin.redo();
  }
});

// Listen for history changes to update UI
const plugin = graph.getPluginInstance('history');
// Or retrieve by key
// plugins: [{ type: 'history', key: 'myHistory', stackSize: 50 }]

// Batch operations merged into a single history entry
graph.batch(() => {
  graph.addNodeData([{ id: 'n3', data: { label: 'C' } }]);
  graph.addEdgeData([{ source: 'n1', target: 'n3' }]);
});
graph.draw();
// The above two operations are merged via batch, and will be rolled back together on undo
```

### History Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `stackSize` | `number` | `0` | History stack size, 0 means no limit |
| `beforeAddCommand` | `(cmd, revert) => boolean \| void` | — | Intercept before adding a command, return false to cancel |
| `afterAddCommand` | `(cmd, revert) => void` | — | Callback after adding a command |

### history API

```javascript
const history = graph.getPluginInstance('history-plugin-key');

history.undo();          // Undo
history.redo();          // Redo
history.canUndo();       // Can undo (boolean)
history.canRedo();       // Can redo (boolean)
history.clear();         // Clear history
```

---

## Legend

Automatically generate an interactive legend based on node/edge data fields.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'A', type: 'Engineer' } },
       { id: 'n2', data: { label: 'B', type: 'Product' } },
       { id: 'n3', data: { label: 'C', type: 'Engineer' } },
       { id: 'n4', data: { label: 'D', type: 'Designer' } },
    ],
    edges: [
       { source: 'n1', target: 'n2', data: { relation: 'Collaboration' } },
       { source: 'n1', target: 'n3', data: { relation: 'Subordinate' } },
    ],
  },
  node: {
    type: 'circle',
    style: {
      size: 40,
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
    palette: {
      type: 'group',
      field: 'type',           // Legend categorizes by this field
    },
  },
  edge: {
    style: {
      stroke: '#aaa',
      endArrow: true,
    },
  },
  layout: { type: 'force', preventOverlap: true },
  behaviors: ['drag-canvas', 'zoom-canvas'],
  plugins: [
    {
      type: 'legend',
      position: 'bottom-left',       // Legend position
      trigger: 'click',              // 'hover' | 'click' (click to filter)
      // Categorization field for node legend
      nodeField: 'type',
      // Categorization field for edge legend
      edgeField: 'relation',
      // Legend orientation
      orientation: 'horizontal',     // 'horizontal' | 'vertical'
    },
  ],
});

graph.render();
```

### Legend Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `position` | `CardinalPlacement` | `'bottom'` | Legend position |
| `trigger` | `'hover' \| 'click'` | `'hover'` | Interaction trigger method |
| `nodeField` | `string \| ((d) => string)` | — | Node classification field |
| `edgeField` | `string \| ((d) => string)` | — | Edge classification field |
| `comboField` | `string \| ((d) => string)` | — | Combo classification field |
| `orientation` | `'horizontal' \| 'vertical'` | `'horizontal'` | Legend arrangement direction |
| `container` | `HTMLElement \| string` | — | Custom container |