---
id: "g6-core-transforms-animation"
title: "G6 Data Transforms and Animation System"
description: |
  Transforms: Process graph data before rendering (node size mapping, parallel edge processing, etc.).
  Animation: Element enter/exit/update animations, viewport animations, custom animation configurations.

library: "g6"
version: "5.x"
category: "core"
subcategory: "data"
tags:
  - "transforms"
  - "animation"
  - "map-node-size"
  - "process-parallel-edges"
  - "animation"

related:
  - "g6-core-graph-init"
  - "g6-core-graph-api"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Data Transformations (Transforms)

Transforms are the processing pipelines that occur before data is bound to chart elements, used for mapping data to visual attributes.

### map-node-size (Node Size Mapping)

Map node data fields to node size ranges:

```javascript
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'A', value: 10 } },
       { id: 'n2', data: { label: 'B', value: 50 } },
       { id: 'n3', data: { label: 'C', value: 100 } },
    ],
    edges: [
       { source: 'n1', target: 'n2' },
       { source: 'n2', target: 'n3' },
    ],
  },
  // transforms at the top level of Graph configuration
  transforms: [
    {
      type: 'map-node-size',
      field: 'value',          // Data field to map (read from node.data)
      range: [16, 60],         // Size range to map to [min, max] (px)
    },
  ],
  node: {
    type: 'circle',
    style: {
      // size does not need to be manually set, transform calculates it automatically
      fill: '#1783FF',
      stroke: '#fff',
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
  },
  layout: { type: 'force', preventOverlap: true },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

### process-parallel-edges (Parallel Edge Processing)

When there are multiple edges between two nodes, they are automatically staggered for display:

```javascript
transforms: [
  {
    type: 'process-parallel-edges',
    offset: 15,                // Spacing between parallel edges (px)
    // Apply curves only to edges with parallel relationships
  },
],
edge: {
  type: 'quadratic',           // Recommended to use with quadratic
  style: {
    stroke: '#aaa',
    endArrow: true,
  },
},
```

### Built-in Transforms List

| Type | Description | Common Parameters |
|------|-------------|---------------|
| `map-node-size` | Data-driven node size | `field`, `range` |
| `process-parallel-edges` | Offset parallel edges for display | `offset` |
| `place-radial-labels` | Automatic positioning of labels in radial layouts | — |
| `arrange-draw-order` | Adjust element rendering order | `nodeBeforeEdge` |
| `get-edge-actual-ends` | Calculate actual edge endpoints (port support) | — |
| `update-related-edge` | Update related edges when a node moves | — |

---

## Animation System

### Global Animation Switch

```javascript
const graph = new Graph({
  container: 'container',
  // Disable all animations (improve performance for large graphs)
  animation: false,
  // ...
});
```

### Element Enter/Exit/Update Animation

```javascript
const graph = new Graph({
  container: 'container',
    { nodes: [...], edges: [...] },
  node: {
    type: 'circle',
    style: { size: 40, fill: '#1783FF' },
    // Animation configuration (each stage is independent)
    animation: {
      // Initial node enter animation
      enter: [
        {
          fields: ['opacity'],         // Animation properties
          from: { opacity: 0 },        // Starting value
          to: { opacity: 1 },          // Ending value
          duration: 500,
          easing: 'ease-in',
        },
      ],
      // Node update animation (when data changes)
      update: [
        {
          fields: ['fill', 'size'],
          duration: 300,
          easing: 'linear',
        },
      ],
      // Node exit animation (when deleted)
      exit: [
        {
          fields: ['opacity'],
          to: { opacity: 0 },
          duration: 300,
        },
      ],
    },
  },
});
```

### Viewport Animation Configuration

All viewport operations (`fitView`, `focusElement`, `zoomTo`, `translateTo`) support animation parameters:

```javascript
// ViewportAnimationEffectTiming
await graph.fitView({
  padding: 20,
  // Animation configuration
  easing: 'ease-in-out',
  duration: 600,
});

await graph.zoomTo(1.5, {
  easing: 'ease-out',
  duration: 400,
});

await graph.focusElement('n1', {
  easing: 'ease-in-out',
  duration: 500,
});
```

### Common easing values

| Value | Description |
|----|------|
| `'linear'` | Constant speed |
| `'ease'` | Slow, then fast, then slow |
| `'ease-in'` | Slow, then fast |
| `'ease-out'` | Fast, then slow |
| `'ease-in-out'` | Slow, fast, slow |
| `'cubic-bezier(...)` | Custom cubic Bézier |

---

## Performance Optimization Suggestions

```javascript
// 1. Disable animations for large graphs (> 1000 nodes)
animation: false,

// 2. Use optimize-viewport-transform behavior to reduce rendering
behaviors: [
  'drag-canvas',
  'zoom-canvas',
  {
    type: 'optimize-viewport-transform',
    // Hide details (labels, etc.) during viewport transformation to improve frame rate
    shapes: (id, elementType) => {
      if (elementType === 'node') return ['label', 'icon', 'halo'];
      return ['label'];
    },
  },
],

// 3. Stop force-directed iteration after layout completion
layout: {
  type: 'force',
  maxIteration: 300,           // Limit maximum number of iterations
  minMovement: 0.5,            // Convergence threshold
},
```