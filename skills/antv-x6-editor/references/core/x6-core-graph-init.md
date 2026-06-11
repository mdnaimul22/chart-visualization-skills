---
id: "x6-core-graph-init"
title: "X6 Canvas Initialization"
description: |
  A complete configuration guide for creating a graph editing canvas using new Graph({...}).
  Includes configuration methods for container, size, background, grid, panning, zooming, and edge interaction.

library: "x6"
version: "3.x"
category: "core"
subcategory: "init"
tags:
  - "initialization"
  - "Graph"
  - "container"
  - "canvas"
  - "background"
  - "grid"
  - "background"
  - "container"
  - "new Graph"
  - "panning"
  - "mousewheel"
  - "zooming"
  - "scrolling"

related:
  - "x6-core-node"
  - "x6-core-edge"
  - "x6-core-ports"

use_cases:
  - "Create a graph editing canvas"
  - "Configure canvas background and grid"
  - "Enable canvas panning and zooming"
  - "Set canvas size"

anti_patterns:
  - "Do not omit the container parameter"
  - "Do not use @antv/x6-plugin-xxx standalone packages"

difficulty: "beginner"
completeness: "full"
---

## Core Concepts

Graph is the canvas container of X6, managing all nodes and edges. X6 uses a **declarative API**: first create the canvas, then gradually add elements using `addNode()`/`addEdge()`.

**Key differences between X6 and G6:**
- X6 is a graph **editing** engine (focus on interaction), G6 is a graph **visualization** engine (focus on layout rendering)
- X6 has no built-in layout algorithm, node positions are manually specified via `x`/`y`
- X6 uses ports as the core mechanism for connecting nodes

## Basic Initialization

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',  // Required: DOM id or HTMLElement
  width: 800,              // Optional: Auto-adapts to container if not set
  height: 600,
});
```

## Background and Grid

```javascript
const graph = new Graph({
  container: 'container',
  background: {
    color: '#F2F7FA',      // Background color
  },
  grid: {
    visible: true,         // Show grid
    size: 10,              // Grid size
    type: 'dot',           // 'dot' | 'mesh' | 'double-mesh'
  },
});
```

### Double-Layer Grid

```javascript
grid: {
  size: 10,
  visible: true,
  type: 'double-mesh',
  args: [
    { color: '#eee', thickness: 1 },
    { color: '#ddd', thickness: 1, factor: 4 },
  ],
},
```

## Panning and Zooming

```javascript
const graph = new Graph({
  container: 'container',
  panning: true,                    // Drag to pan (left mouse button drag on blank area)
  mousewheel: {
    enabled: true,
    modifiers: 'ctrl',              // Hold Ctrl + scroll wheel to zoom
    minScale: 0.2,
    maxScale: 4,
  },
});
```

### Panning Configuration Details

```javascript
panning: {
  enabled: true,
  modifiers: 'shift',    // Hold Shift to enable panning
  eventTypes: ['leftMouseDown', 'rightMouseDown'],
}
```

## Canvas Transformations

```javascript
// Center content
graph.centerContent();

// Zoom to fit canvas
graph.zoomToFit({ padding: 20 });

// Set zoom level
graph.zoom(0.5);     // Relative zoom
graph.zoomTo(1.5);   // Absolute zoom

// Scroll to a specific node
graph.centerCell(node);

// Zoom to a specified rectangular area (local magnification)
graph.zoomToRect({
  x: 0,
  y: 0,
  width: 400,
  height: 300,
});
```

## Connection Interaction Configuration

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    allowBlank: false,          // Prohibit connection to blank
    allowLoop: false,           // Prohibit self-loop
    allowNode: false,           // Prohibit connection to nodes (only ports allowed)
    allowEdge: false,           // Prohibit connection to edges
    allowMulti: true,           // Allow multiple edges
    highlight: true,            // Highlight connectable points during dragging
    router: 'orth',             // Default router
    connector: 'rounded',       // Default connector
    createEdge() {              // Edge style created during dragging
      return this.createEdge({
        attrs: {
          line: { stroke: '#1890ff', strokeWidth: 2, targetMarker: 'classic' },
        },
      });
    },
    validateConnection({ sourcePort, targetPort }) {
      return sourcePort !== targetPort;  // Custom validation logic
    },
  },
});
```

## Node Movement Restriction

```javascript
const graph = new Graph({
  container: 'container',
  translating: {
    restrict: true,   // Restrict node movement within the canvas area
  },
});

// Or customize the restriction area
translating: {
  restrict(cellView) {
    return { x: 0, y: 0, width: 800, height: 600 };
  },
},
```

## Node Embedding (Grouping)

```javascript
const graph = new Graph({
  container: 'container',
  embedding: {
    enabled: true,
    findParent: 'bbox',   // Use bounding box to detect parent nodes
  },
});
```

## Data Manipulation

### Clear Canvas

Use `graph.clearCells()` to clear all nodes and edges on the canvas, commonly used for resetting or reloading data.

```javascript
// Clear all nodes and edges
graph.clearCells();
```

### Add Nodes and Edges

```javascript
// Add a node
const node = graph.addNode({
  shape: 'rect',
  x: 60,
  y: 60,
  width: 100,
  height: 40,
  label: 'Node 1',
  attrs: {
    body: { stroke: '#1890ff', fill: '#e6f7ff' },
  },
});

// Add an edge (pass in node instances or node IDs)
graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' },
  },
});
```

### Clear and Reload Data

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
});

// Load initial data
graph.addNode({ shape: 'rect', x: 60, y: 60, width: 100, height: 40, label: 'Old Node 1' });
graph.addNode({ shape: 'rect', x: 240, y: 60, width: 100, height: 40, label: 'Old Node 2' });

// Clear the canvas
graph.clearCells();

// Reload new data
const newSource = graph.addNode({
  id: 'newSource',
  shape: 'rect',
  x: 60,
  y: 80,
  width: 100,
  height: 40,
  label: 'New Node A',
  attrs: { body: { stroke: '#52c41a', strokeWidth: 2, fill: '#f6ffed' } },
});

const newTarget = graph.addNode({
  id: 'newTarget',
  shape: 'rect',
  x: 260,
  y: 80,
  width: 100,
  height: 40,
  label: 'New Node B',
  attrs: { body: { stroke: '#52c41a', strokeWidth: 2, fill: '#f6ffed' } },
});

graph.addEdge({
  source: newSource,
  target: newTarget,
  attrs: { line: { stroke: '#52c41a', strokeWidth: 2, targetMarker: 'classic' } },
});
```

## Complete Configuration Example

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
  grid: { visible: true, size: 10 },
  panning: true,
  mousewheel: { enabled: true, modifiers: 'ctrl' },
  connecting: {
    allowBlank: false,
    router: 'orth',
    connector: 'rounded',
    createEdge() {
      return this.createEdge({
        attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
      });
    },
  },
});

// Register plugins
import { Selection, Snapline, History } from '@antv/x6';
graph.use(new Selection({ enabled: true, rubberband: true }));
graph.use(new Snapline({ enabled: true }));
graph.use(new History({ enabled: true }));
```

## Common Errors and Fixes

### 1. Omitted container parameter

```javascript
// ❌ Incorrect
const graph = new Graph({ width: 800, height: 600 });

// ✅ Correct
const graph = new Graph({ container: 'container', width: 800, height: 600 });
```

### 2. Failure to Reload Data After Clearing the Canvas

When you need to clear the canvas and reload new data, you must explicitly call `graph.clearCells()`, followed by using `graph.addNode()` and `graph.addEdge()` to add new elements.

```javascript
// ❌ Incorrect: Overwriting variables without clearing the canvas, resulting in residual old data
graph.addNode({ shape: 'rect', label: 'Old' });
// Missing clearCells()

// ✅ Correct: Clear first, then load
graph.clearCells();
graph.addNode({ shape: 'rect', label: 'New' });
```

### 3. Using Deprecated Standalone Plugin Packages

X6 3.x has integrated all plugins, so there is no need to install the `@antv/x6-plugin-xxx` series of packages.

```javascript
// ❌ Incorrect
import { Snapline } from '@antv/x6-plugin-snapline';

// ✅ Correct: Import from @antv/x6 and register via graph.use()
import { Graph, Snapline } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Snapline({ enabled: true }));
```

### 4. Incorrect edge source/target format

```javascript
// ❌ Incorrect: Passing undefined variables directly
graph.addEdge({ source: 'node1', target: 'node2' }); // Throws an error if nodes are not set with id or do not exist

// ✅ Correct: Pass node instances or ensure ids exist
const node1 = graph.addNode({ id: 'n1', shape: 'rect', x: 0, y: 0, width: 100, height: 40 });
const node2 = graph.addNode({ id: 'n2', shape: 'rect', x: 200, y: 0, width: 100, height: 40 });
graph.addEdge({ source: node1, target: node2 });
// or
graph.addEdge({ source: 'n1', target: 'n2' });
```

### 5. Container Usage Guidelines

The `container` variable is automatically injected by the runtime environment. **Do not** declare `const container = ...` in your code, as it will result in the error `Identifier 'container' has already been declared`.

```javascript
// ✅ Correct: Directly use the string 'container'
const graph = new Graph({ container: 'container' });

// ❌ Incorrect: Redeclaring the container variable
const container = document.getElementById('container');
const graph = new Graph({ container }); // Error: Identifier 'container' has already been declared
```

### 6. Failure to Call Canvas Transformation Methods After Initialization

```javascript
// ❌ Incorrect: centerContent or zoomToFit not called
const graph = new Graph({ container: 'container' });
graph.addNode(...);
// Missing center or zoom call

// ✅ Correct: Transformation methods called after initialization
const graph = new Graph({ container: 'container' });
graph.addNode(...);
graph.zoomToFit();
graph.centerContent();
```

### 7. container must be valid

```javascript
// ✅ Correct: Use the string 'container' (injected in the runtime environment)
const graph = new Graph({ container: 'container' });

// ❌ Incorrect: Passing a non-existent element
const graph = new Graph({ container: document.getElementById('not-exist') }); // Throws an error
```

### 8. Failure to Call `centerContent` After Using `zoomToFit`

```javascript
// ❌ Incorrect: Only calling zoomToFit without centering the content
graph.zoomToFit();

// ✅ Correct: Zoom and then center
graph.zoomToFit();
graph.centerContent();
```

### 9. Incorrect Usage of `source` and `target` as Strings Instead of Node Instances

```javascript
// ❌ Incorrect: source and target are strings, but node existence is not ensured
graph.addEdge({ source: 'source', target: 'target' });

// ✅ Correct: Pass node instances or ensure nodes exist
const sourceNode = graph.addNode({ id: 'source', shape: 'rect', x: 40, y: 40, width: 100, height: 40 });
const targetNode = graph.addNode({ id: 'target', shape: 'rect', x: 200, y: 200, width: 100, height: 40 });
graph.addEdge({ source: sourceNode, target: targetNode });
// or
graph.addEdge({ source: 'n1', target: 'n2' });
```

### 10. Incorrect Usage of `router` and `connector` Configuration

```javascript
// ❌ Incorrect: router and connector configuration is incorrect
connecting: {
  router: 'manhattan',
  connector: {
    name: 'rounded',
    args: {
      radius: 8,
    },
  },
}

// ✅ Correct: Using standard configuration
connecting: {
  router: 'orth',
  connector: 'rounded',
}
```

### 11. Using the string 'container' for the container

```javascript
// ✅ Correct: Use the default 'container' string
const graph = new Graph({ container: 'container' });

// ❌ Incorrect: Declaring the container variable in the code (the runtime environment has already injected it, and redeclaring it will throw an error)
const container = document.getElementById('my-container');
const graph = new Graph({ container }); // Identifier 'container' has already been declared
```

### 12. Incorrect Order of `zoomToFit` and `centerContent`

```javascript
// ❌ Incorrect: Center first, then zoom
graph.centerContent();
graph.zoomToFit();

// ✅ Correct: Zoom first, then center
graph.zoomToFit();
graph.centerContent();
```

### 13. Incorrect Usage of `mousewheel` Configuration

```javascript
// ❌ Incorrect: mousewheel not enabled
const graph = new Graph({
  container: 'container',
  mousewheel: {
    enabled: false,
  },
});

// ✅ Correct: mousewheel enabled
const graph = new Graph({
  container: 'container',
  mousewheel: {
    enabled: true,
    modifiers: 'ctrl',
  },
});
```

### 14. Incorrect Usage of `panning` Configuration

```javascript
// ❌ Incorrect: panning is not enabled
const graph = new Graph({
  container: 'container',
  panning: false,
});

// ✅ Correct: panning is enabled
const graph = new Graph({
  container: 'container',
  panning: true,
});
```

### 15. Incorrect Usage of `background` Configuration

```javascript
// ❌ Incorrect: Background not set
const graph = new Graph({
  container: 'container',
});

// ✅ Correct: Background set
const graph = new Graph({
  container: 'container',
  background: {
    color: '#F2F7FA',
  },
});
```

### 16. Incorrect Usage of `grid` Configuration

```javascript
// ❌ Incorrect: grid not set
const graph = new Graph({
  container: 'container',
});

// ✅ Correct: grid set
const graph = new Graph({
  container: 'container',
  grid: {
    visible: true,
    size: 10,
  },
});
```

### 17. Canvas is empty when `graph.centerContent()` and `graph.zoom()` are used incorrectly

```javascript
// ❌ Incorrect: Calling centerContent and zoom when the canvas is empty results in a white screen
const graph = new Graph({ container: 'container' });
graph.centerContent(); // White screen
graph.zoom(0.8);       // White screen

// ✅ Correct: Add nodes before calling centerContent and zoom
const graph = new Graph({ container: 'container' });
graph.addNode({ shape: 'rect', x: 50, y: 50, width: 100, height: 40, label: 'Node A' });
graph.centerContent();
graph.zoom(0.8);
```

### 18. Misuse of `graph.zoom()` Parameters

```javascript
// ❌ Incorrect: Using a negative number as the zoom parameter
graph.zoom(-0.2); // Not recommended, may cause abnormal behavior

// ✅ Correct: Using a positive number or relative value
graph.zoom(0.8);  // Zoom out
graph.zoom(1.2);  // Zoom in
graph.zoomTo(1.0); // Set absolute zoom ratio
```

### 19. Incorrect Usage of `zoomToRect` Method

```javascript
// ❌ Incorrect: Syntax or spelling errors causing rendering failure
graph.zoomToRect({
  x: 0,
  y: 0,
  width: 400,
  height: 300
}); // Note: No semicolon or other syntax errors at the end

// ✅ Correct: Using zoomToRect to zoom to a specified rectangular area
graph.zoomToRect({
  x: 0,
  y: 0,
  width: 400,
  height: 300,
});
```

### 20. Incorrect Use of `container` Variable (Duplicate Declaration)

```javascript
// ❌ Incorrect: Repeated declaration of container variable in the code
const container = document.getElementById('my-container');
const graph = new Graph({ container });

// ✅ Correct: Use the string 'container'
const graph = new Graph({ container: 'container' });
```