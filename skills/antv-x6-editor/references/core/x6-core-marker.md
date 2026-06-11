---
id: "x6-core-marker"
title: "X6 Arrow Marker"
description: |
  Configuration for arrow markers at the start and end of edges.
  Includes built-in arrow types (classic, block, diamond, circle, cross, ellipse, etc.) and custom arrows.

library: "x6"
version: "3.x"
category: "core"
subcategory: "marker"
tags:
  - "marker"
  - "arrow"
  - "targetMarker"
  - "sourceMarker"
  - "classic"
  - "block"
  - "diamond"
  - "circle"
  - "cross"
  - "ellipse"
  - "custom arrow"
  - "SVG path"
  - "gradient arrow"
  - "defineGradient"
  - "linearGradient"

related:
  - "x6-core-edge"
  - "x6-core-anchor"
  - "x6-intermediate-custom-edge"

use_cases:
  - "Add arrows to edges"
  - "Customize arrow style and size"
  - "Set different arrows for start and end points"
  - "Hollow arrows, diamond arrows, circular arrows"
  - "Custom SVG path arrows"
  - "Gradient-filled arrows"

difficulty: "beginner"
completeness: "full"
---

## Core Concepts

**Marker (Arrow Marker)** is a decorative element at the starting end (sourceMarker) or ending end (targetMarker) of an edge. It is configured through the `attrs.line` property of the edge.

## Configuration Method

```javascript
graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: {
      stroke: '#8f8f8f',
      strokeWidth: 1,
      targetMarker: 'classic',       // Arrow at the end (string shorthand)
      sourceMarker: null,            // No arrow at the start
    },
  },
});
```

## Built-in Arrow Types

| Name | Description | Effect |
|------|-------------|---------|
| `'classic'` | Classic solid arrow (V-shaped, with indentation) | ▶ With indentation |
| `'block'` | Solid triangular arrow (no indentation) | ▶ Full triangle |
| `'diamond'` | Diamond-shaped arrow | ◆ |
| `'circle'` | Circular arrow | ● |
| `'circlePlus'` | Circle with a cross | ⊕ |
| `'ellipse'` | Elliptical arrow | ⬮ |
| `'cross'` | X-shaped cross (hollow) | ✕ |
| `'async'` | Diagonal mark (acute triangle, often used for asynchronous signals) | ◁ Diagonal |

## Parameter Configuration

Parameters can be passed using object format:

```javascript
attrs: {
  line: {
    targetMarker: {
      name: 'classic',
      size: 10,        // Unified size
      width: 12,       // Width (higher priority than size)
      height: 8,       // Height (higher priority than size)
      offset: 0,       // Offset along the path direction
    },
  },
}
```

### classic Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `size` | `number` | `10` | Arrow size (default value for width and height) |
| `width` | `number` | `size` | Arrow width |
| `height` | `number` | `size` | Arrow height |
| `offset` | `number` | `-width/2` | Path direction offset |
| `factor` | `number` | `0.75` | Concavity coefficient, 0~1, larger values result in shallower concavity |

### block parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `size` | `number` | `10` | Arrow size |
| `width` | `number` | `size` | Arrow width |
| `height` | `number` | `size` | Arrow height |
| `offset` | `number` | `-width/2` | Path direction offset |
| `open` | `boolean` | `false` | Whether to be hollow (stroke only) |

### diamond Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `size` | `number` | `10` | Diamond size |
| `width` | `number` | `size` | Diamond width |
| `height` | `number` | `size` | Diamond height |
| `offset` | `number` | `-width/2` | Path direction offset |

### circle Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `r` | `number` | `5` | Circle radius |

### ellipse Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `rx` | `number` | `5` | Radius in the X direction |
| `ry` | `number` | `5` | Radius in the Y direction |

### cross Parameter

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `size` | `number` | `10` | Cross size |
| `width` | `number` | `size` | Width |
| `height` | `number` | `size` | Height |
| `offset` | `number` | `-width/2` | Path direction offset |

### async Parameter

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `width` | `number` | `10` | Width |
| `height` | `number` | `6` | Height |
| `offset` | `number` | `-width/2` | Path direction offset |
| `open` | `boolean` | `false` | Whether to be hollow (stroke only) |
| `flip` | `boolean` | `false` | Whether to flip direction |

## Complete Example

### Common Arrow Combinations

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

const node1 = graph.addNode({
  shape: 'rect', x: 50, y: 50, width: 80, height: 40, label: 'A',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 4, ry: 4 } },
});

const node2 = graph.addNode({
  shape: 'rect', x: 300, y: 50, width: 80, height: 40, label: 'B',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 4, ry: 4 } },
});

// Classic Arrow
graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: { stroke: '#333', strokeWidth: 1, targetMarker: 'classic' },
  },
});
```

### Customizing Arrow Size and Color

```javascript
graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: {
      stroke: '#1890ff',
      strokeWidth: 2,
      targetMarker: {
        name: 'block',
        size: 14,
        open: true,        // Hollow triangle
        stroke: '#1890ff',
        fill: 'none',
      },
    },
  },
});
```

### Bidirectional Arrow

```javascript
graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: {
      stroke: '#333',
      strokeWidth: 1,
      sourceMarker: 'classic',
      targetMarker: 'classic',
    },
  },
});
```

### Diamond and Circular Arrows in ER Diagrams

```javascript
// One-to-many relationship
graph.addEdge({
  source: tableA,
  target: tableB,
  attrs: {
    line: {
      stroke: '#333',
      strokeWidth: 1,
      sourceMarker: { name: 'diamond', size: 12, fill: '#fff', stroke: '#333' },
      targetMarker: { name: 'classic', size: 10 },
    },
  },
});
```

### Remove Default Arrow

```javascript
graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: {
      stroke: '#8f8f8f',
      targetMarker: null,    // No arrow
    },
  },
});
```

## Custom SVG Path Arrow

**When built-in arrows are insufficient**, you can directly pass a `{ tagName, d, ...attrs }` object. X6 will automatically register it in the SVG `<defs>` and generate the corresponding `<marker>` element. **It is neither necessary nor allowed** to manually call `document.createElementNS` or access `graph.svgDoc`, `graph.defs` (these are not public APIs in 3.x).

- `tagName` is typically `'path'`, used with the `d` path
- Coordinate system of the path: The local coordinate system of the marker, with the origin at the endpoint of the edge, and the **X-axis along the direction of the edge**. A common diamond path is: `'M 20 -10 0 0 20 10 Z'`
- SVG attributes such as `fill`, `stroke`, `strokeWidth` can be directly written within the object

```javascript
graph.addEdge({
  source: [100, 140],
  target: [400, 140],
  attrs: {
    line: {
      stroke: '#8f8f8f',
      strokeWidth: 1,
      // Source end: default gray diamond
      sourceMarker: {
        tagName: 'path',
        d: 'M 20 -10 0 0 20 10 Z',
      },
      // Target end: custom diamond with red border and green fill
      targetMarker: {
        tagName: 'path',
        stroke: '#D94111',
        strokeWidth: 2,
        fill: '#90C54C',
        d: 'M 20 -10 0 0 20 10 Z',
      },
    },
  },
});
```

## Gradient-Filled Arrow

If you must set a gradient color for a custom marker, the **only correct** approach is to use the X6 public API `graph.defineGradient(options)` to obtain the `gradientId`, and then set `fill` to `url(#gradientId)`.

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
});

const source = graph.addNode({
  shape: 'rect', x: 80, y: 100, width: 100, height: 40, label: 'Source',
  attrs: { body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 } },
});

const target = graph.addNode({
  shape: 'rect', x: 360, y: 100, width: 100, height: 40, label: 'Target',
  attrs: { body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 } },
});

// 1) Register a linear gradient via the public API and obtain the id
const gradientId = graph.defineGradient({
  type: 'linearGradient',
  stops: [
    { offset: 0, color: '#ff0000' },
    { offset: 1, color: '#00ff00' },
  ],
});

// 2) Reference the gradient in the marker object using url(#id)
graph.addEdge({
  source,
  target,
  attrs: {
    line: {
      stroke: '#8f8f8f',
      strokeWidth: 2,
      sourceMarker: 'classic',
      targetMarker: {
        tagName: 'path',
        d: 'M 0 -10 10 0 0 10 -10 0 Z',
        fill: `url(#${gradientId})`,
        stroke: 'none',
      },
    },
  },
});
```

> ⚠️ The `stops[].offset` in `graph.defineGradient` should be a number between `0` and `1` (not a string like `'0%'`).

## Common Errors

### ❌ Manually Creating SVG `<defs>` / `<linearGradient>`

```javascript
// Error: X6 does not have public properties like graph.svgDoc / graph.defs, and this bypasses X6's defs management
const defs = graph.svgDoc.createElementNS('http://www.w3.org/2000/svg', 'defs');           // ❌
const gradient = graph.svgDoc.createElementNS(                                              // ❌
  'http://www.w3.org/2000/svg',
  'linearGradient',
);
gradient.setAttribute('id', 'gradient');
// ...
graph.svgDoc.appendChild(defs);                                                             // ❌ Runtime error
```

```javascript
// Correct: Use graph.defineGradient to get the id and then use url(#id) in fill
const gradientId = graph.defineGradient({
  type: 'linearGradient',
  stops: [
    { offset: 0, color: '#ff0000' },
    { offset: 1, color: '#00ff00' },
  ],
});
attrs.line.targetMarker = {
  tagName: 'path',
  d: 'M 0 -10 10 0 0 10 -10 0 Z',
  fill: `url(#${gradientId})`,
  stroke: 'none',
};
```

### ❌ Setting the marker in the wrong position

```javascript
// Error: marker is not a top-level property of the edge
graph.addEdge({
  source: node1,
  target: node2,
  targetMarker: 'classic', // ❌ Invalid
});

// Correct: marker is under attrs.line
graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: { targetMarker: 'classic' }, // ✅
  },
});
```

### ❌ Forgot to Set `fill` for Hollow Arrow

```javascript
// Hollow arrow requires `block + open: true`, or manually set `fill: 'none'`
attrs: {
  line: {
    targetMarker: {
      name: 'block',
      open: true,  // ✅ `block` supports `open` parameter
    },
  },
}
```