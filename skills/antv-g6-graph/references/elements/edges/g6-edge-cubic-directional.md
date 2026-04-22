---
id: "g6-edge-cubic-directional"
title: "G6 Directed Cubic Bezier Curve Edge (cubic-horizontal / cubic-vertical)"
description: |
  cubic-horizontal: Horizontal cubic Bezier curve, with control points distributed horizontally, suitable for horizontal flowcharts (LR direction).
  cubic-vertical: Vertical cubic Bezier curve, with control points distributed vertically, suitable for vertical hierarchy charts (TB direction).
  Both are directional variants of the cubic edge, used in conjunction with the LR and TB direction layouts of dagre/antv-dagre, respectively.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "edges"
tags:
  - "cubic-horizontal"
  - "cubic-vertical"
  - "Bezier curve"
  - "directed edge"
  - "flowchart edge"
  - "hierarchy chart edge"

related:
  - "g6-edge-cubic"
  - "g6-layout-dagre"
  - "g6-pattern-flow-chart"

difficulty: "beginner"
completeness: "full"
created: "2026-04-16"
updated: "2026-04-16"
---

## Edge Type Comparison

| Type | Direction | Control Point Axis | Best Matching Layout |
|------|------|---------|-------------|
| `cubic` | Arbitrary | Distance between endpoints | General |
| `cubic-horizontal` | Horizontal (Left→Right) | X-axis | dagre `rankdir: 'LR'` |
| `cubic-vertical` | Vertical (Top→Bottom) | Y-axis | dagre `rankdir: 'TB'` |

---

## Horizontal Cubic Bezier Curve (cubic-horizontal)

Control points are primarily distributed along the X-axis, ignoring changes along the Y-axis, resulting in a horizontal S-shaped curve effect. Suitable for horizontal flowcharts.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 500,
  data: {
    nodes: [
      { id: 'start', data: { label: 'Start' } },
      { id: 'process', data: { label: 'Process' } },
      { id: 'decision', data: { label: 'Decision' } },
      { id: 'end', data: { label: 'End' } },
    ],
    edges: [
      { source: 'start', target: 'process' },
      { source: 'process', target: 'decision' },
      { source: 'decision', target: 'end' },
    ],
  },
  node: {
    type: 'rect',
    style: {
      size: [80, 36],
      fill: '#e6f7ff',
      stroke: '#1783FF',
      radius: 4,
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      // Set connection points to the left and right sides
      ports: [{ placement: 'right' }, { placement: 'left' }],
    },
  },
  edge: {
    type: 'cubic-horizontal',    // Horizontal cubic Bezier curve
    style: {
      stroke: '#1783FF',
      lineWidth: 1.5,
      endArrow: true,
      labelText: (d) => d?.data?.label,
      labelBackground: true,
    },
  },
  layout: {
    type: 'antv-dagre',
    rankdir: 'LR',           // From left to right, combined with cubic-horizontal
    nodesep: 20,
    ranksep: 100,
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

### Style Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `curvePosition` | `number \| [number, number]` | `[0.5, 0.5]` | Relative position of the control point on the line connecting the endpoints (0-1) |
| `curveOffset` | `number \| [number, number]` | `[0, 0]` | Offset distance of the control point from the line connecting the endpoints (px) |

Common Edge Style Parameters (Inherited from BaseEdge):

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `stroke` | `string` | — | Edge color |
| `lineWidth` | `number` | `1` | Line width |
| `endArrow` | `boolean` | `false` | Whether to display the end arrow |
| `startArrow` | `boolean` | `false` | Whether to display the start arrow |
| `lineDash` | `number[]` | — | Dashed line style |
| `labelText` | `string \| Function` | — | Label text |
| `labelBackground` | `boolean` | `false` | Whether to display the label background |

---

## Vertical Cubic Bezier Curve (cubic-vertical)

Control points are primarily distributed along the Y-axis, ignoring changes along the X-axis, resulting in a vertical S-shaped curve effect. Suitable for vertical hierarchical charts and organizational structure diagrams.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 600,
  height: 700,
  data: {
    nodes: [
      { id: 'ceo', data: { label: 'CEO' } },
      { id: 'cto', data: { label: 'CTO' } },
      { id: 'cfo', data: { label: 'CFO' } },
      { id: 'dev1', data: { label: 'Frontend Team' } },
      { id: 'dev2', data: { label: 'Backend Team' } },
      { id: 'finance', data: { label: 'Finance Department' } },
    ],
    edges: [
      { source: 'ceo', target: 'cto' },
      { source: 'ceo', target: 'cfo' },
      { source: 'cto', target: 'dev1' },
      { source: 'cto', target: 'dev2' },
      { source: 'cfo', target: 'finance' },
    ],
  },
  node: {
    type: 'rect',
    style: {
      size: [100, 36],
      fill: '#f6ffed',
      stroke: '#52c41a',
      radius: 4,
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      // Set connection points to top and bottom sides
      ports: [{ placement: 'top' }, { placement: 'bottom' }],
    },
  },
  edge: {
    type: 'cubic-vertical',    // Vertical cubic Bezier curve
    style: {
      stroke: '#52c41a',
      lineWidth: 1.5,
      endArrow: true,
    },
  },
  layout: {
    type: 'antv-dagre',
    rankdir: 'TB',          // Top to bottom, coordinated with cubic-vertical
    nodesep: 40,
    ranksep: 80,
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

---

## Adjust Curvature

```javascript
edge: {
  type: 'cubic-horizontal',
  style: {
    // curvePosition: Control point position (0-1), 0.5 is the midpoint between the two endpoints
    curvePosition: 0.3,        // Single value: both control points at the same position
    // curvePosition: [0.4, 0.6], // Array: control the two control points separately

    // curveOffset: Control point offset (px), positive value offsets to one side, negative to the other
    curveOffset: 30,           // Increase curvature
  },
}
```

---

## State Styles

```javascript
edge: {
  type: 'cubic-horizontal',
  style: {
    stroke: '#d9d9d9',
    lineWidth: 1,
    endArrow: true,
  },
  state: {
    selected: {
      stroke: '#1783FF',
      lineWidth: 2,
      shadowColor: 'rgba(24,131,255,0.3)',
      shadowBlur: 8,
    },
    active: {
      stroke: '#40a9ff',
      lineWidth: 2,
    },
    inactive: {
      stroke: '#f0f0f0',
      lineWidth: 1,
    },
  },
},
```

---

## Selection Guide

```javascript
// Horizontal Flowchart (Left → Right)
// dagre rankdir: 'LR' + edge type: 'cubic-horizontal'
// Node ports: [{placement:'right'}, {placement:'left'}]

// Vertical Hierarchy Chart (Top → Bottom)
// dagre rankdir: 'TB' + edge type: 'cubic-vertical'
// Node ports: [{placement:'top'}, {placement:'bottom'}]

// General Curved Connection (Direction-Independent)
// edge type: 'cubic' (default)

// Orthogonal Polyline (Flowchart Style)
// edge type: 'polyline'
```