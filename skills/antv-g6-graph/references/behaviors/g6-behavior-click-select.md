---
id: "g6-behavior-click-select"
title: "G6 Click Select Interaction"
description: |
  Use the click-select behavior to select nodes/edges by clicking, supporting multiple selection, neighbor highlighting,
  and state synchronization.

library: "g6"
version: "5.x"
category: "behaviors"
subcategory: "selection"
tags:
  - "interaction"
  - "click"
  - "select"
  - "click-select"
  - "behavior"
  - "selection"

related:
  - "g6-behavior-hover-activate"
  - "g6-behavior-drag-element"
  - "g6-state-overview"

use_cases:
  - "Click a node to view details"
  - "Select a node to highlight associated relationships"
  - "Multi-select nodes for batch operations"

anti_patterns:
  - "Do not configure if selection is not needed, as it may affect click event handling"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/behavior/click-select"
---

## Core Concepts

`click-select` allows users to select nodes/edges by clicking, supporting:
- Selection state marking (default state name `selected`)
- Neighbor node/edge linkage highlighting
- Multi-select (Shift/Ctrl + click)
- Click on blank area to cancel selection

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
       { source: 'n1', target: 'n2' },
       { source: 'n2', target: 'n3' },
    ],
  },
  node: {
    type: 'circle',
    style: {
      size: 40,
      fill: '#1783FF',
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: '#fff',
    },
    state: {
      selected: {
        fill: '#ff4d4f',
        stroke: '#cf1322',
        lineWidth: 3,
        halo: true,
        haloFill: '#ff4d4f',
        haloOpacity: 0.2,
      },
    },
  },
  layout: { type: 'force', preventOverlap: true },
  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    'click-select',              // String shorthand
  ],
});

graph.render();
```

## Common Variants

### Complete Configuration (Including Neighbor Highlighting)

```javascript
behaviors: [
  'drag-canvas',
  'zoom-canvas',
  {
    type: 'click-select',
    // Supports multiple selection (hold Shift or Ctrl and click)
    multiple: true,
    // Trigger method
    trigger: ['click'],           // 'click' | 'dblclick'
    // Selected state name
    state: 'selected',
    // Neighbor state name
    neighborState: 'highlight',
    // Unselected element state name
    unselectedState: 'inactive',
    // Number of hops to expand neighbors (0 = select only itself)
    degree: 1,
    // Click callback
    onClick: (event) => {
      const { targetType, target } = event;
      if (targetType === 'node') {
        console.log('Selected node:', target.id);
      }
    },
  },
],
// Corresponding state styles
node: {
  state: {
    selected: { fill: '#ff4d4f', lineWidth: 3 },
    highlight: { fill: '#ffa940', opacity: 1 },
    inactive: { opacity: 0.3 },
  },
},
edge: {
  state: {
    highlight: { stroke: '#ffa940', lineWidth: 2 },
    inactive: { opacity: 0.2 },
  },
},
```

### Display Detail Panel on Click

```javascript
// Listen for node click events
graph.on('node:click', (event) => {
  const nodeId = event.target.id;
  const nodeData = graph.getNodeData(nodeId);
  
  // Update UI panel
  document.getElementById('detail-panel').innerHTML = `
    <h3>${nodeData.data.name}</h3>
    <p>${nodeData.data.description}</p>
  `;
});
```

### Set Selected State via API

```javascript
// Select a specific node
graph.setElementState('n1', 'selected');

// Multiple state overlays
graph.setElementState('n1', ['selected', 'highlight']);

// Clear state
graph.setElementState('n1', []);

// Get currently selected nodes
const selectedNodes = graph.getElementDataByState('node', 'selected');
```

## Common Errors

### Error 1: `click-select` is configured but state style is not defined

```javascript
// ❌ Only behavior is configured, no state style, no visual feedback after node is clicked
behaviors: ['click-select'],

// ✅ Configure state style simultaneously
behaviors: ['click-select'],
node: {
  state: {
    selected: {
      fill: '#ff4d4f',
      lineWidth: 3,
    },
  },
},
```

### Error 2: Conflict between point event and click-select

```javascript
// click-select internally consumes the click event
// If custom click logic is needed, use the onClick callback
behaviors: [
  {
    type: 'click-select',
    onClick: (event) => {
      // Custom handling
    },
  },
],
```