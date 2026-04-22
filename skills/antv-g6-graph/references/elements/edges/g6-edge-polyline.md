---
id: "g6-edge-polyline"
title: "G6 Polyline Edge"
description: |
  Connect nodes using polyline edges, automatically avoiding node obstacles,
  suitable for orthogonal layouts and flowchart scenarios.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "edges"
tags:
  - "edge"
  - "polyline"
  - "orthogonal"
  - "flowchart"

related:
  - "g6-edge-line"
  - "g6-edge-cubic"
  - "g6-layout-dagre"

use_cases:
  - "Orthogonal layout graphs"
  - "Flowcharts"
  - "UML class diagrams"
  - "Module dependency graphs"

anti_patterns:
  - "Polylines tend to detour in node-dense areas, consider using cubic or line edges instead"
  - "Polyline path calculation is slower, pay attention to performance with a large number of nodes"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/element/edge/polyline"
---

## Core Concepts

Polyline edges (`polyline`) automatically calculate breakpoints, connecting nodes with right-angled polylines for a visually clean appearance.

**Features:**
- **Automatic Obstacle Avoidance:** Automatically calculates paths to bypass nodes
- **Orthogonal Polylines:** Edges consist only of horizontal and vertical segments
- **Configurable `radius`:** Allows corners to be rounded

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'Step 1' } },
       { id: 'n2', data: { label: 'Step 2' } },
       { id: 'n3', data: { label: 'Step 3' } },
       { id: 'n4', data: { label: 'Step 4' } },
    ],
    edges: [
       { source: 'n1', target: 'n2' },
       { source: 'n2', target: 'n3' },
       { source: 'n3', target: 'n4' },
       { source: 'n1', target: 'n4' },
    ],
  },
  node: {
    type: 'rect',
    style: {
      size: [100, 40],
      radius: 4,
      fill: '#f0f5ff',
      stroke: '#adc6ff',
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
    },
  },
  edge: {
    type: 'polyline',
    style: {
      stroke: '#adc6ff',
      lineWidth: 1.5,
      radius: 8,                  // Corner radius
      endArrow: true,
    },
  },
  layout: {
    type: 'dagre',
    rankdir: 'LR',
    ranksep: 60,
    nodesep: 30,
  },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

## Common Errors

### Error 1: Poor Performance of Polyline in Force Layout

```javascript
// ❌ Polyline path calculation is inaccurate in force layout (random positions)
layout: { type: 'force' },
edge: { type: 'polyline' },

// ✅ Polyline is suitable for orthogonal/hierarchical layouts
layout: { type: 'dagre', rankdir: 'LR' },
edge: { type: 'polyline' },
```