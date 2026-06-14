---
id: "x6-core-anchor"
title: "X6 Anchor"
description: |
  Anchor positioning strategy when an edge connects to a node/edge.
  Includes nodeAnchor (node anchor) and edgeAnchor (edge anchor), controlling the precise position of the connection endpoint on the target element.

library: "x6"
version: "3.x"
category: "core"
subcategory: "anchor"
tags:
  - "anchor"
  - "anchor point"
  - "nodeAnchor"
  - "edgeAnchor"
  - "connection endpoint"
  - "center"
  - "top"
  - "bottom"
  - "left"
  - "right"
  - "midSide"
  - "orth"
  - "ratio"

related:
  - "x6-core-edge"
  - "x6-intermediate-connection-point"
  - "x6-core-ports"

use_cases:
  - "Control where the connection connects to a node"
  - "Set the anchor point when an edge connects to another edge"
  - "Automatically align connection endpoints in orthogonal layouts"
  - "Connect from the center/edge/nearest side of a node"

difficulty: "intermediate"
completeness: "full"
---

## Core Concepts

**Anchor** determines the reference position of the connection endpoint on the target element. In X6, there are two types of anchors:

- **nodeAnchor**: The anchor position when an edge connects to a node.
- **edgeAnchor**: The anchor position when an edge connects to another edge.

Anchors are used in conjunction with **connectionPoint**: the anchor determines the reference point, and the connectionPoint determines the final connection position (usually the intersection of the anchor and the node boundary).

## Node Anchor

(Note: The original content provided only contains a header. Below is the translated header as per the instructions.)

## Node Anchor
### Configuration Method

Set through the `anchor` field in the edge's `source` / `target`:

```javascript
graph.addEdge({
  source: { cell: node1, anchor: 'center' },
  target: { cell: node2, anchor: { name: 'midSide', args: { direction: 'H' } } },
});
```

Global defaults can also be set in the Graph's `connecting`:

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    anchor: 'center', // Global default node anchor
  },
});
```

### Built-in Node Anchors

| Name | Description | Parameters |
|------|-------------|------------|
| `center` | Center of the node's BBox (**default**) | `dx`, `dy`, `rotate` |
| `top` | Top center of the node | `dx`, `dy`, `rotate` |
| `bottom` | Bottom center of the node | `dx`, `dy`, `rotate` |
| `left` | Left center of the node | `dx`, `dy`, `rotate` |
| `right` | Right center of the node | `dx`, `dy`, `rotate` |
| `topLeft` | Top-left corner of the node | `dx`, `dy`, `rotate` |
| `topRight` | Top-right corner of the node | `dx`, `dy`, `rotate` |
| `bottomLeft` | Bottom-left corner of the node | `dx`, `dy`, `rotate` |
| `bottomRight` | Bottom-right corner of the node | `dx`, `dy`, `rotate` |
| `midSide` | Midpoint of the side closest to the opposite end | `direction`, `padding`, `rotate` |
| `orth` | Orthogonal anchor, keeps the connection orthogonal | `padding` |
| `nodeCenter` | Actual center of the node (not the magnet BBox) | `dx`, `dy` |

### BBox Anchor Parameters

`center`、`top`、`bottom`、`left`、`right`、`topLeft`、`topRight`、`bottomLeft`、`bottomRight` shared parameters:

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `dx` | `number \| string` | `0` | Offset in the X direction, supports percentages like `'25%'` |
| `dy` | `number \| string` | `0` | Offset in the Y direction, supports percentages like `'25%'` |
| `rotate` | `boolean` | `false` | Whether to rotate with the node |

### midSide Parameter

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `direction` | `'H' \| 'V'` | None | Restrict direction, `H` selects left/right only, `V` selects top/bottom only |
| `padding` | `number` | None | BBox expansion value |
| `rotate` | `boolean` | `false` | Whether to rotate with the node |

### orth Parameter

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `padding` | `number` | `0` | Inner padding from the BBox boundary |

## Edge Anchor

Used when an edge connects to another edge.

### Built-in Edge Anchor Points

| Name | Description | Parameter |
|------|-------------|------------|
| `ratio` | Positioning on the edge path by ratio (**default**) | `ratio` |
| `length` | Positioning on the edge path by length | `length` |
| `closest` | The point closest to the opposite end on the edge path | None |
| `orth` | Orthogonal anchor point, intersection of the orthogonal line drawn from the opposite end with the edge path | `fallbackAt` |

### ratio Parameter

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `ratio` | `number` | `0.5` | Position ratio, between 0 and 1; automatically divided by 100 when greater than 1 |

### length Parameter

| Parameter | Type | Default Value | Description |
|-----------|------|---------------|-------------|
| `length` | `number` | `20` | Length (in pixels) from the start of the path |

### orth Parameter (Edge Anchor Point)

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `fallbackAt` | `number \| string` | None | Fallback position when there is no orthogonal intersection, specified as a ratio (0~1) or a pixel length string such as `'20'` |

The `orth` edge anchor point draws horizontal and vertical lines from the reference point at the opposite end, selecting the nearest intersection point with the edge path. If no intersection exists, the fallback position specified by `fallbackAt` is used. If `fallbackAt` is also not specified, it defaults to `closest`.

## Complete Example

### Implementing Automatic Side Connection with midSide

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  connecting: {
    anchor: { name: 'midSide', args: { direction: 'H' } },
    connectionPoint: 'boundary',
    router: 'orth',
    connector: 'rounded',
  },
});

const node1 = graph.addNode({
  shape: 'rect',
  x: 100,
  y: 100,
  width: 120,
  height: 60,
  label: 'Start',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
});

const node2 = graph.addNode({
  shape: 'rect',
  x: 400,
  y: 250,
  width: 120,
  height: 60,
  label: 'End',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
});

// midSide automatically selects the closest side to the target
graph.addEdge({
  source: node1,
  target: node2,
  attrs: { line: { stroke: '#8f8f8f', targetMarker: 'classic' } },
});
```

### Specify source/target anchor points separately

```javascript
graph.addEdge({
  source: { cell: node1, anchor: 'right' },
  target: { cell: node2, anchor: { name: 'left', args: { dy: 10 } } },
  attrs: { line: { stroke: '#8f8f8f', targetMarker: 'classic' } },
});
```

### Edge Connecting to Edge

```javascript
const edge1 = graph.addEdge({
  source: node1,
  target: node2,
});

// edge2 connects to the midpoint of edge1
graph.addEdge({
  source: node3,
  target: { cell: edge1, anchor: { name: 'ratio', args: { ratio: 0.5 } } },
  attrs: { line: { stroke: '#f5222d', targetMarker: 'classic' } },
});
```

## Common Errors

### ❌ Confusing anchor with connectionPoint

```javascript
// Incorrect: anchor does not determine the final connection position, it is only a reference point
graph.addEdge({
  source: { cell: node1, anchor: 'boundary' }, // ❌ boundary is a connectionPoint, not an anchor
  target: node2,
});

// Correct: anchor sets the reference position, connectionPoint determines the boundary intersection
graph.addEdge({
  source: { cell: node1, anchor: 'center', connectionPoint: 'boundary' },
  target: node2,
});
```

### ❌ Mixed Usage Error of String Abbreviation and Object Format

```javascript
// Two correct ways of writing
anchor: 'center'                                    // String abbreviation
anchor: { name: 'midSide', args: { direction: 'H' } }  // Object format (with parameters)
```