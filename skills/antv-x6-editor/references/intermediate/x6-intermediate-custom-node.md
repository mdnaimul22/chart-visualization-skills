---
id: "x6-intermediate-custom-node"
title: "X6 Custom Node"
description: |
  Comprehensive guide to X6 custom nodes: Graph.registerNode for registering custom SVG nodes, Shape.HTML.register for registering HTML nodes.
  Includes markup/attrs customization, inheriting built-in nodes, HTML node rendering and updating, and effect responsiveness.

library: "x6"
version: "3.x"
category: "intermediate"
subcategory: "custom-node"
tags:
  - "custom node"
  - "registerNode"
  - "Graph.registerNode"
  - "Shape.HTML.register"
  - "HTML node"
  - "markup"
  - "attrs"
  - "inherit"
  - "foreignObject"
  - "shape"
  - "effect"
  - "custom shape"
  - "Shape.Group"
  - "grouped node"
  - "parent-child node"
  - "embed"
  - "addChild"
  - "box-sizing"
  - "font-size"
  - "Invalid left-hand side"
  - "style property"
  - "camelCase"

related:
  - "x6-core-node"
  - "x6-core-graph-init"
  - "x6-intermediate-tools"

use_cases:
  - "Register custom SVG node shapes"
  - "Render complex node content using HTML/DOM"
  - "Inherit and extend built-in nodes"
  - "Implement data-driven responsive HTML nodes"
  - "Reuse custom node configurations"

anti_patterns:
  - "Do not use position:absolute/relative/transform/opacity in HTML nodes (may cause rendering issues)"
  - "Do not forget to set the effect field, otherwise HTML nodes will not respond to data changes"
  - "Do not use Shape.Group / Shape.Group.define / new Shape.Group, the Shape namespace in X6 3.x does not have Group"
  - "Do not use hyphenated properties like el.style.box-sizing / el.style.font-size in html() callbacks, use camelCase or bracket notation instead"
---

# X6 Custom Nodes

## Method 1: Graph.registerNode (SVG Node)

Customize the node appearance through `markup` (structure) and `attrs` (style), then register it as a custom shape.

### Basic Registration

```javascript
import { Graph } from '@antv/x6';

Graph.registerNode(
  'custom-rect',
  {
    inherit: 'rect',  // Inherit from built-in rect node
    width: 120,
    height: 50,
    attrs: {
      body: {
        fill: '#ffffff',
        stroke: '#1890ff',
        strokeWidth: 2,
        rx: 8,
        ry: 8,
      },
      label: {
        fontSize: 14,
        fill: '#333',
      },
    },
  },
  true, // Override registration with the same name
);

// Use custom node
const graph = new Graph({ container: 'container', width: 800, height: 600 });

graph.addNode({
  shape: 'custom-rect',
  x: 100,
  y: 100,
  label: 'Custom Node',
});
```

### Custom Markup (Multi-Element Node)

```javascript
Graph.registerNode(
  'status-node',
  {
    inherit: 'rect',
    width: 160,
    height: 60,
    markup: [
      { tagName: 'rect', selector: 'body' },
      { tagName: 'circle', selector: 'statusIndicator' },
      { tagName: 'text', selector: 'label' },
      { tagName: 'text', selector: 'description' },
    ],
    attrs: {
      body: {
        refWidth: '100%',
        refHeight: '100%',
        fill: '#fff',
        stroke: '#d9d9d9',
        strokeWidth: 1,
        rx: 6,
        ry: 6,
      },
      statusIndicator: {
        r: 5,
        cx: 15,
        cy: 15,
        fill: '#52c41a',  // Green=Normal
      },
      label: {
        refX: 30,
        refY: 15,
        fontSize: 14,
        fill: '#333',
        textAnchor: 'start',
        textVerticalAnchor: 'middle',
        text: 'Node',
      },
      description: {
        refX: 15,
        refY: 40,
        fontSize: 12,
        fill: '#999',
        textAnchor: 'start',
        textVerticalAnchor: 'middle',
        text: 'Description',
      },
    },
  },
  true,
);

graph.addNode({
  shape: 'status-node',
  x: 100,
  y: 100,
  attrs: {
    label: { text: 'Data Processing' },
    description: { text: 'ETL Pipeline' },
    statusIndicator: { fill: '#52c41a' },
  },
});
```

### Diamond Decision Node (polygon)

```javascript
Graph.registerNode(
  'decision-node',
  {
    inherit: 'polygon',
    width: 80,
    height: 80,
    attrs: {
      body: {
        refPoints: '0,10 10,0 20,10 10,20',  // Diamond vertices
        fill: '#fff',
        stroke: '#faad14',
        strokeWidth: 2,
      },
      label: {
        fontSize: 12,
        fill: '#333',
        refX: 0.5,
        refY: 0.5,
        textAnchor: 'middle',
        textVerticalAnchor: 'middle',
      },
    },
  },
  true,
);
```

## Method Two: Shape.HTML.register (HTML Node)

Use HTML/DOM to render complex node content (tables, charts, rich text, etc.), implemented based on SVG `foreignObject`.

### Basic Usage

```javascript
import { Graph, Shape } from '@antv/x6';

Shape.HTML.register({
  shape: 'custom-html',
  width: 200,
  height: 80,
  html() {
    const div = document.createElement('div');
    div.style.width = '100%';
    div.style.height = '100%';
    div.style.background = '#fff';
    div.style.border = '1px solid #d9d9d9';
    div.style.borderRadius = '8px';
    div.style.display = 'flex';
    div.style.alignItems = 'center';
    div.style.justifyContent = 'center';
    div.style.fontSize = '14px';
    div.style.color = '#333';
    div.textContent = 'HTML Node';
    return div;
  },
});

const graph = new Graph({ container: 'container', width: 800, height: 600 });

graph.addNode({
  shape: 'custom-html',
  x: 100,
  y: 100,
});
```

### Responsive HTML Node (Data-Driven Updates)

Declare dependencies through the `effect` field. When these properties change, the `html()` method is automatically re-invoked to update the DOM.

```javascript
import { Graph, Shape, Dom } from '@antv/x6';

Shape.HTML.register({
  shape: 'data-card',
  width: 200,
  height: 100,
  effect: ['data'],  // Listen for data changes
  html(cell) {
    const { title, status, progress } = cell.getData() || {};
    const div = document.createElement('div');
    Dom.css(div, {
      width: '100%',
      height: '100%',
      background: '#fff',
      border: '1px solid #d9d9d9',
      borderRadius: '8px',
      padding: '12px',
      boxSizing: 'border-box',
      fontFamily: 'Arial, sans-serif',
    });
    div.innerHTML = `
      <div style="font-size:14px;font-weight:bold;color:#333">${title || 'Untitled'}</div>
      <div style="font-size:12px;color:#999;margin-top:4px">Status: ${status || 'pending'}</div>
      <div style="margin-top:8px;height:6px;background:#f0f0f0;border-radius:3px">
        <div style="width:${(progress || 0) * 100}%;height:100%;background:#1890ff;border-radius:3px"></div>
      </div>
    `;
    return div;
  },
});

const graph = new Graph({ container: 'container', width: 800, height: 600 });

const node = graph.addNode({
  shape: 'data-card',
  x: 100,
  y: 100,
  data: { title: 'Data Cleaning', status: 'running', progress: 0.6 },
});

// Node automatically refreshes after updating data
node.setData({ title: 'Data Cleaning', status: 'completed', progress: 1.0 });
```

### ER Diagram Table Node

```javascript
Shape.HTML.register({
  shape: 'er-table',
  width: 200,
  height: 150,
  effect: ['data'],
  html(cell) {
    const { tableName, fields } = cell.getData() || {};
    const div = document.createElement('div');
    Dom.css(div, {
      width: '100%',
      height: '100%',
      background: '#fff',
      border: '1px solid #5B8FF9',
      borderRadius: '4px',
      overflow: 'hidden',
      fontFamily: 'monospace',
      fontSize: '12px',
    });
    const header = `<div style="background:#5B8FF9;color:#fff;padding:6px 8px;font-weight:bold">${tableName || 'table'}</div>`;
    const rows = (fields || [])
      .map((f) => `<div style="padding:4px 8px;border-bottom:1px solid #f0f0f0">${f.name}: <span style="color:#999">${f.type}</span></div>`)
      .join('');
    div.innerHTML = header + rows;
    return div;
  },
});

graph.addNode({
  shape: 'er-table',
  x: 100,
  y: 100,
  data: {
    tableName: 'users',
    fields: [
      { name: 'id', type: 'int' },
      { name: 'name', type: 'varchar' },
      { name: 'email', type: 'varchar' },
    ],
  },
});
```

## Cooperate with Ports

Custom nodes can be used with ports:

```javascript
graph.addNode({
  shape: 'custom-rect',
  x: 100,
  y: 100,
  label: 'With Ports',
  ports: {
    groups: {
      in: {
        position: 'left',
        attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
      out: {
        position: 'right',
        attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
    },
    items: [
      { id: 'in-1', group: 'in' },
      { id: 'out-1', group: 'out' },
    ],
  },
});
```

## Common Errors

### ❌ `Shape.Group` / `Shape.Group.define()` Does Not Exist

The `Shape` namespace in X6 3.x **only exports**: `Circle / Edge / Ellipse / HTML / Image / Path / Polygon / Polyline / Rect / TextBlock`. **There is no `Group`**. The following code will throw `Cannot read properties of undefined (reading 'define')` / `Shape.Group is not a constructor` at runtime:

```javascript
// ❌
Shape.Group.define({ shape: 'dept-group', ... });
new Shape.Group({ ... });
import { Group } from '@antv/x6'; // ❌ The main package also does not export Group
```

**Correct Approaches for Parent-Child Grouping / Container Nodes (Choose One):**

```javascript
// 1) Use a regular rect as the parent node and establish parent-child relationships via embed / addChild
const parent = graph.addNode({ shape: 'rect', x: 40, y: 40, width: 300, height: 200, label: 'Department', attrs: { body: { fill: '#f5f5f5', stroke: '#999' } } });
const child  = graph.addNode({ shape: 'rect', x: 80, y: 90, width: 100, height: 40, label: 'Employee A' });
parent.addChild(child);            // Maintain parent-child relationship
// Alternatively: parent.embed(child)         // Embed (depends on Graph's embedding configuration)

// 2) Register a custom group shape and use it
Graph.registerNode('dept-group', {
  inherit: 'rect',
  width: 300, height: 200,
  attrs: {
    body: { fill: '#f5f5f5', stroke: '#999', strokeDasharray: '4,2' },
    label: { refX: 8, refY: 8, textAnchor: 'start', textVerticalAnchor: 'top' },
  },
});
graph.addNode({ shape: 'dept-group', x: 40, y: 40, label: 'Department' });

// 3) Enable embedding interaction in Graph constructor options (not a plugin!)
const graph = new Graph({
  container: 'container',
  embedding: { enabled: true, findParent: 'bbox', frontOnly: false },
});
```

> Similarly, `Shape.Cylinder` / `Shape.Diamond` / `Shape.Cloud`, etc., do not exist. For custom shapes, use either `'polygon'` with custom `points` or `Graph.registerNode` with custom `markup`.

### ❌ HTML Node `el.style.box-sizing = '...'` Throws Invalid Left-Hand Side

In the `html(node)` callback of `Shape.HTML.register` or any DOM operation, **do not** directly assign hyphenated property names to `style`—JS will parse `style.box-sizing` as `style.box - sizing` (a subtraction expression) and throw `Uncaught SyntaxError: Invalid left-hand side in assignment`, causing the entire script to fail:

```javascript
// ❌ All will throw Invalid left-hand side in assignment
html() {
  const wrap = document.createElement('div');
  wrap.style.box-sizing      = 'border-box';
  wrap.style.font-size       = '14px';
  wrap.style.background-color= '#fff';
  wrap.style.border-radius   = '8px';
  return wrap;
}
```

**Correct Approaches (Choose any, first two recommended):**

```javascript
// 1) Camel Case
wrap.style.boxSizing       = 'border-box';
wrap.style.fontSize        = '14px';
wrap.style.backgroundColor = '#fff';
wrap.style.borderRadius    = '8px';

// 2) Square Brackets (Preserve Hyphens)
wrap.style['box-sizing']     = 'border-box';
wrap.style['font-size']      = '14px';
wrap.style['background-color']= '#fff';
wrap.style['border-radius']  = '8px';

// 3) cssText in One Go
wrap.style.cssText = 'box-sizing:border-box;font-size:14px;background:#fff;border-radius:8px;';

// 4) Object.assign for Batch Assignment
Object.assign(wrap.style, {
  boxSizing: 'border-box', fontSize: '14px',
  backgroundColor: '#fff', borderRadius: '8px',
});
```

### ❌ Rendering Anomalies Caused by `position:absolute` in HTML Nodes

```javascript
// Error: Using absolute positioning within foreignObject may result in incomplete display
html() {
  const div = document.createElement('div');
  div.style.position = 'absolute';  // ❌ May cause rendering anomalies
  return div;
}

// Correct: Use flex or normal flow layout
html() {
  const div = document.createElement('div');
  div.style.display = 'flex';  // ✅
  return div;
}
```

### ❌ Forgetting to Set `effect` Causes Node Not to Update

```javascript
// Error: Node does not refresh after modifying data
Shape.HTML.register({
  shape: 'my-node',
  html(cell) {
    const { value } = cell.getData();
    // ...
  },
  // Missing effect: ['data']
});

// Correct: Declare effect
Shape.HTML.register({
  shape: 'my-node',
  effect: ['data'],  // ✅ Listen for data changes
  html(cell) {
    const { value } = cell.getData();
    // ...
  },
});
```

### ❌ registerNode Not Setting the Third Parameter Causes Duplicate Registration Error

```javascript
// Error: Throws an error on duplicate registration
Graph.registerNode('my-node', { ... });
Graph.registerNode('my-node', { ... }); // Error: already registered

// Correct: Pass true as the third parameter to allow override
Graph.registerNode('my-node', { ... }, true);
```