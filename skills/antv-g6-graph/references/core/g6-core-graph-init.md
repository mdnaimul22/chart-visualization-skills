---
id: "g6-core-graph-init"
title: "G6 Graph Instance Initialization"
description: |
  Comprehensive configuration guide for creating a graph instance using new Graph({...}).
  Includes one-time configuration for container, size, data, style, layout, and interactions.

library: "g6"
version: "5.x"
category: "core"
subcategory: "init"
tags:
  - "initialization"
  - "Graph"
  - "container"
  - "configuration"
  - "graph init"
  - "container"
  - "new Graph"

related:
  - "g6-core-data-structure"
  - "g6-node-circle"
  - "g6-layout-force"

use_cases:
  - "Create any type of graph visualization"
  - "Configure basic appearance and behavior of the graph"

anti_patterns:
  - "Do not use the v4 method new G6.Graph() and graph.data()"
  - "Avoid modifying basic configurations multiple times outside the constructor"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/graph/graph"
---

## Core Concepts

Graph is the core container of G6, managing all elements (nodes, edges, Combos) and operations (interactions, rendering).

**Key differences between G6 v5 and v4:**
- All configurations are completed in `new Graph({...})` at once
- Data is passed through the `data` field in the constructor (no longer using `graph.data()`)
- Node labels are configured through the `style.labelText` callback (no longer using `label` or `labelCfg`)
- `behaviors` is directly an array (no longer has the Mode concept)

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',   // Required: DOM element id or HTMLElement
  width: 800,
  height: 600,
  data: {
    nodes: [
      { id: 'node1', data: { label: 'Node 1' } },
      { id: 'node2', data: { label: 'Node 2' } },
      { id: 'node3', data: { label: 'Node 3' } },
    ],
    edges: [
      { id: 'e1', source: 'node1', target: 'node2' },
      { id: 'e2', source: 'node2', target: 'node3' },
    ],
  },
  layout: { type: 'force' },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

## Complete Configuration Guide

### Container and Dimensions

```javascript
const graph = new Graph({
  container: 'container',         // String id or DOM element
  width: 800,                     // Canvas width (px)
  height: 600,                    // Canvas height (px)
  autoFit: 'view',                // Auto-fit: 'center' | 'view' | false
  padding: [20, 20, 20, 20],      // Padding [top, right, bottom, left]
  devicePixelRatio: 2,            // Device pixel ratio, for high-DPI screens
});
```

### Renderer Configuration

```javascript
const graph = new Graph({
  container: 'container',
  renderer: () => new CanvasRenderer(),    // Default Canvas renderer
  // renderer: () => new SVGRenderer(),    // SVG renderer (requires separate import)
  // renderer: () => new WebGLRenderer(),  // WebGL renderer (requires separate import)
});
```

### Complete Example (Includes All Common Configurations)

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  // Container
  container: 'container',
  width: 960,
  height: 600,
  autoFit: 'view',

  // Data
  data: {
    nodes: [
      { id: 'n1', data: { label: 'Product', type: 'product', value: 80 } },
      { id: 'n2', data: { label: 'User', type: 'user', value: 50 } },
      { id: 'n3', data: { label: 'Order', type: 'order', value: 30 } },
    ],
    edges: [
      { id: 'e1', source: 'n1', target: 'n2', data: { label: 'Purchase' } },
      { id: 'e2', source: 'n2', target: 'n3', data: { label: 'Generate' } },
    ],
  },

  // Node Configuration
  node: {
    type: 'circle',
    style: {
      size: 40,
      fill: '#1783FF',
      stroke: '#fff',
      lineWidth: 2,
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
      labelFill: '#333',
    },
  },

  // Edge Configuration
  edge: {
    type: 'line',
    style: {
      stroke: '#aaa',
      lineWidth: 1.5,
      endArrow: true,
      labelText: (d) => d.data.label,
    },
  },

  // Layout
  layout: {
    type: 'force',
    preventOverlap: true,
    nodeSize: 40,
    linkDistance: 100,
  },

  // Theme
  theme: 'light',

  // Interaction Behaviors
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element', 'click-select'],

  // Plugins
  plugins: ['grid-line', 'minimap'],

  // Animation
  animation: true,
});

await graph.render();
```

## Edge Data ID Rules

**⚠️ Important: Edge ID Auto-Generation Rules**

When an `id` is not specified in the edge data, G6 automatically generates an edge ID in the format `${source}-${target}`.

**This means: If two edges have the same source and target (i.e., parallel edges), they will generate the same ID, resulting in an `Edge already exists` error.**

```javascript
// ❌ Error: Two edges with the same source/target, auto-generated id is "A-B" for both, causing an error
edges: [
  { source: 'A', target: 'B' },
  { source: 'A', target: 'B' },  // Duplicate!
]

// ✅ Correct: Explicitly specify a unique id for each edge
edges: [
  { id: 'e1', source: 'A', target: 'B' },
  { id: 'e2', source: 'A', target: 'B' },
]
```

**Best Practice: Always explicitly specify a unique `id` for edge data to avoid auto-generated ID conflicts.**

```javascript
// ✅ Recommended: Each edge has a unique id
const edges = [
  { id: 'e-0-1', source: '0', target: '1' },
  { id: 'e-0-2', source: '0', target: '2' },
  { id: 'e-1-2', source: '1', target: '2' },
];

// ✅ When dynamically generating edges, use an index to ensure unique ids
const edges = rawEdges.map((e, i) => ({
  id: `edge-${i}`,
  source: e.source,
  target: e.target,
}));
```

## Lifecycle Methods

```javascript
// Render (must be called)
await graph.render();

// Redraw after updating data
graph.draw();

// Adapt view
graph.fitView();
graph.fitCenter();

// Destroy
graph.destroy();

// Listen for events
graph.on('node:click', (event) => {
  const { target } = event;
  console.log('Node clicked:', target.id);
});

// Get rendering status
console.log(graph.rendered);   // boolean
console.log(graph.destroyed);  // boolean
```

## Dynamic Operations

```javascript
// Add node
graph.addNodeData([{ id: 'n4', data: { label: 'New Node' } }]);
await graph.draw();

// Remove node (associated edges will also be removed)
graph.removeNodeData(['n4']);
await graph.draw();

// Update element style
graph.updateNodeData([{ id: 'n1', style: { fill: 'red' } }]);
await graph.draw();

// Set element state
graph.setElementState('n1', 'selected');
graph.setElementState('n1', []);  // Clear state

// Zoom
graph.zoomTo(1.5);
graph.zoomTo(1, true);  // With animation

// Move viewport
graph.translateTo([400, 300]);

// Focus on an element
graph.focusElement('n1');
```

## Tree Data Transformation

If the data is in a tree structure (with parent-child hierarchical relationships), the `treeToGraphData` utility function must be used to convert it into the G6 standard graph data format before passing it to `data`.

```javascript
import { Graph, treeToGraphData } from '@antv/g6';

const treeData = {
  id: 'root',
  children: [
    { id: 'child1', children: [{ id: 'leaf1' }] },
    { id: 'child2' },
  ],
};

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: treeToGraphData(treeData),   // ✅ Must be converted before passing
  layout: { type: 'compact-box' },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

> ⚠️ `treeToGraphData` must be explicitly imported from `@antv/g6` and cannot be called directly without being imported.

## Common Errors

### Error 1: Missing container

```javascript
// ❌ Incorrect
const graph = new Graph({ width: 800, height: 600 });

// ✅ Correct
const graph = new Graph({ container: 'container', width: 800, height: 600 });
```

### Error 2: Using v4's graph.data() Method

```javascript
// ❌ Incorrect (v4 Syntax)
const graph = new G6.Graph({ container: 'container', width: 800, height: 600 });
graph.data({ nodes: [...], edges: [...] });
graph.render();

// ✅ Correct (v5 Syntax)
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: { nodes: [...], edges: [...] },
});
graph.render();
```

### Error 3: Directly Writing Labels in Data

```javascript
// ❌ Incorrect: Label directly written in node data
{ id: 'node1', label: 'Node 1' }

// ✅ Correct: Business data placed in the `data` field
{ id: 'node1', data: { label: 'Node 1' } }
// Then in the style:
node: {
  style: {
    labelText: (d) => d.data.label,
  },
}
```

### Error 4: Using v4 `modes` Configuration

```javascript
// ❌ Incorrect (v4 modes)
modes: { default: ['drag-canvas', 'zoom-canvas'] }

// ✅ Correct (v5 behaviors)
behaviors: ['drag-canvas', 'zoom-canvas']
```

### Error 5: Conflict Between autoFit and Fixed Dimensions

```javascript
// ❌ Setting autoFit: true along with width/height will produce unpredictable results
const graph = new Graph({
  autoFit: true,   // Old syntax
  width: 800,
  height: 600,
});

// ✅ Correct: Use 'view' or 'center'
const graph = new Graph({
  autoFit: 'view',   // or 'center', or false (manual control)
  width: 800,
  height: 600,
});
```

### Error 6: Edge ID Conflict Causes "Edge already exists"

When dynamically generating edge data, if multiple edges have the same source and target (parallel edges), and no id is specified, it will result in duplicate automatically generated ids, throwing the `Edge already exists` error.

```javascript
// ❌ Error: Randomly generating edges may produce duplicate source-target pairs
const edges = [];
for (let i = 0; i < 34; i++) {
  for (let j = 0; j < 3; j++) {
    const target = Math.floor(Math.random() * 34);
    if (target !== i) {
      edges.push({ source: `${i}`, target: `${target}` }); // No id, may duplicate!
    }
  }
}

// ✅ Correct Solution 1: Assign a unique id to each edge (recommended)
const edges = [];
let edgeIndex = 0;
for (let i = 0; i < 34; i++) {
  for (let j = 0; j < 3; j++) {
    const target = Math.floor(Math.random() * 34);
    if (target !== i) {
      edges.push({ id: `edge-${edgeIndex++}`, source: `${i}`, target: `${target}` });
    }
  }
}

// ✅ Correct Solution 2: Deduplicate existing edge array and add ids
const edgeSet = new Set();
const edges = [];
let edgeIndex = 0;
for (let i = 0; i < 34; i++) {
  for (let j = 0; j < 3; j++) {
    const target = Math.floor(Math.random() * 34);
    const key = `${i}-${target}`;
    if (target !== i && !edgeSet.has(key)) {
      edgeSet.add(key);
      edges.push({ id: `edge-${edgeIndex++}`, source: `${i}`, target: `${target}` });
    }
  }
}
```

### Error 7: Tree Data Passed Directly Without Conversion

```javascript
// ❌ Error: Tree structure data cannot be passed directly to data
const graph = new Graph({
  data: { id: 'root', children: [...] },  // Error!
});

// ❌ Error: Using treeToGraphData without importing it
const graph = new Graph({
  data: treeToGraphData(treeData),  // ReferenceError: treeToGraphData is not defined
});

// ✅ Correct: Import from @antv/g6 and use
import { Graph, treeToGraphData } from '@antv/g6';
const graph = new Graph({
  data: treeToGraphData(treeData),
});
```