---
id: "x6-core-edge"
title: "X6 Edge Configuration and Styling"
description: |
  X6 edge creation, router, connector, arrow, label, and vertex configuration.
  Includes usage of orth/manhattan/smooth/rounded routers and connectors.

library: "x6"
version: "3.x"
category: "core"
subcategory: "edge"
tags:
  - "edge"
  - "connection"
  - "router"
  - "connector"
  - "arrow"
  - "marker"
  - "targetMarker"
  - "label"
  - "vertices"
  - "orth"
  - "manhattan"
  - "smooth"
  - "rounded"
  - "strokeDasharray"
  - "dashed"

related:
  - "x6-core-node"
  - "x6-core-ports"
  - "x6-core-graph-init"

use_cases:
  - "Creating connections between nodes"
  - "Setting edge routers and connectors"
  - "Configuring edge arrow styles"
  - "Adding text labels to edges"
  - "Creating dashed/curved edges"
  - "Setting intermediate vertices for edges"

anti_patterns:
  - "Do not confuse the roles of router and connector"
  - "Do not omit source/target"

difficulty: "beginner"
completeness: "full"
---
## Add Edge

```javascript
// Method 1: Pass node instances
graph.addEdge({ source: sourceNode, target: targetNode });

// Method 2: Pass node IDs
graph.addEdge({ source: 'node1', target: 'node2' });

// Method 3: Connect to ports
graph.addEdge({
  source: { cell: 'node1', port: 'out1' },
  target: { cell: 'node2', port: 'in1' },
});

// Method 4: Use coordinates
graph.addEdge({
  source: { x: 100, y: 50 },
  target: { x: 400, y: 50 },
});
// Or use shorthand
graph.addEdge({
  sourcePoint: [100, 50],
  targetPoint: [400, 50],
});
```

## Edge Style

```javascript
graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: {
      stroke: '#8f8f8f',        // Line color
      strokeWidth: 1,           // Line width
      strokeDasharray: '5 3',   // Dashed line (5px line + 3px gap)
      targetMarker: 'classic',  // Target end arrow
      sourceMarker: null,       // No arrow at source end
    },
  },
});
```

## Arrow Types

```javascript
// Built-in Arrows
targetMarker: 'classic'        // Classic triangle arrow
targetMarker: 'block'          // Solid triangle
targetMarker: 'circle'         // Circle
targetMarker: 'circlePlus'     // Circle with + sign
targetMarker: 'diamond'        // Diamond
targetMarker: 'ellipse'        // Ellipse
targetMarker: 'cross'          // Cross
targetMarker: 'async'          // Async marker

// Custom Arrows
targetMarker: {
  name: 'block',
  width: 12,
  height: 8,
  offset: -4,
  fill: '#333',
}
```

## Router

The router determines the path points (turning points) that an edge passes through.

```javascript
// Orthogonal routing (vertical/horizontal folding)
graph.addEdge({ source, target, router: 'orth' });

// Manhattan routing (intelligent obstacle avoidance)
graph.addEdge({ source, target, router: 'manhattan' });

// Router with configuration
graph.addEdge({
  source, target,
  router: { name: 'orth', args: { padding: 20 } },
});

// ER diagram dedicated routing
graph.addEdge({ source, target, router: 'er' });

// Metro line routing
graph.addEdge({ source, target, router: 'metro' });
```

## Connector

The connector determines how lines are drawn between path points.

```javascript
// Rounded polyline
graph.addEdge({ source, target, router: 'orth', connector: 'rounded' });

// Bezier curve
graph.addEdge({ source, target, connector: 'smooth' });

// Jumpover (jumps at intersections)
graph.addEdge({ source, target, connector: 'jumpover' });

// Connector with configuration
graph.addEdge({
  source, target,
  connector: { name: 'rounded', args: { radius: 10 } },
});
```

## Edge Labels

```javascript
// Shorthand
graph.addEdge({ source, target, label: 'Yes' });

// Detailed Configuration
graph.addEdge({
  source, target,
  labels: [
    {
      position: 0.5,           // Label position on the edge (0-1)
      attrs: {
        text: { text: 'label text', fontSize: 12, fill: '#333' },
        rect: { fill: '#fff', stroke: '#8f8f8f', rx: 3, ry: 3 },
      },
    },
  ],
});

// Multiple Labels
graph.addEdge({
  source, target,
  labels: [
    { position: 0.25, attrs: { text: { text: 'start' } } },
    { position: 0.75, attrs: { text: { text: 'end' } } },
  ],
});
```

## Vertices

Manually specify intermediate vertices for an edge:

```javascript
graph.addEdge({
  source: node1,
  target: node2,
  vertices: [
    { x: 200, y: 50 },
    { x: 200, y: 200 },
  ],
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
});
```

## Dynamically Modify Edge

```javascript
// Modify style
edge.attr('line/stroke', '#f5222d');
edge.attr('line/strokeWidth', 2);

// Modify label
edge.setLabels([{ attrs: { text: { text: 'Updated' } } }]);

// Modify router
edge.setRouter('manhattan');

// Modify connector
edge.setConnector('smooth');

// Modify source/target
edge.setSource(newSourceNode);
edge.setTarget({ cell: 'node3', port: 'in1' });
```

## Common Border Style Combinations

### Flowchart Edge

```javascript
graph.addEdge({
  source, target,
  router: 'orth',
  connector: 'rounded',
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
});
```

### Lineage Graph Edge

```javascript
graph.addEdge({
  source: { cell: srcNode, port: 'out1' },
  target: { cell: tgtNode, port: 'in1' },
  connector: 'smooth',
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1 } },
});
```

### Dashed Edge (Call Relationship)

```javascript
graph.addEdge({
  source, target,
  attrs: {
    line: { stroke: '#aaa', strokeWidth: 1, strokeDasharray: '5 3', targetMarker: 'classic' },
  },
});
```

### Highlighted State Edge

```javascript
graph.addEdge({
  source, target,
  attrs: { line: { stroke: '#1890ff', strokeWidth: 2, targetMarker: 'classic' } },
});
```