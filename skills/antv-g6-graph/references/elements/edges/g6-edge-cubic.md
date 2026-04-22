---
id: "g6-edge-cubic"
title: "G6 Cubic Bezier Curve Edge (Cubic Edge)"
description: |
  Connect nodes using cubic Bezier curve edges (cubic), with smooth curves suitable for any layout.
  Provides three variants: cubic, cubic-horizontal, and cubic-vertical.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "edges"
tags:
  - "edge"
  - "curve"
  - "cubic"
  - "Bezier"
  - "bezier"
  - "edge"

related:
  - "g6-edge-line"
  - "g6-edge-polyline"
  - "g6-layout-dagre"

use_cases:
  - "General graphs (suitable for various layouts)"
  - "Edges in hierarchical graphs (cubic-vertical with dagre TB)"
  - "Horizontal flowcharts (cubic-horizontal with dagre LR)"
  - "Parallel edge scenarios"

anti_patterns:
  - "For tree graphs, use cubic-vertical or cubic-horizontal instead of polyline"
  - "When edges are very dense, curves increase visual complexity; consider the edge-bundling plugin"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/element/edge/cubic"
---

## Core Concepts

`cubic` uses cubic Bezier curves to connect two points, providing a more aesthetically pleasing result than straight lines and is suitable for any node position.

**Three Variants:**
- `cubic`: General-purpose curve, suitable for all layouts
- `cubic-horizontal`: Horizontal S-shaped curve, works well with LR/RL direction layouts
- `cubic-vertical`: Vertical S-shaped curve, works well with TB/BT direction layouts

**Key Parameters for Controlling Curvature:**
- `curveOffset`: Degree of curve bending (positive/negative values control direction)
- `curvePosition`: Control point position (0~1)
- `controlPoints`: Custom control point coordinates

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'A' } },
       { id: 'n2', data: { label: 'B' } },
       { id: 'n3', data: { label: 'C' } },
    ],
    edges: [
       { source: 'n1', target: 'n2' },
       { source: 'n2', target: 'n3' },
       { source: 'n3', target: 'n1' },  // loop edge
    ],
  },
  node: {
    type: 'circle',
    style: {
      size: 40,
      fill: '#1783FF',
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: '#fff',
    },
  },
  edge: {
    type: 'cubic',                 // general curve
    style: {
      stroke: '#aaa',
      lineWidth: 1.5,
      endArrow: true,
    },
  },
  layout: { type: 'circular', radius: 150 },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

## Common Variants

### Vertical Hierarchy Graph (with dagre TB)

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'root', data: { label: 'Root Node' } },
       { id: 'a', data: { label: 'Child Node A' } },
       { id: 'b', data: { label: 'Child Node B' } },
       { id: 'c', data: { label: 'Child Node C' } },
    ],
    edges: [
       { source: 'root', target: 'a' },
       { source: 'root', target: 'b' },
       { source: 'root', target: 'c' },
    ],
  },
  node: {
    type: 'rect',
    style: {
      size: [100, 36],
      radius: 4,
      fill: '#f0f5ff',
      stroke: '#adc6ff',
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
    },
  },
  edge: {
    type: 'cubic-vertical',       // Vertical S-shaped curve
    style: {
      stroke: '#adc6ff',
      endArrow: true,
    },
  },
  layout: {
    type: 'dagre',
    rankdir: 'TB',
    ranksep: 60,
    nodesep: 20,
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});
```

### Horizontal Flowchart (with dagre LR)

```javascript
edge: {
  type: 'cubic-horizontal',      // Horizontal S-shaped curve
  style: {
    stroke: '#91caff',
    lineWidth: 2,
    endArrow: {
      type: 'triangle',
      fill: '#91caff',
      size: 8,
    },
    labelText: (d) => d.data.label,
    labelBackground: true,
    labelBackgroundFill: '#fff',
    labelBackgroundOpacity: 0.9,
  },
},
layout: {
  type: 'dagre',
  rankdir: 'LR',                  // From left to right
  ranksep: 80,
  nodesep: 30,
},
```

### Curved Edges in Radial Layout

```javascript
// Cubic edges work best in radial layouts
edge: {
  type: 'cubic',
  style: {
    stroke: '#ccc',
    lineWidth: 1,
    endArrow: false,
    curveOffset: 30,              // Controls the curvature
  },
},
layout: {
  type: 'radial',
  unitRadius: 100,
  focusNode: 'center',
},
```

### Gradient Edge

```javascript
// Using linear gradient (requires @antv/g gradient support)
edge: {
  type: 'cubic',
  style: {
    stroke: 'l(0) 0:#1783FF 1:#FF6B6B',  // Gradient color
    lineWidth: 2,
    endArrow: true,
  },
},
```

## Common Errors

### Error 1: Direction Mismatch

```javascript
// ❌ dagre LR layout with cubic-vertical (vertical curve)
layout: { type: 'dagre', rankdir: 'LR' },
edge: { type: 'cubic-vertical' },   // Direction mismatch, curve is not aesthetically pleasing

// ✅ LR layout with cubic-horizontal
layout: { type: 'dagre', rankdir: 'LR' },
edge: { type: 'cubic-horizontal' },

// ✅ TB layout with cubic-vertical
layout: { type: 'dagre', rankdir: 'TB' },
edge: { type: 'cubic-vertical' },
```

### Error 2: curveOffset Direction Confusion

```javascript
// Positive curveOffset bends right/up, negative bends left/down
edge: {
  type: 'cubic',
  style: {
    curveOffset: 50,   // Positive value bends to one side
    // curveOffset: -50,  // Negative value bends to the other side
  },
},
```