---
id: "g6-plugin-edge-bundling-bubble"
title: "G6 Edge Bundling Plugin + Bubble Sets Plugin (edge-bundling / bubble-sets)"
description: |
  edge-bundling: Bundles adjacent edges together to reduce visual clutter and reveal higher-level structures.
  bubble-sets: Encloses node sets with bubble shapes to intuitively express relationships between sets (intersections, groupings, etc.).

library: "g6"
version: "5.x"
category: "plugins"
subcategory: "advanced"
tags:
  - "edge-bundling"
  - "bubble-sets"
  - "边绑定"
  - "气泡集"
  - "集合关系"
  - "节点分组"

related:
  - "g6-plugin-fisheye-hull-watermark"
  - "g6-layout-circular"
  - "g6-layout-force"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-16"
updated: "2026-04-16"
---
## Edge Bundling

Bundles edges with similar directions in the graph to reduce edge crossings and visual clutter in large-scale graphs, while revealing high-level connection patterns. Based on the FEDB (Force-Directed Edge Bundling) algorithm.

```javascript
import { Graph } from '@antv/g6';

// Edge bundling works best with circular layouts
fetch('https://assets.antv.antgroup.com/g6/circular.json')
  .then((res) => res.json())
  .then((data) => {
    const graph = new Graph({
      container: 'container',
      width: 800,
      height: 600,
      autoFit: 'view',
      data,
      layout: { type: 'circular' },
      node: { style: { size: 20 } },
      behaviors: ['drag-canvas', 'drag-element'],
      plugins: [
        {
          type: 'edge-bundling',
          key: 'bundling',
          bundleThreshold: 0.6,  // Edge compatibility threshold (0-1, higher values result in fewer edges being bundled)
          K: 0.1,                // Edge strength (attraction)
        },
      ],
    });

    graph.render();
  });
```

### edge-bundling Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `type` | `string` | `'edge-bundling'` | Plugin type |
| `key` | `string` | — | Unique identifier for dynamic updates |
| `bundleThreshold` | `number` | `0.6` | Edge bundling threshold: higher values result in fewer bundled edges; 0.4 shows significant bundling, 0.8 shows less bundling |
| `cycles` | `number` | `6` | Number of simulation cycles, affecting computation quality |
| `divisions` | `number` | `1` | Initial number of division points, affecting edge subdivision |
| `divRate` | `number` | `2` | Division point growth rate |
| `iterations` | `number` | `90` | Number of iterations in the first cycle |
| `iterRate` | `number` | `2/3` | Iteration count reduction rate |
| `K` | `number` | `0.1` | Edge strength (attraction/repulsion): 0.05 weak, 0.2 strong |
| `lambda` | `number` | `0.1` | Initial step size |

```javascript
// Shorthand form (using default configuration)
plugins: ['edge-bundling']

// Custom configuration
plugins: [
  {
    type: 'edge-bundling',
    bundleThreshold: 0.1,   // Low threshold = more edges bundled
    cycles: 8,
    K: 0.2,
  },
]

// Dynamic update
graph.updatePlugin({ key: 'bundling', bundleThreshold: 0.8 });
```

---

## Bubble Sets (bubble-sets)

Enclose specified node sets with organic bubble contours, which can be used to express node grouping, set intersection, and other relationships. Supports the side-by-side display of multiple bubble instances.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
      { id: 'n0', data: { cluster: 'a' }, style: { x: 200, y: 150 } },
      { id: 'n1', data: { cluster: 'a' }, style: { x: 300, y: 200 } },
      { id: 'n2', data: { cluster: 'a' }, style: { x: 250, y: 300 } },
      { id: 'n3', data: { cluster: 'b' }, style: { x: 500, y: 150 } },
      { id: 'n4', data: { cluster: 'b' }, style: { x: 550, y: 280 } },
    ],
    edges: [
      { source: 'n0', target: 'n1' },
      { source: 'n1', target: 'n2' },
      { source: 'n2', target: 'n3' },
      { source: 'n3', target: 'n4' },
    ],
  },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
  plugins: [
    {
      type: 'bubble-sets',
      key: 'bubble-a',
      members: ['n0', 'n1', 'n2'],   // Required: Node IDs to enclose
      fill: '#1783FF',
      fillOpacity: 0.1,
      stroke: '#1783FF',
      label: true,
      labelText: 'Group A',
    },
    {
      type: 'bubble-sets',
      key: 'bubble-b',
      members: ['n3', 'n4'],
      fill: '#F08F56',
      fillOpacity: 0.1,
      stroke: '#F08F56',
      label: true,
      labelText: 'Group B',
    },
  ],
});

graph.render();
```

### bubble-sets Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `type` | `string` | `'bubble-sets'` | Plugin type |
| `key` | `string` | — | Unique identifier (required for multiple instances) |
| `members` | `string[]` | — | **Required**: List of node/edge IDs to wrap |
| `avoidMembers` | `string[]` | — | Node IDs for the outline to avoid |
| `fill` | `string` | — | Bubble fill color |
| `fillOpacity` | `number` | — | Fill opacity (recommended 0.05-0.2) |
| `stroke` | `string` | — | Border color |
| `strokeOpacity` | `number` | — | Border opacity |
| `label` | `boolean` | `true` | Whether to display the label |
| `labelText` | `string` | — | Label text content |
| `labelPlacement` | `string` | `'bottom'` | Label position: `left/right/top/bottom/center` |
| `labelBackground` | `boolean` | `false` | Whether to display the label background |
| `labelPadding` | `number \| number[]` | `0` | Label inner padding |
| `labelCloseToPath` | `boolean` | `true` | Whether the label adheres to the outline |
| `labelAutoRotate` | `boolean` | `true` | Whether the label rotates with the outline |

### Dynamically Update Bubble Set Members

```javascript
// Update members after initialization
graph.updatePlugin({
  key: 'bubble-a',
  members: ['n0', 'n1', 'n2', 'n3'],  // Add n3 to Group A
});
```

### Pattern of Automatic Grouping by Data Fields

```javascript
// After rendering, automatically build bubble sets by the cluster field
graph.render().then(() => {
  const nodesByCluster = {};
  graph.getNodeData().forEach((node) => {
    const cluster = node.data.cluster;
    nodesByCluster[cluster] = nodesByCluster[cluster] || [];
    nodesByCluster[cluster].push(node.id);
  });

  const colors = { a: '#1783FF', b: '#F08F56', c: '#52C41A' };
  const plugins = Object.entries(nodesByCluster).map(([cluster, ids]) => ({
    type: 'bubble-sets',
    key: `bubble-${cluster}`,
    members: ids,
    fill: colors[cluster] || '#ccc',
    fillOpacity: 0.1,
    stroke: colors[cluster] || '#ccc',
    labelText: `cluster-${cluster}`,
    labelBackground: true,
    labelPadding: 4,
  }));

  graph.setPlugins(plugins);
  graph.draw();
});
```