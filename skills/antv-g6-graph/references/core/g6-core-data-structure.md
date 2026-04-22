---
id: "g6-core-data-structure"
title: "G6 Data Structure"
description: |
  Graph data format specification for G6 5.x, including complete field descriptions for NodeData, EdgeData, and ComboData,
  data manipulation APIs, and best practices.

library: "g6"
version: "5.x"
category: "core"
subcategory: "data"
tags:
  - "data structure"
  - "NodeData"
  - "EdgeData"
  - "ComboData"
  - "graph data"
  - "nodes"
  - "edges"

related:
  - "g6-core-graph-init"
  - "g6-node-circle"
  - "g6-edge-line"

use_cases:
  - "Define the data format for a graph"
  - "Load data from the server and render the graph"
  - "Dynamically add or remove nodes and edges"

anti_patterns:
  - "Do not place business attributes directly at the top level of nodes; they should be placed in the data field"
  - "Do not include business logic data in the style field; style should only contain rendering-related properties"
  - "Do not generate duplicate edges (edges with the same source and target), as this will result in an 'Edge already exists' error"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/data"
---

## Core Concepts

G6 is a data-driven graph visualization engine that uses standard JSON format to describe graph structures.

**GraphData Basic Structure:**
```typescript
interface GraphData {
  nodes?: NodeData[];
  edges?: EdgeData[];
  combos?: ComboData[];
}
```

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
      { id: 'n1', data: { name: 'Node A', type: 'user' } },
      { id: 'n2', data: { name: 'Node B', type: 'product' } },
    ],
    edges: [
      { id: 'e1', source: 'n1', target: 'n2', data: { weight: 5 } },
    ],
  },
  node: {
    style: { labelText: (d) => d.data.name },
  },
  layout: { type: 'force' },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

## Complete Structure of NodeData

```typescript
interface NodeData {
  id: string;                      // Required, unique identifier
  type?: string;                   // Node type, e.g., 'circle', 'rect', 'image'
  data?: Record<string, unknown>;  // Business data (recommended for storing custom attributes)
  style?: NodeStyle;               // Node style (overrides global configuration)
  states?: string[];               // Initial state list
  combo?: string;                  // ID of the belonging combo
  children?: string[];             // List of child node IDs in tree data
}

// Example
const nodes = [
  {
    id: 'user-001',
    type: 'circle',                  // Overrides global node type
    data: {
      name: 'Zhang San',
      role: 'admin',
      score: 95,
    },
    style: {
      fill: '#ff7875',               // Overrides global style
      size: 60,
    },
    states: ['selected'],            // Initially in selected state
  },
];
```

## EdgeData Complete Structure

```typescript
interface EdgeData {
  id?: string;                     // Optional, unique identifier, automatically generated if not specified
  source: string;                  // Required, source node id
  target: string;                  // Required, target node id
  type?: string;                   // Edge type, e.g., 'line', 'cubic', 'polyline'
  data?: Record<string, unknown>;  // Business data
  style?: EdgeStyle;               // Edge style (overrides global configuration)
  states?: string[];               // Initial state list
}

// Example
const edges = [
  {
    id: 'edge-001',
    source: 'user-001',
    target: 'product-001',
    data: {
      type: 'purchase',
      amount: 299,
      date: '2024-01-15',
    },
    style: {
      stroke: '#ff4d4f',
      lineWidth: 2,
    },
  },
];
```

## ComboData Complete Structure

```typescript
interface ComboData {
  id: string;                      // Required, unique identifier
  type?: string;                   // combo type: 'circle' | 'rect'
  data?: Record<string, unknown>;  // Business data
  style?: ComboStyle;              // combo style
  states?: string[];               // Initial states
  combo?: string;                  // Parent combo id (nested combo)
}

// Example: Node grouping
const data = {
  nodes: [
    { id: 'n1', combo: 'group1', data: { label: 'Member 1' } },
    { id: 'n2', combo: 'group1', data: { label: 'Member 2' } },
    { id: 'n3', combo: 'group2', data: { label: 'Member 3' } },
  ],
  edges: [
    { source: 'n1', target: 'n3' },
  ],
  combos: [
    { id: 'group1', data: { label: 'Team A' } },
    { id: 'group2', data: { label: 'Team B' } },
  ],
};
```

## Tree Data

Tree layouts (mindmap, compact-box, etc.) use `treeToGraphData()` for conversion, which must be imported from `@antv/g6`:

```javascript
import { Graph, treeToGraphData } from '@antv/g6';

// Tree structure data
const treeData = {
  id: 'root',
  data: { label: 'Root Node' },
  children: [
    {
      id: 'child1',
      data: { label: 'Child Node 1' },
      children: [
        { id: 'grandchild1', data: { label: 'Grandchild Node 1' } },
        { id: 'grandchild2', data: { label: 'Grandchild Node 2' } },
      ],
    },
    {
      id: 'child2',
      data: { label: 'Child Node 2' },
    },
  ],
};

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: treeToGraphData(treeData),   // Convert to GraphData format
  layout: {
    type: 'mindmap',
    direction: 'H',
  },
  behaviors: ['drag-canvas', 'zoom-canvas', 'collapse-expand'],
});

graph.render();
```

## Remote Data Loading

```javascript
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: { nodes: [], edges: [] },  // Initial empty data
  layout: { type: 'force' },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

// Asynchronous data loading
fetch('https://api.example.com/graph-data')
  .then((res) => res.json())
  .then((data) => {
    graph.setData(data);     // Or set before render
    graph.render();
  });

// Recommended approach: Update after render
await graph.render();
const data = await fetch('/api/data').then((r) => r.json());
graph.setData(data);
await graph.draw();
```

## Data Manipulation API

```javascript
// Read data
const allNodes = graph.getNodeData();
const oneNode = graph.getNodeData('n1');
const allEdges = graph.getEdgeData();
const oneEdge = graph.getEdgeData('e1');

// Add
graph.addNodeData([
  { id: 'n10', data: { label: 'New Node' } },
]);
graph.addEdgeData([
  { source: 'n1', target: 'n10' },
]);
await graph.draw();

// Update
graph.updateNodeData([
  { id: 'n1', data: { label: 'Updated' }, style: { fill: 'red' } },
]);
await graph.draw();

// Delete
graph.removeNodeData(['n10']);    // Also deletes associated edges
graph.removeEdgeData(['e1']);
await graph.draw();

// Batch update data (replace all)
graph.setData({ nodes: [...], edges: [...] });
await graph.draw();
```

## Separation of Style and Data (Best Practice)

```javascript
// ✅ Recommended: Place business data in `data`, and calculate styles through callback functions from `data`
const nodes = [
  { id: 'n1', data: { name: 'High Priority', priority: 'high', value: 100 } },
  { id: 'n2', data: { name: 'Low Priority', priority: 'low', value: 30 } },
];

const graph = new Graph({
  container: 'container',
  data: { nodes, edges: [] },
  node: {
    style: {
      // Map data to styles through callback functions
      fill: (d) => d.data.priority === 'high' ? '#ff4d4f' : '#1783FF',
      size: (d) => Math.max(20, d.data.value / 2),
      labelText: (d) => d.data.name,
    },
  },
});
```

## Common Errors and Fixes

### Error 1: Business Attributes at the Node Top Level

```javascript
// ❌ Incorrect: label, type, and other business attributes directly at the node top level
{ id: 'n1', label: 'Node 1', category: 'user', value: 100 }

// ✅ Correct: Business attributes placed in the data field
{ id: 'n1', data: { label: 'Node 1', category: 'user', value: 100 } }
```

### Error 2: Edge Missing `source` or `target`

```javascript
// ❌ Incorrect: Missing `source` or `target`
{ id: 'e1', from: 'n1', to: 'n2' }    // v4 syntax

// ✅ Correct
{ id: 'e1', source: 'n1', target: 'n2' }
```

### Error 3: Duplicate Node IDs

```javascript
// ❌ Error: Duplicate IDs cause rendering anomalies
const nodes = [
  { id: 'node1', data: { label: 'A' } },
  { id: 'node1', data: { label: 'B' } },   // Duplicate ID
];

// ✅ Correct: Each node ID must be unique
const nodes = [
  { id: 'node-a', data: { label: 'A' } },
  { id: 'node-b', data: { label: 'B' } },
];
```

### Error 4: Edge source/target references a non-existent node

```javascript
// ❌ Error: References a non-existent node id
const edges = [
  { source: 'n1', target: 'n999' },  // n999 does not exist
];

// ✅ Correct: Ensure both source and target exist in nodes
```

### Error 5: Duplicate Edges Causing "Edge already exists" Error

G6 does not allow duplicate edges (edges with the same source and target). When dynamically generating edges, duplicates must be removed; otherwise, an `Edge already exists: xxx-yyy` error will be thrown.

```javascript
// ❌ Incorrect: Randomly generated edges may result in duplicates
const edges = [];
for (let i = 0; i < 34; i++) {
  for (let j = 0; j < 3; j++) {
    const target = Math.floor(Math.random() * 34);
    if (target !== i) {
      edges.push({ source: `${i}`, target: `${target}` }); // Potential duplicate!
    }
  }
}

// ✅ Correct: Use a Set to deduplicate, ensuring each source-target pair is unique
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

**Best Practice: Prioritize using explicit static edge data to avoid randomly generating edges.** If dynamic generation is necessary, ensure duplicates are checked before adding:

```javascript
// ✅ Recommended: Use explicit edge data, avoiding reliance on random generation
const data = {
  nodes: Array.from({ length: 10 }, (_, i) => ({ id: `${i}` })),
  edges: [
    { source: '0', target: '1' },
    { source: '0', target: '2' },
    { source: '1', target: '3' },
    { source: '2', target: '3' },
    // Each source-target pair appears only once
  ],
};

const graph = new Graph({
  container: 'container',
  autoFit: 'view',
  data,
  node: {
    style: {
      labelText: (d) => d.id,
      labelPlacement: 'center',
      labelFill: '#fff',
    },
  },
  layout: { type: 'circular' },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

### Error 6: treeToGraphData Not Imported

```javascript
// ❌ Error: Forgot to import treeToGraphData from @antv/g6
import { Graph } from '@antv/g6';
// ...
data: treeToGraphData(treeData),  // ReferenceError: treeToGraphData is not defined

// ✅ Correct: Must explicitly import
import { Graph, treeToGraphData } from '@antv/g6';
// ...
data: treeToGraphData(treeData),
```