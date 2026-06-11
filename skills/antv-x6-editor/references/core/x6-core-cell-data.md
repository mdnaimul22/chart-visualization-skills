---
id: "x6-core-cell-data"
title: "X6 Cell Data Manipulation API (prop/attr/data)"
description: |
  Node and edge data read/write API: prop() for general attribute operations, attr() for style attribute operations, and getData()/setData() for business data operations.
library: x6
version: 3.x
category: "core"
tags:
  - cell
  - data
  - prop
  - attr
  - getData
  - setData
  - node
  - edge
---

# Cell Data Operation API

## Overview

In X6, each Cell (node or edge) has three layers of data manipulation APIs:

| API | Function | Typical Use Cases |
|-----|----------|-------------|
| `prop()` | Read/write any property (shape, size, position, etc.) | Modify node position, size |
| `attr()` | Read/write style properties under `attrs` | Modify fill color, border, text |
| `getData()` / `setData()` | Read/write `data` field (business data) | Store business state, custom data |

## prop — Common Property Operation

`prop()` is the most fundamental property operation method, capable of reading and writing any property of a Cell.

### Read Properties

```javascript
// Get all properties
const allProps = node.prop();

// Get specified property
const position = node.prop('position');    // { x: 100, y: 200 }
const shape = node.prop('shape');          // 'rect'

// Get nested path property
const fill = node.prop('attrs/body/fill'); // '#fff'
```

### Set Properties

```javascript
// Set a single property
node.prop('position', { x: 200, y: 300 });

// Set nested properties via path
node.prop('attrs/body/fill', '#f0f0f0');

// Batch set multiple properties (deep merge)
node.prop({
  position: { x: 200, y: 300 },
  size: { width: 120, height: 60 },
});
```

### Delete Attribute

```javascript
// Set to null to delete
node.prop('attrs/body/stroke', null);
```

### setProp / removeProp

```javascript
// setProp is equivalent to prop(key, value)
node.setProp('label', 'Hello');
node.setProp({ label: 'Hello', size: { width: 100, height: 40 } });

// removeProp deletes the specified property
node.removeProp('data');
node.removeProp('attrs/body/stroke');
```

## attr — Style Attribute Operations

`attr()` is a shorthand for `prop('attrs', ...)`, specifically designed to manipulate SVG styles under `attrs`.

### Read Style

```javascript
// Get all attrs
const attrs = node.attr();
// { body: { fill: '#fff', stroke: '#333' }, label: { text: 'Hello' } }

// Get attributes of a specified selector
const bodyAttrs = node.attr('body');        // { fill: '#fff', stroke: '#333' }
const fill = node.attr('body/fill');        // '#fff'
```

### Set Style

```javascript
// Set the value of the specified path
node.attr('body/fill', '#ff0000');
node.attr('label/text', 'New Title');

// Batch setting
node.attr({
  body: { fill: '#ff0000', stroke: '#333' },
  label: { text: 'New Title', fontSize: 14 },
});
```

### Edge's attr Operation

```javascript
edge.attr('line/stroke', '#ff0000');
edge.attr('line/strokeWidth', 3);
edge.attr('line/targetMarker', 'classic');
```

## getData / setData — Business Data Operations

The `data` field is used to store business data unrelated to rendering, and it is the most commonly used method for state storage.

### Set data during initialization

```javascript
const node = graph.addNode({
  shape: 'rect',
  x: 100, y: 100, width: 120, height: 60,
  data: {
    status: 'running',
    progress: 0.75,
    taskId: 'task-001',
  },
});
```

### Read data

```javascript
const data = node.getData();
// { status: 'running', progress: 0.75, taskId: 'task-001' }
```

### Set data (Deep Merge, Default Behavior)

```javascript
// Deep Merge: Only update the specified field, retain other fields
node.setData({ status: 'completed' });
// data becomes: { status: 'completed', progress: 0.75, taskId: 'task-001' }
```

### Set data (shallow merge)

```javascript
// Shallow merge: Object.assign behavior
node.setData({ status: 'failed', error: 'timeout' }, { deep: false });
```

### Replace data (completely overwrite)

```javascript
// Completely overwrite, discard old data
node.replaceData({ status: 'new', version: 2 });
// Equivalent to
node.setData({ status: 'new', version: 2 }, { overwrite: true });
```

### Delete data

```javascript
node.removeData();
```

## Listening to Data Changes

```javascript
// Listen to data changes of a single node
node.on('change:data', ({ current, previous }) => {
  console.log('data changed from', previous, 'to', current);
});

// Listen to data changes of all nodes through the graph
graph.on('node:change:data', ({ node, current, previous }) => {
  console.log(`${node.id} data changed`);
});

// Listen to attrs changes
graph.on('node:change:attrs', ({ node }) => {
  console.log(`${node.id} attrs changed`);
});
```

## Batch Operations

Multiple prop/attr/setData calls will trigger multiple events. Use batch to merge them into one:

```javascript
graph.startBatch('update');
node.prop('position', { x: 200, y: 300 });
node.attr('body/fill', '#ff0000');
node.setData({ status: 'updated' });
graph.stopBatch('update');
// Only triggers one batch:stop event
```

## Complete Example: Dynamic Status Update

```javascript
import { Graph, Shape } from '@antv/x6';

// Register an HTML node with status rendering
Shape.HTML.register({
  shape: 'status-node',
  effect: ['data'],
  html(node) {
    const { status, label } = node.getData() || {};
    const colors = { running: '#52c41a', error: '#f5222d', pending: '#faad14' };
    const div = document.createElement('div');
    div.style.cssText = `
      width: 100%; height: 100%; display: flex; align-items: center;
      padding: 8px; border: 2px solid ${colors[status] || '#d9d9d9'};
      border-radius: 4px; background: #fff;
    `;
    div.innerHTML = `<span style="color:${colors[status] || '#333'}">${label || 'Node'}</span>`;
    return div;
  },
});

const graph = new Graph({ container: 'container', width: 800, height: 600 });

const node = graph.addNode({
  shape: 'status-node',
  x: 100, y: 100, width: 160, height: 50,
  data: { status: 'pending', label: 'Data Processing' },
});

// Simulate status update —— setData triggers effect re-rendering
setTimeout(() => node.setData({ status: 'running' }), 1000);
setTimeout(() => node.setData({ status: 'error', label: 'Data Processing (Failed)' }), 3000);
```

## Common Errors

```javascript
// ❌ Error: Directly modifying the object returned by getData() does not trigger updates
const data = node.getData();
data.status = 'done';  // Will not trigger re-rendering!

// ✅ Correct: Modify using setData
node.setData({ status: 'done' });

// ❌ Error: Using '.' instead of '/' as the attr path separator
node.attr('body.fill', '#fff');  // Incorrect, will not take effect

// ✅ Correct: Use '/' as the path separator
node.attr('body/fill', '#fff');

// ❌ Error: Setting only part of attrs using prop will lose others
node.prop('attrs', { body: { fill: '#f00' } });
// This will overwrite the entire attrs, losing other selectors like label!

// ✅ Correct: Use path form or attr() method
node.prop('attrs/body/fill', '#f00');  // Only modifies body.fill
node.attr('body/fill', '#f00');        // Equivalent
```