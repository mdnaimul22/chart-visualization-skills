---
id: "g6-layout-circular"
title: "G6 Circular Layout"
description: |
  Use the circular layout to evenly arrange nodes on a circle.
  Suitable for displaying cyclic relationships, comparative relationships, and peer-to-peer networks.

library: "g6"
version: "5.x"
category: "layouts"
subcategory: "circular"
tags:
  - "layout"
  - "circular"
  - "circle"
  - "ring"

related:
  - "g6-layout-force"
  - "g6-layout-dagre"
  - "g6-node-circle"

use_cases:
  - "Cyclic dependency graphs"
  - "Peer-to-peer network topologies"
  - "Ring organizational structures"
  - "Relationship graphs with fewer nodes"

anti_patterns:
  - "Circumference becomes too long and affects readability when there are too many nodes"
  - "Switch to dagre when hierarchical relationships need to be displayed"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/layout/circular"
---

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const nodes = Array.from({ length: 8 }, (_, i) => ({
  id: `n${i}`,
  data: { label: `Node${i + 1}` },
}));

const edges = nodes.map((n, i) => ({
  source: n.id,
  target: nodes[(i + 1) % nodes.length].id,
}));

const graph = new Graph({
  container: 'container',
  width: 600,
  height: 600,
  data: { nodes, edges },
  node: {
    type: 'circle',
    style: {
      size: 36,
      fill: '#1783FF',
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
  },
  edge: {
    type: 'line',
    style: { stroke: '#aaa', endArrow: true },
  },
  layout: {
    type: 'circular',
    radius: 200,          // Circle radius (px)
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

## Common Variants

### Clockwise/Counterclockwise Arrangement

```javascript
layout: {
  type: 'circular',
  radius: 200,
  startAngle: 0,          // Start angle (in radians)
  endAngle: Math.PI * 2,  // End angle
  clockwise: true,        // Clockwise (false = counterclockwise)
},
```

### Sort Nodes by Attribute

```javascript
layout: {
  type: 'circular',
  radius: 200,
  // Sort nodes based on a specific field in the node data
  ordering: 'degree',     // Sort by degree, options: 'topology' | 'degree' | null
},
```

### Using Existing Data (Recommended Approach)

When the data is already provided, directly use the original data and avoid dynamically generating edges randomly:

```javascript
import { Graph } from '@antv/g6';

const data = {
  nodes: [
    { id: '0' }, { id: '1' }, { id: '2' }, { id: '3' },
  ],
  edges: [
    { source: '0', target: '1' },
    { source: '0', target: '2' },
    { source: '1', target: '3' },
  ],
};

const graph = new Graph({
  container: 'container',
  autoFit: 'view',
  data,
  node: {
    style: {
      labelText: (d) => d.id,
      labelFill: '#fff',
      labelPlacement: 'center',
    },
  },
  layout: {
    type: 'circular',
  },
  behaviors: ['drag-canvas', 'drag-element'],
});

graph.render();
```

## Parameter Reference

```typescript
interface CircularLayoutOptions {
  radius?: number;           // Radius of the circle, default calculated based on canvas size
  startAngle?: number;       // Start angle (in radians), default 0
  endAngle?: number;         // End angle (in radians), default 2π
  clockwise?: boolean;       // Clockwise direction, default true
  divisions?: number;        // Number of segments to divide the circle into
  ordering?: 'topology' | 'degree' | null;  // Ordering method, default null
  angleRatio?: number;       // Angle ratio between nodes, default 1
  workerEnabled?: boolean;
}
```

## Edge ID Rules and Duplicate Edge Issues

⚠️ **Important**: The edge ID rules in G6 are as follows:
- If the edge data **explicitly specifies an `id`**, that `id` is used.
- If the edge data **does not specify an `id`**, G6 automatically uses `"${source}-${target}"` as the edge ID.

Therefore, **multiple edges without a specified id cannot exist between the same source-target pair**, otherwise an error will occur:
```
Edge already exists: 12-20
```

**Solutions**:
1. **Deduplication**: Ensure that the edge array does not contain duplicate source-target combinations.
2. **Explicitly specify id**: Assign a unique id to each edge, for example `{ id: 'e-0-1', source: '0', target: '1' }`.

## Common Errors and Fixes

### ❌ Error: Randomly Generated Edges Cause Duplicates, Triggering "Edge already exists"

```javascript
// ❌ Incorrect Approach: Randomly generating edges may produce duplicate source-target pairs
const edges = [];
for (let i = 0; i < 34; i++) {
  const numEdges = 2 + Math.floor(Math.random() * 2);
  for (let j = 0; j < numEdges; j++) {
    const target = Math.floor(Math.random() * 34);
    if (target !== i) {
      edges.push({ source: `${i}`, target: `${target}` });
      // If source-target pairs are duplicated, G6 will generate duplicate IDs, causing errors!
    }
  }
}
```

```javascript
// ✅ Correct Approach 1: Use a Set to eliminate duplicates and avoid repeated edges
const edgeSet = new Set();
const edges = [];
for (let i = 0; i < 34; i++) {
  const numEdges = 2 + Math.floor(Math.random() * 2);
  for (let j = 0; j < numEdges; j++) {
    const target = Math.floor(Math.random() * 34);
    const key = `${i}-${target}`;
    if (target !== i && !edgeSet.has(key)) {
      edgeSet.add(key);
      edges.push({ source: `${i}`, target: `${target}` });
    }
  }
}
```

```javascript
// ✅ Correct Approach 2: Explicitly assign a unique id to each edge (prevents conflicts even with duplicate source-target pairs)
const edges = [];
let edgeIndex = 0;
for (let i = 0; i < 34; i++) {
  const numEdges = 2 + Math.floor(Math.random() * 2);
  for (let j = 0; j < numEdges; j++) {
    const target = Math.floor(Math.random() * 34);
    if (target !== i) {
      edges.push({ id: `e${edgeIndex++}`, source: `${i}`, target: `${target}` });
    }
  }
}
```

```javascript
// ✅ Correct Approach 3 (Most Recommended): When provided with data, use the original data directly instead of randomly generating edges
// If the query provides reference data (nodes/edges), use it directly and avoid replacing it with random generation logic
const data = {
  nodes: [ { id: '0' }, { id: '1' }, /* ... */ ],
  edges: [ { source: '0', target: '1' }, /* ... */ ],
};
```

### ❌ Error: `sortBy` Field Does Not Exist

```javascript
// ❌ Error: The circular layout does not have a sortBy parameter
layout: {
  type: 'circular',
  sortBy: 'degree',   // This parameter does not exist!
}

// ✅ Correct: Use the ordering parameter
layout: {
  type: 'circular',
  ordering: 'degree', // 'topology' | 'degree' | null
}
```