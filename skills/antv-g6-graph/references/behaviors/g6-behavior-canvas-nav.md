---
id: "g6-behavior-canvas-nav"
title: "G6 Canvas Navigation Interaction (Drag/Zoom/Scroll)"
description: |
  Use drag-canvas, zoom-canvas, and scroll-canvas to implement canvas dragging, zooming, and scrolling navigation.
  It is the foundational interaction configuration for almost all graph visualizations.

library: "g6"
version: "5.x"
category: "behaviors"
subcategory: "navigation"
tags:
  - "interaction"
  - "canvas"
  - "drag"
  - "zoom"
  - "drag-canvas"
  - "zoom-canvas"
  - "scroll-canvas"
  - "behavior"

related:
  - "g6-behavior-click-select"
  - "g6-behavior-drag-element"
  - "g6-plugin-minimap"

use_cases:
  - "Large graph navigation"
  - "Basic graph interaction"
  - "All graph visualization scenarios"

anti_patterns:
  - "Mobile scenarios require special handling of touch events"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/behavior/drag-canvas"
---

## Core Concepts

Three canvas navigation behaviors:
- `drag-canvas`: Mouse drag to move the canvas
- `zoom-canvas`: Mouse wheel to zoom the canvas
- `scroll-canvas`: Mouse wheel to scroll the canvas (alternative to zoom, suitable for pages with scrollbars)

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
      { id: 'node1' },
      { id: 'node2' },
      { id: 'node3' },
      { id: 'node4' },
      { id: 'node5' },
    ],
    edges: [
      { id: 'edge1', source: 'node1', target: 'node2' },
      { id: 'edge2', source: 'node1', target: 'node3' },
      { id: 'edge3', source: 'node2', target: 'node4' },
      { id: 'edge4', source: 'node3', target: 'node5' },
    ],
  },
  layout: { type: 'grid' },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

## Common Configurations

### Complete Parameter Configuration

```javascript
behaviors: [
  {
    type: 'drag-canvas',
    // Allowed drag direction
    direction: 'both',          // 'both' | 'x' | 'y'
    // Drag boundary limit
    range: Infinity,            // Distance limit beyond the boundary
    // Key trigger
    trigger: {
      up: ['ArrowUp'],
      down: ['ArrowDown'],
      left: ['ArrowLeft'],
      right: ['ArrowRight'],
    },
  },
  {
    type: 'zoom-canvas',
    // Zoom range
    range: [0.1, 10],           // [Minimum zoom, Maximum zoom]
    // Animation
    animation: { duration: 200 },
  },
],
```

### Preventing Accidental Node Interaction During Canvas Dragging

```javascript
behaviors: [
  {
    type: 'drag-canvas',
    // Only drag on the canvas background (to avoid conflicts with node dragging)
    enable: (event) => event.targetType === 'canvas',
  },
  'drag-element',
],
```

### Keyboard Arrow Keys to Move Canvas

```javascript
behaviors: [
  {
    type: 'drag-canvas',
    trigger: {
      up: ['ArrowUp'],
      down: ['ArrowDown'],
      left: ['ArrowLeft'],
      right: ['ArrowRight'],
    },
  },
  'zoom-canvas',
],
```

### Adapt to Scenarios with Page Scrollbars

```javascript
// When the page has a scrollbar, the mouse wheel scrolls the page by default instead of zooming the chart
// Use scroll-canvas instead of zoom-canvas
behaviors: [
  'drag-canvas',
  'scroll-canvas',    // Scroll the canvas with the mouse wheel (up, down, left, right)
  // Zoom when holding Ctrl
  {
    type: 'zoom-canvas',
    key: 'ctrl',      // Zoom only when holding Ctrl + scrolling
  },
  'drag-element',
],
```

## Program Control Viewport

```javascript
// Zoom to a specified ratio
graph.zoomTo(1.5);
graph.zoomTo(1.5, true);   // With animation

// Restore default zoom
graph.zoomTo(1);

// Pan the canvas
graph.translateBy(100, 50);    // Relative movement
graph.translateTo([400, 300]); // Move to absolute position

// Auto-fit view
graph.fitView();               // Zoom to make the entire graph visible
graph.fitCenter();             // Center without zooming

// Focus on a specific node
graph.focusElement('node1');
```

## Common Errors and Fixes

### Error 1: Missing Unique IDs in Edge Data Causes Duplicate Edge Conflicts

**Error Description**: `Edge already exists: 12-20`

**Root Cause Analysis**: In G6 5.x, if edge data does not explicitly specify an `id`, the system automatically uses `${source}-${target}` as the edge ID. When edges are generated using random numbers, duplicate edges with the same source-target combination may occur, leading to ID conflicts and errors.

```javascript
// ❌ Incorrect Example: Randomly generated edges may produce duplicate source-target combinations
const edges = [];
for (let i = 0; i < 34; i++) {
  const target = Math.floor(Math.random() * 34);
  if (target !== i) {
    edges.push({ source: `${i}`, target: `${target}` });
    // If the same source-target is added twice, the ID "i-target" is duplicated, causing an error
  }
}
```

**Solution 1**: Explicitly assign a unique `id` to each edge

```javascript
// ✅ Correct Example: Assign a unique id to each edge
const edges = [];
let edgeIndex = 0;
for (let i = 0; i < 34; i++) {
  const target = Math.floor(Math.random() * 34);
  if (target !== i) {
    edges.push({
      id: `edge-${edgeIndex++}`,  // Explicitly assign a unique id
      source: `${i}`,
      target: `${target}`,
    });
  }
}
```

**Solution 2**: Deduplicate edges during generation to avoid duplicate source-target combinations

```javascript
// ✅ Correct Example: Use a Set to deduplicate edges
const edgeSet = new Set();
const edges = [];
for (let i = 0; i < 34; i++) {
  const target = Math.floor(Math.random() * 34);
  const key = `${i}-${target}`;
  if (target !== i && !edgeSet.has(key)) {
    edgeSet.add(key);
    edges.push({ source: `${i}`, target: `${target}` });
  }
}
```

**Solution 3 (Recommended)**: Use explicit static data instead of relying on random generation

```javascript
// ✅ Recommended: Use deterministic data to avoid randomness
const data = {
  nodes: Array.from({ length: 34 }, (_, i) => ({ id: `${i}` })),
  edges: [
    { source: '0', target: '1' },
    { source: '0', target: '2' },
    { source: '1', target: '3' },
    // ... Explicitly specified edge list with no duplicates
  ],
};
```

### Error 2: Syntax Error in Minimal Example Code

**Error Description**: Missing or incomplete `data` field in the code results in blank rendering.

**Cause**: The `data` field is mandatory in the `Graph` constructor and must include `nodes` and `edges` arrays.

```javascript
// ❌ Incorrect Example: Missing data field
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  { nodes: [...], edges: [...] },  // Syntax error, missing data: key
  behaviors: ['drag-canvas'],
});

// ✅ Correct Example
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [{ id: 'node1' }, { id: 'node2' }],
    edges: [{ source: 'node1', target: 'node2' }],
  },
  behaviors: ['drag-canvas'],
});
```

### Error 3: treeToGraphData is not defined

**Error Description**: `treeToGraphData is not defined`

**Cause**: `treeToGraphData` is a utility function provided by G6, used to convert tree-structured data into graph data. It needs to be explicitly imported from `@antv/g6` and cannot be used directly.

```javascript
// ❌ Incorrect Example: Using without importing
const data = treeToGraphData(treeData);

// ✅ Correct Example: Import before use
import { Graph, treeToGraphData } from '@antv/g6';

const data = treeToGraphData(treeData);
const graph = new Graph({
  container: 'container',
  data,
  behaviors: ['drag-canvas', 'zoom-canvas'],
});
graph.render();
```

### Error 4: Canvas Rendering Blank

**Common Causes and Fixes**:

1. **Container Size is 0**: Ensure the container DOM element has explicit width and height, or specify `width` and `height` in the Graph configuration.
2. **Data is Empty**: Ensure the `data.nodes` array is not empty.
3. **render() Not Called**: Explicitly call `graph.render()` to trigger rendering.
4. **autoFit Configuration**: Use `autoFit: 'view'` to automatically fit the view, preventing the graph from being invisible due to exceeding the canvas boundaries.

```javascript
// ✅ Complete Runnable Example
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  autoFit: 'view',
  data: {
    nodes: [{ id: 'node1' }, { id: 'node2' }, { id: 'node3' }],
    edges: [
      { source: 'node1', target: 'node2' },
      { source: 'node2', target: 'node3' },
    ],
  },
  layout: { type: 'circular' },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```