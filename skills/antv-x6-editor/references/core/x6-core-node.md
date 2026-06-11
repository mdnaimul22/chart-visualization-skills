---
id: "x6-core-node"
title: "X6 Node Configuration and Customization"
description: |
  Creation, built-in shapes, style configuration, and custom node registration in X6.
  Includes built-in nodes like rect/circle/polygon/html and custom extension methods.

library: "x6"
version: "3.x"
category: "core"
subcategory: "node"
tags:
  - "node"
  - "shape"
  - "rect"
  - "circle"
  - "ellipse"
  - "polygon"
  - "html"
  - "custom node"
  - "register node"
  - "register"
  - "attrs"
  - "label"
  - "diamond"

related:
  - "x6-core-graph-init"
  - "x6-core-ports"
  - "x6-core-edge"

use_cases:
  - "Add rectangle/circle/ellipse nodes"
  - "Create diamond decision nodes"
  - "Register custom shapes"
  - "Create HTML rich text nodes"
  - "Set node styles and labels"
  - "Dynamically modify node attributes"

anti_patterns:
  - "Do not use CSS property names (use SVG attributes)"
  - "Do not omit x/y coordinates"

difficulty: "beginner"
completeness: "full"
---

## Add Node

```javascript
const node = graph.addNode({
  shape: 'rect',          // Shape type
  x: 100,                 // Top-left corner X coordinate
  y: 60,                  // Top-left corner Y coordinate
  width: 120,             // Width
  height: 50,             // Height
  label: 'Hello',         // Label text (shorthand)
  attrs: {                // SVG attributes
    body: {
      fill: '#fff',
      stroke: '#8f8f8f',
      strokeWidth: 1,
      rx: 6,              // Border radius X
      ry: 6,              // Border radius Y
    },
    label: {
      text: 'Hello',     // Equivalent to outer label
      fontSize: 14,
      fill: '#333',
    },
  },
});
```

## Built-in Node Shapes

### rect (Rectangle) — Most Commonly Used

```javascript
graph.addNode({
  shape: 'rect',
  x: 40, y: 40,
  width: 100, height: 40,
  label: 'Rect Node',
  attrs: {
    body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 },
  },
});
```

### circle (Circle)

```javascript
graph.addNode({
  shape: 'circle',
  x: 200, y: 100,
  width: 60, height: 60,   // For a circle, width = height = diameter
  label: 'Start',
  attrs: {
    body: { fill: '#f6ffed', stroke: '#52c41a', strokeWidth: 2 },
  },
});
```

### ellipse (Ellipse)

```javascript
graph.addNode({
  shape: 'ellipse',
  x: 100, y: 100,
  width: 120, height: 60,
  label: 'Ellipse',
  attrs: {
    body: { fill: '#e6f7ff', stroke: '#1890ff', strokeWidth: 1 },
  },
});
```

### polygon (Polygon / Diamond)

```javascript
// Diamond (Node Judgment)
Graph.registerNode('diamond', {
  inherit: 'polygon',
  width: 80,
  height: 80,
  attrs: {
    body: {
      refPoints: '0,10 10,0 20,10 10,20',  // Diamond vertices
      fill: '#fff',
      stroke: '#8f8f8f',
      strokeWidth: 1,
    },
  },
}, true);

graph.addNode({ shape: 'diamond', x: 200, y: 100, label: 'Decision?' });
```

### text (Plain Text)

```javascript
graph.addNode({
  shape: 'text',
  x: 100, y: 100,
  attrs: {
    text: { text: 'Annotation', fontSize: 14, fill: '#666' },
  },
});
```

### image (Image Node)

```javascript
graph.addNode({
  shape: 'image',
  x: 100, y: 100,
  width: 60, height: 60,
  imageUrl: 'https://example.com/icon.png',
});
```

## HTML Custom Node

```javascript
import { Graph, Shape } from '@antv/x6';

Shape.HTML.register({
  shape: 'custom-html',
  width: 180,
  height: 80,
  effect: ['data'],      // Re-render when data changes
  html(cell) {
    const data = cell.getData() || {};
    const div = document.createElement('div');
    div.style.cssText = 'width:100%;height:100%;border:1px solid #8f8f8f;border-radius:4px;background:#fff;';
    div.innerHTML = `<div style="padding:8px;font-size:12px;">${data.title || 'Node'}</div>`;
    return div;
  },
});

graph.addNode({
  shape: 'custom-html',
  x: 100, y: 100,
  data: { title: 'My HTML Node' },
});
```

## Register Custom Node

```javascript
Graph.registerNode('my-rect', {
  inherit: 'rect',           // Inherit from built-in rect
  width: 120,                // Default width
  height: 50,                // Default height
  attrs: {
    body: { fill: '#e6f7ff', stroke: '#1890ff', strokeWidth: 2, rx: 8, ry: 8 },
    label: { fontSize: 14, fill: '#333' },
  },
  ports: {                   // Default port configuration
    groups: {
      in: { position: 'top', attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff' } } },
      out: { position: 'bottom', attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff' } } },
    },
  },
}, true);  // true indicates overriding existing registration with the same name

graph.addNode({ shape: 'my-rect', x: 100, y: 80, label: 'Custom' });
```

## Dynamically Modify Nodes

```javascript
// Modify position
node.setPosition(200, 100);

// Modify size
node.setSize(160, 60);

// Modify attributes
node.attr('body/fill', '#e6f7ff');
node.attr('label/text', 'Updated');

// Modify data
node.setData({ status: 'running' });

// Retrieve information
const { x, y } = node.getPosition();
const { width, height } = node.getSize();
const data = node.getData();
```

## Node ID

```javascript
// Specify ID
graph.addNode({ id: 'node-1', shape: 'rect', x: 40, y: 40, width: 100, height: 40 });

// Retrieve node by ID
const node = graph.getCellById('node-1');

// Automatically generate UUID if ID is not specified
const node2 = graph.addNode({ shape: 'rect', x: 200, y: 40, width: 100, height: 40 });
console.log(node2.id); // Automatically generated UUID
```

## Node Hierarchy

```javascript
// Set zIndex
graph.addNode({ shape: 'rect', x: 40, y: 40, width: 100, height: 40, zIndex: 10 });

// Dynamic Adjustment
node.toFront();   // Bring to front
node.toBack();    // Send to back
```

## Common Errors and Fixes

### Error 1: Node Dragging Range Restriction

Incorrect Example (Using Event for Manual Restriction):

```javascript
// ❌ Incorrect Approach: Using node:move event for manual restriction
graph.on('node:move', ({ node }) => {
  const boundary = { x: 100, y: 100, width: 600, height: 400 };
  const nodeBBox = node.getBBox();
  let x = nodeBBox.x;
  let y = nodeBBox.y;

  if (x < boundary.x) x = boundary.x;
  if (y < boundary.y) y = boundary.y;
  if (x + nodeBBox.width > boundary.x + boundary.width) {
    x = boundary.x + boundary.width - nodeBBox.width;
  }
  if (y + nodeBBox.height > boundary.y + boundary.height) {
    y = boundary.y + boundary.height - nodeBBox.height;
  }

  if (x !== nodeBBox.x || y !== nodeBBox.y) {
    node.position(x, y);
  }
});
```

Correct Approach (Using `translating.restrict` Configuration):

```javascript
// ✅ Correct Approach: Using graph configuration
const graph = new Graph({
  container: 'container',
  width: 600,
  height: 400,
  translating: {
    restrict: {
      x: 0,
      y: 0,
      width: 600,
      height: 400,
    },
  },
});
```

### Error 2: Handling Node Nesting Relationships

Incorrect Example (Using the `parent` Property):

```javascript
// ❌ Incorrect Approach: Setting nesting relationships via the `parent` field
graph.addNode({
  id: 'child1',
  shape: 'rect',
  label: 'Child 1',
  x: 100,
  y: 160,
  width: 80,
  height: 40,
  parent: 'innerGroup',
});
```

Correct Approach (Using the `addChild` Method):

```javascript
// ✅ Correct Approach: Establishing parent-child relationships using the `addChild` method
const outerGroup = graph.addNode({ shape: 'rect', x: 40, y: 40, width: 400, height: 240 });
const innerGroup = graph.addNode({ shape: 'rect', x: 80, y: 100, width: 200, height: 140 });
const child1 = graph.addNode({ shape: 'rect', x: 100, y: 160, width: 80, height: 40 });

outerGroup.addChild(innerGroup);
innerGroup.addChild(child1);
```

### Error 3: Edge Connection Point Configuration

Incorrect Example (Set in graph configuration but not taking effect):

```javascript
// ❌ Incorrect Approach: Incomplete connectionPoint configuration
const graph = new Graph({
  container: 'container',
  connecting: {
    connectionPoint: 'boundary', // Only sets the connection point type, missing edge creation configuration
  },
});
```

Correct Approach (Complete Configuration):

```javascript
// ✅ Correct Approach: Complete configuration of connection point and edge creation behavior
const graph = new Graph({
  container: 'container',
  connecting: {
    connectionPoint: 'boundary',
    createEdge() {
      return this.createEdge({
        attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
      });
    },
  },
});
```

### Error 4: Vertical Drag Restriction for Nodes

Incorrect Example (Using Complex Event Handling):

```javascript
// ❌ Incorrect Approach: Using complex event handling logic
graph.on('node:mousemove', ({ node }) => {
  const nodeId = node.id;
  const nodeY = node.position().y;
  const nodes = graph.getNodes();
  
  nodes.sort((a, b) => a.position().y - b.position().y);
  
  const currentIndex = nodes.findIndex(n => n.id === nodeId);
  let newIndex = currentIndex;
  
  for (let i = 0; i < nodes.length; i++) {
    if (i !== currentIndex) {
      const otherNode = nodes[i];
      const otherY = otherNode.position().y;
      if (nodeY < otherY && currentIndex > i) {
        newIndex = i;
        break;
      } else if (nodeY > otherY && currentIndex < i) {
        newIndex = i;
      }
    }
  }
  
  if (newIndex !== currentIndex) {
    nodes.splice(currentIndex, 1);
    nodes.splice(newIndex, 0, node);
    
    nodes.forEach((n, index) => {
      n.position(100, 20 + index * 60);
    });
  }
});
```

Correct Approach (Using `translating.restrict` to Limit Movement Direction):

```javascript
// ✅ Correct Approach: Using translating.restrict to allow only vertical node movement
const graph = new Graph({
  container: 'container',
  translating: {
    restrict(cellView) {
      const cell = cellView.cell;
      const bbox = cell.getBBox();
      return { x: 100, y: 0, width: 1, height: 400 };
    },
  },
});
```

### Error 5: Edge Connector Configuration Not Taking Effect

Error Example (Incorrect Edge Connector Configuration):

```javascript
// ❌ Incorrect Approach: Setting in graph configuration but not taking effect in edges
const graph = new Graph({
  container: 'container',
  connecting: {
    router: 'manhattan',
    connector: {
      name: 'smooth',
    },
  },
});
```

Correct Approach (Explicitly Specifying Connector in Edge):

```javascript
// ✅ Correct Approach: Explicitly specifying connector when adding an edge
const edge = graph.addEdge({
  source: node1,
  target: node2,
  connector: 'smooth',
  attrs: {
    line: {
      stroke: '#8f8f8f',
      strokeWidth: 1,
    }
  }
});
```

### Error 6: Node parent Property Cannot Be Properly Nested

Error Example (Using parent Property to Set Nesting Relationship):

```javascript
// ❌ Incorrect Approach: Directly Using parent Property
graph.addNode({
  id: 'child1',
  shape: 'rect',
  label: 'Child 1',
  x: 100,
  y: 160,
  width: 80,
  height: 40,
  parent: 'innerGroup',
});
```

Correct Approach (Using addChild Method):

```javascript
// ✅ Correct Approach: Using addChild Method to Establish Parent-Child Relationship
const outerGroup = graph.addNode({ shape: 'rect', x: 40, y: 40, width: 400, height: 240 });
const innerGroup = graph.addNode({ shape: 'rect', x: 80, y: 100, width: 200, height: 140 });
const child1 = graph.addNode({ shape: 'rect', x: 100, y: 160, width: 80, height: 40 });

outerGroup.addChild(innerGroup);
innerGroup.addChild(child1);
```

### Error 7: Inaccurate Node Dragging Range Restriction

Error Example (Using Complex Event Handling):

```javascript
// ❌ Incorrect Approach: Using complex event handling logic
graph.on('node:mousemove', ({ node }) => {
  const position = node.position();
  const size = node.size();
  
  let newX = position.x;
  let newY = position.y;
  
  if (position.x < 0) newX = 0;
  if (position.y < 0) newY = 0;
  if (position.x + size.width > 600) newX = 600 - size.width;
  if (position.y + size.height > 400) newY = 400 - size.height;
  
  if (newX !== position.x || newY !== position.y) {
    node.position(newX, newY);
  }
});
```

Correct Approach (Using `translating.restrict` Configuration):

```javascript
// ✅ Correct Approach: Using translating.restrict configuration
const graph = new Graph({
  container: 'container',
  translating: {
    restrict: {
      x: 0,
      y: 0,
      width: 600,
      height: 400,
    },
  },
});
```

### Error 8: Incorrect Configuration When Using `smooth` Connector for Edges

Error Example (Incorrect Edge Connector Configuration):

```javascript
// ❌ Incorrect Approach: Setting in graph configuration but not effective in edges
const graph = new Graph({
  container: 'container',
  connecting: {
    router: 'manhattan',
    connector: {
      name: 'smooth',
    },
  },
});
```

Correct Approach (Explicitly Specifying Connector in Edges):

```javascript
// ✅ Correct Approach: Explicitly specify connector when adding an edge
const edge = graph.addEdge({
  source: node1,
  target: node2,
  connector: 'smooth',
  attrs: {
    line: {
      stroke: '#8f8f8f',
      strokeWidth: 1,
    }
  }
});
```

### Error 9: Using graph.render() Causes an Error

Error Example (Calling graph.render() Method):

```javascript
// ❌ Incorrect Approach: Calling graph.render()
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

graph.render(); // Error: graph.render is not a function
```

Correct Approach (No Need to Call graph.render()):

```javascript
// ✅ Correct Approach: No need to call graph.render()
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});
```

### Error 10: Declaring `const container` in Code

The `container` variable is automatically injected by the runtime environment and **must not** be redeclared in the code, otherwise it will throw the error `Identifier 'container' has already been declared`.

```javascript
// ❌ Incorrect: Redeclaring the container variable
const container = document.getElementById('container');
const graph = new Graph({ container });

// ✅ Correct: Directly use the string 'container'
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});
```

### Error 11: Using Unregistered Custom Edge Shape

**⚠️ Key Constraint: Prohibit the use of custom edge shape names that have not been registered via `Graph.registerEdge()`.**

X6 provides only two built-in edge shapes: `'edge'` and `'double-edge'`. If you need to customize edge styles, **do not invent new shape names**. Instead, configure the styles within the `attrs` property:

```javascript
// ❌ Error: Using an unregistered shape name → Throws "Edge with name 'xxx' does not exist"
graph.addEdge({
  shape: 'my-custom-edge',  // Unregistered, will throw an error!
  source: 'node1',
  target: 'node2',
});

// ✅ Correct Approach 1: Use built-in 'edge' shape + custom attrs
graph.addEdge({
  shape: 'edge',
  source: 'node1',
  target: 'node2',
  attrs: {
    line: {
      stroke: '#1890ff',
      strokeWidth: 3,
      strokeDasharray: '5 5',
      targetMarker: 'classic',
    },
  },
});

// ✅ Correct Approach 2: Register before use
Graph.registerEdge(
  'my-custom-edge',
  {
    inherit: 'edge',
    attrs: {
      line: { stroke: '#1890ff', strokeWidth: 3, targetMarker: 'classic' },
    },
  },
  true,
);
// Use after registration
graph.addEdge({ shape: 'my-custom-edge', source: 'node1', target: 'node2' });
```

**Available built-in edge shapes:** `'edge'`, `'double-edge'`. All other shape names must be registered first using `Graph.registerEdge()`.

### Error 12: Incorrect Node Data Format

Error Example (Incorrect Node Data Format):

```javascript
// ❌ Incorrect Approach: Incorrect Node Data Format
const data = [
  { shape: 'rect', x: 100, y: 20, width: 200, height: 44, label: 'Item 1' },
  { shape: 'rect', x: 10  shape: 'rect', x: 100, y: 140, width: 200, height: 44, label: 'Item 4' },
  { shape: 'rect', x: 100, y: 184, width: 200, height: 44, label: 'Item 5' },
];
```

Correct Approach (Correct Node Data Format):

```javascript
// ✅ Correct Approach: Correct Node Data Format
const data = [
  { shape: 'rect', x: 100, y: 20, width: 200, height: 44, label: 'Item 1' },
  { shape: 'rect', x: 100, y: 80, width: 200, height: 44, label: 'Item 2' },
  { shape: 'rect', x: 100, y: 140, width: 200, height: 44, label: 'Item 3' },
  { shape: 'rect', x: 100, y: 200, width: 200, height: 44, label: 'Item 4' },
  { shape: 'rect', x: 100, y: 260, width: 200, height: 44, label: 'Item 5' },
];
```

### Error 13: Using Non-existent `graph.highlightNode()` / `graph.highlightCell()` Methods

**⚠️ X6 does not have `graph.highlightNode()` and `graph.highlightCell()` methods.**

```javascript
// ❌ Error: These methods do not exist
graph.highlightNode(node);   // TypeError
graph.highlightCell(cell);   // TypeError

// ✅ Correct Approach 1: Highlight by modifying styles using `node.attr()`
const neighbors = graph.getNeighbors(centerNode);
neighbors.forEach((node) => {
  node.attr('body/fill', '#d9f7be');
  node.attr('body/stroke', '#52c41a');
  node.attr('body/strokeWidth', 2);
});

// ✅ Correct Approach 2: Highlight using CSS classes (requires stylesheet)
neighbors.forEach((node) => {
  const view = graph.findViewByCell(node);
  if (view) view.addClass('highlighted');
});
```

### Error 14: SVG Gradient Definition Syntax Error

**⚠️ X6 does not have a `graph.defs` property. Do not use `document.createElementNS` to manually create SVG gradient elements.**

```javascript
// ❌ Error: graph.defs does not exist, and `graph.svg defs()` is a syntax error
const gradientId = 'gradient-blue-green';
const defs = graph.defs;  // undefined
// or
const svgDefs = document.createElementNS('http://www.w3.org/2000/svg', 'defs'); // Do not do this
```

Correct Approach (Using attrs.fill to Configure Gradient):

```javascript
// ✅ Correct Approach: Using attrs.fill to Configure Gradient
graph.addNode({
  shape: 'rect',
  x: 100,
  y: 60,
  width: 160,
  height: 80,
  label: 'Gradient Node',
  attrs: {
    body: {
      fill: {
        type: 'linearGradient',
        stops: [
          { offset: '0%', color: '#1890ff' },
          { offset: '100%', color: '#52c41a' },
        ],
      },
      stroke: '#8f8f8f',
      strokeWidth: 1,
      rx: 6,
      ry: 6,
    },
    label: {
      fill: '#fff',
      fontSize: 14,
    },
  },
});
```