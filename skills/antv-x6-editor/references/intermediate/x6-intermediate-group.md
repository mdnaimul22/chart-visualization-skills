---
id: "x6-intermediate-group"
title: "X6 Grouping and Nesting"
description: |
  Configuration guide for parent-child relationships (Group) of X6 nodes.
  Includes combined nodes, interactive embedding, child node movement restrictions, automatic expansion of parent nodes, and expand/collapse functionality.

library: "x6"
version: "3.x"
category: "intermediate"
subcategory: "group"
tags:
  - "group"
  - "grouping"
  - "nesting"
  - "parent"
  - "children"
  - "embedding"
  - "combination"
  - "collapse"
  - "expand"
  - "grouping"
  - "restrict"
  - "translating"

related:
  - "x6-core-node"
  - "x6-core-graph-init"
  - "x6-core-events"

use_cases:
  - "Combine multiple nodes into a single group"
  - "Drag and drop nodes to embed them within another node, forming a parent-child relationship"
  - "Restrict child nodes to move only within the parent node"
  - "Automatically expand parent nodes to enclose child nodes"
  - "Implement expand and collapse functionality for parent nodes"

anti_patterns:
  - "Do not manually set parent/children fields; use API operations instead"
  - "Do not forget to enable the embedding option for interactive embedding"
---

# X6 Grouping and Nesting

## Basic Concepts

X6 implements grouping functionality through parent-child relationships. When a parent node moves, its child nodes follow, and the path points of edges also move along with the common parent node.

## Combining Nodes via API

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

// Create parent node
const parent = graph.addNode({
  shape: 'rect',
  x: 40,
  y: 40,
  width: 360,
  height: 200,
  label: 'Parent',
  attrs: {
    body: { fill: '#f5f5f5', stroke: '#d9d9d9', strokeWidth: 1 },
  },
  zIndex: 1,
});

// Create child nodes
const child1 = graph.addNode({
  shape: 'rect',
  x: 80,
  y: 80,
  width: 100,
  height: 40,
  label: 'Child 1',
  attrs: {
    body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 },
  },
  zIndex: 2,
});

const child2 = graph.addNode({
  shape: 'rect',
  x: 240,
  y: 140,
  width: 100,
  height: 40,
  label: 'Child 2',
  attrs: {
    body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 },
  },
  zIndex: 2,
});

// Establish parent-child relationships
parent.addChild(child1);
parent.addChild(child2);
```

## Parent-Child Relationship API

```javascript
// Add child node
parent.addChild(childNode);

// Get child nodes
const children = parent.getChildren(); // Cell[] | null

// Get parent node
const parentNode = child.getParent(); // Cell | null

// Determine relationship
parent.isParentOf(child);  // true
child.isChildOf(parent);   // true

// Get all descendant nodes (recursive)
const descendants = parent.getDescendants();

// Remove child node (does not delete the node itself)
parent.removeChild(child);

// Embed edge (set edge as child node)
parent.addChild(edge);
```

## Interactive Embedding (Embedding)

Embed a node into another node as a child node by dragging:

```javascript
const graph = new Graph({
  container: 'container',
  embedding: {
    enabled: true,
    // Method to find the parent node: Traverse the nodes on the canvas while dragging the node, and return the node as the target parent node
    findParent({ node }) {
      const bbox = node.getBBox();
      return this.getNodes().filter((candidate) => {
        const targetBBox = candidate.getBBox();
        return bbox.isIntersectWithRect(targetBBox);
      });
    },
  },
});
```

### embedding Configuration Options

| Configuration Item | Type | Description |
|--------------------|------|-------------|
| `enabled` | boolean | Whether to enable embedding |
| `findParent` | Function | Method to find parent nodes, returns an array of nodes |
| `validate` | Function | Validates whether embedding is allowed |

## Restrict Child Node Movement Range

Restrict the movement of child nodes within the parent node:

```javascript
const graph = new Graph({
  container: 'container',
  translating: {
    restrict(cellView) {
      const cell = cellView.cell;
      const parentNode = cell.getParent();
      if (parentNode) {
        return parentNode.getBBox();
      }
      return undefined; // No restriction
    },
  },
});
```

## Auto-Expand Parent Node

Listen for child node movement events and automatically expand the parent node to always enclose the child nodes:

```javascript
graph.on('node:change:position', ({ node, options }) => {
  if (options.skipParentHandler) return;

  const parentNode = node.getParent();
  if (parentNode) {
    let originSize = parentNode.prop('originSize');
    let originPosition = parentNode.prop('originPosition');
    if (!originSize || !originPosition) {
      originSize = parentNode.getSize();
      originPosition = parentNode.getPosition();
      parentNode.prop('originSize', originSize);
      parentNode.prop('originPosition', originPosition);
    }

    const children = parentNode.getChildren();
    if (children && children.length) {
      // Calculate the bounding box of all child nodes
      let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
      children.filter(child => child.isNode()).forEach((child) => {
        const bbox = child.getBBox();
        minX = Math.min(minX, bbox.x);
        minY = Math.min(minY, bbox.y);
        maxX = Math.max(maxX, bbox.x + bbox.width);
        maxY = Math.max(maxY, bbox.y + bbox.height);
      });

      const padding = 20;
      parentNode.prop(
        {
          position: { x: minX - padding, y: minY - padding },
          size: { width: maxX - minX + 2 * padding, height: maxY - minY + 2 * padding },
        },
        { skipParentHandler: true },
      );
    }
  }
});
```

## Expand and Collapse Parent Nodes

Implement collapsible groups through custom nodes:

```javascript
import { Graph } from '@antv/x6';

// Register collapsible group node
Graph.registerNode(
  'collapsible-group',
  {
    inherit: 'rect',
    width: 200,
    height: 120,
    attrs: {
      body: { fill: '#f5f5f5', stroke: '#d9d9d9', strokeWidth: 1 },
      label: { refX: 10, refY: 10, textAnchor: 'start', textVerticalAnchor: 'top', fontSize: 14 },
    },
  },
  true,
);

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

const group = graph.addNode({
  shape: 'collapsible-group',
  x: 40,
  y: 40,
  label: 'Group',
});

const child = graph.addNode({
  shape: 'rect',
  x: 60,
  y: 80,
  width: 100,
  height: 40,
  label: 'Child',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 } },
});

group.addChild(child);

// Toggle collapse state
function toggleCollapse(groupNode, collapsed) {
  const children = groupNode.getDescendants();
  children.forEach((cell) => {
    if (collapsed) {
      cell.hide();
    } else {
      cell.show();
    }
  });
  // Adjust parent node size
  if (collapsed) {
    groupNode.prop('expandedSize', groupNode.getSize());
    groupNode.resize(200, 40);
  } else {
    const size = groupNode.prop('expandedSize');
    if (size) {
      groupNode.resize(size.width, size.height);
    }
  }
}

// Double-click to toggle collapse
graph.on('node:dblclick', ({ node }) => {
  if (node === group) {
    const isCollapsed = node.prop('collapsed') || false;
    node.prop('collapsed', !isCollapsed);
    toggleCollapse(node, !isCollapsed);
  }
});
```

## Collapsible Group Node with Button

Below is a more complete example demonstrating how to create a group node with a collapsible button:

```javascript
import { Graph } from '@antv/x6';

// Register collapsible group node
Graph.registerNode(
  'collapsable-group',
  {
    inherit: 'rect',
    markup: [
      { tagName: 'rect', selector: 'body' },
      { tagName: 'text', selector: 'label' },
      {
        tagName: 'g',
        selector: 'buttonGroup',
        children: [
          { tagName: 'rect', selector: 'button', attrs: { width: 16, height: 16, rx: 2, ry: 2 } },
          { tagName: 'text', selector: 'buttonSign', attrs: { x: 8, y: 12, textAnchor: 'middle', fontSize: 12 } },
        ],
      },
    ],
    attrs: {
      body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#e6f7ff', rx: 6, ry: 6 },
      label: { refY: 14, textAnchor: 'middle', textVerticalAnchor: 'top', fontSize: 13 },
      button: { fill: '#fff', stroke: '#8f8f8f', cursor: 'pointer', refX: 8, refY: 8 },
      buttonSign: { fill: '#333', cursor: 'pointer' },
    },
  },
  true,
);

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
});

const group = graph.addNode({
  shape: 'collapsable-group',
  x: 60,
  y: 40,
  width: 300,
  height: 200,
  label: 'Group (Click to collapse)',
  attrs: {
    buttonSign: { text: '-' },
  },
});

const child1 = graph.addNode({
  shape: 'rect',
  x: 100,
  y: 100,
  width: 80,
  height: 40,
  label: 'Task A',
  attrs: {
    body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 },
  },
});

const child2 = graph.addNode({
  shape: 'rect',
  x: 240,
  y: 100,
  width: 80,
  height: 40,
  label: 'Task B',
  attrs: {
    body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 },
  },
});

group.addChild(child1);
group.addChild(child2);

graph.addEdge({
  source: child1,
  target: child2,
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1 } },
});

let collapsed = false;
graph.on('node:click', ({ node }) => {
  if (node === group) {
    collapsed = !collapsed;
    const children = group.getChildren();
    if (children) {
      children.forEach((child) => {
        collapsed ? child.hide() : child.show();
      });
    }
    node.attr('buttonSign/text', collapsed ? '+' : '-');
    if (collapsed) {
      node.resize(300, 50);
    } else {
      node.resize(300, 200);
    }
  }
});
```

## Common Errors and Fixes

### ❌ Attempting to Drag and Embed Without Enabling Embedding

```javascript
// Error: Embedding is not configured, dragging will not trigger embedding
const graph = new Graph({ container: 'container' });

// Correct: Embedding must be enabled
const graph = new Graph({
  container: 'container',
  embedding: { enabled: true },
});
```

### ❌ Manually Setting parent/children Fields

```javascript
// Incorrect: Directly manipulating internal fields
node.prop('parent', parentId);

// Correct: Using API
parentNode.addChild(childNode);
```

### ❌ Incorrect Usage of Shape.Group.define or Non-existent API

```javascript
// Incorrect: Using a non-existent API
Shape.Group.define('collapsable-group', { ... });

// Correct: Using Graph.registerNode to register a custom node
Graph.registerNode('collapsable-group', { ... }, true);
```

### ❌ Incorrect Collapse Logic, Failing to Update Button State and Size

```javascript
// Error: Fails to correctly update button text and node size
graph.on('node:click', ({ node }) => {
  if (node.shape === 'collapsable-group') {
    const collapsed = !node.prop('collapsed');
    node.prop('collapsed', collapsed);
    
    if (collapsed) {
      node.getChildren().forEach((child) => child.hide());
    } else {
      node.getChildren().forEach((child) => child.show());
    }
  }
});

// Correct: Fully handles collapse state, button text, and node size
let collapsed = false;
graph.on('node:click', ({ node }) => {
  if (node === group) {
    collapsed = !collapsed;
    const children = group.getChildren();
    if (children) {
      children.forEach((child) => {
        collapsed ? child.hide() : child.show();
      });
    }
    node.attr('buttonSign/text', collapsed ? '+' : '-');
    if (collapsed) {
      node.resize(300, 50);
    } else {
      node.resize(300, 200);
    }
  }
});
```

</skill>