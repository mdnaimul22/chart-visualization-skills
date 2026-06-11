---
id: "x6-core-grid"
title: "X6 Grid Configuration"
description: |
  X6 canvas grid configuration: dot grid, fixedDot fixed grid, mesh grid lines, doubleMesh double-layer grid, and grid color, size, visibility control.

library: "x6"
version: "3.x"
category: "core"
subcategory: "grid"
tags:
  - "grid"
  - "网格"
  - "dot"
  - "mesh"
  - "doubleMesh"
  - "alignment"
  - "background grid"

related:
  - "x6-core-graph-init"
  - "x6-core-background"

use_cases:
  - "Display dot grid"
  - "Display grid lines"
  - "Customize grid color and size"
  - "Dynamically show/hide grid"
  - "Double-layer grid (primary and secondary grid lines)"

difficulty: "beginner"
completeness: "full"
---

## Basic Usage

The grid is configured in the Graph constructor via the `grid` field:

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  grid: {
    visible: true,
    size: 10,  // Grid step size (pixels)
  },
});
```

## Configuration Options

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `visible` | boolean | `false` | Whether to display the grid |
| `size` | number | `10` | Grid step size (minimum interval nodes snap to when moving) |
| `type` | string | `'dot'` | Grid type: `'dot'`, `'fixedDot'`, `'mesh'`, `'doubleMesh'` |
| `args` | object | - | Parameters corresponding to the grid type |

**Note**: Even if `visible: false`, `size` still takes effect—nodes will snap to grid points with `size` as the step size during dragging.

## Grid Type

### dot (Dot Matrix, Default)

Displayed as evenly distributed dots, the size of which changes with zoom:

```javascript
const graph = new Graph({
  container: 'container',
  grid: {
    visible: true,
    size: 10,
    type: 'dot',
    args: {
      color: '#aaaaaa',   // Dot color
      thickness: 1,        // Dot size
    },
  },
});
```

### fixedDot (Fixed Dot Grid)

Similar to `dot`, but the size of the dots remains unchanged when the zoom ratio ≤ 1 (they won't become too small to see clearly):

```javascript
const graph = new Graph({
  container: 'container',
  grid: {
    visible: true,
    size: 10,
    type: 'fixedDot',
    args: {
      color: '#aaaaaa',
      thickness: 2,
    },
  },
});
```

### mesh (Grid Lines)

Displayed as intersecting grid lines:

```javascript
const graph = new Graph({
  container: 'container',
  grid: {
    visible: true,
    size: 10,
    type: 'mesh',
    args: {
      color: 'rgba(224, 224, 224, 1)',  // Line color
      thickness: 1,                      // Line thickness
    },
  },
});
```

### doubleMesh (Double Mesh)

Displays two layers of grid lines—primary grid and secondary grid, with the secondary grid spacing amplified by a `factor` multiplier:

```javascript
const graph = new Graph({
  container: 'container',
  grid: {
    visible: true,
    size: 10,
    type: 'doubleMesh',
    args: [
      // First layer: Fine grid
      {
        color: 'rgba(224, 224, 224, 1)',
        thickness: 1,
      },
      // Second layer: Coarse grid (spacing = size * factor)
      {
        color: 'rgba(224, 224, 224, 0.2)',
        thickness: 3,
        factor: 4,  // Spacing is 4 times the base size
      },
    ],
  },
});
```

## Programmatic API

```javascript
// Get grid step size
graph.getGridSize();  // number

// Set grid step size
graph.setGridSize(20);

// Show grid
graph.showGrid();

// Hide grid
graph.hideGrid();

// Redraw grid (switch type)
graph.drawGrid({
  type: 'mesh',
  args: { color: '#ddd', thickness: 1 },
});
```

## Complete Example

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  grid: {
    visible: true,
    size: 20,
    type: 'doubleMesh',
    args: [
      { color: '#eee', thickness: 1 },
      { color: '#ddd', thickness: 1, factor: 4 },
    ],
  },
});

// Nodes will automatically snap to grid points with a step of 20px
graph.addNode({
  x: 100,  // Actual position will snap to multiples of size
  y: 100,
  width: 80,
  height: 40,
  label: 'Snaps to grid',
});
```

## Common Errors

### ❌ Confusing size with visible

```javascript
// Incorrect understanding: Assuming visible: false means no grid effect
const graph = new Graph({
  container: 'container',
  grid: { visible: false, size: 20 },
});
// In reality, nodes will still snap to a 20px grid during dragging!
```

### ❌ doubleMesh's args should be an array instead of an object

```javascript
// Error: doubleMesh's args must be an array
grid: {
  type: 'doubleMesh',
  args: { color: '#eee', thickness: 1 },  // ❌ Should be an array
}

// Correct
grid: {
  type: 'doubleMesh',
  args: [
    { color: '#eee', thickness: 1 },
    { color: '#ddd', thickness: 1, factor: 4 },
  ],  // ✅
}
```