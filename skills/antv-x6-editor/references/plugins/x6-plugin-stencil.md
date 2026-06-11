---
id: "x6-plugin-stencil"
title: "X6 Stencil Drag Panel Plugin"
description: |
  Stencil is a sidebar drag panel that provides grouped display and search functionality for predefined node templates.
  Users can drag nodes from the Stencil panel onto the canvas, commonly used in flowchart editors and DAG editor toolboxes.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "stencil"
tags:
  - "stencil"
  - "drag panel"
  - "sidebar"
  - "toolbox"
  - "node template"
  - "grouping"
  - "search"
  - "drag"
  - "panel"

related:
  - "x6-plugins"
  - "x6-plugin-dnd"
  - "x6-core-graph-init"
  - "x6-pattern-flowchart"

use_cases:
  - "Left-side node panel in flowchart editors"
  - "Node toolbox with grouping"
  - "Component library panel with search support"
  - "Drag predefined nodes from sidebar to canvas"

difficulty: "intermediate"
completeness: "full"
---

## Core Concepts

**Stencil** is an independent sidebar component that maintains a separate small canvas for displaying node templates. Users drag nodes from the Stencil to the target canvas, and the Stencil internally uses the Dnd plugin to implement drag-and-drop logic.

Stencil Features:
- Supports **grouping** of node templates
- Supports **search filtering**
- Supports **collapse/expand** of groups
- Supports custom **layout** (grid layout, etc.)
- Allows customization of `dragNode` and `dropNode` during drag-and-drop

## Basic Usage

```javascript
import { Graph, Stencil } from '@antv/x6';

// 1. Create the target canvas
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  grid: { visible: true },
});

// 2. Register the Stencil plugin using graph.use()
const stencil = new Stencil({
  title: 'Component Library',
  target: graph,
  stencilGraphWidth: 200,
  stencilGraphHeight: 300,
  groups: [
    { name: 'basic', title: 'Basic Nodes' },
    { name: 'advanced', title: 'Advanced Nodes' },
  ],
});
graph.use(stencil);

// 3. Mount the Stencil container to the DOM
document.getElementById('stencil-container').appendChild(stencil.container);

// 4. Load node templates into groups (recommended to use graph.createNode to create node templates)
const rect = graph.createNode({
  shape: 'rect',
  width: 80,
  height: 40,
  label: 'Rectangle',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f' } },
});

const circle = graph.createNode({
  shape: 'circle',
  width: 60,
  height: 60,
  label: 'Circle',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f' } },
});

stencil.load([rect, circle], 'basic');

stencil.load(
  [
    graph.createNode({
      shape: 'rect',
      width: 80,
      height: 40,
      label: 'Custom',
      attrs: { body: { fill: '#efdbff', stroke: '#9254de', rx: 6, ry: 6 } },
    }),
  ],
  'advanced',
);
```

## Configuration Options

### StencilOptions

| Parameter | Type | Required | Default Value | Description |
|------|------|------|--------|------|
| `target` | `Graph` | ✓ | - | Target canvas instance |
| `title` | `string` | | `'Stencil'` | Panel title |
| `groups` | `StencilGroup[]` | | - | Group configuration |
| `stencilGraphWidth` | `number` | | `200` | Width of the canvas inside the panel |
| `stencilGraphHeight` | `number` | | `800` | Height of the canvas inside the panel |
| `stencilGraphPadding` | `number` | | - | Inner padding of the canvas inside the panel |
| `stencilGraphOptions` | `Options` | | - | Additional configuration for the canvas inside the panel |
| `collapsable` | `boolean` | | `false` | Whether groups can be collapsed |
| `search` | `boolean \| Function \| object` | | - | Search configuration |
| `placeholder` | `string` | | `'Search'` | Placeholder text for the search input box |
| `notFoundText` | `string` | | `'No matches found'` | No results found prompt for search |
| `layout` | `Function` | | Grid layout | Node layout function |
| `layoutOptions` | `object` | | - | Layout parameters |
| `getDragNode` | `Function` | | Clone source node | Custom node during drag |
| `getDropNode` | `Function` | | Clone dragged node | Custom node when dropped onto the canvas |
| `validateNode` | `Function` | | - | Validate if a node can be dropped |

### StencilGroup

| Parameter | Type | Required | Default Value | Description |
|------|------|------|--------|------|
| `name` | `string` | ✓ | - | Unique identifier for the group |
| `title` | `string` | | `name` | Display title for the group |
| `collapsed` | `boolean` | | `false` | Whether the group is collapsed by default |
| `collapsable` | `boolean` | | Inherited from parent | Whether the group is collapsible |
| `graphWidth` | `number` | | Inherited from `stencilGraphWidth` | Canvas width for the group |
| `graphHeight` | `number` | | Inherited from `stencilGraphHeight` | Canvas height for the group |
| `graphPadding` | `number` | | Inherited | Inner padding for the group canvas |
| `graphOptions` | `Options` | | - | Additional configuration for the group canvas |
| `layout` | `Function` | | Inherited from parent | Layout function for the group nodes |
| `layoutOptions` | `object` | | Inherited from parent | Layout parameters for the group |

## Search Configuration

### Enable Search

```javascript
const stencil = new Stencil({
  target: graph,
  search: true,  // Search by shape name by default
  placeholder: 'Search nodes...',
  notFoundText: 'No matching nodes found',
  groups: [{ name: 'basic', title: 'Basic Nodes' }],
});
```

### Custom Search Filtering

```javascript
const stencil = new Stencil({
  target: graph,
  search(cell, keyword, groupName, stencil) {
    // Search by label text
    return cell.attr('label/text')?.includes(keyword) || false;
  },
  groups: [{ name: 'basic', title: 'Basic Nodes' }],
});
```

## Custom Drag and Drop Nodes

```javascript
const stencil = new Stencil({
  target: graph,
  groups: [{ name: 'basic', title: 'Basic Nodes' }],

  // Node displayed during drag (can be simplified)
  getDragNode(sourceNode, options) {
    return sourceNode.clone();
  },

  // Node placed on the canvas (can add extra attributes)
  getDropNode(draggingNode, options) {
    const node = draggingNode.clone();
    node.setAttrs({
      body: { stroke: '#1890ff', strokeWidth: 2 },
    });
    return node;
  },

  // Validate if drop is allowed
  validateNode(droppingNode, options) {
    // Return false to prevent drop
    return true;
  },
});
```

## Custom Layout

By default, a 2-column grid layout is used. It can be customized as follows:

```javascript
const stencil = new Stencil({
  target: graph,
  groups: [{ name: 'basic', title: 'Basic Nodes' }],
  layoutOptions: {
    columns: 2,        // Number of columns
    columnWidth: 90,   // Column width
    rowHeight: 80,     // Row height
    dx: 10,            // X offset
    dy: 10,            // Y offset
    resizeToFit: false,
  },
});
```

## API Methods

| Method | Description |
|------|------|
| `stencil.load(nodes, groupName?)` | Load an array of nodes into the specified group |
| `stencil.load({ groupA: nodes, groupB: nodes })` | Batch load into multiple groups according to object mapping |
| `stencil.unload(nodes, groupName?)` | Remove nodes from the specified group |
| `stencil.unload({ groupA: nodes })` | Batch remove according to object mapping |
| `stencil.toggleGroup(groupName)` | Toggle the expanded/collapsed state of a group |
| `stencil.isGroupCollapsed(groupName)` | Determine if a group is collapsed |
| `stencil.container` | Get the DOM container element of the Stencil |

## Complete Example: Flowchart Editor Toolbox

```javascript
import { Graph, Stencil, Snapline, History } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  grid: { visible: true, size: 10 },
  connecting: {
    allowBlank: false,
    router: 'orth',
    connector: 'rounded',
  },
});

graph.use(new Snapline({ enabled: true }));
graph.use(new History({ enabled: true }));

const stencil = new Stencil({
  title: 'Flow Nodes',
  target: graph,
  stencilGraphWidth: 180,
  stencilGraphHeight: 400,
  collapsable: true,
  search: true,
  placeholder: 'Search nodes',
  groups: [
    { name: 'basic', title: 'Basic Shapes', collapsed: false },
    { name: 'flow', title: 'Flow Control', collapsed: false },
  ],
  layoutOptions: {
    columns: 2,
    columnWidth: 80,
    rowHeight: 60,
    dx: 10,
    dy: 10,
  },
});

document.getElementById('stencil-container').appendChild(stencil.container);

// Basic Shapes
const rect = graph.createNode({
  shape: 'rect',
  width: 60,
  height: 40,
  label: 'Rectangle',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 4, ry: 4 } },
});

const circle = graph.createNode({
  shape: 'circle',
  width: 50,
  height: 50,
  label: 'Circle',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f' } },
});

const ellipse = graph.createNode({
  shape: 'ellipse',
  width: 60,
  height: 40,
  label: 'Ellipse',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f' } },
});

stencil.load([rect, circle, ellipse], 'basic');

// Flow Control
const decision = graph.createNode({
  shape: 'polygon',
  width: 60,
  height: 40,
  label: 'Decision',
  attrs: {
    body: {
      fill: '#fff',
      stroke: '#8f8f8f',
      refPoints: '0,10 10,0 20,10 10,20',
    },
  },
});

const subProcess = graph.createNode({
  shape: 'rect',
  width: 60,
  height: 40,
  label: 'Subprocess',
  attrs: { body: { fill: '#e6f7ff', stroke: '#1890ff', rx: 4, ry: 4 } },
});

stencil.load([decision, subProcess], 'flow');
```

## Common Errors and Fixes

### ❌ Incorrect Usage of layout Configuration as an Object

```javascript
// Error: layout should be a function, not an object
const stencil = new Stencil({
  target: graph,
  layout: { columns: 1 }, // ❌ Error: t.call is not a function
});

// Correct: Use layoutOptions to configure layout parameters
const stencil = new Stencil({
  target: graph,
  layoutOptions: { columns: 1 }, // ✅
});
```

### ❌ Directly Passing a Shape Configuration Object Instead of a Node Instance

```javascript
// Error: Directly passing a shape configuration object may cause rendering anomalies
stencil.load([{ shape: 'rect', width: 80, height: 40 }], 'basic'); // ❌

// Correct: Use graph.createNode to create a node instance
const node = graph.createNode({ shape: 'rect', width: 80, height: 40 });
stencil.load([node], 'basic'); // ✅
```

### ❌ Forgot to Mount Stencil Container to DOM

```javascript
// Error: Only registered the plugin but did not mount the stencil panel to the page DOM
const stencil = new Stencil({ target: graph, groups: [...] });
graph.use(stencil);
// Missing DOM mounting, the panel will not display ❌

// Correct: After registration, also need to mount stencil.container to DOM
const stencil = new Stencil({ target: graph, groups: [...] });
graph.use(stencil);
document.getElementById('panel').appendChild(stencil.container); // ✅
```

### ❌ Forgot to Set Target

```javascript
// Error: Missing target
const stencil = new Stencil({
  groups: [{ name: 'basic', title: 'Basic' }],
}); // ❌ Dragging without a target

// Correct: Must specify the target canvas
const stencil = new Stencil({
  target: graph,  // ✅
  groups: [{ name: 'basic', title: 'Basic' }],
});
```

### ❌ Pass an Array Without Specifying groupName (When Groups Exist)

```javascript
// Not Recommended: When multiple groups exist, not specifying groupName will load into the default group
stencil.load([{ shape: 'rect', width: 80, height: 40 }]); // May not be the expected group

// Recommended Method 1: Specify groupName
stencil.load([{ shape: 'rect', width: 80, height: 40 }], 'basic'); // ✅

// Recommended Method 2: Use Object Mapping for Batch Loading
stencil.load({
  basic: [{ shape: 'rect', width: 80, height: 40 }],
  advanced: [{ shape: 'circle', width: 60, height: 60 }],
}); // ✅
```

</skill>