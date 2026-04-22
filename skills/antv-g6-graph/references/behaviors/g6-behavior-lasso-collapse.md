---
id: "g6-behavior-lasso-collapse"
title: "G6 Lasso Select (lasso-select) and Collapse/Expand (collapse-expand)"
description: |
  lasso-select: Freely draw a selection lasso to select multiple elements.
  collapse-expand: Click/Double-click a node or combo to collapse/expand its subtree or internal nodes.

library: "g6"
version: "5.x"
category: "behaviors"
subcategory: "interaction"
tags:
  - "interaction"
  - "lasso"
  - "box select"
  - "lasso-select"
  - "collapse-expand"
  - "collapse"
  - "expand"

related:
  - "g6-behavior-click-select"
  - "g6-combo-overview"
  - "g6-pattern-tree-graph"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Lasso Select (lasso-select)

Allows users to draw a freehand selection area, marking enclosed elements as selected.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: Array.from({ length: 20 }, (_, i) => ({
      id: `n${i}`,
      data: { label: `Node${i}` },
    })),
    edges: Array.from({ length: 15 }, (_, i) => ({
      source: `n${i % 10}`,
      target: `n${(i + 3) % 20}`,
    })),
  },
  node: {
    type: 'circle',
    style: {
      size: 30,
      fill: '#1783FF',
      stroke: '#fff',
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
    state: {
      selected: {
        fill: '#ff4d4f',
        stroke: '#cf1322',
        halo: true,
        haloFill: '#ff4d4f',
        haloOpacity: 0.2,
      },
    },
  },
  layout: { type: 'force', preventOverlap: true },
  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    {
      type: 'lasso-select',
      // Trigger lasso selection on right mouse button drag (to avoid conflict with canvas drag)
      trigger: 'pointerdown',
      // Lasso style
      style: {
        fill: 'rgba(99, 149, 255, 0.1)',
        stroke: '#6395ff',
        lineWidth: 1,
        lineDash: [4, 2],
      },
      // Selected state name
      state: 'selected',
      // Real-time update (dynamically highlight during drag)
      immediately: false,
      // Element types within the selection area
      itemTypes: ['node'],         // Select only nodes, not edges
    },
  ],
});

graph.render();

// Get all selected nodes
graph.on('canvas:pointerup', () => {
  const selectedNodes = graph.getElementDataByState('node', 'selected');
  console.log('Selected nodes:', selectedNodes.map(n => n.id));
});
```

### lasso-select Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `trigger` | `string` | `'pointerdown'` | Trigger event |
| `immediately` | `boolean` | `false` | Real-time update of selection status during dragging |
| `state` | `string` | `'selected'` | Selection state name |
| `itemTypes` | `('node' \| 'edge' \| 'combo')[]` | `['node', 'edge', 'combo']` | Types of elements participating in the selection |
| `style` | `PathStyleProps` | — | Lasso path style |

---

## Collapse-Expand

Click/double-click a node (tree graph) or combo to collapse/expand the subtree.

```javascript
import { Graph, treeToGraphData } from '@antv/g6';

const treeData = {
  id: 'root',
  data: { label: 'Root Node' },
  children: [
    {
      id: 'branch1',
      data: { label: 'Branch 1' },
      children: [
        { id: 'leaf1', data: { label: 'Leaf 1' } },
        { id: 'leaf2', data: { label: 'Leaf 2' } },
      ],
    },
    {
      id: 'branch2',
      data: { label: 'Branch 2' },
      children: [
        { id: 'leaf3', data: { label: 'Leaf 3' } },
      ],
    },
  ],
};

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: treeToGraphData(treeData),
  node: {
    type: 'rect',
    style: {
      size: [100, 36],
      fill: '#1783FF',
      stroke: '#fff',
      radius: 4,
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: '#fff',
    },
  },
  edge: {
    type: 'cubic-horizontal',
    style: { stroke: '#aaa' },
  },
  layout: {
    type: 'mindmap',
    direction: 'H',
    getHeight: () => 36,
    getWidth: () => 100,
    getVGap: () => 10,
    getHGap: () => 60,
  },
  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    {
      type: 'collapse-expand',
      trigger: 'click',              // 'click' | 'dblclick'
      animation: true,               // animate during collapse
      // Collapse/expand callbacks
      onCollapse: (id) => console.log('Collapsed:', id),
      onExpand: (id) => console.log('Expanded:', id),
    },
  ],
});

graph.render();
```

### collapse-expand Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `trigger` | `'click' \| 'dblclick'` | `'dblclick'` | Trigger method |
| `animation` | `boolean` | `true` | Collapse/expand animation |
| `enable` | `boolean \| ((event) => boolean)` | `true` | Whether to enable |
| `align` | `boolean` | `true` | Whether to automatically center after collapse |
| `onCollapse` | `(id: string) => void` | — | Callback after collapse is complete |
| `onExpand` | `(id: string) => void` | — | Callback after expand is complete |

### Control Collapse/Expand via API

```javascript
// Collapse a node and its subtree
await graph.collapseElement('branch1');

// Expand
await graph.expandElement('branch1');

// Check status
console.log(graph.isCollapsed('branch1')); // true/false
```

## Common Errors

### Error: Using collapse-expand in non-tree graphs

```javascript
// collapse-expand is only applicable to tree data (each node has a unique parent)
// Using it in regular network graphs will result in unexpected behavior

// ✅ Tree graph exclusive, use with treeToGraphData
import { treeToGraphData } from '@antv/g6';
data: treeToGraphData(treeData),
behaviors: [{ type: 'collapse-expand' }],
```