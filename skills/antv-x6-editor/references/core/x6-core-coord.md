---
id: "x6-core-coord"
title: "X6 Coordinate Transformation (Coord)"
description: |
  X6 Coordinate System Transformation API: mutual conversion between local (canvas local coordinates), graph (viewport coordinates), client (browser viewport coordinates), and page (document coordinates).

library: "x6"
version: "3.x"
category: "core"
subcategory: "coord"
tags:
  - "coord"
  - "coordinate transformation"
  - "localToGraph"
  - "clientToLocal"
  - "snapToGrid"
  - "coordinate system"

related:
  - "x6-core-graph-init"
  - "x6-core-panning"
  - "x6-core-mousewheel"

use_cases:
  - "Convert mouse event coordinates to canvas coordinates"
  - "Add nodes based on screen position"
  - "Drag external elements to the canvas and position them"
  - "Snap coordinates to grid"
  - "Custom right-click menu positioning"

difficulty: "intermediate"
completeness: "full"
---

## Coordinate System Explanation

There are four coordinate systems in X6:

| Coordinate System | Description | Application Scenarios |
|-------------------|-------------|-----------------------|
| **local** | Canvas local coordinates, where the x/y of nodes belong to this system | Node positioning, addNode, node attributes |
| **graph** | Viewport coordinates after translation/scaling transformations | Actual rendering pixel positions on the canvas |
| **client** | Browser window viewport coordinates (`getBoundingClientRect`) | Mouse event clientX/clientY |
| **page** | Document coordinates (including page scroll offsets) | Mouse event pageX/pageY |

Transformation relationships:

```
local --[matrix]--> graph --[offset]--> client --[scroll]--> page
```

## Point Coordinate Transformation API

### local → Others

```javascript
// local → graph (Apply scaling and panning)
graph.localToGraph({ x: 100, y: 100 });      // Point
graph.localToGraph(100, 100);                  // Point

// local → client (Browser viewport coordinates)
graph.localToClient({ x: 100, y: 100 });      // Point

// local → page (Document coordinates)
graph.localToPage({ x: 100, y: 100 });        // Point
```

### Other → local

```javascript
// graph → local (Inverse transformation)
graph.graphToLocal({ x: 200, y: 150 });       // Point

// client → local (Most commonly used: Mouse event → Canvas coordinates)
graph.clientToLocal({ x: e.clientX, y: e.clientY });   // Point
graph.clientToLocal(e.clientX, e.clientY);              // Point

// client → graph
graph.clientToGraph({ x: e.clientX, y: e.clientY });   // Point

// page → local
graph.pageToLocal({ x: e.pageX, y: e.pageY });         // Point
```

## Rectangle Coordinate Transformation API

All point transformations have corresponding rectangle versions, returning a `Rectangle` object:

```javascript
// local → graph
graph.localToGraphRect({ x: 100, y: 100, width: 200, height: 150 });

// local → client
graph.localToClientRect(100, 100, 200, 150);

// graph → local
graph.graphToLocalRect({ x: 200, y: 150, width: 300, height: 200 });

// client → local
graph.clientToLocalRect(e.clientX, e.clientY, width, height);

// client → graph
graph.clientToGraphRect({ x: 0, y: 0, width: 100, height: 100 });

// page → local
graph.pageToLocalRect({ x: 0, y: 0, width: 100, height: 100 });
```

## snapToGrid

Converts client coordinates to local coordinates and snaps them to the grid:

```javascript
// Snap mouse position to the grid
const pos = graph.snapToGrid(e.clientX, e.clientY);
// Returns the snapped local coordinates Point { x, y }
```

## Common Use Case Examples

### Scenario 1: Dragging External Elements to the Canvas to Create Nodes

```javascript
document.getElementById('drag-source').addEventListener('drop', (e) => {
  e.preventDefault();
  // Convert the mouse release position to canvas coordinates and snap to the grid
  const pos = graph.snapToGrid(e.clientX, e.clientY);
  graph.addNode({
    x: pos.x,
    y: pos.y,
    width: 100,
    height: 50,
    label: 'New Node',
  });
});
```

### Scenario 2: Customizing Right-Click Menu Positioning

```javascript
graph.on('node:contextmenu', ({ e, node }) => {
  // Position the menu using client coordinates (relative to the browser viewport)
  const menu = document.getElementById('context-menu');
  menu.style.left = `${e.clientX}px`;
  menu.style.top = `${e.clientY}px`;
  menu.style.display = 'block';
});
```

### Scenario 3: Obtain the Actual Position of a Node on the Screen

```javascript
const node = graph.getCellById('node1');
const { x, y } = node.getPosition();  // local coordinates

// Convert to browser viewport coordinates (can be used for positioning floating layers)
const clientPos = graph.localToClient({ x, y });
console.log(`Node position on the screen: (${clientPos.x}, ${clientPos.y})`);
```

### Scenario 4: Calculate Nodes Within the Visible Area of the Canvas

```javascript
// Get the current visible area (graph coordinate system)
const visibleArea = graph.getGraphArea();  // Rectangle

// Convert to local coordinate system
const localArea = graph.graphToLocalRect(visibleArea);

// Filter nodes within the visible area
const visibleNodes = graph.getNodes().filter((node) => {
  const bbox = node.getBBox();
  return localArea.isIntersectWithRect(bbox);
});
```

## Common Errors

### ❌ Directly Using Mouse clientX/clientY as Node Coordinates

```javascript
// Error: Mouse coordinates are in the client coordinate system and cannot be used directly for node positioning
document.addEventListener('click', (e) => {
  graph.addNode({ x: e.clientX, y: e.clientY, width: 80, height: 40 });  // ❌ Incorrect position
});
```

```javascript
// Correct: Convert the coordinate system first
document.addEventListener('click', (e) => {
  const pos = graph.clientToLocal(e.clientX, e.clientY);
  graph.addNode({ x: pos.x, y: pos.y, width: 80, height: 40 });  // ✅
});
```

### ❌ Confusing localToGraph and localToClient

```javascript
// localToGraph: Includes canvas scaling/panning transformations, used for internal canvas pixel calculations
// localToClient: Converts to browser viewport coordinates, used for positioning DOM elements (e.g., popups, menus)
```

### ❌ Coordinates in X6 Events Are Already Local Coordinates

```javascript
// The x, y in X6 event callbacks are already local coordinates, no need for further conversion
graph.on('blank:click', ({ e, x, y }) => {
  // x, y are already local coordinates ✅
  graph.addNode({ x, y, width: 80, height: 40 });
});
```