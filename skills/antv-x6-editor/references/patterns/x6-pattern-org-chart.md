---
id: "x6-pattern-org-chart"
title: "X6 Organizational Chart"
description: |
  Best practices for building an Organizational Chart (Org Chart) using X6: tree hierarchy layout, custom employee card nodes, collapsing and expanding subtrees, etc.

library: "x6"
version: "3.x"
category: "patterns"
subcategory: "org-chart"
tags:
  - "Organizational Chart"
  - "org chart"
  - "Organizational Structure"
  - "Tree Diagram"
  - "Employee Relationships"
  - "Hierarchical Structure"

related:
  - "x6-intermediate-group"
  - "x6-intermediate-custom-node"
  - "x6-intermediate-layout"
  - "x6-core-edge"

use_cases:
  - "Company Organizational Structure Display"
  - "Team Hierarchy Relationships"
  - "Reporting Relationship Diagram"
  - "Department Structure Visualization"

difficulty: "intermediate"
completeness: "full"
---

## Scene Characteristics

The core features of an organizational structure chart:
- **Tree Structure**: Top-down hierarchical relationship
- **Custom Card Nodes**: Contains information such as name, position, and avatar
- **Vertical Edges**: Connections are typically orthogonal or smooth curves, from the bottom of the parent node to the top of the child node
- **Collapse/Expand**: Subtrees can be collapsed, improving readability when there are many nodes

## Register Card Node

```javascript
import { Graph } from '@antv/x6';

Graph.registerNode('org-card', {
  inherit: 'rect',
  width: 180,
  height: 70,
  attrs: {
    body: {
      fill: '#fff',
      stroke: '#e8e8e8',
      strokeWidth: 1,
      rx: 8,
      ry: 8,
    },
    label: {
      fontSize: 14,
      fontWeight: 'bold',
      fill: '#333',
      refY: 20,
      refX: 0.5,
    },
  },
  ports: {
    groups: {
      top: {
        position: 'top',
        attrs: { circle: { r: 0 } },  // Hide port circle
      },
      bottom: {
        position: 'bottom',
        attrs: { circle: { r: 0 } },
      },
    },
    items: [
      { id: 'top', group: 'top' },
      { id: 'bottom', group: 'bottom' },
    ],
  },
}, true);
```

## Complete Example

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 1000,
  height: 600,
  background: { color: '#F8FAFC' },
  panning: { enabled: true, modifiers: 'ctrl' },
  mousewheel: { enabled: true, modifiers: 'ctrl' },
  interacting: { nodeMovable: false },  // Organizational charts typically disable free dragging
});

// Define organizational data
const orgData = {
  id: 'ceo',
  label: 'CEO\nJohn Doe',
  children: [
    {
      id: 'cto',
      label: 'CTO\nJane Smith',
      children: [
        { id: 'fe-lead', label: 'Frontend Lead\nTom Brown' },
        { id: 'be-lead', label: 'Backend Lead\nEmily White' },
      ],
    },
    {
      id: 'cfo',
      label: 'CFO\nMichael Green',
      children: [
        { id: 'finance', label: 'Finance Manager\nSarah Lee' },
      ],
    },
    {
      id: 'coo',
      label: 'COO\nWilliam Harris',
    },
  ],
};

// Recursively create nodes and edges
function buildOrgChart(data, parentId, yOffset, xCenter) {
  const node = graph.addNode({
    id: data.id,
    x: xCenter - 90,
    y: yOffset,
    width: 180,
    height: 60,
    label: data.label,
    attrs: {
      body: { fill: '#fff', stroke: '#5B8FF9', strokeWidth: 1.5, rx: 8, ry: 8 },
      label: { fontSize: 13, fill: '#333' },
    },
  });

  if (parentId) {
    graph.addEdge({
      source: { cell: parentId },
      target: { cell: data.id },
      attrs: { line: { stroke: '#A3B1BF', strokeWidth: 1.5, targetMarker: null } },
      router: 'orth',
      connector: 'rounded',
    });
  }

  if (data.children && data.children.length > 0) {
    const childCount = data.children.length;
    const spacing = 220;
    const startX = xCenter - ((childCount - 1) * spacing) / 2;

    data.children.forEach((child, index) => {
      buildOrgChart(child, data.id, yOffset + 120, startX + index * spacing);
    });
  }
}

buildOrgChart(orgData, null, 50, 500);
```

## Using @antv/hierarchy Layout

For complex tree structures, it is recommended to use `@antv/hierarchy` for automatic layout calculations:

```javascript
import { Graph } from '@antv/x6';
import Hierarchy from '@antv/hierarchy';

const result = Hierarchy.compactBox(orgData, {
  direction: 'TB',  // Top-to-Bottom
  getWidth: () => 180,
  getHeight: () => 60,
  getHGap: () => 40,
  getVGap: () => 60,
});

// result contains the calculated x, y coordinates
function renderTree(node) {
  graph.addNode({
    id: node.id,
    x: node.x,
    y: node.y,
    width: 180,
    height: 60,
    label: node.data.label,
    attrs: { body: { fill: '#fff', stroke: '#5B8FF9', rx: 8, ry: 8 } },
  });

  if (node.children) {
    node.children.forEach((child) => {
      renderTree(child);
      graph.addEdge({
        source: node.id,
        target: child.id,
        attrs: { line: { stroke: '#A3B1BF', targetMarker: null } },
        router: 'orth',
        connector: 'rounded',
      });
    });
  }
}

renderTree(result);
```

## Collapse/Expand Subtree

```javascript
// Mark whether the node is collapsed
function toggleCollapse(nodeId) {
  const node = graph.getCellById(nodeId);
  const collapsed = node.getData()?.collapsed;

  // Get all descendant nodes and edges
  const descendants = getDescendants(nodeId);

  if (collapsed) {
    // Expand: Show descendants
    descendants.forEach((cell) => cell.show());
    node.setData({ collapsed: false });
  } else {
    // Collapse: Hide descendants
    descendants.forEach((cell) => cell.hide());
    node.setData({ collapsed: true });
  }
}

function getDescendants(nodeId) {
  const result = [];
  const edges = graph.getEdges().filter((e) => e.getSourceCellId() === nodeId);

  edges.forEach((edge) => {
    result.push(edge);
    const targetId = edge.getTargetCellId();
    const targetNode = graph.getCellById(targetId);
    if (targetNode) {
      result.push(targetNode);
      result.push(...getDescendants(targetId));
    }
  });

  return result;
}

// Double-click node to collapse/expand
graph.on('node:dblclick', ({ node }) => {
  toggleCollapse(node.id);
});
```

## Best Practices

1. **Orthogonal Routing + No Arrows**: Organizational charts typically do not require arrows. Set `targetMarker: null`.
2. **Disable Free Dragging**: Use `interacting: { nodeMovable: false }` to maintain a neat layout.
3. **Top-to-Bottom Layout**: Utilize `@antv/hierarchy` with `direction: 'TB'`.
4. **Color-Coded Hierarchy**: Use different colors to distinguish between hierarchy levels.
5. **Enable Virtual Rendering for Large Organizations**: For organizational charts with more than 100 people, configure `virtual: true`.