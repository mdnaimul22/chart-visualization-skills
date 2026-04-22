---
id: "g6-edge-line"
title: "G6 Line Edge"
description: |
  The line edge is the simplest type of edge, used to connect nodes with a straight line.
  It supports various style configurations such as arrows, labels, and dashed lines.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "edges"
tags:
  - "edge"
  - "line"
  - "arrow"
  - "directed graph"

related:
  - "g6-edge-cubic"
  - "g6-edge-polyline"
  - "g6-node-circle"

use_cases:
  - "Simple network graphs"
  - "Topology diagrams"
  - "Directed graphs"
  - "Flowcharts (combined with polyline edges)"

anti_patterns:
  - "When nodes are close and there are many edges, lines can overlap; consider using cubic or quadratic edges instead"
  - "For parallel edge scenarios (multiple edges with the same source and target), use the process-parallel-edges transform"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/element/edge/line"
---

## Core Concepts

The straight line edge (`line`) is the simplest edge type in G6, directly connecting two nodes without any curvature.

**Main Style Attributes:**
- `stroke`: Edge color
- `lineWidth`: Edge width
- `endArrow`: End arrow (`true` or arrow configuration object)
- `startArrow`: Start arrow
- `lineDash`: Dashed line configuration

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'A' } },
       { id: 'n2', data: { label: 'B' } },
       { id: 'n3', data: { label: 'C' } },
    ],
    edges: [
       { id: 'e1', source: 'n1', target: 'n2', data: { label: 'Connection' } },
       { id: 'e2', source: 'n2', target: 'n3' },
    ],
  },
  node: {
    type: 'circle',
    style: {
      size: 36,
      fill: '#1783FF',
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: '#fff',
    },
  },
  edge: {
    type: 'line',
    style: {
      stroke: '#999',
      lineWidth: 1.5,
      endArrow: true,              // Display arrow
      labelText: (d) => d.data.label,
    },
  },
  layout: { type: 'dagre', rankdir: 'LR' },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

## Common Variants

### Weighted Edges (Width Mapping)

```javascript
edge: {
  type: 'line',
  style: {
    stroke: '#aaa',
    lineWidth: (d) => Math.max(1, d.data.weight / 10),  // Set width based on weight
    endArrow: true,
    labelText: (d) => d.data.weight ? `${d.data.weight}` : '',
    labelFontSize: 12,
    labelFill: '#666',
  },
},
```

### Dashed Edge

```javascript
edge: {
  type: 'line',
  style: {
    stroke: '#aaa',
    lineWidth: 1.5,
    lineDash: [4, 4],        // Dashed line: [solid length, gap length]
    endArrow: true,
  },
},
```

### Custom Arrow

```javascript
edge: {
  type: 'line',
  style: {
    stroke: '#1783FF',
    lineWidth: 2,
    endArrow: {
      type: 'triangle',      // 'triangle' | 'circle' | 'diamond' | 'rect' | 'vee' | 'simple'
      fill: '#1783FF',
      stroke: '#1783FF',
      size: 10,
    },
    startArrow: {
      type: 'circle',
      fill: '#fff',
      stroke: '#1783FF',
      size: 8,
    },
  },
},
```

### Color by Edge Type

```javascript
edge: {
  type: 'line',
  style: {
    stroke: (d) => {
      const colors = {
        'dependency': '#4096ff',
        'extends': '#52c41a',
        'implements': '#fa8c16',
      };
      return colors[d.data.type] || '#aaa';
    },
    lineWidth: 1.5,
    endArrow: true,
    lineDash: (d) => d.data.type === 'implements' ? [4, 4] : [],
    labelText: (d) => d.data.type,
    labelFontSize: 11,
  },
},
```

### Handling Parallel Edges

```javascript
// Use the process-parallel-edges transform when there are multiple edges between the same pair of nodes
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
       { id: 'a', data: { label: 'A' } },
       { id: 'b', data: { label: 'B' } },
    ],
    edges: [
       { id: 'e1', source: 'a', target: 'b', data: { label: 'Call' } },
       { id: 'e2', source: 'a', target: 'b', data: { label: 'Callback' } },
       { id: 'e3', source: 'b', target: 'a', data: { label: 'Return' } },
    ],
  },
  // Use transform to handle parallel edges
  transforms: ['process-parallel-edges'],
  edge: {
    type: 'quadratic',          // Curves are more aesthetically pleasing for parallel edges
    style: {
      stroke: '#aaa',
      endArrow: true,
      labelText: (d) => d.data.label,
    },
  },
  layout: { type: 'force' },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});
```

## Edge State Styles

```javascript
edge: {
  type: 'line',
  style: {
    stroke: '#aaa',
    lineWidth: 1,
    endArrow: true,
  },
  state: {
    selected: {
      stroke: '#1783FF',
      lineWidth: 3,
    },
    hover: {
      stroke: '#40a9ff',
      lineWidth: 2,
    },
    inactive: {
      opacity: 0.2,
    },
  },
},
```

## Common Errors

### Error 1: Edge Labels Not Displayed

```javascript
// ❌ Data contains label, but labelText is not configured
const edges = [{ source: 'n1', target: 'n2', data: { label: 'relation' } }];
edge: { type: 'line', style: { stroke: '#aaa' } }  // labelText is missing

// ✅ labelText needs to be configured
edge: {
  type: 'line',
  style: {
    stroke: '#aaa',
    labelText: (d) => d.data.label || '',  // Read from data
  },
},
```

### Error 2: Arrow Direction Does Not Match Expectations

```javascript
// ❌ Assumed startArrow is at the source end, but actual rendering position is confused
// Clarification: endArrow is at the target (end) end, startArrow is at the source (start) end

// ✅ Directed graph using endArrow
edge: {
  type: 'line',
  style: {
    endArrow: true,    // Arrow at the target end
  },
},
```