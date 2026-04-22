---
id: "g6-core-graph-api"
title: "G6 Graph Core API Reference"
description: |
  Commonly used methods on the Graph instance: data CRUD operations, viewport control (zoom, pan, fit),
  element state management, event listening, dynamic updates of layout/behavior/plugins, etc.

library: "g6"
version: "5.x"
category: "core"
subcategory: "api"
tags:
  - "API"
  - "Graph"
  - "Data Operations"
  - "Viewport"
  - "State"
  - "Event"

related:
  - "g6-core-graph-init"
  - "g6-core-data-structure"
  - "g6-core-events"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Data Manipulation API

### Read Data

```javascript
// Get all data
const allData = graph.getData();         // { nodes, edges, combos }
const nodes   = graph.getNodeData();     // NodeData[]
const edges   = graph.getEdgeData();     // EdgeData[]
const combos  = graph.getComboData();    // ComboData[]

// Get a single element by id
const node  = graph.getNodeData('n1');
const edge  = graph.getEdgeData('e1');
const combo = graph.getComboData('c1');

// Batch get by id array
const someNodes = graph.getNodeData(['n1', 'n2', 'n3']);
```

### Add Elements

```javascript
// Add node
graph.addNodeData([
   { id: 'n3', data: { label: 'New Node', type: 'server' } },
]);

// Add edge
graph.addEdgeData([
   { source: 'n1', target: 'n3', data: { weight: 5 } },
]);

// Add combo
graph.addComboData([
   { id: 'c1', data: { label: 'New Group' } },
]);

// Need to call draw after adding to take effect
graph.draw();
```

### Update Elements

```javascript
// Update node data (only pass the fields that need to be updated)
graph.updateNodeData([
   { id: 'n1', data: { label: 'Updated Label', value: 200 } },
]);

// Update edge
graph.updateEdgeData([
   { id: 'e1', data: { weight: 10 } },
]);

graph.draw();
```

### Remove Elements

```javascript
graph.removeNodeData(['n3']);         // Remove node (associated edges are automatically removed)
graph.removeEdgeData(['e1']);         // Remove edge
graph.removeComboData(['c1']);        // Remove combo

graph.draw();
```

### Batch Operations (Merged into One History Record)

```javascript
// Operations within batch are merged into one render and history record
graph.batch(() => {
  graph.addNodeData([{ id: 'n10', data: { label: 'Batch A' } }]);
  graph.addNodeData([{ id: 'n11', data: { label: 'Batch B' } }]);
  graph.addEdgeData([{ source: 'n10', target: 'n11' }]);
});
graph.draw();
```

---

## Viewport Control API

### Zoom

```javascript
// Get the current zoom level
const zoom = graph.getZoom();         // Returns a number, 1.0 = original size

// Zoom to a specified level (with animation)
await graph.zoomTo(1.5, { easing: 'ease-out', duration: 300 });

// Relative zoom (based on the current level)
await graph.zoom(0.8);                // Zoom out to 80% of the current size
```

### Translation

```javascript
// Get the current translation
const { x, y } = graph.getTranslate();

// Translate to an absolute position
await graph.translateTo({ x: 100, y: 200 });

// Relative translation
await graph.translate({ x: 50, y: 0 });
```

### Fit View

```javascript
// Auto-scale and center all elements
await graph.fitView({
  padding: 20,                        // Padding
  direction: 'both',                  // 'x' | 'y' | 'both'
  when: 'overflow',                   // Fit only when content overflows
});

// Center (without scaling)
await graph.fitCenter();

// Focus on a specific element (pan and zoom to the element)
await graph.focusElement('n1', {
  easing: 'ease-in-out',
  duration: 500,
});
```

---

## Element State API

```javascript
// Set the state of a single element
graph.setElementState('n1', 'selected');
graph.setElementState('n1', ['selected', 'highlight']);
graph.setElementState('n1', []);          // Clear all states

// Batch setting (recommended, better performance)
graph.setElementState({
  'n1': 'selected',
  'n2': ['highlight'],
  'e1': 'active',
});

// Read state
const states = graph.getElementState('n1'); // string[]

// Query elements by state
const selectedNodes = graph.getElementDataByState('node', 'selected');
const activeEdges   = graph.getElementDataByState('edge', 'active');
```

---

## Element Visibility API

```javascript
// Hide/Show (with optional animation)
graph.hideElement(['n1', 'n2'], true);     // true = with animation
graph.showElement(['n1', 'n2'], true);

// Adjust Z-axis order
graph.frontElement(['n1']);               // Bring to front
graph.backElement(['n1']);                // Send to back
```

---

## Association Query API

```javascript
// Query all associated edges of a node
const relatedEdges  = graph.getRelatedEdgesData('n1');
const incomingEdges = graph.getIncomingEdgesData('n1');
const outgoingEdges = graph.getOutgoingEdgesData('n1');

// Query element type
const type = graph.getElementType('n1'); // 'node' | 'edge' | 'combo' | null
```

---

## Layout / Behavior / Plugin Dynamic Update

```javascript
// Dynamically switch layout
graph.setLayout({ type: 'circular' });
await graph.layout();                    // Re-execute layout

// Dynamically update behaviors (no need to re-render)
graph.setBehaviors([
  'drag-canvas',
  'zoom-canvas',
  { type: 'click-select', multiple: true },
]);

// Partially update a specific behavior configuration
graph.updateBehavior({
  key: 'click-select',
  multiple: false,
});

// Dynamically add/remove plugins
graph.setPlugins(['minimap', { type: 'tooltip', getContent: () => '' }]);

// Get plugin instance (requires setting a key for the plugin)
// plugins: [{ type: 'history', key: 'h1', stackSize: 20 }]
const history = graph.getPluginInstance('h1');
```

---

## Image Export

```javascript
// Export as PNG Data URL
const dataURL = await graph.toDataURL({ type: 'image/png', encoderOptions: 0.9 });

// Download Image
const link = document.createElement('a');
link.download = 'graph.png';
link.href = dataURL;
link.click();
```

---

## Destroy

```javascript
// Destroy the graph instance and release memory
graph.destroy();
```