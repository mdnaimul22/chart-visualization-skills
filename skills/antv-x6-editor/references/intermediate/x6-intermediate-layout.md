---
id: "x6-intermediate-layout"
title: "X6 Layout"
description: |
  A comprehensive guide to graph layout in X6 using @antv/layout and @antv/hierarchy.
  Includes Dagre (Directed Graph), Grid, Circle, Force-Directed, Tree, and Mind Map layouts.

library: "x6"
version: "3.x"
category: "intermediate"
subcategory: "layout"
tags:
  - "layout"
  - "dagre"
  - "grid"
  - "circle"
  - "force"
  - "tree"
  - "mindmap"
  - "hierarchy"
  - "@antv/layout"
  - "@antv/hierarchy"
  - "rankdir"
  - "auto-arrange"

related:
  - "x6-core-graph-init"
  - "x6-core-node"
  - "x6-core-edge"
  - "x6-pattern-dag"

use_cases:
  - "Automatic hierarchical layout for DAG nodes"
  - "Arrange nodes in a grid"
  - "Arrange nodes in a circular pattern"
  - "Automatic layout using force-directed algorithm"
  - "Automatic tree hierarchy layout"
  - "Mind map layout"

anti_patterns:
  - "Layout algorithms do not automatically add nodes to the canvas; manually call graph.fromJSON()"
  - "Do not confuse @antv/layout with X6's built-in port-layout"
---

# X6 Layout

X6 itself does not have built-in graph layout algorithms. Instead, it calculates node positions using `@antv/layout` (general layout) and `@antv/hierarchy` (hierarchical layout), and then renders the graph using `graph.fromJSON()`.

## Install Dependencies

```bash

# General Layouts (dagre, grid, circle, force, etc.)
npm install @antv/layout dagre

# Tree Layout (Mind Map, Compact Tree, etc.)
npm install @antv/hierarchy
```

## Dagre Layout (Directed Graph/DAG)

The most commonly used hierarchical layout, suitable for flowcharts, DAG data pipelines.

```javascript
import { Graph } from '@antv/x6';
import { DagreLayout } from '@antv/layout';

// Prepare data
const data = {
  nodes: [
    { id: '1', shape: 'rect', width: 100, height: 40, label: 'Start', attrs: { body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 } } },
    { id: '2', shape: 'rect', width: 100, height: 40, label: 'Process', attrs: { body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 } } },
    { id: '3', shape: 'rect', width: 100, height: 40, label: 'End', attrs: { body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 } } },
  ],
  edges: [
    { source: '1', target: '2', attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } } },
    { source: '2', target: '3', attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } } },
  ],
};

// Execute layout calculation
const dagreLayout = new DagreLayout({
  type: 'dagre',
  rankdir: 'TB',    // Layout direction: TB (top to bottom) | BT | LR (left to right) | RL
  align: 'UL',     // Alignment: UL | UR | DL | DR
  ranksep: 50,     // Layer spacing
  nodesep: 30,     // Node spacing within the same layer
});

const model = dagreLayout.layout(data);

// Render to canvas
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
});

graph.fromJSON(model);
graph.centerContent();
```

### Dagre Configuration Options

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `rankdir` | string | `'TB'` | Layout direction: `'TB'`/`'BT'`/`'LR'`/`'RL'` |
| `align` | string | `'UL'` | Node alignment: `'UL'`/`'UR'`/`'DL'`/`'DR'` |
| `nodesep` | number | 50 | Spacing between nodes in the same rank |
| `ranksep` | number | 50 | Spacing between ranks |
| `controlPoints` | boolean | false | Whether to retain control points for edges |

## Grid Layout

Arrange nodes in a grid.

```javascript
import { Graph } from '@antv/x6';
import { GridLayout } from '@antv/layout';

const data = {
  nodes: Array.from({ length: 12 }, (_, i) => ({
    id: `${i + 1}`,
    shape: 'circle',
    width: 32,
    height: 32,
    label: `${i + 1}`,
    attrs: { body: { fill: '#5F95FF', stroke: 'transparent' }, label: { fill: '#fff' } },
  })),
  edges: [],
};

const gridLayout = new GridLayout({
  type: 'grid',
  width: 600,
  height: 400,
  rows: 3,
  cols: 4,
});

const model = gridLayout.layout(data);

const graph = new Graph({ container: 'container' });
graph.fromJSON(model);
```

## Circular Layout

Arranges nodes in a circular pattern.

```javascript
import { Graph } from '@antv/x6';
import { CircularLayout } from '@antv/layout';

const circularLayout = new CircularLayout({
  type: 'circular',
  width: 600,
  height: 600,
  radius: 200,
});

const model = circularLayout.layout(data);

const graph = new Graph({ container: 'container' });
graph.fromJSON(model);
```

## Force Layout (Force-Directed)

Force-directed layout based on physical simulation.

```javascript
import { Graph } from '@antv/x6';
import { ForceLayout } from '@antv/layout';

const forceLayout = new ForceLayout({
  type: 'force',
  width: 800,
  height: 600,
  preventOverlap: true,
  nodeStrength: -50,
  edgeStrength: 0.1,
});

const model = forceLayout.layout(data);

const graph = new Graph({ container: 'container' });
graph.fromJSON(model);
```

## Tree Layout (@antv/hierarchy)

Suitable for hierarchical data, such as organizational charts and mind maps.

### Mind Map Layout

```javascript
import { Graph } from '@antv/x6';
import Hierarchy from '@antv/hierarchy';

// Tree data structure
const treeData = {
  id: 'root',
  label: 'Central Theme',
  children: [
    {
      id: 'c1',
      label: 'Branch 1',
      children: [
        { id: 'c1-1', label: 'Subtopic 1-1' },
        { id: 'c1-2', label: 'Subtopic 1-2' },
      ],
    },
    {
      id: 'c2',
      label: 'Branch 2',
      children: [
        { id: 'c2-1', label: 'Subtopic 2-1' },
      ],
    },
  ],
};

// Calculate layout
const result = Hierarchy.mindmap(treeData, {
  direction: 'H',      // H (Horizontal) | V (Vertical)
  getHeight() { return 30; },
  getWidth() { return 100; },
  getHGap() { return 60; },
  getVGap() { return 20; },
  getSide() { return 'right'; },
});

// Traverse layout result and convert to X6 data format
const model = { nodes: [], edges: [] };

function traverse(node) {
  model.nodes.push({
    id: node.id,
    x: node.x + 400,  // Offset to canvas center
    y: node.y + 300,
    shape: 'rect',
    width: 100,
    height: 30,
    label: node.data.label || node.id,
    attrs: { body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 4, ry: 4 } },
  });
  if (node.children) {
    node.children.forEach((child) => {
      model.edges.push({
        source: node.id,
        target: child.id,
        connector: 'smooth',
        attrs: { line: { stroke: '#A2B1C3', strokeWidth: 1, targetMarker: null } },
      });
      traverse(child);
    });
  }
}

traverse(result);

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  connecting: { connector: 'smooth' },
});

graph.fromJSON(model);
graph.centerContent();
```

### Compact Tree Layout

```javascript
import Hierarchy from '@antv/hierarchy';

const result = Hierarchy.compactBox(treeData, {
  direction: 'TB',     // TB | BT | LR | RL | H | V
  getHeight() { return 30; },
  getWidth() { return 100; },
  getHGap() { return 40; },
  getVGap() { return 20; },
});
```

## @antv/hierarchy Layout Algorithm List

| Algorithm | Method | Applicable Scenarios |
|------|------|----------|
| Compact Tree | `Hierarchy.compactBox(data, options)` | Organizational Chart, File Tree |
| Mind Map | `Hierarchy.mindmap(data, options)` | Mind Map |
| Indented Tree | `Hierarchy.indented(data, options)` | Directory Structure |
| Dendrogram | `Hierarchy.dendrogram(data, options)` | Phylogenetic Tree |

## Dynamic Layout (Re-layout After Data Changes)

```javascript
// Re-layout after adding new nodes
function relayout() {
  const currentData = graph.toJSON();
  const newModel = dagreLayout.layout(currentData);
  graph.fromJSON(newModel);
  graph.centerContent();
}
```

## Common Errors

### ❌ Using data directly after layout without calling fromJSON

```javascript
// Error: Layout only calculates positions and does not automatically render
const model = dagreLayout.layout(data);
// Nothing is displayed on the canvas

// Correct: Manual rendering is required
const model = dagreLayout.layout(data);
graph.fromJSON(model);
```

### ❌ DagreLayout Error Due to Missing dagre Dependency

```bash

# Error: DagreLayout in @antv/layout depends on the dagre package

# Error: Cannot find module 'dagre'

# Correct: Need to install both
npm install @antv/layout dagre
```