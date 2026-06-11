---
id: "x6-core-virtual-render"
title: "X6 Virtual Rendering"
description: |
  X6 virtual rendering mechanism, rendering only nodes and edges within the visible area, suitable for large data scenarios (thousands of nodes or more).
  Enabled via the virtual configuration option, it allows setting buffer margins and supports integration with the Scroller plugin.

library: "x6"
version: "3.x"
category: "core"
subcategory: "virtual-render"
tags:
  - "virtual"
  - "virtual rendering"
  - "performance"
  - "large data"
  - "visible area"
  - "on-demand rendering"
  - "performance"

related:
  - "x6-core-graph-init"
  - "x6-plugins"

use_cases:
  - "Rendering large graphs with thousands of nodes"
  - "Optimizing performance during canvas scrolling/zooming"
  - "Reducing the number of DOM nodes"
  - "Performance optimization for large flowcharts/lineage graphs"

difficulty: "intermediate"
completeness: "full"
---

## Core Concepts

**Virtual Render** is a performance optimization strategy: only nodes and edges within the currently visible area (plus a buffer margin) are rendered, and elements outside the viewport are not created as DOM nodes. When the user pans or zooms the canvas, the rendering area is automatically updated.

Applicable Scenarios:
- Number of nodes exceeds 500
- Large lineage graphs, organizational charts, network topology diagrams
- Requires smooth canvas interaction experience

## Configuration Methods

### Basic Enablement

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  virtual: true,  // Enable virtual rendering with default buffer margin of 120px
});
```

### Custom Buffer Margin

```javascript
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  virtual: {
    enabled: true,
    margin: 200,  // Elements within 200px outside the visible area will also be rendered
  },
});
```

## Configuration Options

### virtual Parameter

| Type | Description |
|------|------|
| `boolean` | `true` to enable, `false` to disable |
| `{ enabled?: boolean; margin?: number }` | Object form, allows configuring buffer margin |

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `enabled` | `boolean` | `true` | Whether to enable |
| `margin` | `number` | `120` | Buffer margin outside the visible area (in pixels), the larger the value, the larger the pre-rendering range, and the lower the probability of white screen during scrolling |

## API Methods

| Method | Description |
|--------|-------------|
| `graph.enableVirtualRender()` | Dynamically enable virtual rendering |
| `graph.disableVirtualRender()` | Dynamically disable virtual rendering (revert to full rendering) |

## Interacting with Scroller

Virtual rendering automatically listens to the scroll events of the Scroller plugin and updates the rendering area during scrolling:

```javascript
import { Graph, Scroller } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  virtual: { enabled: true, margin: 150 },
});

// After Scroller is registered, virtual rendering automatically binds to its scroll events
graph.use(new Scroller({ enabled: true }));
```

## Complete Example: Large Data Volume Scenario

```javascript
import { Graph, Scroller, MiniMap } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 1000,
  height: 600,
  virtual: { enabled: true, margin: 200 },
  async: true,
  grid: { visible: true, size: 10 },
});

graph.use(new Scroller({ enabled: true }));
graph.use(new MiniMap({ enabled: true, container: document.getElementById('minimap-container') }));

// Batch add a large number of nodes
const nodes = [];
const edges = [];

for (let i = 0; i < 2000; i++) {
  const row = Math.floor(i / 50);
  const col = i % 50;
  nodes.push({
    id: `node-${i}`,
    shape: 'rect',
    x: col * 160,
    y: row * 100,
    width: 120,
    height: 40,
    label: `Node ${i}`,
    attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 4, ry: 4 } },
  });

  // Add horizontal edges
  if (col > 0) {
    edges.push({
      source: `node-${i - 1}`,
      target: `node-${i}`,
      attrs: { line: { stroke: '#ccc', strokeWidth: 1 } },
    });
  }
}

graph.fromJSON({ nodes, edges });
graph.centerContent();
```

## Dynamic Switching

```javascript
// Disable virtual rendering when the data volume is small (to avoid the overhead of frequent visible area calculations)
if (nodeCount < 200) {
  graph.disableVirtualRender();
} else {
  graph.enableVirtualRender();
}
```

## Notes

1. **Buffer Margin Selection**: A margin that is too small can cause a white screen during fast scrolling (elements not rendered in time); a margin that is too large reduces the optimization effect. A margin of 100~200px is recommended.
2. **Use with async**: Virtual rendering is typically used with `async: true` (default value). Asynchronous rendering further improves initialization performance with large datasets.
3. **Event Listening**: Virtual rendering listens to `translate` (panning), `scale` (zooming), `resize` (container size changes) events, and the Scroller's scroll event to update the rendering area.
4. **No Impact on Data**: Virtual rendering only affects DOM rendering. `graph.toJSON()` still exports all element data.

## Common Errors

### ❌ Large Data Volume Without Virtual Rendering Causes Lag

```javascript
// Problem: Full rendering of 2000 nodes, excessive DOM elements lead to interaction lag
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});
// Add 2000 nodes... Canvas is very laggy

// Solution: Enable virtual rendering
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  virtual: true,  // ✅ Render only the visible area
});
```

### ❌ Enabling Virtual Rendering for Small Datasets Increases Overhead

```javascript
// Not recommended: Virtual rendering is unnecessary for only 20 nodes
const graph = new Graph({
  container: 'container',
  virtual: { enabled: true, margin: 200 }, // Calculating the visible area overhead exceeds the time saved by rendering
});

// Recommended: Do not enable for small datasets
const graph = new Graph({
  container: 'container',
  // virtual defaults to false
});
```