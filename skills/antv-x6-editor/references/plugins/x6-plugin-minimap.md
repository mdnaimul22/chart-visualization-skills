---
id: "x6-plugin-minimap"
title: "X6 MiniMap Plugin"
description: |
  The MiniMap plugin displays a thumbnail view of the canvas in a separate container, supporting quick navigation through dragging the viewport frame. It is suitable for large canvas scenarios.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "minimap"
tags:
  - "MiniMap"
  - "小地图"
  - "缩略图"
  - "导航"
  - "minimap"
  - "overview"

related:
  - "x6-plugins"
  - "x6-plugin-scroller"
  - "x6-core-graph-init"

use_cases:
  - "Global preview of large canvases"
  - "Quick navigation via MiniMap"
  - "View the current viewport's position in the global context"

difficulty: "beginner"
completeness: "full"
---
## Basic Usage

```javascript
import { Graph, MiniMap } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new MiniMap({
  enabled: true,
  container: document.getElementById('minimap'),
  width: 200,
  height: 160,
}));
```

**Important**: MiniMap requires a separate DOM container and cannot share the same container as the canvas.

## Configuration Options

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `container` | HTMLElement | **Required** | DOM container for the mini-map |
| `width` | number | `300` | Width of the mini-map |
| `height` | number | `200` | Height of the mini-map |
| `padding` | number | `10` | Inner padding of the mini-map |
| `scalable` | boolean | `true` | Whether the canvas can be scaled via the mini-map (by dragging the viewport box corners) |
| `minScale` | number | `0.01` | Minimum scale ratio |
| `maxScale` | number | `16` | Maximum scale ratio |
| `graphOptions` | object | `{}` | Configuration passed to the internal thumbnail Graph |
| `createGraph` | function | - | Custom method to create the thumbnail Graph |

## Complete Example

```javascript
import { Graph, Scroller, MiniMap } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
  grid: { visible: true },
});

// Scroller provides scrolling capability
graph.use(new Scroller({ enabled: true, pannable: true }));

// MiniMap provides a global preview
graph.use(new MiniMap({
  enabled: true,
  container: document.getElementById('minimap'),
  width: 200,
  height: 160,
  padding: 10,
  scalable: true,
}));

// Add a large number of nodes
for (let i = 0; i < 30; i++) {
  graph.addNode({
    x: Math.random() * 3000,
    y: Math.random() * 2000,
    width: 100,
    height: 50,
    label: `Node ${i + 1}`,
  });
}
```

## HTML Layout Example

The minimap container needs to be prepared in advance in HTML:

```html
<div style="display: flex;">
  <!-- Canvas container -->
  <div id="container" style="flex: 1; height: 600px;"></div>
  <!-- Minimap container -->
  <div id="minimap" style="width: 200px; height: 160px; border: 1px solid #ccc;"></div>
</div>
```

## Common Errors

### ❌ Container Not Provided

```javascript
// Error: Missing container
graph.use(new MiniMap({
  enabled: true,
  width: 200,
  height: 160,
  // ❌ Missing container, minimap has nowhere to render
}));
```

```javascript
// Correct: Provide an independent DOM container
graph.use(new MiniMap({
  enabled: true,
  container: document.getElementById('minimap'),  // ✅
  width: 200,
  height: 160,
}));
```

### ❌ container is the same as the canvas container

```javascript
// Error: The minimap and canvas cannot use the same container
const el = document.getElementById('container');
const graph = new Graph({ container: el });
graph.use(new MiniMap({ container: el }));  // ❌ Conflict
```

```javascript
// Correct: Use an independent container
const graph = new Graph({ container: document.getElementById('container') });
graph.use(new MiniMap({
  container: document.getElementById('minimap'),  // ✅ Independent container
}));
```

### ❌ Configure minimap in the constructor

```javascript
// Error: Not supported in 3.x
const graph = new Graph({
  container: 'container',
  minimap: { enabled: true, container: el },  // ❌
});
```

```javascript
// Correct
import { Graph, MiniMap } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new MiniMap({ enabled: true, container: el }));  // ✅
```