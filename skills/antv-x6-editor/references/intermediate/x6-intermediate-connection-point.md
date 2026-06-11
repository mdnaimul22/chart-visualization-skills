---
id: "x6-intermediate-connection-point"
title: "X6 Connection Points and Anchors"
description: |
  Comprehensive guide to X6 Anchors and Connection Points.
  Includes built-in anchor types, connection point calculation methods, global and per-side configurations, and custom anchors and connection points.

library: "x6"
version: "3.x"
category: "intermediate"
subcategory: "connection-point"
tags:
  - "connectionPoint"
  - "anchor"
  - "nodeAnchor"
  - "sourceAnchor"
  - "targetAnchor"
  - "boundary"
  - "bbox"
  - "rect"
  - "center"
  - "top"
  - "bottom"
  - "left"
  - "right"
  - "midSide"
  - "orth"

related:
  - "x6-core-edge"
  - "x6-core-ports"
  - "x6-core-graph-init"

use_cases:
  - "Control the precise connection position between edges and nodes"
  - "Achieve evenly spaced connections when multiple edges connect to the same node"
  - "Set specific connection directions (top, bottom, left, right) for edges connecting to nodes"
  - "Customize connection point calculation methods"

anti_patterns:
  - "Do not confuse anchor and connectionPoint concepts"
  - "Do not confuse port and anchor——port is a connection stub, anchor is an anchor position"
---

# X6 Connection Points and Anchors

## Core Concepts

- **Anchor**: The reference point position of an edge on a node (e.g., center, top, left, etc.)
- **ConnectionPoint**: The actual start/end point of an edge calculated based on the anchor and reference line

By default:
- The anchor is `center` (node center)
- The connection point is `boundary` (intersection of the reference line with the node border)

## Usage

### Method 1: Global Configuration (Graph.connecting)

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  connecting: {
    // Global anchor configuration
    sourceAnchor: 'right',
    targetAnchor: 'left',
    // Global connection point configuration
    connectionPoint: 'anchor',
  },
});
```

### Method Two: Unilateral Configuration (Higher Priority)

```javascript
graph.addEdge({
  source: {
    cell: 'node1',
    anchor: {
      name: 'right',
      args: { dy: -10 },
    },
    connectionPoint: 'anchor',
  },
  target: {
    cell: 'node2',
    anchor: {
      name: 'left',
      args: { dy: -10 },
    },
    connectionPoint: 'anchor',
  },
});
```

## Built-in Anchor Types

| Anchor | Position | Description |
|------|------|------|
| `center` | Node Center | Default Value |
| `top` | Top Center | |
| `bottom` | Bottom Center | |
| `left` | Left Center | |
| `right` | Right Center | |
| `topLeft` | Top Left Corner | |
| `topRight` | Top Right Corner | |
| `bottomLeft` | Bottom Left Corner | |
| `bottomRight` | Bottom Right Corner | |
| `midSide` | Nearest Side Center | Automatically selects the side closest to the reference line |
| `orth` | Orthogonal Intersection | Ensures vertical/horizontal connection |
| `nodeCenter` | Node Center | Always the geometric center of the node |

### Anchor Parameters

All anchors support the following parameters:

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `dx` | number \| string | 0 | X-axis offset (supports percentage) |
| `dy` | number \| string | 0 | Y-axis offset (supports percentage) |
| `rotate` | boolean | false | Whether to rotate with the node |

### midSide Additional Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `padding` | number | 0 | Offset |
| `direction` | `'H'` \| `'V'` | - | Restriction direction (H=connect only left and right, V=connect only up and down) |

## Built-in Connector Types

| Connector | Description |
|--------|------|
| `boundary` | Default. Intersection of the reference line with the node border |
| `bbox` | Intersection of the reference line with the bounding box |
| `rect` | Intersection of the reference line with the rotated rectangle |
| `anchor` | Directly use the anchor point as the connector (no intersection calculation) |

### boundary Parameter

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `offset` | number \| Point | 0 | Offset |
| `stroked` | boolean | true | Whether to consider border width |
| `sticky` | boolean | false | Use the nearest point when there is no intersection |
| `selector` | string | - | Specify the child element used for calculation |

## Common Configuration Combinations

### DAG Left-Right Connection

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    sourceAnchor: 'right',
    targetAnchor: 'left',
    connectionPoint: 'anchor',
    router: 'orth',
    connector: 'rounded',
  },
});
```

### Multiple Edges Dispersedly Connected (midSide)

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    anchor: 'midSide',
    connectionPoint: 'boundary',
  },
});
```

### Orthogonal Connection (orth anchor)

Ensures edges connect from the orthogonal direction of the node (closest side up, down, left, or right):

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    anchor: 'orth',
    connectionPoint: 'anchor',
    router: 'orth',
    connector: 'rounded',
  },
});
```

### Anchors with Offset

```javascript
graph.addEdge({
  source: {
    cell: 'node1',
    anchor: { name: 'right', args: { dy: -15 } },  // Offset upwards on the right side
    connectionPoint: 'anchor',
  },
  target: {
    cell: 'node2',
    anchor: { name: 'left', args: { dy: -15 } },   // Offset upwards on the left side
    connectionPoint: 'anchor',
  },
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
});

graph.addEdge({
  source: {
    cell: 'node1',
    anchor: { name: 'right', args: { dy: 15 } },   // Offset downwards on the right side
    connectionPoint: 'anchor',
  },
  target: {
    cell: 'node2',
    anchor: { name: 'left', args: { dy: 15 } },    // Offset downwards on the left side
    connectionPoint: 'anchor',
  },
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
});
```

## Custom Connection Point

```javascript
Graph.registerConnectionPoint(
  'custom-cp',
  (line, view, magnet, args) => {
    // line: reference line
    // view: node view
    // magnet: connected SVG element
    // returns Point { x, y }
    const { offset = 0 } = args;
    const bbox = view.getBBox();
    return { x: bbox.x + bbox.width + offset, y: bbox.y + bbox.height / 2 };
  },
  true,
);

// Usage
new Graph({
  connecting: {
    connectionPoint: { name: 'custom-cp', args: { offset: 5 } },
  },
});
```

## Dynamically Modify Anchor Points

```javascript
const edge = graph.addEdge({ source: 'node1', target: 'node2' });

// Modify source anchor point
edge.setSource({
  cell: 'node1',
  anchor: { name: 'bottom', args: { dx: 10 } },
  connectionPoint: 'anchor',
});

// Modify target anchor point
edge.setTarget({
  cell: 'node2',
  anchor: 'top',
  connectionPoint: 'boundary',
});
```

## Common Errors

### ❌ Confusing anchor with connectionPoint

```javascript
// Incorrect: Assuming anchor:'right' will make the edge start from the right side (but the default connectionPoint is boundary, which recalculates the intersection point)
graph.addEdge({
  source: { cell: 'node1', anchor: 'right' },
  target: { cell: 'node2', anchor: 'left' },
});
// The edge may not precisely start from the center of the right side

// Correct: Use connectionPoint:'anchor' in conjunction to skip intersection point calculation
graph.addEdge({
  source: { cell: 'node1', anchor: 'right', connectionPoint: 'anchor' },
  target: { cell: 'node2', anchor: 'left', connectionPoint: 'anchor' },
});
```

### ❌ Confusing port with anchor

```javascript
// port is the connection stub (connection point UI on the node), anchor is the calculation method for the edge connection position
// When port exists, use the port field for source/target:
graph.addEdge({
  source: { cell: 'node1', port: 'out-1' },  // Connect to port
  target: { cell: 'node2', port: 'in-1' },
});

// When no port exists, use the anchor field to control the connection position:
graph.addEdge({
  source: { cell: 'node1', anchor: 'right' },  // Connect to anchor point
  target: { cell: 'node2', anchor: 'left' },
});
```