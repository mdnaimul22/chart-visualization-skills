---
id: "g6-transform-parallel-edges-radial"
title: "G6 Data Transform: Parallel Edge Processing + Radial Label Placement (process-parallel-edges / place-radial-labels)"
description: |
  process-parallel-edges: Handles multiple parallel edges between two nodes, supporting bundled mode (expanded into arcs) and merged mode (folded into one).
  place-radial-labels: Automatically adjusts label angles and positions for radial layouts (radial trees, radial compact trees) to prevent label overlap.

library: "g6"
version: "5.x"
category: "transforms"
subcategory: "data"
tags:
  - "process-parallel-edges"
  - "place-radial-labels"
  - "parallel edges"
  - "multiple edges"
  - "radial labels"
  - "transforms"
  - "data transforms"

related:
  - "g6-edge-quadratic-loop"
  - "g6-layout-advanced"
  - "g6-core-transforms-animation"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-16"
updated: "2026-04-16"
---

## Parallel Edge Processing (process-parallel-edges)

When there are multiple edges between two nodes, automatically process these parallel edges to avoid overlapping. Two modes are provided:
- **bundle mode** (default): Expand each edge into a quadratic Bezier curve with different curvature
- **merge mode**: Merge multiple parallel edges into a single aggregated edge

### Bundle Mode (bundle)

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 500,
  data: {
    nodes: [
      { id: 'A', style: { x: 100, y: 300 } },
      { id: 'B', style: { x: 400, y: 150 } },
      { id: 'C', style: { x: 700, y: 300 } },
    ],
    edges: [
      // 5 parallel edges from A to B
      ...Array.from({ length: 5 }, (_, i) => ({
        id: `AB-${i}`,
        source: 'A',
        target: 'B',
        data: { label: `Relation ${i + 1}` },
      })),
      // Bidirectional edges are also supported
      { source: 'A', target: 'C' },
      { source: 'C', target: 'A' },
    ],
  },
  node: {
    style: {
      labelText: (d) => d.id,
      ports: [{ placement: 'center' }],
    },
  },
  edge: {
    // ⚠️ In bundle mode, do not set global edge.type here
    // process-parallel-edges will automatically set the parallel edge type to quadratic
    style: {
      labelText: (d) => d?.data?.label,
      endArrow: true,
    },
  },
  behaviors: ['drag-element', 'drag-canvas', 'zoom-canvas'],
  transforms: [
    {
      type: 'process-parallel-edges',
      mode: 'bundle',   // Default is bundle
      distance: 20,     // Distance between edges in bundle mode (px)
    },
  ],
});

graph.render();
```

> **Important:** Bundle mode will forcibly change the parallel edge type to `quadratic`. Therefore, do not set the global edge type in `edge.type`, as it will override the bundle processing result.

### Merge Mode (merge)

```javascript
const graph = new Graph({
  // ...
  edge: {
    style: {
      labelText: (d) => `${d.source}->${d.target}`,
      endArrow: true,
    },
  },
  transforms: [
    {
      type: 'process-parallel-edges',
      mode: 'merge',        // Merge into a single aggregated edge
      style: {              // Additional styles for the merged edge
        stroke: '#ff7a45',
        lineWidth: 3,
        halo: true,
        haloOpacity: 0.3,
        haloStroke: '#ff7a45',
      },
    },
  ],
});
```

> Note: The merged style is assigned to `datum.style`, which has a lower priority than `edge.style` (the default style configured in Graph).

### process-parallel-edges Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `type` | `string` | `'process-parallel-edges'` | Transformation type |
| `key` | `string` | — | Unique identifier for dynamic updates |
| `mode` | `'bundle' \| 'merge'` | `'bundle'` | Processing mode |
| `distance` | `number` | `15` | Edge spacing in bundle mode (px) |
| `edges` | `string[]` | — | Specifies the edge IDs to process (default: all) |
| `style` | `PathStyleProps \| Function` | — | Aggregated edge style in merge mode |

### Abbreviated Form

```javascript
// Use default configuration (bundle mode, distance=15)
transforms: ['process-parallel-edges']

// Dynamically update configuration
graph.updateTransform({ key: 'parallel', mode: 'bundle', distance: 30 });
```

---

## Radial Labels (place-radial-labels)

A label auto-layout transformation specifically designed for radial layouts (radial, dendrogram, etc.). Automatically adjusts the position and rotation angle of labels based on the angle of nodes in the circular layout to ensure readability.

```javascript
import { Graph, treeToGraphData } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 800,
  autoFit: 'view',
  data: treeToGraphData({
    id: 'root',
    children: [
      { id: 'a1', children: [{ id: 'a1-1' }, { id: 'a1-2' }] },
      { id: 'a2', children: [{ id: 'a2-1' }] },
      { id: 'a3', children: [{ id: 'a3-1' }, { id: 'a3-2' }, { id: 'a3-3' }] },
      { id: 'b1' },
      { id: 'b2', children: [{ id: 'b2-1' }, { id: 'b2-2' }] },
    ],
  }),
  node: {
    style: {
      size: 8,
      labelText: (d) => d.id,
      labelFontSize: 12,
    },
  },
  layout: {
    type: 'dendrogram',    // or 'compact-box' with radial
    radial: true,
  },
  transforms: [
    {
      type: 'place-radial-labels',
      offset: 4,           // Offset of labels from nodes (px)
    },
  ],
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

### place-radial-labels Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `type` | `string` | `'place-radial-labels'` | Transformation type |
| `offset` | `number` | — | Additional offset of the label from the node (px) |

### Radial Tree Complete Example

```javascript
import { Graph, treeToGraphData } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 800,
  autoFit: 'view',
  data: treeToGraphData({
    id: 'Root Node',
    children: Array.from({ length: 6 }, (_, i) => ({
      id: `Branch${i + 1}`,
      children: Array.from({ length: 3 }, (_, j) => ({
        id: `${i + 1}-${j + 1}`,
      })),
    })),
  }),
  node: {
    type: 'circle',
    style: {
      size: 10,
      fill: '#1783FF',
      labelText: (d) => d.id,
      labelFontSize: 11,
      labelFill: '#333',
    },
  },
  edge: {
    type: 'line',
    style: { stroke: '#aaa', lineWidth: 1 },
  },
  layout: {
    type: 'radial',          // Radial layout
    unitRadius: 120,
    preventOverlap: true,
    nodeSize: 20,
  },
  transforms: [
    {
      type: 'place-radial-labels',
      offset: 4,
    },
  ],
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

---

## Combined Usage: Bidirectional Graph + Parallel Edge Handling

```javascript
import { Graph } from '@antv/g6';

// Microservice dependency graph: Service A calls multiple APIs of Service B, and Service B returns responses
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 500,
  data: {
    nodes: [
      { id: 'service-a', data: { label: 'Service A' } },
      { id: 'service-b', data: { label: 'Service B' } },
      { id: 'service-c', data: { label: 'Service C' } },
    ],
    edges: [
      { source: 'service-a', target: 'service-b', data: { label: 'API /users' } },
      { source: 'service-a', target: 'service-b', data: { label: 'API /orders' } },
      { source: 'service-b', target: 'service-a', data: { label: 'Response' } },
      { source: 'service-b', target: 'service-c', data: { label: 'Query' } },
      { source: 'service-c', target: 'service-b', data: { label: 'Result' } },
    ],
  },
  node: {
    type: 'rect',
    style: {
      size: [120, 40],
      fill: '#e6f7ff',
      stroke: '#1783FF',
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      ports: [{ placement: 'center' }],
    },
  },
  edge: {
    style: {
      labelText: (d) => d?.data?.label,
      labelBackground: true,
      endArrow: true,
      stroke: '#1783FF',
    },
  },
  layout: { type: 'force', linkDistance: 200 },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
  transforms: [
    {
      type: 'process-parallel-edges',
      mode: 'bundle',
      distance: 25,
    },
  ],
});

graph.render();
```