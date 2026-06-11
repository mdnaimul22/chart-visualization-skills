---
id: "x6-pattern-er"
title: "X6 ER Diagram"
description: |
  Best practices for building ER (Entity-Relationship) diagrams using X6.
  Suitable for database modeling, table structure visualization, and similar scenarios.

library: "x6"
version: "3.x"
category: "patterns"
subcategory: "er"
tags:
  - "ER Diagram"
  - "Entity-Relationship"
  - "Database"
  - "Table Structure"
  - "Fields"
  - "HTML Node"
  - "er router"

related:
  - "x6-core-node"
  - "x6-core-edge"
  - "x6-plugins"

use_cases:
  - "Database Table Structure Visualization"
  - "Entity-Relationship Modeling"
  - "Table Fields and Associations Display"

difficulty: "intermediate"
completeness: "full"
---

## ⚠️ Key Constraints (Must Comply)

1. **Must call `Shape.HTML.register()` to register the `er-entity` node before creating a Graph instance and adding nodes**
2. **The `html(cell)` function in `Shape.HTML.register()` must return a valid DOM element** (cannot return an HTML string)
3. **Use the string `'container'` for the container**, do not use `document.getElementById('container')`
4. **Do not call `graph.render()`** — X6 renders automatically
5. **Do not call `graph.dispose()`** — will cause a white screen

## ER Diagram Core Features

- **Tabular Nodes**: Use HTML nodes to display table names + field lists
- **Relationship Edges**: 1:1, 1:N, N:M annotations
- **ER Router**: Dedicated routing with `router: 'er'` to prevent edges from passing through nodes

## HTML Entity Node Registration

```javascript
import { Graph, Shape } from '@antv/x6';

Shape.HTML.register({
  shape: 'er-entity',
  width: 200,
  height: 120,
  effect: ['data'],
  html(cell) {
    const data = cell.getData() || {};
    const div = document.createElement('div');
    div.style.cssText = 'width:100%;height:100%;border:1px solid #8f8f8f;border-radius:4px;overflow:hidden;font-size:12px;background:#fff;';

    const header = `<div style="background:#1890ff;color:#fff;padding:6px 8px;font-weight:bold;">${data.name || 'Table'}</div>`;
    const fields = (data.fields || []).map(f =>
      `<div style="padding:4px 8px;border-top:1px solid #eee;">
        <span>${f.name}</span>
        <span style="color:#999;float:right">${f.type}</span>
        ${f.pk ? '<span style="color:#fa8c16;margin-left:4px">PK</span>' : ''}
        ${f.fk ? '<span style="color:#1890ff;margin-left:4px">FK</span>' : ''}
      </div>`
    ).join('');

    div.innerHTML = header + '<div style="max-height:200px;overflow-y:auto">' + fields + '</div>';
    return div;
  },
});
```

## Complete ER Diagram Example

```javascript
import { Graph, Shape } from '@antv/x6';

// Register ER Entity Node (as above)
Shape.HTML.register({ shape: 'er-entity', width: 200, height: 120, effect: ['data'], html(cell) { /* ... */ } });

const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
  panning: true,
  mousewheel: { enabled: true, modifiers: 'ctrl' },
});

// User Table
const userTable = graph.addNode({
  shape: 'er-entity',
  x: 40, y: 60,
  data: {
    name: 'User',
    fields: [
      { name: 'id', type: 'INT', pk: true },
      { name: 'name', type: 'VARCHAR(100)' },
      { name: 'email', type: 'VARCHAR(200)' },
      { name: 'created_at', type: 'DATETIME' },
    ],
  },
});

// Order Table
const orderTable = graph.addNode({
  shape: 'er-entity',
  x: 360, y: 40,
  data: {
    name: 'Order',
    fields: [
      { name: 'id', type: 'INT', pk: true },
      { name: 'user_id', type: 'INT', fk: true },
      { name: 'product_id', type: 'INT', fk: true },
      { name: 'amount', type: 'DECIMAL(10,2)' },
      { name: 'status', type: 'VARCHAR(20)' },
    ],
  },
});

// Product Table
const productTable = graph.addNode({
  shape: 'er-entity',
  x: 360, y: 240,
  data: {
    name: 'Product',
    fields: [
      { name: 'id', type: 'INT', pk: true },
      { name: 'name', type: 'VARCHAR(200)' },
      { name: 'price', type: 'DECIMAL(10,2)' },
      { name: 'category_id', type: 'INT', fk: true },
    ],
  },
});

// Relationship Edges
graph.addEdge({
  source: userTable, target: orderTable,
  label: '1:N',
  router: 'er',
  connector: 'rounded',
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
});

graph.addEdge({
  source: productTable, target: orderTable,
  label: '1:N',
  router: 'er',
  connector: 'rounded',
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
});
```

## Relationship Type Annotation

```javascript
// 1:1 Relationship
graph.addEdge({ source: tableA, target: tableB, label: '1:1', router: 'er' });

// 1:N Relationship
graph.addEdge({ source: tableA, target: tableB, label: '1:N', router: 'er' });

// N:M Relationship (typically through a middle table)
graph.addEdge({ source: tableA, target: middleTable, label: 'N', router: 'er' });
graph.addEdge({ source: tableB, target: middleTable, label: 'M', router: 'er' });
```

## Dynamic Height Adjustment

The height of entity nodes should adapt automatically based on the number of fields:

```javascript
function createEntityNode(graph, config) {
  const { x, y, name, fields } = config;
  const headerHeight = 30;
  const fieldHeight = 28;
  const height = headerHeight + fields.length * fieldHeight;

  return graph.addNode({
    shape: 'er-entity',
    x, y,
    width: 200,
    height,
    data: { name, fields },
  });
}
```

## Common Errors and Fixes

### Error: Rendering Failure Due to Using Regular Nodes Instead of HTML Nodes

**Error Example:**
```javascript
// Error: Attempting to simulate ER table structure using rect nodes, resulting in complex structure and incorrect rendering
graph.createNode({
  shape: 'rect',
  x: 40,
  y: 60,
  width: 200,
  height: 120,
  children: [/* Complex child element structure */]
});
```

**Correction Method:**
```javascript
// Correct: Register a custom HTML node using Shape.HTML.register
Shape.HTML.register({
  shape: 'er-entity',
  width: 200,
  height: 120,
  effect: ['data'],
  html(cell) {
    const data = cell.getData() || {};
    const div = document.createElement('div');
    div.style.cssText = 'width:100%;height:100%;border:1px solid #8f8f8f;border-radius:4px;overflow:hidden;font-size:12px;background:#fff;';
    const header = '<div style="background:#1890ff;color:#fff;padding:6px 8px;font-weight:bold;">' + (data.name || 'Entity') + '</div>';
    const fields = (data.fields || []).map(f => '<div style="padding:4px 8px;border-top:1px solid #eee;">' + f.name + ' <span style="color:#999">' + f.type + '</span></div>').join('');
    div.innerHTML = header + fields;
    return div;
  },
});

// Then directly add the node
graph.addNode({
  shape: 'er-entity',
  x: 40,
  y: 60,
  data: {
    name: 'User',
    fields: [
      { name: 'id', type: 'INT PK' },
      { name: 'name', type: 'VARCHAR' },
    ],
  },
});
```

### Error: Edge Not Using router: 'er' Causes Layout Chaos

**Error Example:**
```javascript
// Error: No router specified, edge may pass through nodes
graph.addEdge({
  source: tableA,
  target: tableB,
  label: '1:N'
});
```

**Correction Method:**
```javascript
// Correct: Use router: 'er' to avoid edges passing through nodes
graph.addEdge({
  source: tableA,
  target: tableB,
  label: '1:N',
  router: 'er',
  connector: 'rounded',
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
});
```

### Error: Incorrect Use of Graph.registerNode to Register HTML Nodes

**Error Example:**
```javascript
// Error: Using Graph.registerNode to register HTML nodes, should use Shape.HTML.register instead
Graph.registerNode('er-entity', {
  inherit: 'rect',
  width: 200,
  height: 100,
  attrs: {
    body: {
      strokeWidth: 1,
      fill: '#ffffff',
      stroke: '#333',
    },
    title: {
      text: '',
      refX: 0.5,
      refY: 0,
      textAnchor: 'middle',
      fontSize: 14,
      fontWeight: 'bold',
      fill: '#333',
    },
    fields: {
      text: '',
      refX: 10,
      refY: 30,
      textAnchor: 'start',
      fontSize: 12,
      fill: '#333',
    },
  },
  markup: [
    {
      tagName: 'rect',
      selector: 'body',
    },
    {
      tagName: 'text',
      selector: 'title',
    },
    {
      tagName: 'text',
      selector: 'fields',
    },
  ],
});
```

**Correction:**
```javascript
// Correct: Using Shape.HTML.register to register HTML nodes
Shape.HTML.register({
  shape: 'er-entity',
  width: 200,
  height: 120,
  effect: ['data'],
  html(cell) {
    const data = cell.getData() || {};
    const div = document.createElement('div');
    div.style.cssText = 'width:100%;height:100%;border:1px solid #8f8f8f;border-radius:4px;overflow:hidden;font-size:12px;background:#fff;';
    const header = '<div style="background:#1890ff;color:#fff;padding:6px 8px;font-weight:bold;">' + (data.name || 'Entity') + '</div>';
    const fields = (data.fields || []).map(f => '<div style="padding:4px 8px;border-top:1px solid #eee;">' + f.name + ' <span style="color:#999">' + f.type + '</span></div>').join('');
    div.innerHTML = header + fields;
    return div;
  },
});
```

### Error: Calling graph.dispose() Causes the Chart to Go Blank

**Error Example:**
```javascript
// Error: Calling graph.dispose() destroys the entire canvas, causing the chart to go blank
const graph = new Graph({ container: 'container' });
graph.addNode({ shape: 'rect', x: 100, y: 60, width: 120, height: 50, label: 'Temporary' });
graph.dispose(); // ❌ Incorrect Operation
```

**Correction Method:**
```javascript
// Correct: Avoid calling graph.dispose(). To reset the canvas, use graph.clearCells()
const graph = new Graph({ container: 'container' });
graph.addNode({ shape: 'rect', x: 100, y: 60, width: 120, height: 50, label: 'Temporary' });

// To clear canvas content, use:
// graph.clearCells();

// To save the state and reload:
const jsonData = graph.toJSON();
graph.clearCells();
graph.fromJSON(jsonData);
```

</skill>