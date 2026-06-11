---
id: "x6-core-connection-point"
title: "X6 Connection Point"
description: |
  Actual intersection calculation strategy between edge and node boundary.
  connectionPoint determines the final landing position of the connection endpoint on the node boundary, used in conjunction with anchor.

library: "x6"
version: "3.x"
category: "core"
subcategory: "connection-point"
tags:
  - "connectionPoint"
  - "connection point"
  - "boundary"
  - "bbox"
  - "rect"
  - "anchor"
  - "connection intersection"

related:
  - "x6-core-anchor"
  - "x6-core-edge"
  - "x6-core-ports"

use_cases:
  - "Control the intersection between connection and node shape boundary"
  - "Make connections precisely connect to node contours"
  - "Handle connection intersections for rotated nodes"
  - "Set connection endpoint offsets"

difficulty: "intermediate"
completeness: "full"
---

## Core Concepts

**ConnectionPoint** is the actual intersection point of the edge path with the node boundary. Its relationship with the anchor is as follows:

1. **Anchor** → Determines the reference point (e.g., node center)
2. **ConnectionPoint** → Draws a ray from the opposite end to the anchor and calculates the intersection point with the node boundary

```
Opposite End ─────────────── connectionPoint (Boundary Intersection) ─── anchor (Reference Point, Inside Node)
                           ↑
                      This is the final connection endpoint
```

## Configuration Methods

### Global Configuration

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    connectionPoint: 'boundary',  // Global default
  },
});
```

### Single-sided Configuration

```javascript
graph.addEdge({
  source: { cell: node1, connectionPoint: 'boundary' },
  target: { cell: node2, connectionPoint: { name: 'boundary', args: { sticky: true } } },
});
```

## Built-in Connector Types

| Name | Description | Applicable Scenarios |
|------|-------------|----------|
| `'boundary'` | Intersection with the actual shape boundary of the node (**default**) | Circular, elliptical, polygonal, and other irregular shapes |
| `'bbox'` | Intersection with the unrotated BBox of the node | Simple rectangular nodes |
| `'rect'` | Intersection with the rotated BBox of the node | Rotated rectangular nodes |
| `'anchor'` | Directly uses the anchor position (does not calculate boundary intersection) | When the connection line needs to pass through the interior of the node |

## Parameter Details

### boundary Parameter

The most commonly used connection point strategy, calculating the precise intersection point between the ray and the node's SVG shape.

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `offset` | `number \| { x, y }` | `0` | Offset distance along the connection line |
| `stroked` | `boolean` | `false` | Whether to include strokeWidth in calculations |
| `selector` | `string \| string[]` | None | Specifies the child element selector used for intersection calculations |
| `insideout` | `boolean` | `true` | Whether to still calculate the intersection point when the reference point is inside the shape |
| `extrapolate` | `boolean` | `false` | Extends the ray to ensure intersection with the shape |
| `sticky` | `boolean` | `false` | Whether to return the nearest point (instead of anchor) when no intersection is found |
| `precision` | `number` | `2` | Intersection precision for Path elements |

### bbox Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `offset` | `number \| { x, y }` | `0` | Offset distance |
| `stroked` | `boolean` | `false` | Whether to include strokeWidth in the calculation |

### rect Parameters

Same as bbox, but takes into account the node rotation angle.

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `offset` | `number \| { x, y }` | `0` | Offset distance |
| `stroked` | `boolean` | `false` | Whether to include strokeWidth in the calculation |

### anchor Parameter

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `offset` | `number \| { x, y }` | `0` | Offset distance |
| `align` | `'top' \| 'right' \| 'bottom' \| 'left'` | None | Alignment direction |
| `alignOffset` | `number` | `0` | Alignment offset |

## Complete Example

### boundary: Precise Shape Intersection

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  connecting: {
    anchor: 'center',
    connectionPoint: 'boundary',
    router: 'orth',
    connector: 'rounded',
  },
});

// Circular Node - boundary precisely calculates the arc intersection
const circleNode = graph.addNode({
  shape: 'circle',
  x: 100,
  y: 100,
  width: 80,
  height: 80,
  label: 'Start',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f' } },
});

const rectNode = graph.addNode({
  shape: 'rect',
  x: 350,
  y: 100,
  width: 120,
  height: 60,
  label: 'Process',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
});

graph.addEdge({
  source: circleNode,
  target: rectNode,
  attrs: { line: { stroke: '#8f8f8f', targetMarker: 'classic' } },
});
```

### Sticky Mode: Ensure There is Always a Connection Point

```javascript
graph.addEdge({
  source: {
    cell: node1,
    connectionPoint: {
      name: 'boundary',
      args: { sticky: true },  // Returns the nearest point when there is no intersection
    },
  },
  target: node2,
});
```

### Anchor Type: Edge Penetrating Node

```javascript
// The edge directly connects to the anchor position, without stopping at the boundary
graph.addEdge({
  source: {
    cell: node1,
    anchor: 'center',
    connectionPoint: 'anchor',  // Edge reaches the center of the node
  },
  target: node2,
});
```

### Connection Point with Offset

```javascript
graph.addEdge({
  source: {
    cell: node1,
    connectionPoint: {
      name: 'boundary',
      args: { offset: 10 },  // Connection point offset 10px from the boundary
    },
  },
  target: node2,
});
```

## The Coordination Between connectionPoint and anchor

```
Scenario: node1 → node2

1. Determine the anchor position of node2 (e.g., center = node center)
2. Draw a ray from node1 pointing to the anchor of node2
3. Calculate the intersection point of the ray with the boundary of node2 using connectionPoint
4. This intersection point is the actual end position of the connection line
```

| Combination | Effect |
|------|------|
| `anchor: 'center'` + `connectionPoint: 'boundary'` | Connection line reaches the boundary of the node shape (most commonly used) |
| `anchor: 'center'` + `connectionPoint: 'anchor'` | Connection line penetrates the node to reach the center |
| `anchor: 'left'` + `connectionPoint: 'boundary'` | Calculate the boundary intersection point from the left direction |
| `anchor: 'midSide'` + `connectionPoint: 'boundary'` | Automatically select the nearest boundary intersection point |

## Common Errors

### ❌ Confusing `connectionPoint` with `anchor`

```javascript
// Incorrect: Using `anchor` to connect to the node boundary
graph.addEdge({
  source: { cell: node1, anchor: 'boundary' }, // ❌ 'boundary' is not an anchor type
  target: node2,
});

// Correct: `boundary` is a `connectionPoint` type
graph.addEdge({
  source: { cell: node1, connectionPoint: 'boundary' },
  target: node2,
});
```

### ❌ Circular Nodes Using bbox Result in Imprecise Intersection Points

```javascript
// Not Recommended: bbox for circular nodes calculates rectangular boundary intersection points
connectionPoint: 'bbox'  // Circular nodes will have gaps

// Recommended: Use boundary to precisely calculate arc intersection points
connectionPoint: 'boundary'
```