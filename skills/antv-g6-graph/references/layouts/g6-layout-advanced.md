---
id: "g6-layout-advanced"
title: "G6 Advanced Layouts (concentric / radial / mds / fruchterman)"
description: |
  Configuration and usage scenarios for four layouts: concentric (concentric circles), radial (radiating), mds (dimensionality reduction with distance preservation), and fruchterman (fast force-directed).

library: "g6"
version: "5.x"
category: "layouts"
subcategory: "advanced"
tags:
  - "layout"
  - "concentric"
  - "radial"
  - "mds"
  - "fruchterman"

related:
  - "g6-layout-force"
  - "g6-layout-circular"
  - "g6-layout-dagre"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Concentric Layout (concentric)

Nodes are layered based on their attribute values, with nodes having larger values placed in the inner circle.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 640,
  data: {
    nodes: Array.from({ length: 20 }, (_, i) => ({
      id: `n${i}`,
      data: { label: `N${i}`, degree: Math.floor(Math.random() * 10) },
    })),
    edges: Array.from({ length: 25 }, (_, i) => ({
      source: `n${i % 10}`,
      target: `n${(i * 3 + 5) % 20}`,
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
  },
  layout: {
    type: 'concentric',
    // Field used for sorting (nodes with larger values are placed in the inner circle)
    sortBy: 'degree',            // Field name or 'degree' (automatically calculates degree)
    // Minimum spacing between concentric circles (px)
    minNodeSpacing: 20,
    // Distance between levels
    levelDistance: 60,
    // Prevent node overlap
    preventOverlap: true,
    nodeSize: 30,
    // Radius of the outermost circle
    maxLevelDiff: 0.5,
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

---

## Radial Layout (radial)

Arranges nodes in a radial pattern outward from a specified center node, based on graph distance, with clear hierarchical layers.

```javascript
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 800,
  data: {
    nodes: Array.from({ length: 20 }, (_, i) => ({ id: `n${i}`, data: {} })),
    edges: [
       { source: 'n0', target: 'n1' },
       { source: 'n0', target: 'n2' },
       { source: 'n0', target: 'n3' },
       { source: 'n1', target: 'n4' },
       { source: 'n1', target: 'n5' },
      // ...
    ],
  },
  node: {
    type: 'circle',
    style: {
      size: 30,
      fill: '#1783FF',
      stroke: '#fff',
      labelText: (d) => d.id,
      labelPlacement: 'bottom',
    },
  },
  layout: {
    type: 'radial',
    // Center node id (defaults to the first node)
    focusNode: 'n0',
    // Spacing between layers
    unitRadius: 80,
    // Prevent overlap
    preventOverlap: true,
    nodeSize: 30,
    // Strict radius (nodes at each level are arranged at the same radius as much as possible)
    strictRadii: true,
    // Spacing between child nodes
    nodeSpacing: 5,
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

---

## Dimensionality Reduction Layout (MDS)

Maintains the graph distance (shortest path distance) between nodes, suitable for displaying similarity/distance relationships.

```javascript
const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: { nodes: [...], edges: [...] },
  layout: {
    type: 'mds',
    // Edge weight field (read from edge.data, affects node distance calculation)
    linkDistance: 100,
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});
```

---

## Fast Fruchterman (fruchterman)

Faster than d3-force, suitable for medium-sized graphs (hundreds of nodes), and supports GPU acceleration.

```javascript
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: { nodes: [...], edges: [...] },
  layout: {
    type: 'fruchterman',
    // Number of iterations (more iterations lead to more stability but slower performance)
    iterations: 1000,
    // Gravity coefficient (prevents nodes from flying out)
    gravity: 10,
    // Speed (affects convergence speed)
    speed: 5,
    // Enable clustering
    clustering: false,
    // Repulsion force between nodes
    k: undefined,           // Default is auto-calculated
    // Use WebWorker (runs asynchronously, does not block the main thread)
    workerEnabled: true,
  },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

### Comparison of Fruchterman and Force

| Feature | force (d3-force) | fruchterman |
|---------|------------------|-------------|
| Algorithm | D3 Force-Directed | Fruchterman-Reingold |
| Performance | Moderate | Faster |
| GPU Acceleration | Not Supported | Supported |
| Configurable Force Types | Yes (link/many/center...) | No |
| Large Graphs | Requires Optimization | Better |

---

## Layout Selection Guide

```
Need hierarchical relationships?
  → Directed Acyclic Graph (DAG): dagre / antv-dagre
  → Tree structure: compact-box / mindmap / dendrogram / indented

Need circular/symmetric arrangement?
  → Few nodes: circular
  → Layered by attribute: concentric
  → Centered around a point: radial

Need physical spring effect?
  → Small graph (< 200 nodes): force / d3-force
  → Medium graph (< 500 nodes): fruchterman
  → Large graph (> 500 nodes): force-atlas2

Need to preserve original position relationships?
  → Use node x/y coordinates + layout: { type: 'preset' } (or do not set layout)

Other special requirements?
  → Grid alignment: grid
  → Preserve graph distances: mds
```