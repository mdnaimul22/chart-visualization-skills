---
id: "x6-core-connector-advanced"
title: "X6 Advanced Connector"
description: |
  In addition to the commonly used normal, rounded, and smooth connectors, X6 also provides loop (self-loop connector) and jumpover (jump wire connector).
  These are suitable for scenarios such as self-loop edge drawing and cross-line jump wire display.

library: "x6"
version: "3.x"
category: "core"
subcategory: "edge"
tags:
  - "connector"
  - "连接器"
  - "loop"
  - "jumpover"
  - "跳线"
  - "自环"
  - "交叉"

related:
  - "x6-core-edge"
  - "x6-core-router-advanced"

use_cases:
  - "Curved drawing of self-loop edges"
  - "Jump wire display for crossing connections"
  - "Avoiding visual overlap of connections"
  - "State machine self-loop"

difficulty: "intermediate"
completeness: "full"
---
## Full List of Connectors

| Connector | Description | Typical Use Cases |
|-----------|-------------|------------|
| `normal` | Default, straight line connecting route points | Simple connections |
| `rounded` | Rounded corners with folds | Flowcharts |
| `smooth` | Bezier curve | Smooth connections |
| `jumpover` | Jump line, producing arc jumps at intersections | Complex wiring diagrams |
| `loop` | Self-loop curve | Self-loop edges |

---

## Loop Connector

A connector specifically designed for self-loop edges, using quadratic Bézier curves (Q command) to draw arcs, and works in conjunction with the `loop` router.

### Configuration Options

| Property | Type | Default Value | Description |
|----------|------|---------------|-------------|
| `split` | `boolean \| number` | - | Whether to split the curve |

### Example

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({ container: 'container' });

const node = graph.addNode({
  shape: 'rect',
  x: 150,
  y: 100,
  width: 100,
  height: 50,
  label: 'State A',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
});

// Self-loop edge: Must use both loop router and loop connector
graph.addEdge({
  source: node,
  target: node,
  router: {
    name: 'loop',
    args: { width: 60, height: 100, angle: 'auto' },
  },
  connector: { name: 'loop' },
  label: 'Retry',
  attrs: {
    line: { stroke: '#f5222d', strokeWidth: 2, targetMarker: 'classic' },
  },
});
```

### Key Notes

- **Must be used in conjunction with the `loop` router**, which provides intermediate control points for the connector to draw curves accordingly
- The generated path is composed of two Q (quadratic Bézier curves) segments

---

## Jumpover Connector

When multiple edges intersect, draw a jumper arc at the intersection to avoid visual confusion.

### Configuration Options

| Property | Type | Default Value | Description |
|------|------|--------|------|
| `size` | `number` | `5` | Size (radius) of the jumper arc |
| `type` | `'arc' \| 'gap' \| 'cubic'` | `'arc'` | Jumper style type |
| `radius` | `number` | `0` | Radius of the rounded corners of the polyline |
| `ignoreConnectors` | `string[]` | `['smooth']` | Ignore intersections with which connector types |

### Jump Line Type Description

- **`arc`**：Semi-circular arc jump (default), most commonly used
- **`gap`**：Disconnected gap
- **`cubic`**：Cubic curve jump, smoother

### Example

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  connecting: {
    connector: {
      name: 'jumpover',
      args: {
        size: 8,
        type: 'arc',
      },
    },
  },
});

// Create multiple intersecting edges
const node1 = graph.addNode({
  shape: 'rect', x: 50, y: 50, width: 80, height: 40, label: 'A',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 4, ry: 4 } },
});
const node2 = graph.addNode({
  shape: 'rect', x: 300, y: 50, width: 80, height: 40, label: 'B',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 4, ry: 4 } },
});
const node3 = graph.addNode({
  shape: 'rect', x: 50, y: 200, width: 80, height: 40, label: 'C',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 4, ry: 4 } },
});
const node4 = graph.addNode({
  shape: 'rect', x: 300, y: 200, width: 80, height: 40, label: 'D',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 4, ry: 4 } },
});

// Two intersecting edges
graph.addEdge({
  source: node1,
  target: node4,
  connector: { name: 'jumpover', args: { size: 8, type: 'arc' } },
  attrs: { line: { stroke: '#5b8ff9', strokeWidth: 2 } },
});

graph.addEdge({
  source: node2,
  target: node3,
  connector: { name: 'jumpover', args: { size: 8, type: 'arc' } },
  attrs: { line: { stroke: '#52c41a', strokeWidth: 2 } },
});
```

### Single Edge Setting jumpover

```javascript
// Set on a single edge
graph.addEdge({
  source: node1,
  target: node2,
  connector: {
    name: 'jumpover',
    args: {
      size: 6,
      type: 'cubic',
      radius: 4,
    },
  },
  attrs: { line: { stroke: '#333', strokeWidth: 2 } },
});
```

### Global Default Settings jumpover

```javascript
// Global configuration during Graph initialization
const graph = new Graph({
  container: 'container',
  connecting: {
    connector: {
      name: 'jumpover',
      args: { size: 5, type: 'arc' },
    },
  },
});
```

---

## Connector Abbreviation and Object Notation

```javascript
// Abbreviation (no parameters)
graph.addEdge({ source, target, connector: 'rounded' });

// Object notation (with parameters)
graph.addEdge({
  source,
  target,
  connector: {
    name: 'rounded',
    args: { radius: 10 },
  },
});
```

---

## Common Errors and Fixes

### Error 1: Self-loop Edge Uses Only `loop` Connector Without `loop` Router

```javascript
// ❌ Incorrect: Missing `loop` router, connector lacks proper control points
graph.addEdge({
  source: node,
  target: node,
  connector: { name: 'loop' },
});

// ✅ Correct: Router and connector used together
graph.addEdge({
  source: node,
  target: node,
  router: { name: 'loop', args: { width: 50, height: 80 } },
  connector: { name: 'loop' },
});
```

### Error 2: jumpover Not Taking Effect

```javascript
// ❌ Incorrect: Only one edge is set with jumpover, while the other uses smooth (default is ignored)
// jumpover by default ignores intersections with smooth connectors

// ✅ Correct: Ensure all edges that need to jump over use jumpover or non-ignored connectors
// or modify the ignoreConnectors parameter
connector: {
  name: 'jumpover',
  args: { ignoreConnectors: [] },  // Do not ignore any connectors
}
```

### Error 3: Spelling Error in `jumpover`'s `type`

```javascript
// ❌ Incorrect
connector: { name: 'jumpover', args: { type: 'curve' } }

// ✅ Correct: `type` value should be 'arc' | 'gap' | 'cubic'
connector: { name: 'jumpover', args: { type: 'cubic' } }
```