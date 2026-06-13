---
id: "x6-core-edge-anchor"
title: "X6 Edge Anchor"
description: |
  Edge anchors determine the anchoring position when an edge connects to another edge. When the source or target of an edge is another edge, the edge anchor is used to determine the connection point on the target edge.
library: x6
version: 3.x
category: "core"
tags:
  - edge-anchor
  - anchor
  - edge
  - connection
---

# Edge Anchor (Edge Anchor Point)
## Overview

When an edge's `source` or `target` connects to another edge (rather than a node), an Edge Anchor is required to determine the connection point's position on the target edge's path.

## Built-in Edge Anchor Types

| Type | Description | Parameters |
|------|-------------|------------|
| `ratio` | Position by ratio (default 0.5, i.e., midpoint) | `{ ratio: 0~1 }` |
| `length` | Position by absolute length (pixel distance from the start point) | `{ length: number }` |
| `closest` | The path point closest to the reference point | None |
| `orth` | The intersection point closest to the reference point in the orthogonal direction | `{ fallbackAt?: number \| string }` |

## Usage

Edge anchors are configured via `source.anchor` or `target.anchor`:

```javascript
graph.addEdge({
  source: { cell: edge1.id, anchor: { name: 'ratio', args: { ratio: 0.3 } } },
  target: { cell: edge2.id, anchor: { name: 'closest' } },
});
```

## Detailed Explanation of Each Type

### ratio — Positioning by Ratio

Select a point on the target edge path by ratio, where `ratio` is a decimal between 0 and 1 (default is 0.5, i.e., the midpoint). If `ratio` > 1, it will be automatically divided by 100 and treated as a percentage.

```javascript
graph.addEdge({
  source: { cell: anotherEdge.id, anchor: { name: 'ratio', args: { ratio: 0.25 } } },
  target: targetNode,
});
```

### length — Positioning by Absolute Length

A point located at a specified pixel distance (default 20px) along the path from the start of the target edge.

```javascript
graph.addEdge({
  source: { cell: anotherEdge.id, anchor: { name: 'length', args: { length: 50 } } },
  target: targetNode,
});
```

### closest — Closest Point

Retrieves the point on the target edge path that is closest to the reference point.

```javascript
graph.addEdge({
  source: { cell: anotherEdge.id, anchor: { name: 'closest' } },
  target: targetNode,
});
```

### orth — Orthogonal Anchor

Starting from the reference point, find the intersection along the horizontal or vertical direction with the target edge path. If no orthogonal intersection is found, fall back to the position specified by `fallbackAt` (ratio or length). If `fallbackAt` is not set, fall back to `closest`.

```javascript
graph.addEdge({
  source: { cell: anotherEdge.id, anchor: { name: 'orth', args: { fallbackAt: 0.5 } } },
  target: targetNode,
});
```

## Difference from Node Anchor

| Feature | Node Anchor | Edge Anchor |
|------|-------------|-------------|
| Applicable Scenario | Edge connects to a node | Edge connects to another edge |
| Configuration Location | `source/target.anchor` | Same as left (automatically selected based on target type) |
| Built-in Types | center, top, bottom, left, right, etc. | ratio, length, closest, orth |

## Custom Edge Anchor

Register a custom edge anchor point using `Graph.registerEdgeAnchor`:

```javascript
import { Graph } from '@antv/x6';

Graph.registerEdgeAnchor('myAnchor', (view, magnet, ref, options, type) => {
  // view: EdgeView instance
  // ref: reference point
  // Returns a Point object
  const ratio = options.ratio || 0.5;
  return view.getPointAtRatio(ratio);
});

// Usage
graph.addEdge({
  source: { cell: edge1.id, anchor: { name: 'myAnchor', args: { ratio: 0.7 } } },
  target: targetNode,
});
```

## Common Errors

```javascript
// ❌ Error: Edge anchor only works when connecting edges, use node anchor for node connections
graph.addEdge({
  source: { cell: node.id, anchor: { name: 'ratio' } }, // ratio is an edge anchor, not applicable to nodes
  target: targetNode,
});

// ✅ Correct: Use node anchor for node connections
graph.addEdge({
  source: { cell: node.id, anchor: { name: 'center' } },
  target: targetNode,
});
```