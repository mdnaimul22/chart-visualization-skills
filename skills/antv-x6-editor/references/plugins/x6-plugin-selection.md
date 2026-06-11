---
id: "x6-plugin-selection"
title: "X6 Selection Box Plugin"
description: |
  The Selection plugin provides single-click, multi-select, and box selection capabilities for nodes/edges, supporting features such as selection box display, modifier key multi-select, and drag-and-move of selected elements.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "selection"
tags:
  - "Selection"
  - "Select"
  - "Box Selection"
  - "Multi-select"
  - "rubberband"
  - "select"
  - "unselect"
  - "getSelectedCells"

related:
  - "x6-plugins"
  - "x6-plugin-keyboard"
  - "x6-core-events"

use_cases:
  - "Box select multiple nodes"
  - "Click to select nodes/edges"
  - "Ctrl/Meta multi-select"
  - "Get list of selected elements"
  - "Batch delete after selection"
  - "Batch move after selection"

difficulty: "beginner"
completeness: "full"
---

## Basic Usage

```javascript
import { Graph, Selection } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Selection({
  enabled: true,
  rubberband: true,  // Enable box selection
}));
```

## Configuration Options

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `enabled` | boolean | `false` | Whether to enable the selection feature |
| `rubberband` | boolean | `false` | Whether to enable rubberband selection (drag a rectangle to select elements) |
| `multiple` | boolean | `true` | Whether to allow multiple selections |
| `strict` | boolean | `false` | Strict mode: elements must be completely within the selection box to be selected |
| `showNodeSelectionBox` | boolean | `false` | Whether to display the selection box when a node is selected |
| `showEdgeSelectionBox` | boolean | `false` | Whether to display the selection box when an edge is selected |
| `movable` | boolean | `true` | Whether selected elements can be dragged and moved |
| `multipleSelectionModifiers` | string[] | `['ctrl', 'meta']` | Modifier keys for multiple selection |
| `rubberband` | boolean | `false` | Enable rubberband selection |
| `filter` | function/string[] | - | Filter unselectable elements |
| `content` | function | - | Customize the content displayed in the selection box |

## Programmatic API

After the Selection plugin is registered, the following methods are automatically mounted to the graph instance:

```javascript
// Select elements (supports node ID, node instance, array)
graph.select(node);
graph.select([node1, node2]);
graph.select('node-id');

// Deselect elements
graph.unselect(node);
graph.unselect([node1, node2]);

// Check if an element is selected
graph.isSelected(node);       // boolean
graph.isSelected('node-id');  // boolean

// Get selected elements
graph.getSelectedCells();      // Cell[]
graph.getSelectedCellCount();  // number

// Clear selection
graph.cleanSelection();

// Reset selection (replace current selection with new elements)
graph.resetSelection([node1, node2]);

// Check if selection is empty
graph.isSelectionEmpty();  // boolean
```

## Dynamic Control API

```javascript
// Enable/Disable Selection
graph.enableSelection();
graph.disableSelection();
graph.toggleSelection(true);
graph.isSelectionEnabled();  // boolean

// Enable/Disable Multiple Selection
graph.enableMultipleSelection();
graph.disableMultipleSelection();
graph.toggleMultipleSelection(true);
graph.isMultipleSelection();  // boolean

// Enable/Disable Rubberband
graph.enableRubberband();
graph.disableRubberband();
graph.toggleRubberband(true);
graph.isRubberbandEnabled();  // boolean

// Enable/Disable Strict Rubberband
graph.enableStrictRubberband();
graph.disableStrictRubberband();
graph.toggleStrictRubberband(true);
graph.isStrictRubberband();  // boolean

// Allow Selected Elements to be Dragged
graph.enableSelectionMovable();
graph.disableSelectionMovable();
graph.toggleSelectionMovable(true);
graph.isSelectionMovable();  // boolean

// Set Rubberband Modifier Keys
graph.setRubberbandModifiers('alt');
graph.setRubberbandModifiers(['ctrl', 'shift']);

// Set Selection Filter
graph.setSelectionFilter((cell) => cell.isNode());

// Set Custom Content for Selection Box
graph.setSelectionDisplayContent((selection, contentElement) => {
  contentElement.textContent = `${selection.length} items`;
});
```

## Event Listening

```javascript
// Selection change event
graph.on('selection:changed', ({ added, removed, selected }) => {
  // added: Newly selected elements
  // removed: Deselected elements
  // selected: All currently selected elements
  console.log('Currently selected:', selected.length, 'elements');
});
```

## Complete Example: Box Selection + Shortcut Key Deletion

```javascript
import { Graph, Selection, Keyboard } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

graph.use(new Selection({
  enabled: true,
  rubberband: true,
  multiple: true,
  showNodeSelectionBox: true,
  multipleSelectionModifiers: ['ctrl', 'meta'],
}));
graph.use(new Keyboard({ enabled: true }));

// Delete key to remove selected elements
graph.bindKey('delete', () => {
  const cells = graph.getSelectedCells();
  if (cells.length) {
    graph.removeCells(cells);
  }
});

// Ctrl+A to select all
graph.bindKey('ctrl+a', () => {
  graph.select(graph.getCells());
});

// Add sample data
graph.addNode({ id: 'node1', x: 100, y: 100, width: 80, height: 40, label: 'Node 1' });
graph.addNode({ id: 'node2', x: 300, y: 100, width: 80, height: 40, label: 'Node 2' });
graph.addEdge({ source: 'node1', target: 'node2' });
```

## Filter Example: Only Allow Node Selection

```javascript
graph.use(new Selection({
  enabled: true,
  rubberband: true,
  filter: (cell) => cell.isNode(),  // edges cannot be selected
}));
```

Filtering by shape name is also possible:

```javascript
graph.use(new Selection({
  enabled: true,
  filter: ['rect', 'circle'],  // only allow selection of rect and circle shapes
}));
```

## Common Errors

### ❌ Calling graph.select() without registering the plugin

```javascript
// Error: Selection plugin not registered
const graph = new Graph({ container: 'container' });
graph.select(node);  // ❌ Invalid, no error but ineffective
```

```javascript
// Correct: Register the plugin first
import { Graph, Selection } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Selection({ enabled: true }));
graph.select(node);  // ✅
```

### ❌ Configuring `selecting` in the Constructor

```javascript
// Incorrect: Not supported in 3.x
const graph = new Graph({
  container: 'container',
  selecting: { enabled: true, rubberband: true },  // ❌
});
```

```javascript
// Correct: Use graph.use()
import { Graph, Selection } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Selection({ enabled: true, rubberband: true }));  // ✅
```