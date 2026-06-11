---
id: "x6-core-router-advanced"
title: "X6 Advanced Router"
description: |
  In addition to the commonly used orth, manhattan, metro, and er routers, X6 also provides advanced routers such as oneside (single-side routing) and loop (self-loop routing).
  These are suitable for scenarios like single-side wiring, self-loop connections, etc.

library: "x6"
version: "3.x"
category: "core"
subcategory: "edge"
tags:
  - "router"
  - "routing"
  - "oneside"
  - "loop"
  - "self-loop"
  - "single-side"
  - "edge"
  - "connection"

related:
  - "x6-core-edge"
  - "x6-core-connector-advanced"

use_cases:
  - "Edge entering and exiting from the same side of a node"
  - "Self-loop connection (edge within the same node)"
  - "Single-side wiring layout"
  - "Representation of circular dependencies"

difficulty: "intermediate"
completeness: "full"
---

## Complete List of Routers

| Router | Description | Typical Scenario |
|--------|-------------|---------------|
| `normal` | Default, direct connection without intermediate points | Simple connections |
| `orth` | Orthogonal routing (horizontal/vertical segments) | Flowcharts |
| `manhattan` | Smart orthogonal routing, automatically avoids obstacles | Complex flowcharts |
| `metro` | Metro line style (45° diagonal lines) | Metro maps |
| `er` | ER diagram routing | ER diagrams |
| `oneside` | Forces entry/exit from a specified side | Hierarchical layouts, unidirectional flows |
| `loop` | Self-loop routing | Self-loop edges, loop states |

---

## OneSide Router

Forces edges to enter or exit nodes from a specified side (top/bottom/left/right), suitable for hierarchical layouts or scenarios requiring uniform edge direction.

### Configuration Options

| Property | Type | Default Value | Description |
|------|------|--------|------|
| `side` | `'left' \| 'top' \| 'right' \| 'bottom'` | `'bottom'` | Outgoing direction |
| `padding` | `number \| SideOptions` | `40` | Distance from the outgoing point to the node |

### Example

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({ container: 'container' });

const source = graph.addNode({
  shape: 'rect',
  x: 50,
  y: 50,
  width: 100,
  height: 40,
  label: 'Source',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
});

const target = graph.addNode({
  shape: 'rect',
  x: 300,
  y: 200,
  width: 100,
  height: 40,
  label: 'Target',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
});

// Edge enters/exits from the bottom
graph.addEdge({
  source,
  target,
  router: {
    name: 'oneside',
    args: {
      side: 'bottom',
      padding: 50,
    },
  },
  attrs: {
    line: { stroke: '#5b8ff9', strokeWidth: 2, targetMarker: 'classic' },
  },
});

// Edge enters/exits from the right
graph.addEdge({
  source,
  target,
  router: {
    name: 'oneside',
    args: {
      side: 'right',
      padding: 30,
    },
  },
  attrs: {
    line: { stroke: '#52c41a', strokeWidth: 2, targetMarker: 'classic' },
  },
});
```

### How It Works

The OneSide router will:
1. Move the connection points of the source and target to the outside of the specified side of the node
2. Maintain orthogonal paths
3. Automatically align if the outgoing points of two nodes are on the same horizontal/vertical line

---

## Loop Router

Used for self-loop edges (where the source and target are the same node, or where the sourceAnchor and targetAnchor are the same).

### Configuration Options

| Property | Type | Default Value | Description |
|------|------|--------|------|
| `width` | `number` | `50` | Width of the self-loop (distance to the node center) |
| `height` | `number` | `80` | Height of the self-loop (arc span) |
| `angle` | `'auto' \| number` | `'auto'` | Angle direction of the self-loop, `'auto'` automatically finds a direction that does not overlap with the node |
| `merge` | `boolean \| number` | - | Whether to merge start and end points at the same anchor |

### Example: Self-Loop Edge

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

// Self-loop edge: source and target point to the same node
graph.addEdge({
  source: node,
  target: node,
  router: {
    name: 'loop',
    args: {
      width: 60,
      height: 100,
      angle: 'auto',
    },
  },
  connector: { name: 'loop' },
  label: 'Retry',
  attrs: {
    line: { stroke: '#f5222d', strokeWidth: 2, targetMarker: 'classic' },
  },
});
```

### Example: Self-loop at a Specified Angle

```javascript
// Self-loop exiting from the top (angle: -90, i.e., top direction)
graph.addEdge({
  source: node,
  target: node,
  router: {
    name: 'loop',
    args: {
      width: 50,
      height: 80,
      angle: -90,
    },
  },
  connector: { name: 'loop' },
  attrs: {
    line: { stroke: '#722ed1', strokeWidth: 2, targetMarker: 'classic' },
  },
});
```

### angle Angle Description

- `0`: Right side
- `90`: Bottom
- `180` or `-180`: Left side
- `-90` or `270`: Top
- `'auto'`: Automatically select a direction that does not overlap with the node's BBox

---

## Router Abbreviation and Object Notation

```javascript
// Abbreviation (no parameters)
graph.addEdge({ source, target, router: 'orth' });

// Object notation (with parameters)
graph.addEdge({
  source,
  target,
  router: {
    name: 'manhattan',
    args: {
      padding: 20,
      excludeShapes: ['group'],
    },
  },
});
```

---

## Common Errors and Fixes

### Error 1: Self-loop edges do not use the loop router

```javascript
// ❌ Incorrect: Self-loop edges using the orth router will result in edges with a length of 0
graph.addEdge({ source: node, target: node, router: 'orth' });

// ✅ Correct: Self-loop edges use the loop router + loop connector
graph.addEdge({
  source: node,
  target: node,
  router: { name: 'loop', args: { width: 50, height: 80 } },
  connector: { name: 'loop' },
});
```

### Error 2: Spelling Error in `oneside`'s `side`

```javascript
// ❌ Incorrect: Spelling error in `side` value
router: { name: 'oneside', args: { side: 'buttom' } }

// ✅ Correct: `side` value should be 'top' | 'bottom' | 'left' | 'right'
router: { name: 'oneside', args: { side: 'bottom' } }
```

### Error 3: Incorrect Custom Node Registration Causes Rendering Failure

```javascript
// ❌ Incorrect: Using Shape.Rectangle.define to register a node may cause issues due to the define method being undefined
Shape.Rectangle.define({
  shape: 'custom-node',
  width: 80,
  height: 40,
  attrs: {
    body: { fill: '#fff', stroke: '#000' },
    label: { text: '', fill: '#333' },
  },
});

// ✅ Correct: Using Graph.registerNode to register a custom node
Graph.registerNode(
  'custom-node',
  {
    inherit: 'rect',
    width: 100,
    height: 40,
    markup: [
      { tagName: 'rect', selector: 'body' },
      { tagName: 'text', selector: 'label' },
    ],
    attrs: {
      body: {
        stroke: '#8f8f8f',
        strokeWidth: 1,
        fill: '#fff',
        rx: 6,
        ry: 6,
      },
    },
  },
  true,
);
```

### Error 4: orth Router Not Taking Effect or Failing to Bypass Obstacles

```javascript
// ❌ Error: Router not properly configured or missing necessary graph configuration
graph.addEdge({
  source: sourceNode,
  target: targetNode,
  router: 'orth',
});

// ✅ Correct: Ensure router is enabled during graph initialization and explicitly set in addEdge
const graph = new Graph({
  container: 'container',
  connecting: {
    router: 'orth',
  },
});

graph.addEdge({
  source,
  target,
  router: 'orth',
});
```