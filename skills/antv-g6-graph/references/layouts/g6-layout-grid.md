---
id: "g6-layout-grid"
title: "G6 Grid Layout"
description: |
  Use the grid layout to arrange nodes in a rectangular grid.
  Suitable for scenarios with a large number of nodes and no obvious hierarchy or relationships.

library: "g6"
version: "5.x"
category: "layouts"
subcategory: "grid"
tags:
  - "layout"
  - "grid"
  - "matrix"
  - "regular arrangement"

related:
  - "g6-layout-force"
  - "g6-layout-circular"

use_cases:
  - "Node list display"
  - "Node collections with no obvious topological relationships"
  - "Debugging and demonstration purposes"

anti_patterns:
  - "Switch to force or dagre when there are obvious topological relationships"
  - "Too few nodes with excessive spacing, not compact enough"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/layout/grid"
---

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const nodes = Array.from({ length: 12 }, (_, i) => ({
  id: `n${i}`,
  data: { label: `Node${i + 1}`, value: Math.random() * 100 },
}));

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 500,
  data: { nodes, edges: [] },
  node: {
    type: 'circle',
    style: {
      size: 40,
      fill: '#1783FF',
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
  },
  layout: {
    type: 'grid',
    rows: 3,              // Number of rows
    cols: 4,              // Number of columns (optional, auto-calculated)
    rowGap: 40,           // Row spacing
    colGap: 40,           // Column spacing
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

## Parameter Reference

```typescript
interface GridLayoutOptions {
  rows?: number;           // Number of rows
  cols?: number;           // Number of columns
  rowGap?: number;         // Row spacing
  colGap?: number;         // Column spacing
  sortBy?: string;         // Sort by a specific field
  preventOverlap?: boolean;
  nodeSize?: number | [number, number];
  workerEnabled?: boolean;
}
```