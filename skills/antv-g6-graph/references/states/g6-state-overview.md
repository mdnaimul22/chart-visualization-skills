---
id: "g6-state-overview"
title: "G6 Element State System"
description: |
  The Element States system in G6 5.x, including built-in states, custom states,
  state style configurations, and a complete guide to state APIs.

library: "g6"
version: "5.x"
category: "states"
subcategory: "overview"
tags:
  - "state"
  - "selected"
  - "active"
  - "highlight"
  - "inactive"
  - "disabled"

related:
  - "g6-behavior-click-select"
  - "g6-behavior-hover-activate"
  - "g6-core-graph-init"

use_cases:
  - "Highlight selected nodes"
  - "Hover effects"
  - "Disable/activate nodes"
  - "Multiple state overlays"

anti_patterns:
  - "Do not use callback functions in state styles (state styles only support static values)"
  - "Do not define dynamic data mappings in states; that is the job of global styles"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/element/state"
---

## Core Concepts

Characteristics of element states in G6 v5:
- **Multiple states coexistence**: An element can have multiple states simultaneously
- **Style overlay**: Styles of multiple states will be overlaid (later set styles have higher priority)
- **Fully customizable**: Apart from built-in states, any custom state can be defined

**Built-in state names:** `selected`、`active`、`highlight`、`inactive`、`disabled`

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'A' }, states: ['selected'] },  // Initially selected
       { id: 'n2', data: { label: 'B' } },
       { id: 'n3', data: { label: 'C' }, states: ['disabled'] }, // Initially disabled
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
    // State styles
    state: {
      selected: {
        fill: '#ff4d4f',
        stroke: '#cf1322',
        lineWidth: 3,
        halo: true,
        haloFill: '#ff4d4f',
        haloOpacity: 0.2,
      },
      active: {
        fill: '#40a9ff',
        stroke: '#1677ff',
      },
      highlight: {
        fill: '#ffa940',
      },
      inactive: {
        opacity: 0.3,
        fill: '#d9d9d9',
      },
      disabled: {
        fill: '#f0f0f0',
        stroke: '#d9d9d9',
        labelFill: '#bfbfbf',
        cursor: 'not-allowed',
      },
    },
  },
  edge: {
    state: {
      selected: { stroke: '#ff4d4f', lineWidth: 3 },
      active: { stroke: '#40a9ff', lineWidth: 2 },
      inactive: { opacity: 0.2 },
    },
  },
  layout: { type: 'force', preventOverlap: true },
  behaviors: ['drag-canvas', 'zoom-canvas', 'click-select'],
});

graph.render();
```

## State API

```javascript
// Set a single state
graph.setElementState('node1', 'selected');

// Set multiple states (overlay)
graph.setElementState('node1', ['selected', 'highlight']);

// Clear all states
graph.setElementState('node1', []);

// Clear specific states (retain others)
const currentStates = graph.getElementState('node1');
const newStates = currentStates.filter(s => s !== 'selected');
graph.setElementState('node1', newStates);

// Batch set states
graph.setElementState({
  node1: 'selected',
  node2: ['highlight'],
  node3: [],
});

// Query element states
const states = graph.getElementState('node1');
// Returns: ['selected', 'highlight']

// Find elements by state
const selectedNodes = graph.getElementDataByState('node', 'selected');
const activeEdges = graph.getElementDataByState('edge', 'active');
```

## Custom States

```javascript
// Any custom state name can be used
node: {
  state: {
    // Built-in states
    selected: { fill: '#ff4d4f' },
    // Custom states
    warning: {
      fill: '#faad14',
      stroke: '#d48806',
      lineWidth: 2,
    },
    error: {
      fill: '#ff4d4f',
      stroke: '#cf1322',
    },
    success: {
      fill: '#52c41a',
      stroke: '#389e0d',
    },
    loading: {
      opacity: 0.6,
      // Can be combined with animation to achieve dynamic effects
    },
  },
},

// Set custom states
graph.setElementState('node1', 'warning');
graph.setElementState('node1', 'error');
```

## State Style Priority

```
Style in data > State style (later set > earlier set) > Global node/edge style > Theme style
```

```javascript
// Example: Node has two states: selected and highlight
// selected style + highlight style are stacked, with highlight properties taking priority as they are set later
graph.setElementState('n1', ['selected', 'highlight']);
```

## Operating State After Rendering Completion

If you need to perform state-related operations after the chart rendering is complete, you can use `await graph.render()` or listen to lifecycle events:

```javascript
import { Graph, GraphEvent } from '@antv/g6';

const graph = new Graph({ /* ... */ });

// Method 1: Using await
await graph.render();
graph.setElementState('node1', 'selected');

// Method 2: Using GraphEvent (requires import from @antv/g6)
graph.on(GraphEvent.AFTER_RENDER, () => {
  graph.setElementState('node1', 'selected');
});

// Method 3: Using string event name (no import needed)
graph.on('afterrender', () => {
  graph.setElementState('node1', 'selected');
});
```

## Common Errors and Fixes

### Error 1: Using Callback Functions in State Styles

```javascript
// ❌ Incorrect: State styles do not support callback functions
node: {
  state: {
    selected: {
      fill: (d) => d.data.color,  // Will not take effect!
    },
  },
},

// ✅ Correct: State styles should only use static values
node: {
  state: {
    selected: {
      fill: '#ff4d4f',  // Static color value
    },
  },
},
```

### Error 2: Setting State Without Defining Corresponding Styles

```javascript
// ❌ State is set but no styles are defined, nodes will not have visual changes
behaviors: ['click-select'],
// node.state is not configured

// ✅ Configure state styles when setting state
behaviors: ['click-select'],
node: {
  state: {
    selected: { fill: '#ff4d4f', lineWidth: 3 },
  },
},
```

### Error 3: Using GraphEvent Without Importing

```javascript
// ❌ Error: GraphEvent is not defined
import { Graph } from '@antv/g6';

graph.on(GraphEvent.AFTER_RENDER, () => {  // GraphEvent is not defined
  // ...
});

// ✅ Correct: Import GraphEvent from @antv/g6
import { Graph, GraphEvent } from '@antv/g6';

graph.on(GraphEvent.AFTER_RENDER, () => {
  // ...
});

// ✅ Alternatively, use string event names (no import needed)
import { Graph } from '@antv/g6';

graph.on('afterrender', () => {
  // ...
});
```