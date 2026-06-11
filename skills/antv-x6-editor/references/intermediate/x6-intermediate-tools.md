---
id: "x6-intermediate-tools"
title: "X6 Tools"
description: |
  Configuration guide for X6 node and edge tools.
  Includes built-in tools (button, button-remove, boundary, vertices, segments, node-editor, edge-editor, arrowhead) and custom tools.

library: "x6"
version: "3.x"
category: "intermediate"
subcategory: "tools"
tags:
  - "tools"
  - "button"
  - "button-remove"
  - "remove button"
  - "boundary"
  - "vertices"
  - "segments"
  - "node-editor"
  - "edge-editor"
  - "arrowhead"
  - "source-arrowhead"
  - "target-arrowhead"
  - "tool"
  - "interaction"

related:
  - "x6-core-node"
  - "x6-core-edge"
  - "x6-core-events"

use_cases:
  - "Add a remove button to a node"
  - "Add a path point editing tool to an edge"
  - "Double-click to edit node/edge text"
  - "Drag to modify the start or end point of an edge"
  - "Display tools on hover"

anti_patterns:
  - "Do not forget to remove dynamically added tools on mouseleave"
  - "node-editor no longer requires the event parameter (2.8.0+)"
---

# X6 Tools

Tools are widgets rendered on nodes/edges to enhance interactivity, such as delete buttons, path point editing, text editing, etc.

## Add Tools

### Add on Creation

```javascript
// Node tool
graph.addNode({
  shape: 'rect',
  x: 40,
  y: 40,
  width: 100,
  height: 40,
  label: 'Node',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 } },
  tools: [
    {
      name: 'button-remove',
      args: { x: '100%', y: 0, offset: { x: -10, y: 10 } },
    },
  ],
});

// Edge tool
graph.addEdge({
  source: node1,
  target: node2,
  tools: ['vertices', 'segments'],
});
```

### Dynamically Add/Remove

```javascript
// Add tool
node.addTools([{ name: 'button-remove', args: { x: 10, y: 10 } }]);

// Check if a tool exists
node.hasTool('button-remove'); // true

// Remove specified tool
node.removeTool('button-remove');

// Remove all tools
node.removeTools();
```

### Display Tools on Hover

```javascript
graph.on('node:mouseenter', ({ node }) => {
  node.addTools([
    { name: 'boundary' },
    { name: 'button-remove', args: { x: '100%', y: 0, offset: { x: -10, y: 10 } } },
  ]);
});

graph.on('node:mouseleave', ({ node }) => {
  node.removeTools();
});

graph.on('edge:mouseenter', ({ edge }) => {
  edge.addTools([
    { name: 'vertices' },
    { name: 'button-remove', args: { distance: 20 } },
  ]);
});

graph.on('edge:mouseleave', ({ edge }) => {
  edge.removeTools();
});
```

## Built-in Node Tools

### button — Custom Button

Renders a button at a specified position on the node, supporting custom click interactions.

```javascript
node.addTools({
  name: 'button',
  args: {
    x: 0,
    y: 0,
    offset: { x: 18, y: 18 },
    markup: [
      { tagName: 'circle', selector: 'button', attrs: { r: 8, fill: '#1890ff', cursor: 'pointer' } },
      { tagName: 'text', selector: 'icon', attrs: { fill: '#fff', fontSize: 12, textAnchor: 'middle', dominantBaseline: 'central', text: '+' } },
    ],
    onClick({ cell }) {
      console.log('Button clicked on', cell.id);
    },
  },
});
```

| Parameter | Type | Description |
|------|------|------|
| `x` | number \| string | X-coordinate (percentage represents relative position) |
| `y` | number \| string | Y-coordinate |
| `offset` | `{ x, y }` | Offset based on x/y |
| `markup` | Markup | SVG structure of the button |
| `onClick` | Function | Click callback `({ e, cell, view }) => void` |

### button-remove — Remove Button

A special case of button, which deletes the corresponding node when clicked. Supports all configurations of button.

```javascript
graph.addNode({
  shape: 'rect',
  x: 40,
  y: 40,
  width: 100,
  height: 40,
  label: 'Delete me',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 } },
  tools: [
    {
      name: 'button-remove',
      args: { x: '100%', y: 0, offset: { x: -10, y: 10 } },
    },
  ],
});
```

### boundary — Bounding Box

Renders a rectangle based on the node's bounding box, used only for visualization without interaction.

```javascript
node.addTools({
  name: 'boundary',
  args: {
    padding: 5,
    attrs: {
      fill: '#7c68fc',
      stroke: '#333',
      'stroke-width': 1,
      'fill-opacity': 0.2,
    },
  },
});
```

### node-editor — Text Editing

Provides text editing functionality on nodes. Double-click a node to edit its text.

```javascript
// Add node-editor tool (2.8.0+ does not require passing event)
node.addTools({
  name: 'node-editor',
});

// Specify getText/setText when customizing markup
node.addTools({
  name: 'node-editor',
  args: {
    getText: 'attrs/label/text',  // Attribute path
    setText: 'attrs/label/text',
  },
});
```

| Parameter | Type | Description |
|------|------|------|
| `getText` | string \| Function | Attribute path or method to get text |
| `setText` | string \| Function | Attribute path or method to set text |
| `attrs/fontSize` | string | Editing font size, default 14 |
| `attrs/color` | string | Font color, default #000 |

## Built-in Edge Tools

### vertices — Path Point Editing

Renders small dots at path point positions, supporting drag-to-modify position, double-click to delete, and click on edges to add path points.

```javascript
graph.addEdge({
  source: node1,
  target: node2,
  vertices: [{ x: 200, y: 100 }],
  tools: [
    {
      name: 'vertices',
      args: { attrs: { fill: '#666' }, snapRadius: 20 },
    },
  ],
});
```

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `snapRadius` | number | 20 | Path point snap radius |
| `addable` | boolean | true | Whether path points can be added |
| `removable` | boolean | true | Whether path points can be deleted on double-click |

### segments — Segment Tool

Renders a toolbar at the center of each segment. Dragging adjusts the position of the path points at both ends of the segment.

```javascript
graph.addEdge({
  source: node1,
  target: node2,
  router: 'orth',
  connector: 'rounded',
  tools: ['segments'],
});
```

### button-remove (Edge)

Renders a delete button at the specified position on the edge.

```javascript
edge.addTools({
  name: 'button-remove',
  args: { distance: 20 },  // Distance from the starting point
});
```

### source-arrowhead / target-arrowhead

Render arrow graphics at the start or end point of an edge. Dragging can modify the start/end point of the edge.

```javascript
edge.addTools([
  'source-arrowhead',
  'target-arrowhead',
]);
```

### edge-editor — Edge Text Editor

Double-click an edge to edit the text label on it.

```javascript
edge.addTools({
  name: 'edge-editor',
  args: {
    attrs: { fontSize: 14, color: '#333' },
  },
});
```

## Common Patterns

### Display Tools When Selected, Remove When Unselected

```javascript
graph.on('node:selected', ({ node }) => {
  node.addTools([
    { name: 'boundary' },
    { name: 'button-remove', args: { x: '100%', y: 0, offset: { x: -10, y: 10 } } },
  ]);
});

graph.on('node:unselected', ({ node }) => {
  node.removeTools();
});
```

### Double-click to Edit Node Text

```javascript
graph.on('node:dblclick', ({ node }) => {
  node.addTools({ name: 'node-editor' });
});
```

## Common Errors and Fixes

### ❌ Adding Tools on `mouseenter` but Forgetting to Remove on `mouseleave`

```javascript
// Error: Tools will accumulate indefinitely
graph.on('node:mouseenter', ({ node }) => {
  node.addTools([{ name: 'button-remove' }]);
});
// Missing mouseleave handling

// Correct: Paired usage
graph.on('node:mouseenter', ({ node }) => {
  node.addTools([{ name: 'button-remove', args: { x: '100%', y: 0, offset: { x: -10, y: 10 } } }]);
});
graph.on('node:mouseleave', ({ node }) => {
  node.removeTools();
});
```

### ❌ Incorrect Usage of graph.render() Method

```javascript
// Error: Graph instance does not have a render method
const graph = new Graph({ ... });
graph.render(); // ❌ Error: graph.render is not a function

// Correct: The Graph constructor automatically renders, no need to manually call render()
const graph = new Graph({ ... });
```

### ❌ Incorrect Tool Configuration Method

```javascript
// Incorrect: Dynamically adding vertices and segments tools in an event
graph.on('edge:mouseenter', ({ cell }) => {
  cell.addTools([
    'vertices',
    'segments'
  ])
})

// Correct: Directly configure tools when creating an edge
graph.addEdge({
  source: node1,
  target: node2,
  tools: ['vertices', 'segments'],
});
```

### ❌ Incorrect Usage of tools.items Configuration Structure

```javascript
// Error: tools configuration should be an array, not an object
const edge = graph.addEdge({
  source: 'source',
  target: 'target',
  tools: {
    items: [
      { name: 'vertices' },
      { name: 'segments' }
    ]
  }
})

// Correct: tools should be in array form
const edge = graph.addEdge({
  source: 'source',
  target: 'target',
  tools: [
    'vertices',
    'segments'
  ]
})
```

### ❌ Incorrect Configuration Format When Adding Tools to an Edge

```javascript
// Incorrect: The tools configuration should be an array, not an object
const edge = graph.addEdge({
  source: 'source',
  target: 'target',
  tools: {
    name: 'segments'
  }
})

// Correct: tools should be in array format
const edge = graph.addEdge({
  source: 'source',
  target: 'target',
  tools: [
    'segments'
  ]
})
```

### ❌ Incorrectly Calling the render Method on a Graph Instance

```javascript
// Error: Graph instances do not have a render method
const graph = new Graph({ ... });
graph.render(); // ❌ Error: graph.render is not a function

// Correct: The Graph constructor automatically renders, no need to manually call render()
const graph = new Graph({ ... });
```

### ❌ Incorrect Usage of Tools Configuration Format in createEdge

```javascript
// Incorrect: tools configuration in createEdge should be an array, not an object
graph.options.connecting = {
  createEdge() {
    return graph.createEdge({
      shape: 'edge',
      tools: {
        items: [
          'vertices',
          'segments'
        ]
      }
    })
  }
}

// Correct: tools should be in array format
graph.options.connecting = {
  createEdge() {
    return graph.createEdge({
      shape: 'edge',
      tools: [
        'vertices',
        'segments'
      ]
    })
  }
}
```

### ❌ Failure to Properly Handle Node Selection State Results in Duplicate Tool Addition

```javascript
// Error: Adds boundary tool on every click without clearing existing tools
graph.on('node:click', ({ node }) => {
  node.addTools([
    { name: 'boundary' }
  ]);
});

// Correct: Clear existing tools before adding new ones
graph.on('node:click', ({ node }) => {
  graph.getNodes().forEach((n) => n.removeTools());
  node.addTools([
    { name: 'boundary' }
  ]);
});
```

### ❌ Syntax Errors or Incomplete Code Snippets

```javascript
// Error: Incomplete code causes syntax errors
const node2 = graph.addNode({
  shape: 'rect',
  x: 300,
  y: 100,
  width: 10  graph.addEdge({ // ❌ Syntax error
  source: node1,
  target: node2,
  attrs: {
    line: { stroke: '#8f8f8f', strokeWidth: 1 },
  },
});

// Correct: Ensure complete and correct syntax
const node2 = graph.addNode({
  shape: 'rect',
  x: 300,
  y: 100,
  width: 100,
  height: 40,
  label: 'Node 2',
  attrs: {
    body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 },
  },
});

graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: { stroke: '#8f8f8f', strokeWidth: 1 },
  },
});
```

### ❌ Incorrect Usage of the Selection Plugin and Attempting to Access the `node.selected` Event

```javascript
// Incorrect: The Selection plugin does not trigger the `node:selected` event, and the Selection plugin is not imported correctly
import { Graph, Selection } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
  plugins: [
    new Selection({
      enabled: true,
      showNodeSelectionBox: true,
    }),
  ],
});

graph.on('node:selected', ({ node }) => {
  node.addTools([
    {
      name: 'boundary',
      args: {
        attrs: {
          stroke: '#31d0c6',
          strokeWidth: 1,
          strokeDasharray: '5 5',
        },
      },
    },
  ]);
});

// Correct: Use the `click` event instead of the `selected` event, and remove the Selection plugin
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
});

graph.on('node:click', ({ node }) => {
  graph.getNodes().forEach((n) => n.removeTools());
  node.addTools([
    {
      name: 'boundary',
      args: {
        padding: 6,
        attrs: {
          fill: 'none',
          stroke: '#1890ff',
          strokeWidth: 1,
          strokeDasharray: '5 3',
        },
      },
    },
  ]);
});
```

### ❌ Incorrectly Passing the Wrong Data Structure to `addTools`

```javascript
// Error: addTools expects an array, not an object
node.addTools({
  name: 'boundary',
  args: {
    attrs: {
      stroke: '#31d0c6',
      strokeWidth: 1,
      strokeDasharray: '5 5',
    },
  },
});

// Correct: addTools should receive an array
node.addTools([
  {
    name: 'boundary',
    args: {
      attrs: {
        stroke: '#31d0c6',
        strokeWidth: 1,
        strokeDasharray: '5 5',
      },
    },
  },
]);
```

## Minimum Viable Example

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
});

const source = graph.addNode({
  shape: 'rect',
  x: 40,
  y: 40,
  width: 100,
  height: 40,
  label: 'Source',
  tools: ['button-remove'],
  attrs: {
    body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 },
  },
});

const target = graph.addNode({
  shape: 'rect',
  x: 160,
  y: 240,
  width: 100,
  height: 40,
  label: 'Target',
  tools: ['button-remove'],
  attrs: {
    body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 },
  },
});

graph.addEdge({
  source: source,
  target: target,
  vertices: [
    { x: 90, y: 160 },
    { x: 210, y: 160 },
  ],
  tools: ['vertices', 'segments'],
  attrs: {
    line: { stroke: '#8f8f8f', strokeWidth: 1 },
  },
});
```