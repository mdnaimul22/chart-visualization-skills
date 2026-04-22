---
id: "g6-core-events"
title: "G6 Event System"
description: |
  G6 v5 Event System: Element events (click, hover, drag for nodes/edges/combos),
  canvas events, and graph lifecycle event listening methods with a list of commonly used events.

library: "g6"
version: "5.x"
category: "core"
subcategory: "events"
tags:
  - "event"
  - "listen"
  - "node:click"
  - "canvas"
  - "lifecycle"

related:
  - "g6-core-graph-api"
  - "g6-behavior-click-select"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Event Listening Basics

```javascript
// Listen
graph.on('node:click', (event) => {
  const { target, targetType } = event;
  console.log('Node clicked:', target.id);
});

// Unlisten (pass the same function reference)
const handler = (e) => console.log(e);
graph.on('node:click', handler);
graph.off('node:click', handler);

// Remove all listeners for the event
graph.off('node:click');
```

---

## Element Events

Element event format: `{elementType}:{eventType}`, such as `node:click`, `edge:pointerover`.

| Event Name | Description |
|------------|-------------|
| `node:click` | Click on a node |
| `node:dblclick` | Double-click on a node |
| `node:pointerover` | Mouse enters a node |
| `node:pointerout` | Mouse leaves a node |
| `node:pointerdown` | Mouse/touch press down on a node |
| `node:pointerup` | Mouse/touch release |
| `node:contextmenu` | Right-click on a node |
| `node:dragstart` | Start dragging a node |
| `node:drag` | Dragging a node |
| `node:dragend` | End dragging a node |
| `edge:click` | Click on an edge |
| `edge:pointerover` | Mouse enters an edge |
| `combo:click` | Click on a combo |
| `combo:dblclick` | Double-click on a combo |

### Event Object Properties

```typescript
interface IElementEvent {
  target: DisplayObject;    // The graphic object that triggered the event
  targetType: string;       // 'node' | 'edge' | 'combo' | 'canvas'
  originalEvent: Event;     // The original DOM event
  // Coordinates (Canvas coordinate system)
  canvas: { x: number; y: number };
  // Coordinates (Viewport coordinate system)
  viewport: { x: number; y: number };
  // Coordinates (Client coordinate system)
  client: { x: number; y: number };
}
```

### Typical Usage

```javascript
// Get data by clicking on a node
graph.on('node:click', (event) => {
  const nodeId = event.target.id;
  const nodeData = graph.getNodeData(nodeId);
  console.log(nodeData);
});

// Highlight edge on hover
graph.on('edge:pointerover', (event) => {
  graph.setElementState(event.target.id, 'active');
});
graph.on('edge:pointerout', (event) => {
  graph.setElementState(event.target.id, []);
});

// Right-click menu
graph.on('node:contextmenu', (event) => {
  event.originalEvent.preventDefault();
  console.log('Right-click node:', event.target.id);
});
```

---

## Canvas Events

| Event Name | Description |
|------------|-------------|
| `canvas:click` | Click on the blank area of the canvas |
| `canvas:dblclick` | Double-click the canvas |
| `canvas:pointerdown` | Mouse button pressed on the canvas |
| `canvas:pointerup` | Mouse button released |
| `canvas:pointermove` | Mouse moves on the canvas |
| `canvas:wheel` | Canvas scroll wheel event |
| `canvas:contextmenu` | Right-click the canvas |

```javascript
// Click on blank area to cancel selection
graph.on('canvas:click', () => {
  const selected = graph.getElementDataByState('node', 'selected');
  selected.forEach(n => graph.setElementState(n.id, []));
});
```

---

## Graph Lifecycle Events

```javascript
import { GraphEvent } from '@antv/g6';

// Render complete
graph.on(GraphEvent.AFTER_RENDER, () => {
  console.log('Graph render complete');
});

// Layout complete
graph.on(GraphEvent.AFTER_LAYOUT, () => {
  console.log('Layout complete');
});

// Elements created (batch)
graph.on(GraphEvent.AFTER_ELEMENT_CREATE, (event) => {
  console.log('New elements:', event.data);
});

// Viewport transformation (zoom/pan)
graph.on(GraphEvent.AFTER_TRANSFORM, (event) => {
  const { translate, zoom } = event.data;
  console.log('Viewport transformation:', zoom);
});
```

### Common Lifecycle Events

| Event Constant | Event Name | Trigger Timing |
|----------|--------|---------|
| `GraphEvent.BEFORE_RENDER` | `beforerender` | Before render() starts |
| `GraphEvent.AFTER_RENDER` | `afterrender` | After render() completes |
| `GraphEvent.BEFORE_DRAW` | `beforedraw` | Before draw() starts |
| `GraphEvent.AFTER_DRAW` | `afterdraw` | After draw() completes |
| `GraphEvent.AFTER_LAYOUT` | `afterlayout` | After layout calculation completes |
| `GraphEvent.AFTER_ELEMENT_CREATE` | `afterelementcreate` | After an element is added |
| `GraphEvent.AFTER_ELEMENT_UPDATE` | `afterelementupdate` | After an element is updated |
| `GraphEvent.AFTER_ELEMENT_DESTROY` | `afterelementdestroy` | After an element is deleted |
| `GraphEvent.AFTER_TRANSFORM` | `aftertransform` | After viewport transformation |
| `GraphEvent.BEFORE_DESTROY` | `beforedestroy` | Before destroy() |

---

## Common Patterns

### Update Node Coordinates After Dragging

```javascript
graph.on('node:dragend', (event) => {
  const nodeId = event.target.id;
  const { x, y } = graph.getNodeData(nodeId);
  console.log(`Node ${nodeId} new coordinates: (${x}, ${y})`);
});
```

### Dynamically Update Tooltip Data

```javascript
graph.on('node:pointerover', async (event) => {
  const nodeId = event.target.id;
  const detail = await fetchNodeDetail(nodeId);
  graph.updateNodeData([{ id: nodeId, data: { ...detail } }]);
});
```