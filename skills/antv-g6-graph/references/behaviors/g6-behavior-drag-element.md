---
id: "g6-behavior-drag-element"
title: "G6 Drag Element Interaction"
description: |
  Implement node dragging using drag-element and drag-element-force.
  Regular dragging is used for fixed layouts, while the force version is used for force-directed graphs to maintain physical simulation.

library: "g6"
version: "5.x"
category: "behaviors"
subcategory: "dragging"
tags:
  - "interaction"
  - "drag"
  - "drag-element"
  - "behavior"
  - "move node"

related:
  - "g6-behavior-click-select"
  - "g6-behavior-drag-canvas"
  - "g6-layout-force"

use_cases:
  - "Manually adjust node positions"
  - "Interactive force-directed graphs"
  - "Editable charts"

anti_patterns:
  - "Do not use regular drag-element in force-directed layouts; use drag-element-force instead"
  - "Avoid using random methods when generating edge data to prevent duplicate edges causing 'Edge already exists' errors"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/behavior/drag-element"
---

## Core Concepts

- `drag-element`: Drag a node to a specified position, while other nodes remain stationary (suitable for non-force-directed layouts)
- `drag-element-force`: Physical simulation continues during dragging (suitable for force-directed layouts)

## Important Notes

### Edge Data Cannot Be Duplicated

In G6, each edge must be unique (edges with the same source + target cannot be added repeatedly), otherwise it will throw an `Edge already exists: {source}-{target}` error.

**Duplicate removal must be performed when generating edge data**, and edges cannot be directly pushed using a random method. A Set or Map should be used to record existing edges.

```javascript
// ❌ Incorrect: Randomly generating edges may result in duplicates
const edges = [];
for (let i = 0; i < 34; i++) {
  for (let j = 0; j < 3; j++) {
    const target = Math.floor(Math.random() * 34);
    edges.push({ source: `${i}`, target: `${target}` }); // May duplicate!
  }
}

// ✅ Correct: Using Set for duplicate removal
const edges = [];
const edgeSet = new Set();
for (let i = 0; i < 34; i++) {
  for (let j = 0; j < 3; j++) {
    const target = Math.floor(Math.random() * 34);
    const key = `${i}-${target}`;
    const reverseKey = `${target}-${i}`;
    if (target !== i && !edgeSet.has(key) && !edgeSet.has(reverseKey)) {
      edgeSet.add(key);
      edges.push({ source: `${i}`, target: `${target}` });
    }
  }
}
```

### Data should directly use the data provided in the title

When the title provides specific node and edge data, it should be used directly, and random generation should not be performed to avoid issues such as duplicate edges.

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const data = {
  nodes: [
    { id: '0' },
    { id: '1' },
    { id: '2' },
    { id: '3' },
    { id: '4' },
    { id: '5' },
  ],
  edges: [
    { source: '0', target: '1' },
    { source: '0', target: '2' },
    { source: '1', target: '3' },
    { source: '2', target: '4' },
    { source: '3', target: '5' },
  ],
};

const graph = new Graph({
  container: 'container',
  autoFit: 'view',
  data,
  node: {
    style: {
      labelText: (d) => d.id,
      labelFill: '#fff',
      labelPlacement: 'center',
    },
  },
  layout: { type: 'circular' },
  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    'drag-element',
  ],
});

graph.render();
```

## Common Variants

### Dragging in Force-Directed Graphs

```javascript
behaviors: [
  'drag-canvas',
  'zoom-canvas',
  'drag-element-force',       // Force-directed layout must use the force version
],
layout: { type: 'force', preventOverlap: true },
```

### Complete Configuration

```javascript
behaviors: [
  'drag-canvas',
  'zoom-canvas',
  {
    type: 'drag-element',
    // Whether to enable, default is to drag nodes and Combos
    enable: (event) => ['node', 'combo'].includes(event.targetType),
    // Drag animation
    animation: true,
    // Operation effect after drag ends: 'move' | 'link' | 'none'
    dropEffect: 'move',
    // Hide associated edges during drag (improve performance): 'none' | 'out' | 'in' | 'both' | 'all'
    hideEdge: 'none',
    // Display ghost node (shadow node) during drag
    shadow: true,
    // Drag state name
    state: 'selected',
    // Custom mouse style
    cursor: {
      default: 'default',
      grab: 'grab',
      grabbing: 'grabbing',
    },
  },
],
```

### Multi-select and Batch Drag

```javascript
// Implement multi-select drag in conjunction with click-select
behaviors: [
  'drag-canvas',
  'zoom-canvas',
  {
    type: 'click-select',
    multiple: true,
    state: 'selected',
  },
  {
    type: 'drag-element',
    // Dragging will move all nodes in the 'selected' state simultaneously
    state: 'selected',
  },
],
```

## Common Errors and Fixes

### Error 1: Using Regular `drag-element` in Force-Directed Graphs

```javascript
// ❌ Nodes do not participate in physics simulation after dragging in force-directed graphs
layout: { type: 'force' },
behaviors: ['drag-element'],   // Incorrect!

// ✅ Use `drag-element-force` for force-directed graphs
layout: { type: 'force' },
behaviors: ['drag-element-force'],
```

### Error 2: Random Edge Generation Causes Duplicate Edge Errors

**Error Description**: `Edge already exists: 12-20`

**Cause**: When generating edge data randomly, duplicate edges with the same source + target may occur. G6 does not allow duplicate edges.

```javascript
// ❌ Error: Random generation may produce duplicate edges
const edges = [];
for (let i = 0; i < 34; i++) {
  const numEdges = 2 + Math.floor(Math.random() * 2);
  for (let j = 0; j < numEdges; j++) {
    const target = Math.floor(Math.random() * 34);
    if (target !== i) {
      edges.push({ source: `${i}`, target: `${target}` }); // May duplicate!
    }
  }
}

// ✅ Correct Solution 1: Directly use the fixed data provided in the problem
const data = {
  nodes: [{ id: '0' }, { id: '1' }, /* ... */ { id: '33' }],
  edges: [
    { source: '0', target: '1' },
    { source: '0', target: '2' },
    // ... Use deterministic, non-duplicate edge data
  ],
};

// ✅ Correct Solution 2: Use a Set to deduplicate during generation
const edges = [];
const edgeSet = new Set();
for (let i = 0; i < 34; i++) {
  for (let j = i + 1; j < 34; j++) {
    // Generate in order, naturally avoiding duplicates
    if (Math.random() < 0.1) { // Control edge density
      edgeSet.add(`${i}-${j}`);
      edges.push({ source: `${i}`, target: `${j}` });
    }
  }
}
```

### Error 3: Incorrect Position of the `label` Field in Node Data

In G6 5.x, the node's `label` is configured through style settings, not in the `data` field:

```javascript
// ❌ Incorrect: G6 5.x does not support configuring `label` directly in `data`
nodes: [{ id: 'n1', label: 'A' }]

// ✅ Correct: Configure through `node.style.labelText`
node: {
  style: {
    labelText: (d) => d.id,  // or d.data?.label
    labelPlacement: 'center',
    labelFill: '#fff',
  },
},
```

### Error 4: treeToGraphData Not Imported

If you need to convert tree data to graph data, you must import `treeToGraphData` from `@antv/g6`:

```javascript
// ❌ Error: Using an unimported function directly
data: treeToGraphData(treeData),  // ReferenceError: treeToGraphData is not defined

// ✅ Correct: Import before use
import { Graph, treeToGraphData } from '@antv/g6';

const graph = new Graph({
  data: treeToGraphData(treeData),
  // ...
});
```