---
id: "g6-pattern-flow-chart"
title: "G6 Flow Chart Pattern"
description: |
  Create a flow chart using G6, including different shaped nodes (Start/End/Decision/Process),
  dagre hierarchical layout, polyline edges, and complete configuration.

library: "g6"
version: "5.x"
category: "patterns"
subcategory: "flowchart"
tags:
  - "pattern"
  - "flowchart"
  - "dagre"
  - "directed graph"
  - "workflow"

related:
  - "g6-layout-dagre"
  - "g6-node-rect"
  - "g6-edge-polyline"
  - "g6-edge-cubic"

use_cases:
  - "Business Process Diagram"
  - "Workflow Orchestration"
  - "State Machine Diagram"
  - "Decision Flow"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
---

## Complete Example

```javascript
import { Graph } from '@antv/g6';

const data = {
  nodes: [
     { id: 'start', data: { label: 'Start', type: 'start' } },
     { id: 'input', data: { label: 'User Input', type: 'process' } },
     { id: 'validate', data: { label: 'Data Valid?', type: 'decision' } },
     { id: 'process1', data: { label: 'Process Data', type: 'process' } },
     { id: 'error', data: { label: 'Return Error', type: 'process' } },
     { id: 'save', data: { label: 'Save Result', type: 'process' } },
     { id: 'end', data: { label: 'End', type: 'end' } },
  ],
  edges: [
     { source: 'start', target: 'input' },
     { source: 'input', target: 'validate' },
     { source: 'validate', target: 'process1', data: { label: 'Yes' } },
     { source: 'validate', target: 'error', data: { label: 'No' } },
     { source: 'process1', target: 'save' },
     { source: 'error', target: 'end' },
     { source: 'save', target: 'end' },
  ],
};

// Configure styles by node type
const NODE_STYLE = {
  start: { fill: '#f6ffed', stroke: '#52c41a', size: [100, 36] },
  end: { fill: '#fff1f0', stroke: '#ff4d4f', size: [100, 36] },
  process: { fill: '#e6f4ff', stroke: '#91caff', size: [140, 44] },
  decision: { fill: '#fff7e6', stroke: '#ffd591', size: [140, 44] },
};

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 650,
  autoFit: 'view',

  data,

  node: {
    // Select node shape based on type
    type: (d) => {
      if (d.data.type === 'decision') return 'diamond';
      return 'rect';
    },
    style: {
      size: (d) => NODE_STYLE[d.data.type]?.size || [120, 40],
      radius: (d) => ['start', 'end'].includes(d.data.type) ? 18 : 4,
      fill: (d) => NODE_STYLE[d.data.type]?.fill || '#f5f5f5',
      stroke: (d) => NODE_STYLE[d.data.type]?.stroke || '#d9d9d9',
      lineWidth: 1.5,
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: '#333',
      labelFontSize: 13,
      cursor: 'pointer',
    },
    state: {
      selected: { lineWidth: 3 },
      active: { lineWidth: 2, opacity: 0.8 },
    },
  },

  edge: {
    type: 'polyline',
    style: {
      stroke: '#aaa',
      lineWidth: 1.5,
      radius: 6,
      endArrow: true,
      labelText: (d) => d.data.label || '',
      labelFontSize: 11,
      labelFill: '#999',
      labelBackground: true,
      labelBackgroundFill: '#fff',
      labelBackgroundOpacity: 0.9,
    },
  },

  layout: {
    type: 'dagre',
    rankdir: 'TB',
    ranksep: 60,
    nodesep: 40,
    nodeSize: [140, 44],
  },

  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    'click-select',
  ],

  plugins: [
    {
      type: 'tooltip',
      getContent: (event, items) => {
        const [item] = items;
        if (!item) return '';
        const typeLabel = {
          start: 'Start Node',
          end: 'End Node',
          process: 'Process Node',
          decision: 'Decision Node',
        };
        return `<div style="padding:8px 12px">
          <div>${item.data.label}</div>
          <div style="color:#999;font-size:11px">${typeLabel[item.data.type] || ''}</div>
        </div>`;
      },
    },
  ],
});

graph.render();
```

## Key Notes

- **Diverse Node Shapes**: Select `rect` (rectangle), `diamond` (rhombus), etc., based on the `type` field
- **Dagre Layout**: `rankdir: 'TB'` arranges nodes from top to bottom, `nodeSize` matches actual node size
- **Polyline Edges**: Orthogonal polyline edges align better with flowchart visual conventions, `radius` sets corner rounding
- **Edge Label Background**: `labelBackground: true` ensures condition labels on edges are clear and readable