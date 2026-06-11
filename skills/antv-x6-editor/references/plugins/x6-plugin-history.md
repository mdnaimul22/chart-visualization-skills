---
id: "x6-plugin-history"
title: "X6 History Plugin for Undo and Redo"
description: |
  The History plugin provides undo (Undo) and redo (Redo) capabilities for canvas operations, automatically recording operations such as adding, deleting, and changing properties of nodes/edges.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "history"
tags:
  - "History"
  - "Undo"
  - "Redo"
  - "undo"
  - "redo"
  - "History Records"
  - "Operation Rollback"

related:
  - "x6-plugins"
  - "x6-plugin-keyboard"
  - "x6-core-events"

use_cases:
  - "Undo the last operation"
  - "Redo an undone operation"
  - "Implement Ctrl+Z/Ctrl+Y shortcuts"
  - "Limit the size of the history stack"
  - "Ignore specific types of operation changes"
  - "Batch operations as a single undo"

difficulty: "beginner"
completeness: "full"
---

## Basic Usage

```javascript
import { Graph, History } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new History({ enabled: true }));

// Undo
graph.undo();

// Redo
graph.redo();
```

## Configuration Options

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `enabled` | boolean | `false` | Whether to enable history records |
| `stackSize` | number | `0` (unlimited) | Maximum capacity of the history stack, exceeding which the earliest records are discarded |
| `ignoreAdd` | boolean | `false` | Ignore element addition operations |
| `ignoreRemove` | boolean | `false` | Ignore element removal operations |
| `ignoreChange` | boolean | `false` | Ignore element property change operations |
| `beforeAddCommand` | function | - | Hook before command is added to the stack, returning `false` prevents stacking |
| `afterAddCommand` | function | - | Callback after command is added to the stack |
| `executeCommand` | function | - | Custom command execution logic |
| `cancelInvalid` | boolean | `true` | Whether to cancel invalid commands |

## Programmatic API

```javascript
// Undo/Redo
graph.undo();            // Undo the last step
graph.redo();            // Redo
graph.undoAndCancel();   // Undo but do not add to redoStack (cannot redo)

// Query Status
graph.canUndo();  // boolean, whether undo is possible
graph.canRedo();  // boolean, whether redo is possible

// Stack Size Query
graph.getHistoryStackSize();  // History stack capacity (stackSize configuration value, 0 means unlimited)
graph.getUndoStackSize();     // Number of records in the current undo stack
graph.getRedoStackSize();     // Number of records in the current redo stack
graph.getUndoRemainSize();    // Remaining available space in the undo stack

// Clear History
graph.cleanHistory();

// Enable/Disable
graph.enableHistory();
graph.disableHistory();
graph.toggleHistory(true);
graph.isHistoryEnabled();  // boolean
```

## Event Listening

```javascript
// Triggered when undoing
graph.on('history:undo', ({ cmds, options }) => {
  console.log('Undone');
});

// Triggered when redoing
graph.on('history:redo', ({ cmds, options }) => {
  console.log('Redone');
});

// Triggered when a new command is pushed to the stack
graph.on('history:add', ({ cmds, options }) => {
  console.log('New history record added');
});

// Triggered when the history stack is cleared
graph.on('history:clean', ({ cmds, options }) => {
  console.log('History cleared');
});

// Triggered on any history change (undo/redo/add/clean will all trigger this)
graph.on('history:change', ({ cmds, options }) => {
  // Can be used to update UI button states
  updateUndoButton(graph.canUndo());
  updateRedoButton(graph.canRedo());
});
```

## Configure History Stack Size

```javascript
graph.use(new History({
  enabled: true,
  stackSize: 50,  // Maximum of 50 operations saved
}));
```

## Filtering Unnecessary Operations

```javascript
graph.use(new History({
  enabled: true,
  // Ignore all property changes (only record add/delete)
  ignoreChange: true,
}));
```

Use `beforeAddCommand` for fine-grained filtering:

```javascript
graph.use(new History({
  enabled: true,
  beforeAddCommand(event, args) {
    // Ignore changes to specific properties
    if (event === 'cell:change:attrs') {
      return false;  // Do not record attrs changes
    }
  },
}));
```

## Complete Example: Undo/Redo + Shortcuts + UI State

```javascript
import { Graph, History, Keyboard } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

graph.use(new History({ enabled: true, stackSize: 100 }));
graph.use(new Keyboard({ enabled: true, global: true }));

// Bind shortcuts
graph.bindKey('ctrl+z', () => graph.undo());
graph.bindKey('ctrl+shift+z', () => graph.redo());

// Listen for history changes to update UI buttons
graph.on('history:change', () => {
  document.getElementById('undo-btn').disabled = !graph.canUndo();
  document.getElementById('redo-btn').disabled = !graph.canRedo();
});

// Add a test node
graph.addNode({ x: 100, y: 100, width: 80, height: 40, label: 'Node' });
// At this point, canUndo() === true
```

## Batch Operations Merged into a Single Undo

X6's `model.startBatch()` / `model.stopBatch()` can merge multiple operations into a single history record:

```javascript
// Start batch operation
graph.startBatch('custom-batch');

// The following operations will be merged into a single history record
graph.addNode({ id: 'a', x: 100, y: 100, width: 80, height: 40 });
graph.addNode({ id: 'b', x: 300, y: 100, width: 80, height: 40 });
graph.addEdge({ source: 'a', target: 'b' });

// End batch operation
graph.stopBatch('custom-batch');

// A single undo() will revert the above three operations
graph.undo();
```

## Common Errors

### ❌ Calling undo/redo on an unregistered plugin

```javascript
const graph = new Graph({ container: 'container' });
graph.undo();  // ❌ Invalid, History plugin is not registered
```

```javascript
import { Graph, History } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new History({ enabled: true }));
graph.undo();  // ✅
```

### ❌ Configure history in the constructor

```javascript
// Error: Not supported in 3.x
const graph = new Graph({
  container: 'container',
  history: { enabled: true },  // ❌
});
```

```javascript
// Correct
import { Graph, History } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new History({ enabled: true }));  // ✅
```