---
id: "x6-core-connection-strategy"
title: "X6 Connection Strategy"
description: |
  The connection strategy determines how the source/target endpoint data is generated when a connection is established: using default anchors (noop), pinning to absolute coordinates (pinAbsolute), or pinning to relative positions (pinRelative).

library: "x6"
version: "3.x"
category: "core"
subcategory: "connection-strategy"
tags:
  - "connectionStrategy"
  - "Connection Strategy"
  - "pinAbsolute"
  - "pinRelative"
  - "Connection Landing Point"
  - "Anchor Pinning"

related:
  - "x6-core-anchor"
  - "x6-core-connection-point"
  - "x6-core-edge"

use_cases:
  - "Connecting precisely to the mouse release position"
  - "Pinning connections to relative positions on node edges"
  - "Customizing connection endpoint positioning logic"

difficulty: "advanced"
completeness: "full"
---

## Concept Explanation

When a user creates a connection by dragging, the source/target endpoints of the connection default to the anchor points of the nodes. The **Connection Strategy** can alter this default behavior, allowing endpoints to anchor to more precise positions.

Three built-in strategies:

| Strategy | Description |
|------|------|
| `noop` | Default behavior, no additional processing, uses normal anchor calculation |
| `pinAbsolute` | Pins the endpoint to the absolute coordinates where the mouse is released (x/y offset relative to the top-left corner of the node) |
| `pinRelative` | Pins the endpoint to the relative position where the mouse is released (0~1 ratio value) |

## Basic Usage

Set in the `connecting` configuration of Graph:

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  connecting: {
    connectionStrategy: 'pinRelative',
  },
});
```

## pinAbsolute

Endpoints are fixed to the absolute coordinates (pixel values) corresponding to the mouse release position:

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    connectionStrategy: 'pinAbsolute',
  },
});
```

After the edge is created, the source/target data of the edge will include the `anchor` field:

```javascript
// Example of edge data
{
  source: { cell: 'node1', anchor: { name: 'topLeft', args: { dx: 50, dy: 20 } } },
  target: { cell: 'node2', anchor: { name: 'topLeft', args: { dx: 30, dy: 40 } } },
}
```

## pinRelative

Endpoint fixed to the relative ratio (0~1) of the mouse release position:

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    connectionStrategy: 'pinRelative',
  },
});
```

Relative position is represented by a ratio, and the connection endpoint will automatically follow when the node is moved or scaled:

```javascript
// Example of connection data (end value is a relative quantity between -1 and 1)
{
  source: { cell: 'node1', anchor: { name: 'nodeCenter', args: { dx: '20%', dy: '30%' } } },
  target: { cell: 'node2', anchor: { name: 'nodeCenter', args: { dx: '-10%', dy: '15%' } } },
}
```

## Use Case Comparison

| Scenario | Recommended Strategy |
|------|----------|
| General Flowchart/DAG (Connection to Ports) | `noop` (Default) |
| Free Connection to Any Node Position | `pinRelative` |
| Precise Positioning (e.g., Circuit Diagrams) | `pinAbsolute` |

## Working with Ports

When an edge connects to a port, the connection strategy typically does not require configuration (the port itself serves as a precise anchor point). The connection strategy is primarily used in scenarios where there are **no ports, and the connection is made directly to the node body**.

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    allowBlank: false,
    // Usually not needed when ports are present
    // Use when there are no ports and precise anchoring is required:
    connectionStrategy: 'pinRelative',
  },
});
```

## Custom Connection Strategy

You can register a custom strategy:

```javascript
import { Graph } from '@antv/x6';

Graph.registerConnectionStrategy('myStrategy', (terminal, cellView, magnet, coords, edge, type, options) => {
  // terminal: Current terminal data { cell, port, ... }
  // cellView: Target node/edge view
  // magnet: DOM element that triggered the connection
  // coords: Canvas coordinates when the mouse is released { x, y }
  // Return the modified terminal data
  return {
    ...terminal,
    anchor: {
      name: 'center',
    },
  };
});

const graph = new Graph({
  container: 'container',
  connecting: {
    connectionStrategy: 'myStrategy',
  },
});
```

## Common Errors

### ❌ Using pinAbsolute for Nodes with Ports

```javascript
// Not recommended: Using pinAbsolute when nodes have ports can lead to anchor calculation confusion
const graph = new Graph({
  container: 'container',
  connecting: { connectionStrategy: 'pinAbsolute' },
});
graph.addNode({
  x: 100, y: 100, width: 80, height: 40,
  ports: { items: [{ id: 'p1', group: 'out' }] },  // Node already has ports
});
// When connecting, the port position is ignored, and the connection is made to the absolute mouse release position
```

```javascript
// Correct: Use the default strategy (noop) when nodes have ports, allowing connections to naturally attach to ports
const graph = new Graph({
  container: 'container',
  connecting: { allowBlank: false },  // ✅ Use the default strategy
});
```