---
id: "x6-plugin-transform"
title: "X6 Transform Scaling and Rotation Plugin"
description: |
  The Transform plugin provides visual scaling (Resize) and rotation (Rotate) handles for nodes, allowing users to adjust node size and angle by dragging the handles.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "transform"
tags:
  - "Transform"
  - "Scaling"
  - "Rotation"
  - "resize"
  - "rotate"
  - "Drag-to-resize"
  - "Node transformation"

related:
  - "x6-plugins"
  - "x6-core-node"
  - "x6-core-events"

use_cases:
  - "Drag-to-resize nodes"
  - "Rotate node angles"
  - "Restrict node minimum/maximum size"
  - "Maintain node aspect ratio during scaling"
  - "Disable scaling for specific nodes"

difficulty: "beginner"
completeness: "full"
---

## Basic Usage

```javascript
import { Graph, Transform } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Transform({
  resizing: { enabled: true },
  rotating: { enabled: true },
}));
```

## Configuration Options

### resizing Configuration

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `enabled` | boolean \| function | `false` | Whether to enable resizing, can pass a function to filter nodes |
| `minWidth` | number | `0` | Minimum width |
| `maxWidth` | number | `Infinity` | Maximum width |
| `minHeight` | number | `0` | Minimum height |
| `maxHeight` | number | `Infinity` | Maximum height |
| `orthogonalResizing` | boolean | `true` | Whether to enable orthogonal resizing (only horizontal/vertical directions) |
| `restrictedResizing` | boolean \| number | `false` | Restrict resizing range (`true` restricts within the canvas, number represents margin) |
| `preserveAspectRatio` | boolean | `false` | Whether to maintain aspect ratio |
| `allowReverse` | boolean | `true` | Whether to allow control points to reverse when reaching minimum size |
| `autoScrollOnResizing` | boolean | `true` | Whether to automatically scroll the canvas during resizing |

### rotating Configuration

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `enabled` | boolean \| function | `false` | Whether to enable rotation, can pass a function to filter nodes |
| `rotateGrid` | number | `15` | Rotation angle step (interval of angles snapped to each time) |

## Programmatic API

```javascript
// Create a transform widget for the specified node
graph.createTransformWidget(node);

// Clear all transform widgets
graph.clearTransformWidgets();
```

## Event Listening

```javascript
// Resize start
graph.on('node:resize', ({ node, e }) => {
  console.log('Resize started:', node.id);
});

// Resizing
graph.on('node:resizing', ({ node, e }) => {
  console.log('Resizing:', node.getSize());
});

// Resize end
graph.on('node:resized', ({ node, e }) => {
  console.log('Resize completed:', node.getSize());
});

// Rotate start
graph.on('node:rotate', ({ node, e }) => {
  console.log('Rotation started:', node.id);
});

// Rotating
graph.on('node:rotating', ({ node, e }) => {
  console.log('Rotating:', node.getAngle());
});

// Rotate end
graph.on('node:rotated', ({ node, e }) => {
  console.log('Rotation completed:', node.getAngle());
});
```

## Complete Example: Size Constraints + Aspect Ratio Preservation

```javascript
import { Graph, Transform } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  grid: { visible: true },
});

graph.use(new Transform({
  resizing: {
    enabled: true,
    minWidth: 40,
    minHeight: 40,
    maxWidth: 400,
    maxHeight: 400,
    preserveAspectRatio: true,  // Preserve aspect ratio
  },
  rotating: {
    enabled: true,
    rotateGrid: 15,  // Snap every 15°
  },
}));

graph.addNode({
  x: 200,
  y: 200,
  width: 120,
  height: 80,
  label: 'Resize & Rotate me',
  attrs: { body: { fill: '#EFF4FF', stroke: '#5F95FF' } },
});
```

## Filter by Node

`enabled` can accept a function to determine whether scaling/rotation is allowed based on the node:

```javascript
graph.use(new Transform({
  resizing: {
    enabled(node) {
      // Only nodes with shape 'rect' can be scaled
      return node.shape === 'rect';
    },
  },
  rotating: {
    enabled(node) {
      // Control rotatability through node data
      return node.getData()?.rotatable !== false;
    },
  },
}));
```

## Common Errors

### ❌ Configuring resizing/rotating in the constructor

```javascript
// Error: Not supported in 3.x
const graph = new Graph({
  container: 'container',
  resizing: { enabled: true },   // ❌
  rotating: { enabled: true },   // ❌
});
```

```javascript
// Correct
import { Graph, Transform } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Transform({
  resizing: { enabled: true },
  rotating: { enabled: true },
}));  // ✅
```

### ❌ Confusing Transform with CSS transform

```javascript
// Incorrect: Do not use CSS transform to rotate X6 nodes
node.attr('body/transform', 'rotate(45deg)');  // ❌ Ineffective and may break layout
```

```javascript
// Correct: Use node API to set the angle
node.rotate(45);  // ✅ Rotate through the X6 model layer
```