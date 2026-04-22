---
id: "g6-layout-combo-fishbone"
title: "G6 Composite Layout + Fishbone Layout (combo-combined / fishbone)"
description: |
  combo-combined: Designed specifically for graphs containing Combo groups, using force-directed layout for outer nodes and layouts like concentric circles within Combos.
  fishbone: Fishbone diagram layout, suitable for hierarchical structures, causal analysis, fault analysis, and other scenarios.

library: "g6"
version: "5.x"
category: "layouts"
subcategory: "hierarchical"
tags:
  - "combo-combined"
  - "fishbone"
  - "composite layout"
  - "fishbone diagram"
  - "causal analysis"
  - "Combo layout"

related:
  - "g6-combo-overview"
  - "g6-layout-force"
  - "g6-layout-advanced"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-16"
updated: "2026-04-16"
---

## Combo-Combined Layout

Specifically designed for graphs containing Combo groups, this layout uses a force-directed layout (gForce) for the outer layer by default and a concentric layout (Concentric) for the inside of Combos, balancing overall stability with internal structural clarity.

> ⚠️ **autoFit White Screen Trap**: The outer layer of `combo-combined` defaults to an asynchronous force-directed layout (`gForce`). When `autoFit: 'view'` is directly set in the Graph config, `fitView` is executed before the force-directed iteration begins, causing all nodes to pile up at the origin, resulting in a bounding box area of zero and an abnormal zoom ratio → **white screen**.  
>  
> Correct approach: **Do not set `autoFit` in the config**. Instead, listen for `GraphEvent.AFTER_LAYOUT` and then call `fitView()`.

```javascript
import { Graph, GraphEvent } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  // ❌ Do not set autoFit: 'view' here, as it triggers before force-directed iteration and causes a white screen
  data: {
    nodes: [
      { id: 'n1', combo: 'c1', data: { label: 'Node 1' } },
      { id: 'n2', combo: 'c1', data: { label: 'Node 2' } },
      { id: 'n3', combo: 'c1', data: { label: 'Node 3' } },
      { id: 'n4', combo: 'c2', data: { label: 'Node 4' } },
      { id: 'n5', combo: 'c2', data: { label: 'Node 5' } },
      { id: 'n6', data: { label: 'Free Node' } },
    ],
    edges: [
      { source: 'n1', target: 'n4' },
      { source: 'n3', target: 'n5' },
      { source: 'n5', target: 'n6' },
    ],
    combos: [
      { id: 'c1', data: { label: 'Group A' } },
      { id: 'c2', data: { label: 'Group B' } },
    ],
  },
  node: {
    style: {
      size: 24,
      labelText: (d) => d.data.label,
    },
    palette: {
      type: 'group',
      field: (d) => d.combo,
    },
  },
  combo: {
    type: 'rect',
    style: {
      labelText: (d) => d.data.label,  // ✅ Read business data from the `data` field, not the `style` field
      labelPlacement: 'top',
      padding: 20,
    },
  },
  layout: {
    type: 'combo-combined',
    comboPadding: 10,    // Padding inside Combo (used for force calculation, recommended to match visual padding)
    nodeSize: 24,        // Node size (used for collision detection)
    spacing: 8,          // Minimum spacing to prevent overlap
  },
  behaviors: ['drag-element', 'drag-canvas', 'zoom-canvas'],
});

// ✅ Call fitView after the force-directed layout completes to avoid white screen
graph.on(GraphEvent.AFTER_LAYOUT, () => {
  graph.fitView({ padding: 20 });
});

graph.render();
```
---

## Fishbone Layout (fishbone)

The fishbone layout arranges hierarchical data into a fishbone shape. It is suitable for displaying cause-and-effect relationships (Ishikawa diagram/fishbone diagram), fault analysis, multi-factor analysis, and other scenarios.

> Note: fishbone requires tree-structured data and is typically used in conjunction with `treeToGraphData()`.

```javascript
import { Graph, treeToGraphData } from '@antv/g6';

const treeData = {
  id: 'Result',
  children: [
    {
      id: 'Cause A',
      children: [
        { id: 'Sub-cause A1' },
        { id: 'Sub-cause A2' },
      ],
    },
    {
      id: 'Cause B',
      children: [
        { id: 'Sub-cause B1' },
        { id: 'Sub-cause B2', children: [{ id: 'Sub-sub-cause B2-1' }] },
      ],
    },
    { id: 'Cause C' },
  ],
};

const graph = new Graph({
  container: 'container',
  width: 900,
  height: 500,
  autoFit: 'view',
  data: treeToGraphData(treeData),
  node: {
    type: 'rect',
    style: {
      size: [80, 30],
      fill: '#e6f7ff',
      stroke: '#1783FF',
      labelText: (d) => d.id,
      labelPlacement: 'center',
      labelFill: '#333',
    },
  },
  edge: {
    type: 'polyline',
    style: {
      stroke: '#1783FF',
      lineWidth: 2,
    },
  },
  layout: {
    type: 'fishbone',
    direction: 'LR',   // 'LR': fish head on the left; 'RL': fish head on the right (default)
    hGap: 60,          // Horizontal gap
    vGap: 40,          // Vertical gap
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

### Fishbone Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `type` | `string` | `'fishbone'` | Layout type |
| `direction` | `'LR' \| 'RL'` | `'RL'` | Direction: LR for fish head on the left, RL for fish head on the right |
| `hGap` | `number` | — | Horizontal spacing |
| `vGap` | `number` | — | Vertical spacing |
| `getRibSep` | `(node) => number` | `() => 60` | Fishbone spacing callback |
| `nodeSize` | `number \| [number, number] \| Function` | — | Node size |
| `nodeFilter` | `(node) => boolean` | — | Node filter for layout participation |
| `preLayout` | `boolean` | — | Whether to pre-compute layout before initialization |

### 6M Fishbone Diagram (Ishikawa Diagram) Example

```javascript
import { Graph } from '@antv/g6';

// Directly use flat data with depth and children fields (G6 fishbone supports this format)
const graph = new Graph({
  container: 'container',
  width: 1000,
  height: 600,
  autoFit: 'view',
  data: {
    nodes: [
      { id: 'Quality Issue', depth: 0, children: ['Man', 'Machine', 'Material', 'Method', 'Environment', 'Measurement'] },
      { id: 'Man', depth: 1, children: ['Insufficient Training', 'Operational Error'] },
      { id: 'Insufficient Training', depth: 2 },
      { id: 'Operational Error', depth: 2 },
      { id: 'Machine', depth: 1, children: ['Equipment Aging'] },
      { id: 'Equipment Aging', depth: 2 },
      { id: 'Material', depth: 1 },
      { id: 'Method', depth: 1, children: ['Process Missing'] },
      { id: 'Process Missing', depth: 2 },
      { id: 'Environment', depth: 1 },
      { id: 'Measurement', depth: 1 },
    ],
    edges: [
      { source: 'Quality Issue', target: 'Man' },
      { source: 'Quality Issue', target: 'Machine' },
      { source: 'Quality Issue', target: 'Material' },
      { source: 'Quality Issue', target: 'Method' },
      { source: 'Quality Issue', target: 'Environment' },
      { source: 'Quality Issue', target: 'Measurement' },
      { source: 'Man', target: 'Insufficient Training' },
      { source: 'Man', target: 'Operational Error' },
      { source: 'Machine', target: 'Equipment Aging' },
      { source: 'Method', target: 'Process Missing' },
    ],
  },
  node: {
    type: 'rect',
    style: {
      size: [80, 32],
      fill: '#fff7e6',
      stroke: '#fa8c16',
      lineWidth: 1,
      labelText: (d) => d.id,
      labelPlacement: 'center',
    },
  },
  edge: {
    type: 'polyline',
    style: { stroke: '#fa8c16', lineWidth: 2 },
  },
  layout: {
    type: 'fishbone',
    direction: 'RL',
    hGap: 60,
    vGap: 48,
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```