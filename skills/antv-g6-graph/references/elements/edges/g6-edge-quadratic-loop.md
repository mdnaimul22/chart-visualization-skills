---
id: "g6-edge-quadratic-loop"
title: "G6 Quadratic Bezier Edge and Loop Edge"
description: |
  Use quadratic edges to achieve lightweight arc effects; use loop edges to handle self-connections of nodes.
  Quadratic edges have fewer control points than cubic edges, resulting in better performance.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "edges"
tags:
  - "edge"
  - "quadratic curve"
  - "loop"
  - "quadratic"
  - "loop"

related:
  - "g6-edge-line"
  - "g6-edge-cubic"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Quadratic Bézier Edge (quadratic)

`quadratic` is a lighter-weight curved edge compared to `cubic`, with only one control point.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
       { id: 'a', data: { label: 'A' } },
       { id: 'b', data: { label: 'B' } },
       { id: 'c', data: { label: 'C' } },
    ],
    edges: [
       { source: 'a', target: 'b', data: { label: 'Forward' } },
       { source: 'b', target: 'a', data: { label: 'Reverse' } },  // Reverse parallel edge
       { source: 'a', target: 'c', data: { label: 'Direct' } },
    ],
  },
  node: {
    type: 'circle',
    style: {
      size: 40,
      fill: '#1783FF',
      stroke: '#fff',
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: '#fff',
    },
  },
  edge: {
    type: 'quadratic',
    style: {
      stroke: '#aaa',
      lineWidth: 1.5,
      endArrow: true,
      // curveOffset: Controls the curvature (positive values bend right, negative values bend left)
      curveOffset: 30,
      // curvePosition: Controls the relative position of the control point on the path (0~1), default is 0.5
      curvePosition: 0.5,
      labelText: (d) => d.data.label,
      labelBackground: true,
    },
  },
  layout: { type: 'circular' },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

### Quadratic Unique Properties

| Property | Type | Default Value | Description |
|------|------|--------|------|
| `curveOffset` | `number` | `30` | Control point offset distance (px), controls curvature |
| `curvePosition` | `number` | `0.5` | Proportional position of the control point on the line segment (0~1) |
| `controlPoint` | `[number, number]` | — | Directly specifies the control point coordinates (overrides curveOffset/curvePosition) |

---

## Loop Edge

When the `source` and `target` of an edge are the same, G6 automatically renders it as a loop.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'State A' } },
       { id: 'n2', data: { label: 'State B' } },
    ],
    edges: [
       { source: 'n1', target: 'n2', data: { label: 'Transition' } },
      // Loop: source === target
       { source: 'n1', target: 'n1', data: { label: 'Self-Loop' } },
       { source: 'n2', target: 'n2', data: { label: 'Stay' } },
    ],
  },
  node: {
    type: 'circle',
    style: {
      size: 50,
      fill: '#1783FF',
      stroke: '#fff',
      lineWidth: 2,
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: '#fff',
    },
  },
  edge: {
    type: 'line',                   // Regular edges use 'line', loops are handled automatically by G6
    style: {
      stroke: '#aaa',
      lineWidth: 1.5,
      endArrow: true,
      labelText: (d) => d.data.label,
      labelBackground: true,
      // Loop style properties
      loopPlacement: 'top',         // 'top' | 'bottom' | 'left' | 'right', etc.
      loopClockwise: true,          // Clockwise
    },
  },
  layout: { type: 'circular', radius: 100 },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

### loop Style Properties (Effective when source === target)

| Property | Type | Default Value | Description |
|------|------|--------|------|
| `loopPlacement` | `'top' \| 'bottom' \| 'left' \| 'right' \| 'top-left' \| ...` | `'top'` | Loop direction |
| `loopClockwise` | `boolean` | `true` | Clockwise direction |
| `loopDist` | `number` | `20` | Offset distance of the loop from the node |

---

## Parallel Edge Processing

Multiple edges in the same direction overlap by default. Use the `process-parallel-edges` transform to automatically separate them:

```javascript
transforms: [
  {
    type: 'process-parallel-edges',
    offset: 15,                     // Parallel edge spacing
  },
],
edge: {
  type: 'quadratic',                // Recommended to use quadratic for displaying parallel edges
},
```