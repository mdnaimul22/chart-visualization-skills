---
id: "x6-plugin-dnd"
title: "X6 Dnd Drag and Drop Plugin"
description: |
  The Dnd (Drag and Drop) plugin provides the ability to drag nodes from external sources onto the canvas.
  It is used to implement interactions for dragging and creating new nodes from a toolbox/panel, supporting drag preview, alignment snapping, and placement validation.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "dnd"
tags:
  - "dnd"
  - "drag"
  - "drop"
  - "drag-and-drop"
  - "getDragNode"
  - "getDropNode"
  - "validateNode"

related:
  - "x6-plugins"
  - "x6-plugin-stencil"
  - "x6-core-graph-init"

use_cases:
  - "Drag nodes from an external panel onto the canvas"
  - "Customize the style of the drag preview node"
  - "Validate nodes during drag and drop placement"
  - "Simple drag-to-create without using Stencil"

difficulty: "intermediate"
completeness: "full"
---

## Core Concepts

The **Dnd** plugin enables dragging nodes from external DOM elements into the canvas. The difference between Dnd and Stencil is:
- **Stencil**: Encapsulates a complete sidebar panel UI (grouping, search, layout) and internally uses Dnd.
- **Dnd**: Provides low-level drag-and-drop capabilities without UI, requiring custom implementation of the drag trigger interface.

Typical use case for Dnd: Customizing toolbar buttons to add nodes to the canvas upon click or drag.

## Basic Usage

```javascript
import { Graph, Dnd } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

// Create a Dnd instance
const dnd = new Dnd({
  target: graph,
  getDragNode(sourceNode, options) {
    return sourceNode.clone();
  },
  getDropNode(draggingNode, options) {
    return draggingNode.clone();
  },
});

// Trigger drag on an external DOM element
document.getElementById('btn-rect').addEventListener('mousedown', (e) => {
  const node = graph.createNode({
    shape: 'rect',
    width: 100,
    height: 40,
    label: 'New Node',
    attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
  });
  dnd.start(node, e);
});
```

## Configuration Options

### DndOptions

| Parameter | Type | Required | Default Value | Description |
|------|------|------|--------|------|
| `target` | `Graph` | ✓ | - | Target canvas instance |
| `scaled` | `boolean` | | `false` | Whether the dragged node follows canvas scaling |
| `delegateGraphOptions` | `Options` | | - | Additional configuration for the drag proxy canvas |
| `draggingContainer` | `HTMLElement` | | `document.body` | Container element for the node during dragging |
| `dndContainer` | `HTMLElement` | | - | Dnd toolbox container |
| `getDragNode` | `Function` | | Clone source node | Node displayed during dragging |
| `getDropNode` | `Function` | | Clone dragged node | Final node placed on the canvas |
| `validateNode` | `Function` | | - | Validate whether dropping is allowed |

### getDragNode

```typescript
getDragNode(sourceNode: Node, options: {
  sourceNode: Node;
  targetGraph: Graph;
  draggingGraph: Graph;
}) => Node
```

Customizes the node displayed during the drag process. Defaults to `sourceNode.clone()`.

### getDropNode

```typescript
getDropNode(draggingNode: Node, options: {
  sourceNode: Node;
  targetGraph: Graph;
  draggingGraph: Graph;
  draggingNode: Node;
}) => Node
```

Customizes the node that is actually dropped onto the canvas. Defaults to `draggingNode.clone()`.

### validateNode

```typescript
validateNode(droppingNode: Node, options: {
  sourceNode: Node;
  targetGraph: Graph;
  draggingGraph: Graph;
  draggingNode: Node;
  droppingNode: Node;
}) => boolean | Promise<boolean>
```

Validates whether a node is allowed to be dropped onto the canvas. Returns `false` or rejects to cancel the drop. Supports asynchronous validation.

## API Methods

| Method | Description |
|--------|-------------|
| `dnd.start(node, mouseEvent)` | Start dragging. Pass in the source node and mouse event |

## Complete Example

### Custom Toolbar Drag-and-Drop

```javascript
import { Graph, Dnd, Snapline } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  grid: { visible: true, size: 10 },
});

graph.use(new Snapline({ enabled: true }));

const dnd = new Dnd({
  target: graph,
  scaled: true,  // Drag preview follows canvas scaling

  getDragNode(sourceNode) {
    // Display a simplified version during drag
    const node = sourceNode.clone();
    node.setAttrs({ body: { opacity: 0.6 } });
    return node;
  },

  getDropNode(draggingNode) {
    // Restore normal style when dropped onto the canvas
    const node = draggingNode.clone();
    node.setAttrs({ body: { opacity: 1 } });
    return node;
  },

  validateNode(droppingNode) {
    // Validation: No more than 5 nodes of the same shape on the canvas
    const shape = droppingNode.shape;
    const count = graph.getNodes().filter((n) => n.shape === shape).length;
    return count < 5;
  },
});

// Toolbar button binding
const shapes = [
  { id: 'btn-rect', shape: 'rect', width: 100, height: 40, label: 'Rectangle' },
  { id: 'btn-circle', shape: 'circle', width: 60, height: 60, label: 'Circle' },
];

shapes.forEach(({ id, ...nodeProps }) => {
  document.getElementById(id)?.addEventListener('mousedown', (e) => {
    const node = graph.createNode({
      ...nodeProps,
      attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 4, ry: 4 } },
    });
    dnd.start(node, e);
  });
});
```

### Asynchronous Validation Placement

```javascript
const dnd = new Dnd({
  target: graph,
  async validateNode(droppingNode) {
    // Asynchronous validation, such as calling a backend API
    const isValid = await checkNodePlacement(droppingNode.getData());
    return isValid;
  },
});
```

## Dnd vs. Stencil Selection

| Scenario | Recommendation |
|----------|---------------|
| Requires a complete sidebar panel UI | Stencil |
| Only needs a simple drag button | Dnd |
| Requires search and grouping functionality | Stencil |
| Fully custom drag interaction UI | Dnd |
| Needs to initiate drag from non-node template DOM elements | Dnd |

## Common Errors and Fixes

### ❌ Calling start in the click event

```javascript
// Error: Must use mousedown event, click event is triggered after the mouse is released, making dragging impossible
element.addEventListener('click', (e) => {
  dnd.start(node, e); // ❌ Dragging cannot be triggered
});

// Correct: Use mousedown
element.addEventListener('mousedown', (e) => {
  dnd.start(node, e); // ✅
});
```

### ❌ Forgot to Set Target

```javascript
// Error: Missing target will result in inability to place on the canvas
const dnd = new Dnd({
  getDragNode: (node) => node.clone(),
}); // ❌

// Correct
const dnd = new Dnd({
  target: graph, // ✅
});
```

### ❌ Container Not Properly Mounted Causes `appendChild` Error

When using Stencil or manually creating a container, ensure the target container exists and is correctly mounted in the DOM.

```javascript
// Error: If document.getElementById('stencil') returns null, an error will occur
const stencil = new Stencil({...});
document.getElementById('stencil').appendChild(stencil.container); // ❌ Error: Cannot read properties of null

// Correct: First create the container element and mount it to the DOM
const stencilContainer = document.createElement('div');
stencilContainer.id = 'stencil';
document.body.appendChild(stencilContainer);

const stencil = new Stencil({...});
document.getElementById('stencil').appendChild(stencil.container); // ✅
```

### ❌ Using a Non-existent Shape Name

```javascript
// Error: 'cylinder' is not a built-in shape, will throw an error: Node with name 'cylinder' does not exist.
const cylinder = graph.createNode({
  shape: 'cylinder', // ❌
  width: 80,
  height: 60,
});

// Correct: Use a built-in shape name, such as 'rect', 'circle', 'ellipse', 'polygon', etc.
const rect = graph.createNode({
  shape: 'rect',
  width: 100,
  height: 40,
  label: 'Rectangle',
});
```

### ❌ Incorrect Use of Shape Constructor

```javascript
// Error: Shape.Cylinder is not a constructor, which will result in an error
const cylinder = new Shape.Cylinder({ ... }); // ❌

// Correct: Use graph.createNode to create a node
const cylinder = graph.createNode({
  shape: 'rect',
  width: 80,
  height: 60,
  label: 'Cylinder',
});
```

### ✅ Recommended Container Creation Method

```javascript
// Create and mount Stencil container
const stencilContainer = document.createElement('div');
stencilContainer.style.width = '200px';
stencilContainer.style.position = 'absolute';
stencilContainer.style.left = '0';
stencilContainer.style.top = '0';
stencilContainer.style.bottom = '0';
document.getElementById('container').parentElement.prepend(stencilContainer);

// Initialize Stencil and mount
const stencil = new Stencil({
  title: 'Shapes',
  target: graph,
  groups: [{ name: 'basic', title: 'Basic Shapes' }],
});

stencilContainer.appendChild(stencil.container);
```

### ✅ Correctly Using Built-in Shapes to Create Nodes

```javascript
import { Graph, Stencil } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

const stencil = new Stencil({
  title: 'Shapes',
  target: graph,
  groups: [
    { name: 'basic', title: 'Basic Shapes' },
  ],
});

const stencilContainer = document.createElement('div');
document.getElementById('container').parentElement.prepend(stencilContainer);
stencilContainer.appendChild(stencil.container);

// Use graph.createNode to create nodes
const rect = graph.createNode({
  shape: 'rect',
  width: 100,
  height: 40,
  label: 'Rectangle',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f' } },
});

const circle = graph.createNode({
  shape: 'circle',
  width: 60,
  height: 60,
  label: 'Circle',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f' } },
});

stencil.load([rect, circle], 'basic');
```

</skill>