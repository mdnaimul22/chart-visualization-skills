---
id: "g6-combo-overview"
title: "G6 Combo (Composite Node)"
description: |
  Use combo to group/categorize nodes, supporting collapse/expand, drag-and-drop,
  and nested combos. Built-in types include circle-combo and rect-combo.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "combos"
tags:
  - "combo"
  - "composite"
  - "group"
  - "collapse"
  - "expand"

related:
  - "g6-node-circle"
  - "g6-behavior-drag-element"
  - "g6-layout-dagre"

use_cases:
  - "Organizational Structure Chart (Department Grouping)"
  - "Microservice Architecture (Service Grouping)"
  - "Multi-level Nested Relationship Display"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Core Concepts

**Combo** is a bounding container for a group of nodes/sub-combos, associated via the `combo` field:
- In node data, `combo: 'comboId'` indicates the node belongs to the specified combo
- Combo size is automatically calculated based on internal elements
- Supports collapsed state
- **G6 5.x supports combo as a source or target of edges** (i.e., edges can connect to combos)

## Combo Data Structure

| Property | Description | Type | Default Value | Required |
|------|------|------|--------|------|
| `id` | Unique identifier for the combo | `string` | - | ✓ |
| `type` | Combo type (`circle`/`rect`) | `string` | - | |
| `data` | Business data (labels, etc.) | `object` | - | |
| `style` | Style configuration (position, collapse state, etc.) | `object` | - | |
| `combo` | Parent combo ID (for nesting) | `string` | - | |
| `states` | Initial states | `string[]` | - | |

**Important**: Parent combos (containers referenced by other combos) must also be defined in the `combos` array, even if they only have the `id` field.

## Minimum Viable Example (rect-combo)

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'n1', combo: 'c1', data: { label: 'Frontend A' } },
       { id: 'n2', combo: 'c1', data: { label: 'Frontend B' } },
       { id: 'n3', combo: 'c2', data: { label: 'Backend A' } },
       { id: 'n4', combo: 'c2', data: { label: 'Backend B' } },
       { id: 'n5', combo: 'c2', data: { label: 'Backend C' } },
    ],
    edges: [
       { source: 'n1', target: 'n3' },
       { source: 'n2', target: 'n4' },
    ],
    combos: [
       { id: 'c1', data: { label: 'Frontend Team' } },
       { id: 'c2', data: { label: 'Backend Team' } },
    ],
  },
  node: {
    type: 'circle',
    style: {
      size: 36,
      fill: '#1783FF',
      stroke: '#fff',
      lineWidth: 2,
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
  },
  combo: {
    type: 'rect',                      // 'rect' | 'circle'
    style: {
      fill: '#f0f5ff',
      stroke: '#adc6ff',
      lineWidth: 1,
      radius: 8,                       // border radius
      padding: 20,                     // inner padding
      labelText: (d) => d.data.label,
      labelPlacement: 'top',
      labelFill: '#1d39c4',
      labelFontWeight: 600,
      // size after collapse
      collapsedSize: [60, 30],
      collapsedFill: '#1783FF',
    },
  },
  layout: { type: 'antv-dagre', rankdir: 'LR', nodesep: 20, ranksep: 60 },
  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    'drag-element',
    {
      type: 'collapse-expand',
      trigger: 'dblclick',           // double-click combo to collapse/expand
    },
  ],
});

graph.render();
```

## Circle Combo (circle-combo)

```javascript
combo: {
  type: 'circle',
  style: {
    fill: '#f0f5ff',
    stroke: '#adc6ff',
    lineWidth: 1,
    padding: 10,
    labelText: (d) => d.data.label,
    labelPlacement: 'top',
  },
},
```

## Nested Combo

When nesting combos, the child combo specifies the parent combo ID through the `combo` field, and **the parent combo must be defined in the `combos` array**:

```javascript
data: {
  combos: [
     { id: 'parent', data: { label: 'Parent Company' } },           // Parent combo
     { id: 'child1', combo: 'parent', data: { label: 'Subsidiary A' } },  // Child combo
     { id: 'child2', combo: 'parent', data: { label: 'Subsidiary B' } },  // Child combo
  ],
  nodes: [
     { id: 'n1', combo: 'child1', data: { label: 'Employee 1' } },
     { id: 'n2', combo: 'child1', data: { label: 'Employee 2' } },
     { id: 'n3', combo: 'child2', data: { label: 'Employee 3' } },
  ],
},
```

## Combo as Edge Endpoints

G6 5.x supports using combos as the source or target of edges:

```javascript
data: {
  nodes: [
    { id: 'n1', combo: 'c1' },
    { id: 'n2', combo: 'c2' },
  ],
  edges: [
    { source: 'c1', target: 'n2' },    // From combo to node
    { source: 'c1', target: 'c2' },   // From combo to combo
  ],
  combos: [
    { id: 'c1', data: { label: 'Group 1' } },
    { id: 'c2', data: { label: 'Group 2' } },
  ],
},
```

## Collapse / Expand API

```javascript
// Collapse combo
await graph.collapseElement('c1');

// Expand combo
await graph.expandElement('c1');

// Check if collapsed
const isCollapsed = graph.isCollapsed('c1');
```

## Initial Collapsed State

Set the initial collapsed state of a combo in the data:

```javascript
combos: [
  { 
    id: 'c1', 
    data: { label: 'Collapsed Group' },
    style: { collapsed: true }        // Initially collapsed
  },
],
```

## Combo Style Attribute Reference

| Attribute | Type | Default Value | Description |
|------|------|--------|------|
| `fill` | `string` | — | Background fill color |
| `stroke` | `string` | — | Border color |
| `lineWidth` | `number` | `1` | Border width |
| `padding` | `number \| number[]` | `10` | Inner padding |
| `radius` | `number` | `0` | Border radius (rect combo) |
| `collapsed` | `boolean` | `false` | Whether collapsed |
| `collapsedSize` | `[number, number]` | — | Size after collapse |
| `collapsedFill` | `string` | — | Fill color after collapse |
| `labelText` | `string \| ((d) => string)` | — | Label text |
| `labelPlacement` | `'top' \| 'bottom' \| 'center'` | `'top'` | Label position |

## Common Errors and Fixes

### Error: Parent combo mistakenly identified as a regular node

When parsing mixed data, a parent combo (a container referenced by other combos) without clear combo characteristics (such as no `style.collapsed`) can be misidentified as a regular node, resulting in a `Node not found` error.

```javascript
// ❌ Error: combo2 identified as a node
const rawData = [
  {"id":"combo1","combo":"combo2"},  // combo1 belongs to combo2
  {"id":"combo2"},                    // Parent combo, but may be misidentified as a node
];

// Incorrect parsing logic (causes combo2 to become a node instead of a combo)
const nodes = rawData.filter(item => !item.combo && !item.style?.collapsed);
const combos = rawData.filter(item => item.combo || item.style?.collapsed);

// ✅ Correct: First collect all combo IDs, including referenced parent combos
const comboIds = new Set();
rawData.forEach(item => {
  if (item.combo) comboIds.add(item.combo);  // Collect parent combo IDs
  if (item.style?.collapsed !== undefined || item.combo) {
    comboIds.add(item.id);  // Collect explicit combos
  }
});

// Then categorize based on comboIds
const nodes = rawData.filter(item => !comboIds.has(item.id));
const combos = rawData.filter(item => comboIds.has(item.id));
```

### Error: Placing Business Data (`labelText`) in the `style` Field Instead of the `data` Field of a Combo

```javascript
// ❌ The `style` field is used for style overrides (coordinates, dimensions, etc.), not for storing business data
combos: [
  { id: 'a', style: { labelText: 'Combo A' } },
],
combo: {
  style: {
    labelText: (d) => d.style.labelText,  // May fail during style calculation
  },
},

// ✅ Business data should be placed in the `data` field
combos: [
  { id: 'a', data: { label: 'Combo A' } },
],
combo: {
  style: {
    labelText: (d) => d.data.label,
  },
},
```

### Error: Circle Combo Using `radius` Property

```javascript
// ❌ radius is only valid for rect combo (for rounded corners), circle combo radius is automatically calculated based on content
combo: {
  type: 'circle',
  style: { radius: 10 },   // Invalid, will not take effect
},

// ✅ Use padding to control the inner margin of circle combo
combo: {
  type: 'circle',
  style: { padding: 10 },
},
```

### Error: Node combo field references a non-existent combo id

```javascript
// ❌ combo 'cx' is not defined in the combos array
nodes: [{ id: 'n1', combo: 'cx', data: {} }],
combos: [],

// ✅ Ensure the combo id exists
combos: [{ id: 'cx', data: { label: 'Group' } }],
nodes: [{ id: 'n1', combo: 'cx', data: {} }],
```

### Error: Edge references an undefined combo as an endpoint

```javascript
// ❌ Combo 'c1' is not defined in the combos array, but an edge references it
edges: [{ source: 'c1', target: 'n1' }],
nodes: [{ id: 'n1' }],
combos: [],

// ✅ Ensure the combo referenced as an edge endpoint is defined
combos: [{ id: 'c1', data: { label: 'Group 1' } }],
nodes: [{ id: 'n1' }],
edges: [{ source: 'c1', target: 'n1' }],
```