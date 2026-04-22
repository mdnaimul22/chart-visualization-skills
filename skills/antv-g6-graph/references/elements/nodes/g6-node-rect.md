---
id: "g6-node-rect"
title: "G6 Rectangle Node (Rect Node)"
description: |
  Create graph visualizations using rectangle nodes (rect). Rectangle nodes are suitable for displaying modules, components, process steps, etc.,
  and support setting aspect ratios, rounded corners, labels, and more.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "nodes"
tags:
  - "node"
  - "rectangle"
  - "rect"
  - "flowchart"
  - "organizational chart"
  - "UML"

related:
  - "g6-node-circle"
  - "g6-layout-dagre"
  - "g6-state-overview"

use_cases:
  - "Flowchart nodes"
  - "Organizational charts"
  - "UML diagrams"
  - "File trees"
  - "Architecture diagrams"

anti_patterns:
  - "Not suitable for representing undirected entities (use circle instead)"
  - "Use HTML nodes instead when node content is extremely complex"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/element/node/rect"
---

## Core Concepts

Rectangular nodes (`rect`) have clear boundaries, making them suitable for representing entities that require directional distinction, such as modules, components, and process steps.

**Main differences from circle:**
- `size` accepts a `[width, height]` array, supporting different widths and heights
- Can set `radius` to achieve rounded rectangles
- Larger content area, suitable for displaying multi-line information

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'start', data: { label: 'Start' } },
       { id: 'process1', data: { label: 'Process Data' } },
       { id: 'decision', data: { label: 'Is it Approved?' } },
       { id: 'end', data: { label: 'End' } },
    ],
    edges: [
       { source: 'start', target: 'process1' },
       { source: 'process1', target: 'decision' },
       { source: 'decision', target: 'end' },
    ],
  },
  node: {
    type: 'rect',
    style: {
      size: [120, 40],           // [width, height]
      radius: 4,                 // rounded corners
      fill: '#f0f5ff',
      stroke: '#adc6ff',
      lineWidth: 1,
      labelText: (d) => d.data.label,
      labelPlacement: 'center',  // label centered
      labelFill: '#333',
    },
  },
  layout: {
    type: 'dagre',
    rankdir: 'TB',               // top to bottom
    ranksep: 50,
    nodesep: 30,
  },
  edge: {
    type: 'cubic-vertical',
    style: {
      endArrow: true,
      stroke: '#adc6ff',
    },
  },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

## Common Variants

### Organizational Structure Chart

```javascript
import { Graph, treeToGraphData } from '@antv/g6';

const orgData = {
  id: 'ceo',
      data: { label: 'CEO', dept: 'Board of Directors' },
  children: [
    {
      id: 'cto',
      data: { label: 'CTO', dept: 'Technology Department' },
      children: [
         { id: 'dev1', data: { label: 'Front-end Lead', dept: 'Front-end Team' } },
         { id: 'dev2', data: { label: 'Back-end Lead', dept: 'Back-end Team' } },
      ],
    },
    {
      id: 'cmo',
      data: { label: 'CMO', dept: 'Marketing Department' },
    },
  ],
};

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: treeToGraphData(orgData),
  node: {
    type: 'rect',
    style: {
      size: [140, 50],
      radius: 6,
      fill: '#e6f4ff',
      stroke: '#91caff',
      lineWidth: 1,
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFontSize: 14,
      labelFontWeight: 'bold',
    },
  },
  edge: {
    type: 'cubic-vertical',
    style: { stroke: '#91caff', endArrow: true },
  },
  layout: {
    type: 'compact-box',
    direction: 'TB',
    getHeight: () => 50,
    getWidth: () => 140,
    getVGap: () => 40,
    getHGap: () => 20,
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

### Different Colors to Distinguish Types

```javascript
node: {
  type: 'rect',
  style: {
    size: [120, 40],
    radius: 4,
    fill: (d) => {
      const colors = {
        start: '#f6ffed',
        process: '#e6f4ff',
        decision: '#fff7e6',
        end: '#fff1f0',
      };
      return colors[d.data.type] || '#fafafa';
    },
    stroke: (d) => {
      const colors = {
        start: '#73d13d',
        process: '#4096ff',
        decision: '#ffa940',
        end: '#ff4d4f',
      };
      return colors[d.data.type] || '#d9d9d9';
    },
    labelText: (d) => d.data.label,
    labelPlacement: 'center',
  },
},
```

### Rectangle Node with Subtitle

```javascript
// Use custom HTML node to display multi-line content
import { Graph, ExtensionCategory, register } from '@antv/g6';

// Alternatively, use labelText for line breaks
node: {
  type: 'rect',
  style: {
    size: [160, 60],
    radius: 8,
    fill: '#f0f5ff',
    stroke: '#adc6ff',
    // Main title
    labelText: (d) => d.data.title,
    labelPlacement: 'center',
    labelOffsetY: -10,
    labelFontSize: 14,
    labelFontWeight: 'bold',
  },
},
```

## Common Errors

### Error 1: Using a Single Numeric Size for `rect`

```javascript
// ❌ Runnable, but only sets width; height will default
node: {
  type: 'rect',
  style: { size: 100 },
}

// ✅ Recommended: Explicitly set width and height
node: {
  type: 'rect',
  style: { size: [120, 40] },  // [width, height]
}
```

### Error 2: Label Exceeds Node Boundaries

```javascript
// ❌ Long label overflows node
node: {
  type: 'rect',
  style: {
    size: [80, 30],
    labelText: (d) => d.data.longDescription,  // Too long
  },
}

// ✅ Set maximum width and ellipsis
node: {
  type: 'rect',
  style: {
    size: [120, 40],
    labelText: (d) => d.data.label,
    labelMaxWidth: 100,       // Maximum width
    labelWordWrap: false,     // Ellipsis on overflow
  },
}
```

### Error 3: Forgetting to Set Node Size When Using Dagre Layout

```javascript
// ❌ Node size not set, dagre cannot calculate spacing correctly
layout: {
  type: 'dagre',
},
// nodeSize not set

// ✅ Inform dagre of node dimensions
layout: {
  type: 'dagre',
  nodeSize: [120, 40],  // Consistent with node size
  ranksep: 50,
  nodesep: 20,
},
```