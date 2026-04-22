---
id: "g6-layout-force"
title: "G6 Force-Directed Layout (Force Layout)"
description: |
  Automatically arrange nodes using force-directed layout (force / d3-force / fruchterman).
  Based on physical simulation, nodes generate repulsive forces, and edges generate attractive forces, ultimately reaching a balanced state.

library: "g6"
version: "5.x"
category: "layouts"
subcategory: "force"
tags:
  - "layout"
  - "force-directed"
  - "force"
  - "d3-force"
  - "fruchterman"
  - "network"
  - "automatic layout"

related:
  - "g6-core-graph-init"
  - "g6-behavior-drag-element"
  - "g6-node-circle"

use_cases:
  - "Network relationship graph"
  - "Social graph"
  - "Knowledge graph"
  - "Exploratory graph analysis"

anti_patterns:
  - "Force-directed calculation is slow when the number of nodes exceeds 1000; consider fruchterman or force-atlas2"
  - "Switch to dagre when fixed hierarchical order is required"
  - "Use compact-box or mindmap for tree-like data"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/layout/force"
---

## Core Concepts

Force-directed layout achieves visual balance in graphs by simulating physical forces:
- **Repulsion**: Nodes repel each other to prevent overlap
- **Edge Attraction**: Edges pull connected nodes closer
- **Gravity**: Attracts nodes towards the canvas center

G6 provides three force-directed layouts:
| Layout Type | Features |
|----------|------|
| `force` | Built-in G6, intuitive parameters, sufficient for most scenarios |
| `d3-force` | Based on D3, rich force types, highly customizable |
| `fruchterman` | High performance, supports GPU acceleration, suitable for large graphs |

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'Node 1' } },
       { id: 'n2', data: { label: 'Node 2' } },
       { id: 'n3', data: { label: 'Node 3' } },
       { id: 'n4', data: { label: 'Node 4' } },
       { id: 'n5', data: { label: 'Node 5' } },
    ],
    edges: [
       { source: 'n1', target: 'n2' },
       { source: 'n1', target: 'n3' },
       { source: 'n2', target: 'n4' },
       { source: 'n3', target: 'n4' },
       { source: 'n4', target: 'n5' },
    ],
  },
  node: {
    type: 'circle',
    style: {
      size: 36,
      fill: '#1783FF',
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
  },
  edge: {
    type: 'line',
    style: { stroke: '#aaa', endArrow: true },
  },
  layout: {
    type: 'force',
    linkDistance: 100,
    gravity: 10,
  },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

## Common Variants

### G6 Force Layout (Complete Parameters)

```javascript
layout: {
  type: 'force',
  // Ideal length of edges
  linkDistance: 100,
  // Strength of gravity (higher values pull nodes closer to the center)
  gravity: 10,
  // Coulomb repulsion distance scale (smaller values increase repulsion range, helping to spread nodes)
  coulombDisScale: 0.005,
  // Center point
  center: [400, 300],     // [x, y], default is canvas center
  // Maximum number of iterations
  maxIteration: 1000,
  // Damping coefficient (0~1, smaller values converge faster)
  damping: 0.9,
  // Minimum movement distance (convergence is considered if movement is less than this value)
  minMovement: 0.5,
},
// ⚠️ preventOverlap / nodeSize are G6 v4 parameters and are silently ignored in v5's force layout
// To prevent overlap, use d3-force + collide instead (see D3 Force example below)
```

### D3 Force Layout

```javascript
layout: {
  type: 'd3-force',
  // Edge connection force (spring effect)
  link: {
    distance: 100,         // Ideal edge length
    strength: 0.8,         // Force strength 0~1
  },
  // Node repulsion (Coulomb repulsion)
  manyBody: {
    strength: -200,        // Negative value for repulsion, positive value for attraction
    distanceMax: 400,
  },
  // Pull towards center
  center: {
    x: 0,
    y: 0,
    strength: 0.1,
  },
  // Collision detection (prevent overlap)
  collide: {
    radius: 30,
    strength: 0.5,
  },
  // Control iteration
  alpha: 0.5,
  alphaDecay: 0.028,
  alphaMin: 0.001,
},
```

### Fruchterman Layout (Recommended for Large Graphs)

```javascript
layout: {
  type: 'fruchterman',
  gravity: 1,
  speed: 5,
  clustering: true,              // Enable clustering
  clusterGravity: 10,
  // GPU acceleration (requires WebGL renderer)
  // workerEnabled: true,        // Run in Web Worker
},
```

### Drag Nodes in Force-Directed Graph

```javascript
// To drag nodes in a force-directed graph, use drag-element-force
// This ensures that other nodes respond in real-time during dragging
behaviors: [
  'drag-canvas',
  'zoom-canvas',
  'drag-element-force',  // Replace the regular drag-element
],
```

### Fix the Position of Certain Nodes

```javascript
// Fix the position by setting coordinates in the node style
const nodes = [
   { id: 'center', data: { label: 'Center' }, style: { x: 400, y: 300 } },
   { id: 'n1', data: { label: 'Node 1' } },
   { id: 'n2', data: { label: 'Node 2' } },
];

// Or specify fixed nodes in the layout configuration
layout: {
  type: 'force',
  // Callback function: nodes returning true will be fixed
  nodeFixable: (d) => d.id === 'center',
},
```

## Web Worker Acceleration (Large Graphs)

```javascript
layout: {
  type: 'fruchterman',    // fruchterman supports GPU acceleration, recommended for large graphs
  gravity: 1,
  speed: 5,
},
// ⚠️ G6 v5 force layout's workerEnabled has been removed, for large graphs please use fruchterman or force-atlas2 instead
```

## Common Errors

### Error 1: Regular Dragging in Force-Directed Graphs Does Not Respond to Physical Simulation

```javascript
// ❌ drag-element dragging does not affect the physical state of other nodes
behaviors: ['drag-element'],

// ✅ Use drag-element-force to maintain physical simulation
behaviors: ['drag-element-force'],
```

### Error 2: Node Overlap in Force Layout —— `preventOverlap` from v4 is Ineffective

```javascript
// ❌ `preventOverlap` / `nodeSize` are G6 v4 parameters, silently ignored in G6 v5 force layout, nodes still overlap
layout: {
  type: 'force',
  preventOverlap: true,   // Ineffective
  nodeSize: 40,           // Ineffective
},


// ✅ Use d3-force + collide collision detection instead (recommended)
layout: {
  type: 'd3-force',
  link: { distance: 100, strength: 0.8 },
  manyBody: { strength: -200 },
  collide: {
    radius: 25,     // Node radius (nodeSize / 2)
    strength: 0.7,
  },
},
```

### Error 3: Reading Coordinates Before Layout Convergence

```javascript
// ❌ Reading coordinates immediately after render(), layout may not be complete
graph.render();
const pos = graph.getElementPosition('n1');  // may be inaccurate

// ✅ Wait for layout completion
await graph.render();
const pos = graph.getElementPosition('n1');  // read after layout completion
```