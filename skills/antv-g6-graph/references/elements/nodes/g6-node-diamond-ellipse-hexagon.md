---
id: "g6-node-diamond-ellipse-hexagon"
title: "G6 Polygon Nodes (Diamond / Ellipse / Hexagon)"
description: |
  Create graph visualizations using diamond, ellipse, and hexagon nodes.
  Suitable for flowchart decision nodes, emphasizing vertical relationships, honeycomb layouts, and similar scenarios.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "nodes"
tags:
  - "node"
  - "diamond"
  - "ellipse"
  - "hexagon"

related:
  - "g6-node-circle"
  - "g6-node-rect"
  - "g6-state-overview"

use_cases:
  - "Flowchart decision nodes (diamond)"
  - "Honeycomb/hive layouts (hexagon)"
  - "Emphasizing vertical relationships (ellipse)"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Diamond Node (diamond)

The diamond node is commonly used in flowcharts as a decision node (judgment branch).

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
       { id: 'start', data: { label: 'Start' } },
       { id: 'decision', data: { label: 'Does it meet the condition?' } },
       { id: 'yes', data: { label: 'Execute A' } },
       { id: 'no', data: { label: 'Execute B' } },
    ],
    edges: [
       { source: 'start', target: 'decision' },
       { source: 'decision', target: 'yes', data: { label: 'Yes' } },
       { source: 'decision', target: 'no', data: { label: 'No' } },
    ],
  },
  node: {
    // Specify different types by node id through callback
    type: (d) => (d.id === 'decision' ? 'diamond' : 'rect'),
    style: {
      size: (d) => (d.id === 'decision' ? 60 : [100, 40]),
      fill: (d) => (d.id === 'decision' ? '#faad14' : '#1783FF'),
      stroke: '#fff',
      lineWidth: 2,
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: '#fff',
      labelFontSize: 12,
    },
  },
  edge: {
    style: {
      endArrow: true,
      labelText: (d) => d.data.label,
      labelBackground: true,
    },
  },
  layout: { type: 'dagre', rankdir: 'TB', nodesep: 30, ranksep: 40 },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

### diamond Style Properties

| Property | Type | Description |
|------|------|------|
| `size` | `number` | Overall node size, controls width and height |
| `fill` | `string` | Fill color |
| `stroke` | `string` | Stroke color |
| `lineWidth` | `number` | Stroke width |

---

## Ellipse Node (ellipse)

The ellipse node has a default size of [45, 35], suitable for scenarios such as database entities (ER diagrams).

```javascript
node: {
  type: 'ellipse',
  style: {
    size: [80, 50],          // [width, height]
    fill: '#722ED1',
    stroke: '#fff',
    lineWidth: 2,
    labelText: (d) => d.data.label,
    labelPlacement: 'center',
    labelFill: '#fff',
  },
},
```

### Ellipse-specific Attributes

| Attribute | Type | Description |
|------|------|------|
| `size` | `[number, number]` | `[width, height]`, corresponding to rx×2, ry×2 respectively |

---

## Hexagon Node (hexagon)

Hexagon nodes are suitable for honeycomb layouts, offering excellent space utilization.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: Array.from({ length: 12 }, (_, i) => ({
      id: `h${i}`,
      data: { label: `Area${i + 1}`, value: Math.random() * 100 },
    })),
    edges: [],
  },
  node: {
    type: 'hexagon',
    style: {
      size: 60,              // Circumscribed circle radius * 2
      fill: (d) => {
        const level = Math.floor(d.data.value / 33);
        return ['#52c41a', '#faad14', '#ff4d4f'][level] || '#1783FF';
      },
      stroke: '#fff',
      lineWidth: 2,
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: '#fff',
      labelFontSize: 11,
    },
  },
  layout: { type: 'grid', cols: 4 },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

### Hexagon-specific Properties

| Property | Type | Description |
|------|------|------|
| `size` | `number` | Equivalent to `outerR * 2` (diameter of the circumscribed circle) |

---

## Common Errors

### Error: Setting array size for diamond/hexagon

```javascript
// ❌ diamond/hexagon/star/triangle only accept a single number
node: {
  type: 'diamond',
  style: { size: [60, 40] },
}

// ✅ Correct
node: {
  type: 'diamond',
  style: { size: 60 },
}

// Only ellipse/rect support [width, height] array
node: {
  type: 'ellipse',
  style: { size: [80, 50] },
}
```