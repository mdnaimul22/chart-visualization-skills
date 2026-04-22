---
id: g6-mds-layout-cluster-graph
title: G6 MDS Layout Cluster Graph Visualization
description: Build graph visualization using G6's MDS (Multidimensional Scaling) layout, where nodes display different colors based on the cluster field. Supports canvas zoom, drag, and element drag interactions. Covers data format specifications, node style mappings, color palette configurations, and common error fixes.
library: G6
version: 5.x
category: layout
tags:
  - mds
  - layout
  - cluster
  - graph
  - interaction
  - color palette
  - palette
---

# G6 MDS Layout Clustering Visualization

(Note: The original content provided only contained a header. The translation maintains the same structure and syntax as instructed.)

## Overview

MDS (Multidimensional Scaling) layout constructs a distance matrix between nodes and attempts to preserve the relative distances between nodes in high-dimensional space within a two-dimensional space. It is suitable for displaying the similarity or structural relationships between nodes.

This skill introduces how to:
1. Properly organize G6 graph data format (`nodes` + `edges` top-level structure)
2. Configure MDS layout
3. Use `palette` to automatically map colors based on the node's `cluster` field
4. Enable canvas zoom, drag, and element drag interactions

---

## Key Knowledge Points

### 1. Data Format

G6's `data` configuration item must contain top-level `nodes` and `edges` arrays, **and cannot directly pass in a node array**:

```js
// ✅ Correct
const graph = new Graph({
  data: {
    nodes: [ { id: '0', data: { cluster: 'a' } }, ... ],
    edges: [ { source: '0', target: '1' }, ... ],
  },
});

// ❌ Incorrect —— Directly passing in a node array
const graph = new Graph({
  data: [ { id: '0', data: { cluster: 'a' } }, ... ],
});
```

### 2. MDS Layout Configuration

```js
layout: {
  type: 'mds',
  linkDistance: 100,  // Ideal distance between nodes, default is 50
  // center optional, default is [0, 0]
}
```

### 3. Node Color Mapping by Cluster (palette)

Use `node.palette` to automatically assign colors based on node data fields, eliminating the need to manually enumerate colors for each cluster:

```js
node: {
  palette: {
    field: 'cluster',   // Group by the data.cluster field
    color: 'tableau',   // Use built-in color palette, or pass in a color array
  },
}
```

### 4. Built-in Interaction Behaviors

| Behavior Name    | Description          |
| ---------------- | ---------------- |
| `drag-canvas`    | Drag canvas       |
| `zoom-canvas`    | Zoom canvas with mouse wheel |
| `drag-element`   | Drag node/edge    |

```js
behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
```

---

## Minimum Viable Example

```js
import { Graph } from '@antv/g6';

const data = {
  nodes: [
    { id: '0',  data: { cluster: 'a' } },
    { id: '1',  data: { cluster: 'a' } },
    { id: '2',  data: { cluster: 'a' } },
    { id: '3',  data: { cluster: 'a' } },
    { id: '4',  data: { cluster: 'a' } },
    { id: '5',  data: { cluster: 'a' } },
    { id: '6',  data: { cluster: 'a' } },
    { id: '7',  data: { cluster: 'a' } },
    { id: '8',  data: { cluster: 'a' } },
    { id: '9',  data: { cluster: 'a' } },
    { id: '10', data: { cluster: 'a' } },
    { id: '11', data: { cluster: 'a' } },
    { id: '12', data: { cluster: 'a' } },
    { id: '13', data: { cluster: 'b' } },
    { id: '14', data: { cluster: 'b' } },
    { id: '15', data: { cluster: 'b' } },
    { id: '16', data: { cluster: 'b' } },
    { id: '17', data: { cluster: 'b' } },
    { id: '18', data: { cluster: 'c' } },
    { id: '19', data: { cluster: 'c' } },
    { id: '20', data: { cluster: 'c' } },
    { id: '21', data: { cluster: 'c' } },
    { id: '22', data: { cluster: 'c' } },
    { id: '23', data: { cluster: 'c' } },
    { id: '24', data: { cluster: 'c' } },
    { id: '25', data: { cluster: 'c' } },
    { id: '26', data: { cluster: 'c' } },
    { id: '27', data: { cluster: 'c' } },
    { id: '28', data: { cluster: 'c' } },
    { id: '29', data: { cluster: 'c' } },
    { id: '30', data: { cluster: 'c' } },
    { id: '31', data: { cluster: 'd' } },
    { id: '32', data: { cluster: 'd' } },
    { id: '33', data: { cluster: 'd' } },
  ],
  edges: [
    { source: '0',  target: '1'  },
    { source: '0',  target: '2'  },
    { source: '0',  target: '3'  },
    { source: '0',  target: '4'  },
    { source: '0',  target: '5'  },
    { source: '0',  target: '7'  },
    { source: '0',  target: '8'  },
    { source: '0',  target: '9'  },
    { source: '0',  target: '10' },
    { source: '0',  target: '11' },
    { source: '0',  target: '13' },
    { source: '0',  target: '14' },
    { source: '0',  target: '15' },
    { source: '0',  target: '16' },
    { source: '2',  target: '3'  },
    { source: '4',  target: '5'  },
    { source: '4',  target: '6'  },
    { source: '5',  target: '6'  },
    { source: '7',  target: '13' },
    { source: '8',  target: '14' },
    { source: '9',  target: '10' },
    { source: '10', target: '22' },
    { source: '10', target: '14' },
    { source: '10', target: '12' },
    { source: '10', target: '24' },
    { source: '10', target: '21' },
    { source: '10', target: '20' },
    { source: '11', target: '24' },
    { source: '11', target: '22' },
    { source: '11', target: '14' },
    { source: '12', target: '13' },
    { source: '16', target: '17' },
    { source: '16', target: '18' },
    { source: '16', target: '21' },
    { source: '16', target: '22' },
    { source: '17', target: '18' },
    { source: '17', target: '20' },
    { source: '18', target: '19' },
    { source: '19', target: '20' },
    { source: '19', target: '33' },
    { source: '19', target: '22' },
    { source: '19', target: '23' },
    { source: '20', target: '21' },
    { source: '21', target: '22' },
    { source: '22', target: '24' },
    { source: '22', target: '25' },
    { source: '22', target: '26' },
    { source: '22', target: '23' },
    { source: '22', target: '28' },
    { source: '22', target: '30' },
    { source: '22', target: '31' },
    { source: '22', target: '32' },
    { source: '22', target: '33' },
    { source: '23', target: '28' },
    { source: '23', target: '27' },
    { source: '23', target: '29' },
    { source: '23', target: '30' },
    { source: '23', target: '31' },
    { source: '23', target: '33' },
    { source: '32', target: '33' },
  ],
};

const graph = new Graph({
  container: 'container',
  autoFit: 'view',
  padding: 20,
  data,
  node: {
    style: {
      labelText: (d) => d.id,
      labelFill: '#fff',
      labelPlacement: 'center',
      labelFontSize: 10,
    },
    // Automatically assign colors based on the 'cluster' field
    palette: {
      field: 'cluster',
      color: 'tableau',
    },
  },
  layout: {
    type: 'mds',
    nodeSize: 32,
    linkDistance: 100,
  },
  behaviors: ['drag-element', 'drag-canvas', 'zoom-canvas'],
});

graph.render();
```

---

## Complete Configuration Guide

### Graph Configuration Options

| Configuration Item | Description                                          | Type                    | Example Value                              |
| ------------------ | ---------------------------------------------------- | ----------------------- | ------------------------------------------ |
| `container`        | DOM id or HTMLElement of the mounting container      | `string \| HTMLElement` | `'container'`                              |
| `autoFit`          | Auto-fit viewport, `'view'` means scaling to full visibility | `'view' \| 'center'`    | `'view'`                                   |
| `padding`          | Inner padding (in pixels) during auto-fit            | `number \| number[]`    | `20`                                       |
| `data`             | Graph data, must include top-level fields `nodes` and `edges` | `GraphData`             | `{ nodes: [...], edges: [...] }`           |
| `node`             | Global node configuration (style, color palette, etc.) | `NodeOptions`           | See below                                  |
| `layout`           | Layout algorithm configuration                       | `LayoutOptions`         | `{ type: 'mds', linkDistance: 100 }`       |
| `behaviors`        | List of interaction behaviors                        | `string[]`              | `['drag-element', 'drag-canvas', 'zoom-canvas']` |

### MDS Layout Configuration Options

| Configuration Item | Description                      | Type      | Default Value |
| ------------------ | -------------------------------- | --------- | ------------- |
| `type`             | Layout type, fixed as `'mds'`    | `string`  | -             |
| `linkDistance`     | Ideal distance between nodes     | `number`  | `50`          |
| `center`           | Layout center coordinates `[x, y]` | `number[]` | `[0, 0]`      |

### Node Palette Configuration

| Configuration | Description                                                  | Type                    | Example Value  |
| ------------- | ------------------------------------------------------------ | ----------------------- | -------------- |
| `field`       | Data field name used for grouping (corresponds to the field in `node.data`) | `string`                | `'cluster'`    |
| `color`       | Color palette name or array of colors                        | `string \| string[]`    | `'tableau'`    |

---

## Common Errors and Fixes

### Error 1: Directly Passing a Node Array Instead of a GraphData Object

**Cause of Error**: The reference data provided in the query description is a node array (e.g., `[{"id":"0","data":{"cluster":"a"}},...]`), and the LLM may directly assign it to `data`, causing G6 to fail to recognize the data format.

```js
// ❌ Incorrect Usage —— data is directly a node array
const graph = new Graph({
  data: [
    { id: '0', data: { cluster: 'a' } },
    { id: '1', data: { cluster: 'a' } },
    // ...
  ],
});
```

```js
// ✅ Correct Usage —— data must be an object containing nodes/edges
const graph = new Graph({
  data: {
    nodes: [
      { id: '0', data: { cluster: 'a' } },
      { id: '1', data: { cluster: 'a' } },
      // ...
    ],
    edges: [
      { source: '0', target: '1' },
      // ...
    ],
  },
});
```

### Error 2: Hardcoding Node Colors Instead of Using Palette Mapping

**Cause of Error**: Manually using `if/switch` statements in `style.fill` to determine cluster values leads to code redundancy and difficulty in maintenance.

```js
// ❌ Not Recommended —— Manual Color Enumeration
node: {
  style: {
    fill: (d) => {
      if (d.data.cluster === 'a') return '#5B8FF9';
      if (d.data.cluster === 'b') return '#61DDAA';
      if (d.data.cluster === 'c') return '#F6BD16';
      return '#CCC';
    },
  },
},
```

```js
// ✅ Recommended —— Using Palette for Automatic Mapping
node: {
  palette: {
    field: 'cluster',   // Specify grouping field
    color: 'tableau',   // Use built-in color palette
  },
},
```

### Error 3: Missing `edges` Field Causes Layout Abnormalities

**Cause of Error**: The MDS layout relies on the connection relationships of edges to construct a distance matrix. If `edges` are missing in `data`, the layout result may degenerate into a random distribution.

```js
// ❌ Incorrect —— Missing edges
const graph = new Graph({
  data: {
    nodes: [ ... ],
    // edges not provided
  },
  layout: { type: 'mds' },
});
```

```js
// ✅ Correct —— Providing complete nodes and edges
const graph = new Graph({
  data: {
    nodes: [ ... ],
    edges: [ { source: '0', target: '1' }, ... ],
  },
  layout: { type: 'mds', linkDistance: 100 },
});
```

### Error 4: Label Displayed Outside Node Instead of Centered

**Cause of Error**: The default `labelPlacement` is `'bottom'`. To display the label inside the node, explicitly set it to `'center'` and adjust `labelFill` color to ensure readability.

```js
// ❌ Label displayed below the node (default behavior)
node: {
  style: {
    labelText: (d) => d.id,
  },
},
```

```js
// ✅ Label centered inside the node
node: {
  style: {
    labelText: (d) => d.id,
    labelPlacement: 'center',  // Center the label
    labelFill: '#fff',          // White text, contrasting with node fill color
    labelFontSize: 10,
  },
},
```

---

## Extension: Dynamic Layout Switching

To switch to another layout (e.g., Force) at runtime, use `graph.setLayout`:

```js
// Switch to force-directed layout
graph.setLayout({
  type: 'force',
  gravity: 10,
  linkDistance: 80,
});
await graph.layout();
```

---

## Reference Documents

- [MDS Layout Documentation](/manual/layout/mds-layout)
- [Layout Overview](/manual/layout/overview)
- [Common Node Configuration Items](/manual/element/node/base-node)
- [Graph Data Format](/manual/data)
- [Graph Configuration Items](/manual/graph/option)