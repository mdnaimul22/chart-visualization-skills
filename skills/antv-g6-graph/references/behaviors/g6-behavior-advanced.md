---
id: "g6-behavior-advanced"
title: "G6 Advanced Interaction Behaviors (fix-element-size / auto-adapt-label / drag-element-force)"
description: |
  fix-element-size: Maintain the size of specified elements (labels, borders, etc.) unchanged during scaling.
  auto-adapt-label: Automatically hide overlapping labels when viewport space is insufficient.
  drag-element-force: Real-time dragging of nodes and updating the layout in force-directed layouts.

library: "g6"
version: "5.x"
category: "behaviors"
subcategory: "interaction"
tags:
  - "interaction"
  - "fix-element-size"
  - "auto-adapt-label"
  - "drag-element-force"
  - "performance optimization"

related:
  - "g6-behavior-drag-element"
  - "g6-layout-force"

difficulty: "advanced"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Fix Element Size During Zoom (fix-element-size)

When users zoom out the canvas, maintain the absolute pixel size of critical visual elements such as labels and borders to prevent fonts from becoming too small and unreadable.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: Array.from({ length: 20 }, (_, i) => ({
      id: `n${i}`,
      label: `Node${i}`,
    })),
    edges: Array.from({ length: 15 }, (_, i) => ({
      source: `n${i % 10}`,
      target: `n${(i + 5) % 20}`,
    })),
  },
  node: {
    type: 'circle',
    style: {
      size: 36,
      fill: '#1783FF',
      stroke: '#fff',
      lineWidth: 2,
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
      labelFontSize: 12,
    },
  },
  layout: { type: 'force', preventOverlap: true },
  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    'drag-element',
    {
      type: 'fix-element-size',
      // Enable only when zooming out (zoom < 1)
      enable: (event) => event.data.scale < 1,
      // Fix node label size
      node: [
        { shape: 'label' },                    // Fix label (font size and position do not change with zoom)
        { shape: 'key', fields: ['lineWidth'] }, // Fix node border width
      ],
      // Fix edge label and line width
      edge: [
        { shape: 'label' },
        { shape: 'key', fields: ['lineWidth'] },
        { shape: 'halo', fields: ['lineWidth'] },
      ],
    },
  ],
});

graph.render();
```

### fix-element-size Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `enable` | `boolean \| ((event) => boolean)` | `(e) => e.data.scale < 1` | Enable condition |
| `node` | `FixShapeConfig[]` | — | List of shapes to fix in nodes |
| `edge` | `FixShapeConfig[]` | — | List of shapes to fix in edges |
| `combo` | `FixShapeConfig[]` | — | List of shapes to fix in combos |
| `reset` | `boolean` | `false` | Whether to restore the original style when redrawing |

**FixShapeConfig:**
```typescript
interface FixShapeConfig {
  shape: string;           // Shape name: 'key' | 'label' | 'halo' | 'icon' | ...
  fields?: string[];       // Fix only specific properties (e.g., lineWidth), all properties are fixed if not specified
}
```

---

## Auto-Hide Overlapping Labels (auto-adapt-label)

When viewport space is insufficient, automatically hide low-priority labels based on node importance (centrality) to avoid text overlap.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: Array.from({ length: 50 }, (_, i) => ({
      id: `n${i}`,
      label: `Node${i}`,
      degree: Math.floor(Math.random() * 10),
    })),
    edges: Array.from({ length: 60 }, (_, i) => ({
      source: `n${i % 25}`,
      target: `n${(i * 3 + 7) % 50}`,
    })),
  },
  node: {
    type: 'circle',
    style: {
      size: 20,
      fill: '#1783FF',
      stroke: '#fff',
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
      labelFontSize: 11,
    },
  },
  layout: { type: 'force', preventOverlap: true, nodeSize: 20 },
  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    {
      type: 'auto-adapt-label',
      // Label spacing detection padding (px)
      padding: 4,
      // Node importance sorting: Use centrality, nodes with higher degree are prioritized
      sortNode: {
        type: 'degree',              // 'degree' | 'betweenness' | 'closeness' | 'eigenvector'
        direction: 'both',           // 'in' | 'out' | 'both'
      },
      // Debounce delay (ms)
      throttle: 100,
    },
  ],
});

graph.render();
```

### auto-adapt-label Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `padding` | `number` | `0` | Additional spacing for label collision detection |
| `sortNode` | `NodeCentralityOptions \| SortFn` | `{ type: 'degree' }` | Node sorting (determines which labels are displayed first) |
| `sortEdge` | `SortFn` | — | Edge sorting function |
| `sortCombo` | `SortFn` | — | Combo sorting function |
| `throttle` | `number` | `100` | Debounce delay (ms) |

---

## Dragging Nodes in Force-Directed Layout (drag-element-force)

When the d3-force layout is running, dragging nodes simultaneously updates the layout force field, achieving realistic physical effects.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: Array.from({ length: 20 }, (_, i) => ({
      id: `n${i}`,
      label: `N${i}`,
    })),
    edges: Array.from({ length: 25 }, (_, i) => ({
      source: `n${i % 15}`,
      target: `n${(i * 2 + 3) % 20}`,
    })),
  },
  node: {
    type: 'circle',
    style: {
      size: 30,
      fill: '#1783FF',
      stroke: '#fff',
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: '#fff',
    },
  },
  layout: {
    type: 'd3-force',              // Must use d3-force or d3-force-3d
    link: { distance: 80 },
    many: { strength: -200 },
  },
  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    {
      type: 'drag-element-force',
      // true: Node is fixed in current position after dragging (no longer participates in layout)
      // false: Continues to participate in the layout force field after release
      fixed: false,
    },
  ],
});

graph.render();
```

### drag-element-force Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `fixed` | `boolean` | `false` | Whether the node is fixed after dragging and releasing |

> **Note:** `drag-element-force` only supports `d3-force` / `d3-force-3d` layouts and is not compatible with the regular `force` layout. For regular force-directed graphs, please use `drag-element`.