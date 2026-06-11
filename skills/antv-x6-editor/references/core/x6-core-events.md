---
id: "x6-core-events"
title: "X6 Event System"
description: |
  Event listening and handling for X6 canvas, nodes, and edges.
  Includes usage of events such as click, drag, change, and keyboard interactions.

library: "x6"
version: "3.x"
category: "core"
subcategory: "events"
tags:
  - "event"
  - "click"
  - "mouseenter"
  - "mouseleave"
  - "moved"
  - "added"
  - "removed"
  - "changed"
  - "node:click"
  - "edge:click"
  - "blank:click"
  - "interaction"

related:
  - "x6-core-graph-init"
  - "x6-core-node"
  - "x6-core-edge"

use_cases:
  - "Listen for node click events"
  - "Listen for edge selection state"
  - "Listen for canvas blank area clicks"
  - "Listen for node move completion"
  - "Listen for node/edge addition and removal"

anti_patterns:
  - "Do not use positional arguments to destructure event callbacks; use object destructuring instead"
  - "Avoid performing heavy computations in high-frequency events (e.g., mousemove)"

difficulty: "beginner"
completeness: "full"
---

## Event Callback Format

**Important**: X6 event callback parameters are **object destructuring**, not positional arguments.

```javascript
// ✅ Correct: Object destructuring
graph.on('node:click', ({ node, e }) => {
  console.log('Clicked node:', node.id);
});

// ❌ Incorrect: Positional arguments
graph.on('node:click', (node, e) => { ... });
```

## Node Events

```javascript
// Click
graph.on('node:click', ({ node, e }) => {
  console.log('Clicked:', node.id);
});

// Double click
graph.on('node:dblclick', ({ node, e }) => {
  console.log('Double clicked:', node.id);
});

// Right click
graph.on('node:contextmenu', ({ node, e }) => {
  e.preventDefault();
});

// Mouse enter/leave
graph.on('node:mouseenter', ({ node }) => {
  node.attr('body/stroke', '#1890ff');
});

graph.on('node:mouseleave', ({ node }) => {
  node.attr('body/stroke', '#8f8f8f');
});

// Node moving
graph.on('node:moving', ({ node, x, y }) => {
  console.log('Moving to:', x, y);
});

// Node move completed
graph.on('node:moved', ({ node }) => {
  const pos = node.getPosition();
  console.log('Moved to:', pos.x, pos.y);
});

// Node size changed
graph.on('node:resized', ({ node }) => {
  const size = node.getSize();
  console.log('Resized to:', size.width, size.height);
});
```

## Edge Events

```javascript
// Click
graph.on('edge:click', ({ edge, e }) => {
  console.log('Edge:', edge.id);
});

// Mouse Enter/Leave
graph.on('edge:mouseenter', ({ edge }) => {
  edge.attr('line/stroke', '#1890ff');
  edge.attr('line/strokeWidth', 2);
});

graph.on('edge:mouseleave', ({ edge }) => {
  edge.attr('line/stroke', '#8f8f8f');
  edge.attr('line/strokeWidth', 1);
});

// Connection Complete
graph.on('edge:connected', ({ edge, isNew }) => {
  if (isNew) {
    console.log('New edge created:', edge.id);
  }
});
```

## Canvas Events

```javascript
// Click on blank area
graph.on('blank:click', ({ e }) => {
  // Clear selection
  graph.cleanSelection();
});

// Canvas zoom
graph.on('scale', ({ sx, sy }) => {
  console.log('Scale:', sx, sy);
});

// Canvas pan
graph.on('translate', ({ tx, ty }) => {
  console.log('Translate:', tx, ty);
});
```

## Element Change Events

```javascript
// Node/Edge Added
graph.on('cell:added', ({ cell }) => {
  console.log('Added:', cell.id, cell.isNode() ? 'node' : 'edge');
});

// Node/Edge Removed
graph.on('cell:removed', ({ cell }) => {
  console.log('Removed:', cell.id);
});

// Attribute Changed
graph.on('cell:changed', ({ cell, options }) => {
  console.log('Changed:', cell.id);
});
```

## Selection Event

```javascript
// Selection change (requires enabling the selecting plugin)
graph.on('selection:changed', ({ added, removed, selected }) => {
  console.log('Selected nodes:', selected.length);
  added.forEach(cell => cell.attr('body/stroke', '#1890ff'));
  removed.forEach(cell => cell.attr('body/stroke', '#8f8f8f'));
});
```

## History Events

```javascript
// Undo/Redo (requires enabling the history plugin)
graph.on('history:undo', () => {
  console.log('Undo performed');
});

graph.on('history:redo', () => {
  console.log('Redo performed');
});
```

## Event Management

```javascript
// Listen once
graph.once('node:click', ({ node }) => { ... });

// Remove listener
const handler = ({ node }) => { ... };
graph.on('node:click', handler);
graph.off('node:click', handler);

// Remove all listeners
graph.off('node:click');
```

## Common Event Patterns

### Node State Switching

```javascript
graph.on('node:click', ({ node }) => {
  const data = node.getData() || {};
  const isActive = !data.active;
  node.setData({ active: isActive });
  node.attr('body/fill', isActive ? '#e6f7ff' : '#fff');
  node.attr('body/stroke', isActive ? '#1890ff' : '#8f8f8f');
});
```

### Highlight Adjacent Nodes

```javascript
graph.on('node:click', ({ node }) => {
  // Reset all node styles
  graph.getNodes().forEach(n => {
    n.attr('body/fill', '#fff');
  });
  // Highlight the current node
  node.attr('body/fill', '#e6f7ff');
  // Highlight adjacent nodes
  const neighbors = graph.getNeighbors(node);
  neighbors.forEach(n => {
    n.attr('body/fill', '#d9f7be');
  });
});
```

### Delete Selected Elements

```javascript
graph.on('blank:click', () => {
  graph.cleanSelection();
});

// Works with the keyboard plugin
graph.bindKey('delete', () => {
  const cells = graph.getSelectedCells();
  if (cells.length) {
    graph.removeCells(cells);
  }
});
```

## Minimum Viable Example

```javascript
import { Graph } from '@antv/x6'

// Create canvas
const graph = new Graph({
  container: document.getElementById('container'),
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
  grid: { visible: true },
})

// Listen for canvas events
graph.on('blank:click', ({ e }) => {
  console.log('Clicked on blank area')
})

graph.on('cell:added', ({ cell }) => {
  console.log('Element added:', cell.id)
})

graph.on('cell:removed', ({ cell }) => {
  console.log('Element removed:', cell.id)
})

// Add node
graph.addNode({
  shape: 'rect',
  x: 100,
  y: 80,
  width: 100,
  height: 40,
  label: 'Node 1',
  attrs: {
    body: { 
      stroke: '#8f8f8f', 
      strokeWidth: 1, 
      fill: '#fff',
      rx: 6,
      ry: 6
    }
  }
})

// Listen for node events
graph.on('node:mouseenter', ({ node }) => {
  node.attr('body/stroke', '#1890ff')
  node.attr('body/strokeWidth', 2)
})

graph.on('node:mouseleave', ({ node }) => {
  node.attr('body/stroke', '#8f8f8f')
  node.attr('body/strokeWidth', 1)
})
```

## Common Errors and Fixes

### Error: Incorrect Usage of Selection Constructor

```javascript
// ❌ Incorrect: Directly using new Selection()
graph.use(new Selection({ enabled: true, rubberband: true }));

// ✅ Correct: Using graph.use() and properly configuring the plugin
import { Selection } from '@antv/x6-plugin-selection'
graph.use(new Selection({ enabled: true, rubberband: true }))
```

### Error: Incorrect Plugin Initialization Method

```javascript
// ❌ Incorrect: Initializing plugins using the plugins array
const graph = new Graph({
  plugins: [
    new Selection(),
    new Snapline(),
    new Keyboard(),
    new Clipboard(),
    new History()
  ]
});

// ✅ Correct: Initializing plugins using the graph.use() method
import { Selection, Snapline, History } from '@antv/x6-plugin-selection'

graph.use(new Selection({ enabled: true, rubberband: true }));
graph.use(new Snapline({ enabled: true }));
graph.use(new History({ enabled: true }));
```

### Error: Incorrect Node Registration Method

```javascript
// ❌ Incorrect: Using graph.registerNode to register a node
graph.registerNode('start-event', {
  // ...
}, true);

// ✅ Correct: Directly use built-in shapes or create nodes through inheritance
const start = graph.addNode({
  shape: 'circle',
  x: 80,
  y: 200,
  width: 40,
  height: 40,
  attrs: { 
    body: { fill: '#52c41a', stroke: '#389e0d' },
    label: { text: 'Start', fill: '#fff', fontSize: 11 }
  },
  ports: {
    groups: {
      out: {
        position: 'right',
        attrs: {
          circle: { r: 4, magnet: true, stroke: '#52c41a', fill: '#fff' }
        }
      }
    },
    items: [{ id: 'out', group: 'out' }]
  }
});
```

### Error: Context Not Properly Bound When Creating Edge

```javascript
// ❌ Error: Using graph.createEdge in createEdge
connecting: {
  createEdge() {
    return graph.createEdge({ ... }); // Error: this binding issue
  }
}

// ✅ Correct: Using this.createEdge
connecting: {
  createEdge() {
    return this.createEdge({ ... }); // Correct: this refers to the graph instance
  }
}
```

### Error: Incomplete Node Attribute Settings Cause Rendering Abnormalities

```javascript
// ❌ Error: Missing necessary attribute settings
const start = graph.addNode({
  shape: 'circle',
  x: 80,
  y: 200,
  width: 40,
  height: 40
});

// ✅ Correct: Complete node attribute settings
const start = graph.addNode({
  shape: 'circle',
  x: 80,
  y: 200,
  width: 40,
  height: 40,
  attrs: { 
    body: { fill: '#52c41a', stroke: '#389e0d' },
    label: { text: 'Start', fill: '#fff', fontSize: 11 }
  },
  ports: {
    groups: {
      out: {
        position: 'right',
        attrs: {
          circle: { r: 4, magnet: true, stroke: '#52c41a', fill: '#fff' }
        }
      }
    },
    items: [{ id: 'out', group: 'out' }]
  }
});
```