---
id: "g6-layout-dagre"
title: "G6 Dagre Hierarchical Layout"
description: |
  Automatically arrange DAGs (Directed Acyclic Graphs) in a hierarchical manner using the Dagre layout.
  Supports vertical/horizontal directions, suitable for flowcharts, organizational charts, and dependency graphs.

library: "g6"
version: "5.x"
category: "layouts"
subcategory: "hierarchical"
tags:
  - "layout"
  - "hierarchical"
  - "dagre"
  - "directed graph"
  - "DAG"
  - "flowchart"
  - "organizational chart"

related:
  - "g6-node-rect"
  - "g6-edge-cubic"
  - "g6-edge-polyline"
  - "g6-layout-force"

use_cases:
  - "Flowchart"
  - "Dependency Graph"
  - "Workflow Diagram"
  - "Build Dependency Graph"
  - "State Machine Diagram"

anti_patterns:
  - "Cyclic graphs are not suitable for dagre (reverse edges will be ignored)"
  - "Tree data is recommended to use compact-box or mindmap"
  - "Dagre calculation is slow for node counts exceeding 500"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/layout/dagre"
---

## Core Concepts

Dagre layout automatically arranges Directed Acyclic Graphs (DAG) in layers:
- **rankdir**: Arrangement direction (TB=top to bottom, LR=left to right)
- **ranksep**: Inter-layer spacing
- **nodesep**: Intra-layer node spacing
- **ranker**: Ranking algorithm (affects node allocation within layers)

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'start', data: { label: 'Start' } },
       { id: 'step1', data: { label: 'Step 1' } },
       { id: 'step2', data: { label: 'Step 2' } },
       { id: 'step3', data: { label: 'Step 3' } },
       { id: 'end', data: { label: 'End' } },
    ],
    edges: [
       { source: 'start', target: 'step1' },
       { source: 'start', target: 'step2' },
       { source: 'step1', target: 'step3' },
       { source: 'step2', target: 'step3' },
       { source: 'step3', target: 'end' },
    ],
  },
  node: {
    type: 'rect',
    style: {
      size: [120, 40],
      radius: 4,
      fill: '#f0f5ff',
      stroke: '#adc6ff',
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
    },
  },
  edge: {
    type: 'cubic-vertical',
    style: {
      stroke: '#adc6ff',
      endArrow: true,
    },
  },
  layout: {
    type: 'dagre',
    rankdir: 'TB',         // Top to Bottom
    ranksep: 60,           // Layer spacing
    nodesep: 20,           // Node spacing
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

## Common Variants

### Flowchart from Left to Right

```javascript
layout: {
  type: 'dagre',
  rankdir: 'LR',            // From left to right
  ranksep: 80,
  nodesep: 30,
  align: 'UL',              // Node alignment
},
edge: {
  type: 'cubic-horizontal', // Matches LR direction
  style: {
    stroke: '#91caff',
    endArrow: true,
  },
},
```

### AntV Dagre (Optimized Node Ranking Algorithm)

```javascript
// antv-dagre is an optimized version of Dagre by the AntV team, more suitable for Combo scenarios
layout: {
  type: 'antv-dagre',
  rankdir: 'TB',
  ranksep: 50,
  nodesep: 20,
  ranker: 'tight-tree',     // 'network-simplex' | 'tight-tree' | 'longest-path'
},
```

### Flowchart with Polyline Edges

```javascript
node: {
  type: 'rect',
  style: {
    size: [120, 40],
    radius: 0,               // Right-angled rectangle
    fill: '#fff',
    stroke: '#1783FF',
    lineWidth: 1.5,
    labelText: (d) => d.data.label,
    labelPlacement: 'center',
    // Configure ports
    ports: [
       { key: 'top', placement: 'top' },
       { key: 'bottom', placement: 'bottom' },
    ],
  },
},
edge: {
  type: 'polyline',          // Polyline edge
  style: {
    stroke: '#1783FF',
    lineWidth: 1.5,
    radius: 6,
    endArrow: true,
  },
},
layout: {
  type: 'dagre',
  rankdir: 'TB',
  ranksep: 60,
  nodesep: 30,
  controlPoints: true,      // Retain control points
},
```

### Hierarchical Graph with Combo

```javascript
const graph = new Graph({
  container: 'container',
  width: 900,
  height: 600,
  data: {
    nodes: [
       { id: 'n1', combo: 'group1', data: { label: 'Module A' } },
       { id: 'n2', combo: 'group1', data: { label: 'Module B' } },
       { id: 'n3', combo: 'group2', data: { label: 'Module C' } },
    ],
    edges: [
       { source: 'n1', target: 'n3' },
       { source: 'n2', target: 'n3' },
    ],
    combos: [
       { id: 'group1', data: { label: 'Subsystem 1' } },
       { id: 'group2', data: { label: 'Subsystem 2' } },
    ],
  },
  combo: {
    type: 'rect',
    style: {
      fill: '#f5f5f5',
      stroke: '#d9d9d9',
      labelText: (d) => d.data.label,
      labelPlacement: 'top',
    },
  },
  layout: {
    type: 'antv-dagre',     // antv-dagre provides better support for Combo
    rankdir: 'LR',
    ranksep: 60,
    nodesep: 20,
  },
});
```

## Parameter Reference

```typescript
interface DagreLayoutOptions {
  rankdir?: 'TB' | 'BT' | 'LR' | 'RL';     // Layout direction, default 'TB'
  align?: 'UL' | 'UR' | 'DL' | 'DR';        // Node alignment
  nodesep?: number;                           // Node spacing within the same layer, default 50
  ranksep?: number;                           // Layer spacing, default 100
  ranker?: 'network-simplex' | 'tight-tree' | 'longest-path';
  nodeSize?: number | [number, number];        // Node size (used for spacing calculation)
  controlPoints?: boolean;                    // Whether to retain edge control points
  workerEnabled?: boolean;                    // Whether to run in Web Worker
}
```

## Common Errors

### Error 1: Using Dagre for Cyclic Graphs Causes Edge Loss

```javascript
// ❌ Cyclic graphs (e.g., state machines) using Dagre ignore reverse edges
const edges = [
   { source: 'a', target: 'b' },
   { source: 'b', target: 'c' },
   { source: 'c', target: 'a' },  // Forms a cycle, Dagre ignores
];

// ✅ Use force layout for cyclic graphs
layout: { type: 'force', preventOverlap: true },
```

### Error 2: Node Size Inconsistent with Layout `nodeSize`

```javascript
// ❌ Node actual size does not match the `nodeSize` parameter in dagre, causing node overlap
node: {
  type: 'rect',
  style: { size: [200, 60] },   // Actual size 200x60
},
layout: {
  type: 'dagre',
  nodeSize: 40,   // Parameter too small, mismatch
},

// ✅ `nodeSize` matches node size
node: {
  type: 'rect',
  style: { size: [120, 40] },
},
layout: {
  type: 'dagre',
  nodeSize: [120, 40],   // Matches node size
  ranksep: 60,
},
```

### Error 3: Edge Type and Direction Mismatch

```javascript
// ❌ Horizontal curve edge used in TB direction
layout: { type: 'dagre', rankdir: 'TB' },
edge: { type: 'cubic-horizontal' },   // Horizontal curve is not aesthetically pleasing in TB direction

// ✅ Matching direction
layout: { type: 'dagre', rankdir: 'TB' },
edge: { type: 'cubic-vertical' },    // Vertical curve complements TB

layout: { type: 'dagre', rankdir: 'LR' },
edge: { type: 'cubic-horizontal' },  // Horizontal curve complements LR
```