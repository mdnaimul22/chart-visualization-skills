---
id: "g6-plugin-background-snapline"
title: "G6 Background Plugin + Snapline Plugin (background / snapline)"
description: |
  background: Sets the background color, gradient, or image for the canvas.
  snapline: Displays smart alignment reference lines when dragging nodes, supporting automatic snapping.

library: "g6"
version: "5.x"
category: "plugins"
subcategory: "visual"
tags:
  - "background"
  - "snapline"
  - "alignment line"
  - "canvas background"
  - "snapping alignment"

related:
  - "g6-plugin-tooltip"
  - "g6-behavior-drag-element"

difficulty: "beginner"
completeness: "full"
created: "2026-04-16"
updated: "2026-04-16"
---

## Background Plugin (background)

Sets the background color, gradient, or background image for the graph canvas, supporting all CSS style properties.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
      { id: 'n1', data: { label: 'Node 1' } },
      { id: 'n2', data: { label: 'Node 2' } },
    ],
    edges: [{ source: 'n1', target: 'n2' }],
  },
  plugins: [
    {
      type: 'background',
      key: 'bg',
      backgroundColor: '#f0f2f5',   // Background color
    },
  ],
});

graph.render();
```

### background Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `type` | `string` | `'background'` | Plugin type |
| `key` | `string` | — | Unique identifier, used for `graph.updatePlugin()` |
| `backgroundColor` | `string` | — | Background color (CSS color) |
| `backgroundImage` | `string` | — | Background image (`'url(...)'`) |
| `backgroundSize` | `string` | `'cover'` | Background size (CSS background-size) |
| `backgroundRepeat` | `string` | — | Background repeat (CSS background-repeat) |
| `backgroundPosition` | `string` | — | Background position |
| `opacity` | `string` | — | Background opacity (0-1) |
| `transition` | `string` | `'background 0.5s'` | Transition animation |
| `zIndex` | `string` | `-1` | Stacking order, default -1 is below other elements |
| `width` | `string` | `'100%'` | Background width |
| `height` | `string` | `'100%'` | Background height |

> Note: The default `zIndex` of -1 ensures the background is below other DOM plugins such as grid lines.

### Common Background Styles

```javascript
// Solid Color Background
{ type: 'background', backgroundColor: '#f0f2f5' }

// Gradient Background
{ type: 'background', background: 'linear-gradient(45deg, #1890ff, #722ed1)', opacity: '0.8' }

// Image Background
{
  type: 'background',
  backgroundImage: 'url(https://example.com/bg.png)',
  backgroundRepeat: 'no-repeat',
  backgroundSize: 'cover',
  opacity: '0.2',
}

// Dark Theme Background
{ type: 'background', backgroundColor: '#1a1a2e' }
```

### Dynamic Background Update

```javascript
const graph = new Graph({
  plugins: [{ type: 'background', key: 'bg', backgroundColor: '#f0f2f5' }],
});

// Dynamically switch background
graph.updatePlugin({ key: 'bg', backgroundColor: '#e6f7ff', transition: 'background 1s ease' });
```

---

## Snapline Plugin

Automatically displays horizontal/vertical alignment reference lines when dragging nodes, supports automatic snapping, and facilitates precise alignment.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
      { id: 'n1' },
      { id: 'n2' },
      { id: 'n3' },
    ],
    edges: [],
  },
  layout: { type: 'grid' },
  behaviors: ['drag-canvas', 'drag-element'],
  plugins: [
    {
      type: 'snapline',
      key: 'snapline',
      tolerance: 5,        // Distance threshold to trigger alignment (px)
      offset: 20,          // Extension distance of alignment line ends (px)
      autoSnap: true,      // Whether to automatically snap to alignment position
      verticalLineStyle: { stroke: '#1783FF', lineWidth: 1 },
      horizontalLineStyle: { stroke: '#1783FF', lineWidth: 1 },
    },
  ],
});

graph.render();
```

### snapline Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `type` | `string` | `'snapline'` | Plugin type |
| `key` | `string` | — | Unique identifier |
| `tolerance` | `number` | `5` | Distance threshold for triggering alignment (px) |
| `offset` | `number` | `20` | Extension distance of alignment line at both ends (px) |
| `autoSnap` | `boolean` | `true` | Whether to automatically snap to alignment position |
| `shape` | `string \| Function` | `'key'` | Reference shape (`'key'` for main shape) |
| `verticalLineStyle` | `LineStyle` | `{ stroke: '#1783FF' }` | Vertical alignment line style |
| `horizontalLineStyle` | `LineStyle` | `{ stroke: '#1783FF' }` | Horizontal alignment line style |
| `filter` | `(node) => boolean` | `() => true` | Filter nodes that do not participate in alignment |

### Customizing Snapline Style

```javascript
plugins: [
  {
    type: 'snapline',
    tolerance: 8,
    autoSnap: false,     // Only display the line, do not automatically snap
    verticalLineStyle: {
      stroke: '#F08F56',
      lineWidth: 2,
      lineDash: [4, 4],
    },
    horizontalLineStyle: {
      stroke: '#17C76F',
      lineWidth: 2,
      lineDash: [4, 4],
    },
    // Exclude specific nodes from snapping
    filter: (node) => node.id !== 'fixed-node',
  },
]
```

---

## Combined Usage Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 500,
  data: {
    nodes: Array.from({ length: 9 }, (_, i) => ({ id: `n${i}` })),
    edges: [],
  },
  layout: { type: 'grid', cols: 3 },
  node: {
    type: 'rect',
    style: { size: [80, 40], fill: '#1783FF', stroke: '#fff', labelText: (d) => d.id },
  },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
  plugins: [
    {
      type: 'background',
      backgroundColor: '#f8f9fa',
    },
    {
      type: 'snapline',
      tolerance: 6,
      autoSnap: true,
      verticalLineStyle: { stroke: '#ff4d4f', lineWidth: 1 },
      horizontalLineStyle: { stroke: '#52c41a', lineWidth: 1 },
    },
  ],
});

graph.render();
```