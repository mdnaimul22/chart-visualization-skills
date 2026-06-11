---
id: "x6-intermediate-custom-edge"
title: "X6 Custom Edge"
description: |
  Comprehensive guide to X6 custom edges: Graph.registerEdge to register custom edges, markup/attrs to customize edge appearance.
  Includes inheriting built-in edges, custom routers, custom connectors, and registering custom edges.

library: "x6"
version: "3.x"
category: "intermediate"
subcategory: "custom-edge"
tags:
  - "custom edge"
  - "registerEdge"
  - "Graph.registerEdge"
  - "markup"
  - "attrs"
  - "inherit"
  - "edge"
  - "shape"
  - "custom connection"
  - "router"
  - "connector"

related:
  - "x6-core-edge"
  - "x6-core-graph-init"
  - "x6-intermediate-custom-node"

use_cases:
  - "Register custom edges with fixed styles"
  - "Create compound edges with multiple segments"
  - "Register custom routers"
  - "Register custom connectors"
  - "Create special effects like dashed lines, animated flow edges"

anti_patterns:
  - "Don't forget to pass true as the third parameter in Graph.registerEdge to allow overrides"
  - "Custom routers must return an array of points"
---

# X6 Custom Edge

## Graph.registerEdge — Register Custom Edge

Similar to registering custom nodes, use `Graph.registerEdge` to register reusable edge types.

### Basic Registration

```javascript
import { Graph } from '@antv/x6';

Graph.registerEdge(
  'custom-edge',
  {
    inherit: 'edge',  // Inherit from built-in edge
    attrs: {
      line: {
        stroke: '#1890ff',
        strokeWidth: 2,
        targetMarker: 'classic',
      },
    },
    router: 'orth',
    connector: 'rounded',
  },
  true,
);

const graph = new Graph({ container: 'container', width: 800, height: 600 });

graph.addEdge({
  shape: 'custom-edge',
  source: 'node1',
  target: 'node2',
});
```

### Dashed Edge

```javascript
Graph.registerEdge(
  'dashed-edge',
  {
    inherit: 'edge',
    attrs: {
      line: {
        stroke: '#888',
        strokeWidth: 1,
        strokeDasharray: '5 3',
        targetMarker: 'classic',
      },
    },
  },
  true,
);
```

### Flow Edge with Label

```javascript
Graph.registerEdge(
  'flow-edge',
  {
    inherit: 'edge',
    attrs: {
      line: {
        stroke: '#8f8f8f',
        strokeWidth: 1,
        targetMarker: 'classic',
      },
    },
    router: 'orth',
    connector: 'rounded',
    defaultLabel: {
      markup: [
        { tagName: 'rect', selector: 'labelBody' },
        { tagName: 'text', selector: 'labelText' },
      ],
      attrs: {
        labelBody: {
          ref: 'labelText',
          refX: -5,
          refY: -3,
          refWidth: '100%',
          refHeight: '100%',
          refWidth2: 10,
          refHeight2: 6,
          fill: '#fff',
          stroke: '#d9d9d9',
          strokeWidth: 1,
          rx: 3,
          ry: 3,
        },
        labelText: {
          fontSize: 12,
          fill: '#333',
          textAnchor: 'middle',
          textVerticalAnchor: 'middle',
        },
      },
      position: { distance: 0.5 },
    },
  },
  true,
);

graph.addEdge({
  shape: 'flow-edge',
  source: node1,
  target: node2,
  label: 'Yes',
});
```

### Double Edge (Composite Markup)

```javascript
Graph.registerEdge(
  'double-edge',
  {
    inherit: 'edge',
    markup: [
      {
        tagName: 'path',
        selector: 'outline',
        attrs: { fill: 'none' },
      },
      {
        tagName: 'path',
        selector: 'line',
        attrs: { fill: 'none' },
      },
    ],
    attrs: {
      outline: {
        connection: true,
        stroke: '#ccc',
        strokeWidth: 8,
      },
      line: {
        connection: true,
        stroke: '#1890ff',
        strokeWidth: 2,
        targetMarker: 'classic',
      },
    },
  },
  true,
);
```

## Custom Router

The router further processes the path points, adding extra points when necessary to make the edge follow specific rules.

```javascript
Graph.registerRouter(
  'custom-router',
  (vertices, args, view) => {
    // vertices: User-defined path points
    // Returns the processed array of points
    const { offset = 20 } = args;
    const points = [];
    const source = view.sourceAnchor;
    const target = view.targetAnchor;

    // Example: Move right from source first, then turn to target
    points.push({ x: source.x + offset, y: source.y });
    points.push({ x: source.x + offset, y: target.y });

    return points;
  },
  true,
);

// Usage
graph.addEdge({
  source: node1,
  target: node2,
  router: { name: 'custom-router', args: { offset: 40 } },
});
```

## Custom Connector

The connector processes the points returned by the router into SVG pathData.

```javascript
Graph.registerConnector(
  'wobble',
  (sourcePoint, targetPoint, routePoints, args) => {
    // Return SVG path string
    const { amplitude = 10 } = args;
    const points = [sourcePoint, ...routePoints, targetPoint];
    let path = `M ${points[0].x} ${points[0].y}`;
    for (let i = 1; i < points.length; i++) {
      const midX = (points[i - 1].x + points[i].x) / 2;
      const dy = i % 2 === 0 ? amplitude : -amplitude;
      path += ` Q ${midX} ${points[i - 1].y + dy} ${points[i].x} ${points[i].y}`;
    }
    return path;
  },
  true,
);

// Usage
graph.addEdge({
  source: node1,
  target: node2,
  connector: { name: 'wobble', args: { amplitude: 8 } },
});
```

## Specify Default Edge Type in `connecting`

When users create edges by dragging through interaction, the default edge type can be specified via `createEdge`:

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    allowBlank: false,
    router: 'orth',
    connector: 'rounded',
    createEdge() {
      return this.createEdge({
        shape: 'custom-edge',  // Use the registered custom edge
        attrs: {
          line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' },
        },
      });
    },
  },
});
```

## Dynamically Modify Properties of Registered Edges

```javascript
const edge = graph.addEdge({ shape: 'custom-edge', source: node1, target: node2 });

// Modify line color
edge.attr('line/stroke', '#f5222d');

// Modify router
edge.setRouter('manhattan');

// Modify connector
edge.setConnector('smooth');

// Modify label
edge.setLabels([{ attrs: { labelText: { text: 'Updated' } } }]);
```

## Common Errors

### ❌ Repeated Registration Without Overwrite Parameter

```javascript
// Error: Second registration of the same edge name throws an error
Graph.registerEdge('my-edge', { ... });
Graph.registerEdge('my-edge', { ... }); // Error

// Correct: Third parameter `true` allows overwriting
Graph.registerEdge('my-edge', { ... }, true);
```

### ❌ Custom Router Does Not Return an Array

```javascript
// Error: Router must return an array of points
Graph.registerRouter('bad-router', (vertices) => {
  return { x: 100, y: 100 }; // ❌ Returns a single point
});

// Correct: Returns an array of points
Graph.registerRouter('good-router', (vertices) => {
  return [{ x: 100, y: 100 }]; // ✅
}, true);
```