---
id: "x6-plugins"
title: "X6 Plugin Configuration"
description: |
  Usage of built-in plugins in X6: Selection, Snapline, History, Clipboard,
  Keyboard, MiniMap, Scroller, Transform, etc.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "all"
tags:
  - "plugin"
  - "import"
  - "Illegal constructor"
  - "is not a constructor"
  - "Embedding"
  - "embedding"
  - "embedding"
  - "node embedding"
  - "Connecting"
  - "Mousewheel"
  - "Panning"
  - "Selection"
  - "selected"
  - "box selection"
  - "Snapline"
  - "alignment line"
  - "History"
  - "undo"
  - "redo"
  - "undo"
  - "redo"
  - "Clipboard"
  - "copy"
  - "paste"
  - "Keyboard"
  - "shortcuts"
  - "MiniMap"
  - "minimap"
  - "Scroller"
  - "scrolling"
  - "Transform"
  - "scaling"
  - "rotation"
  - "Stencil"
  - "sidebar"
  - "drag-and-drop"

related:
  - "x6-core-graph-init"
  - "x6-core-events"

use_cases:
  - "Enable node box selection"
  - "Add alignment guides"
  - "Implement undo/redo"
  - "Configure keyboard shortcuts"
  - "Add minimap navigation"
  - "Enable canvas scrolling"
  - "Node scaling and rotation"
  - "Sidebar drag-and-drop node creation"

anti_patterns:
  - "Do not use the standalone @antv/x6-plugin-xxx package (deprecated)"
  - "Do not pass selecting/snapline/history options in the Graph constructor (not supported in 3.x)"

difficulty: "intermediate"
completeness: "full"
---
## Plugin Usage

In X6 3.x, plugins are imported directly from `@antv/x6` and registered using `graph.use(new Plugin(options))`. Each plugin implements the `GraphPlugin` interface.

```javascript
import { Graph, Selection, Snapline, History } from '@antv/x6';

const graph = new Graph({ container: 'container' });

// Register plugins using graph.use()
graph.use(new Selection({ enabled: true }));
graph.use(new Snapline({ enabled: true }));
graph.use(new History({ enabled: true }));
```

## ⚠️ Plugin Import Quick Reference (Check Before Outputting Code)

All 11 built-in plugins in X6 are imported from the `@antv/x6` **main package**; **only those used must be listed in the import statement**.

| Usage                                            | Required Import                          |
| ------------------------------------------------ | ---------------------------------------- |
| `new Selection(...)` or `graph.select/unselect/...` | `Selection`                              |
| `new Snapline(...)`                              | `Snapline`                               |
| `new History(...)` or `graph.undo/redo`          | `History`                                |
| `new Clipboard(...)` or `graph.copy/paste/cut`   | `Clipboard`                              |
| `new Keyboard(...)` or `graph.bindKey`           | `Keyboard`                               |
| `new MiniMap(...)`                               | `MiniMap`                                |
| `new Scroller(...)`                              | `Scroller`                               |
| `new Transform(...)`                             | `Transform`                              |
| `new Export()` or `graph.toPNG/toSVG/toJPEG`     | `Export`                                 |
| `new Stencil(...)`                               | `Stencil`                                |
| `new Dnd(...)`                                   | `Dnd`                                    |
| `Shape.HTML.register(...)` / `Shape.HTML.create(...)` | `Shape` (not `HTML`)                     |

> It is recommended to **merge imports into a single line** to avoid omissions:
>
> ```javascript
> import { Graph, Shape, Selection, Keyboard, History, Clipboard } from '@antv/x6';
> ```

### ❌ Missing `import Selection` Causes `Failed to construct 'Selection': Illegal constructor`

The evaluation and Playground use the X6 **UMD build** (`window.X6`), which deconstructs corresponding classes from `window.X6` based on the `import` list before execution. If `Selection` is not included in the import, the **identifier `Selection` falls back to `window.Selection`** (the browser's native Selection interface, **not a constructor**), and subsequently `new Selection({...})` throws `Illegal constructor`.

```javascript
// ❌ Missing Selection import leads to Illegal constructor
import { Graph } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Selection({ enabled: true, rubberband: true })); // ❌ Selection not imported → falls back to window.Selection
```

```javascript
// ✅ Must include Selection in the import
import { Graph, Selection } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Selection({ enabled: true, rubberband: true })); // ✅
```

### ❌ `Embedding` / `Connecting` / `Mousewheel` / `Panning` are not plugins, do not use `new` / `graph.use`

X6 3.x has only **11 plugins** (listed in the table above). The following concepts are **all `new Graph({ ... })` constructor options**, not plugin classes:

| Concept          | Incorrect Usage (Runtime Error)                                  | Correct Usage (Graph Constructor Options)                                                          |
| ---------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Node Embedding   | `import { Embedding } from '@antv/x6'` / `new Embedding(...)` / `graph.use(new Embedding(...))` → `Embedding is not a constructor` | `new Graph({ embedding: { enabled: true, findParent: 'bbox', validate: ({ child, parent }) => true } })` |
| Edge Connecting  | `new Connecting(...)` / `graph.use(...)`                        | `new Graph({ connecting: { snap: true, allowBlank: false, router: 'manhattan', connector: 'rounded' } })` |
| Mousewheel Zoom  | `new Mousewheel(...)`                                           | `new Graph({ mousewheel: { enabled: true, modifiers: ['ctrl'], factor: 1.1 } })`     |
| Panning          | `new Panning(...)`                                              | `new Graph({ panning: { enabled: true, modifiers: 'shift' } })`                      |
| Grid / Background| `new Grid(...)` / `new Background(...)`                         | `new Graph({ grid: true, background: { color: '#f5f5f5' } })`                       |
| Node Translating | `new Translating(...)`                                          | `new Graph({ translating: { restrict: true } })`                                     |
| Highlighting     | `new Highlighting(...)`                                         | `new Graph({ highlighting: { magnetAvailable: { name: 'stroke', args: {...} } } })` |

> Quick Rule: If it appears as `interface XxxOptions extends ...` instead of `class Xxx extends Base` in X6 documentation or source code, it is **definitely** a Graph constructor option and cannot be used with `new` / `graph.use`.

```javascript
// ❌ Keyboard / History not imported
import { Graph } from '@antv/x6';
graph.use(new Keyboard({ enabled: true })); // ❌ Keyboard is not a constructor
graph.use(new History({ enabled: true }));  // ❌ History is not a constructor
```

```javascript
// ✅ Import all in the same line
import { Graph, Keyboard, History } from '@antv/x6';
graph.use(new Keyboard({ enabled: true }));
graph.use(new History({ enabled: true }));
```

### ❌ Using `Shape.HTML.register` but forgetting to import `Shape`

```javascript
// ❌
import { Graph } from '@antv/x6';
Shape.HTML.register({ shape: 'form', html() { /* ... */ } }); // ❌ Shape is not defined
```

```javascript
// ✅
import { Graph, Shape } from '@antv/x6';
Shape.HTML.register({ shape: 'form', html() { /* ... */ } });
```

## Selection (Box Selection)

```javascript
import { Graph, Selection } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Selection({
  enabled: true,
  rubberband: true,        // Enable box selection
  multiple: true,          // Allow multiple selection
  showNodeSelectionBox: true,  // Show selection box
  multipleSelectionModifiers: ['ctrl', 'meta'],  // Multi-selection modifier keys
}));

// Programmatic operations (automatically mounted to the graph instance after plugin registration)
graph.select(node);              // Select
graph.unselect(node);            // Deselect
graph.isSelected(node);          // Check if selected
graph.getSelectedCells();        // Get all selected elements
graph.cleanSelection();          // Clear selection
```

## Snapline

```javascript
import { Graph, Snapline } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Snapline({
  enabled: true,
  tolerance: 10,           // Snap tolerance (pixels)
}));
```

## History (Undo/Redo)

```javascript
import { Graph, History } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new History({ enabled: true }));

// Undo
graph.undo();

// Redo
graph.redo();

// Check if undo/redo is possible
graph.canUndo();
graph.canRedo();

// Listen for events
graph.on('history:undo', () => console.log('Undone'));
graph.on('history:redo', () => console.log('Redone'));

// Batch operations into a single undo step (⚠️ Do not use graph.history.batch(), as this method does not exist)
graph.startBatch('custom-batch');
// Perform multiple operations...
graph.stopBatch('custom-batch');

// Or use batchUpdate shorthand
graph.batchUpdate('custom-batch', () => {
  // All operations here will be combined into a single undo step
  graph.addNode({ shape: 'rect', x: 100, y: 100, width: 80, height: 40 });
  graph.addNode({ shape: 'rect', x: 300, y: 100, width: 80, height: 40 });
});
```

## Clipboard (Copy/Paste)

```javascript
import { Graph, Clipboard } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Clipboard({ enabled: true }));

// Copy selected elements
graph.copy(graph.getSelectedCells());

// Paste (offset by 20px)
graph.paste({ offset: 20 });

// Cut
graph.cut(graph.getSelected());
```

## Keyboard (Shortcuts)

```javascript
import { Graph, Keyboard } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Keyboard({
  enabled: true,
  global: true,            // Global shortcuts (not limited to canvas focus)
}));

// Bind shortcuts
graph.bindKey('ctrl+c', () => {
  const cells = graph.getSelectedCells();
  if (cells.length) graph.copy(cells);
});

graph.bindKey('ctrl+v', () => {
  graph.paste({ offset: 20 });
});

graph.bindKey('ctrl+z', () => {
  graph.undo();
});

graph.bindKey('ctrl+shift+z', () => {
  graph.redo();
});

graph.bindKey('delete', () => {
  const cells = graph.getSelectedCells();
  if (cells.length) graph.removeCells(cells);
});

graph.bindKey('ctrl+a', () => {
  graph.select(graph.getCells());
});
```

## Scroller (Canvas Scrolling)

```javascript
import { Graph, Scroller } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Scroller({
  enabled: true,
  pannable: true,          // Canvas is pannable
  pageVisible: true,       // Show pagination
  pageBreak: false,
}));
```

## MiniMap

```javascript
import { Graph, MiniMap } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new MiniMap({
  enabled: true,
  container: document.getElementById('minimap'),  // MiniMap container
  width: 200,
  height: 160,
}));
```

**Note**: MiniMap requires a separate DOM container.

## Transform (Node Scaling/Rotation)

```javascript
import { Graph, Transform } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Transform({
  resizing: {
    enabled: true,           // Enable resizing
  },
  rotating: {
    enabled: true,           // Enable rotation
  },
}));
```

## Stencil (Sidebar Drag Panel)

Stencil is used to create a draggable node panel (toolbox):

```javascript
import { Graph, Stencil } from '@antv/x6';

const graph = new Graph({ container: 'container' });

const stencil = new Stencil({
  title: 'Components',
  target: graph,
  groups: [
    { name: 'basic', title: 'Basic Shapes' },
    { name: 'custom', title: 'Custom Nodes' },
  ],
});
graph.use(stencil);

document.getElementById('stencil').appendChild(stencil.container);

// Load node templates into groups
const basicNodes = [
  graph.createNode({ shape: 'rect', width: 80, height: 40, label: 'Rect' }),
  graph.createNode({ shape: 'circle', width: 60, height: 60, label: 'Circle' }),
];
stencil.load(basicNodes, 'basic');

const customNodes = [
  graph.createNode({ shape: 'dag-node', width: 140, height: 50, label: 'DAG Node' }),
];
stencil.load(customNodes, 'custom');
```

## Dnd (Drag-and-Drop Creation)

Simple drag-and-drop node creation (without sidebar):

```javascript
import { Graph, Dnd } from '@antv/x6';

const graph = new Graph({ container: 'container' });

const dnd = new Dnd({ target: graph });
graph.use(dnd);

// Start dragging from an external element
document.getElementById('drag-source').addEventListener('mousedown', (e) => {
  const node = graph.createNode({
    shape: 'rect',
    width: 100,
    height: 40,
    label: 'New Node',
  });
  dnd.start(node, e);
});
```

## Combined Usage Example

```javascript
import { Graph, Selection, Snapline, History, Clipboard, Keyboard, Transform } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
  grid: { visible: true },
  panning: true,
  mousewheel: { enabled: true, modifiers: 'ctrl' },
  connecting: { allowBlank: false, router: 'orth', connector: 'rounded' },
});

// Register plugins
graph.use(new Selection({ enabled: true, rubberband: true, showNodeSelectionBox: true }));
graph.use(new Snapline({ enabled: true }));
graph.use(new History({ enabled: true }));
graph.use(new Clipboard({ enabled: true }));
graph.use(new Keyboard({ enabled: true, global: true }));
graph.use(new Transform({ resizing: { enabled: true } }));

// Shortcut key bindings
graph.bindKey('ctrl+c', () => graph.copy(graph.getSelectedCells()));
graph.bindKey('ctrl+v', () => graph.paste({ offset: 20 }));
graph.bindKey('ctrl+z', () => graph.undo());
graph.bindKey('ctrl+shift+z', () => graph.redo());
graph.bindKey('delete', () => graph.removeCells(graph.getSelectedCells()));
```

## Common Errors and Fixes

### ❌ Error: Passing Plugin Options in the Constructor

**Problematic Code**:
```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  selecting: { enabled: true },  // ❌ Not supported in 3.x
  snapline: { enabled: true },   // ❌ Not supported in 3.x
  history: { enabled: true },    // ❌ Not supported in 3.x
});
```

**Cause of Error**:
In X6 3.x, plugins are registered using `graph.use()`, and the constructor options pattern is not supported.

**Corrected Code**:
```javascript
import { Graph, Selection, Snapline, History } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Selection({ enabled: true }));
graph.use(new Snapline({ enabled: true }));
graph.use(new History({ enabled: true }));
```

### ❌ Error: Using `@antv/x6-plugin-xxx` standalone packages

**Problematic Code**:
```javascript
import { Selection } from '@antv/x6-plugin-selection';  // ❌ Deprecated
import { History } from '@antv/x6-plugin-history';      // ❌ Deprecated
```

**Cause of Error**:
Standalone plugin packages are deprecated. In 3.x, all plugins are directly exported from `@antv/x6`.

**Corrected Code**:
```javascript
import { Graph, Selection, History } from '@antv/x6';  // ✅ Correct
```

### ❌ Error: Calling `graph.render()`

**Problematic Code**:
```javascript
const data = { nodes: [...], edges: [...] };
graph.fromJSON(data);
graph.render(); // ❌ Error
```

**Cause of Error**:
`graph.fromJSON()` automatically renders the graph, so there's no need to manually call `render()`.

**Corrected Code**:
```javascript
const data = { nodes: [...], edges: [...] };
graph.fromJSON(data);
```

### ❌ Error: White Screen Due to Incorrect Initialization of Canvas Container or Missing Base Nodes

**Problematic Code**:
```javascript
import { Graph, Selection, Snapline, History, Keyboard } from '@antv/x6';

const graph = new Graph({
  container: container, // ❌ Should use string: container: 'container'
});

graph.use(new Selection({ enabled: true }));
graph.use(new Snapline({ enabled: true }));
graph.use(new History({ enabled: true }));
graph.use(new Keyboard({ enabled: true }));

// ❌ No nodes or edges added, resulting in a blank canvas
```

**Cause of Error**:
1. The `container` parameter should be a DOM element or its ID string.
2. No nodes or edges were added to the canvas, resulting in a white screen.

**Corrected Code**:
```javascript
import { Graph, Selection, Snapline, History, Keyboard, Clipboard } from '@antv/x6';

const graph = new Graph({
  container: 'container', // ✅ Correct: Use string ID
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
  grid: { visible: true },
  panning: true,
  mousewheel: { enabled: true, modifiers: 'ctrl' },
  connecting: { allowBlank: false, router: 'orth', connector: 'rounded' },
});

// Register plugins
graph.use(new Selection({ enabled: true, rubberband: true }));
graph.use(new Snapline({ enabled: true }));
graph.use(new History({ enabled: true }));
graph.use(new Keyboard({ enabled: true }));
graph.use(new Clipboard({ enabled: true }));

// Add base nodes and edges
const node1 = graph.addNode({ shape: 'rect', x: 100, y: 100, width: 80, height: 40, label: 'Start' });
const node2 = graph.addNode({ shape: 'circle', x: 300, y: 100, width: 60, height: 60, label: 'End' });
graph.addEdge({ source: node1, target: node2 });

// Shortcut key bindings
graph.bindKey('delete', () => {
  const cells = graph.getSelectedCells();
  if (cells.length) graph.removeCells(cells);
});
graph.bindKey('ctrl+z', () => graph.undo());
graph.bindKey('ctrl+shift+z', () => graph.redo());
graph.bindKey('ctrl+c', () => graph.copy(graph.getSelectedCells()));
graph.bindKey('ctrl+v', () => graph.paste({ offset: 20 }));
```

### ❌ Error: Incorrect Plugin Method Invocation (e.g., `keyboard.bindKey`)

**Problematic Code**:
```javascript
const keyboard = new Keyboard({ enabled: true, global: true });
graph.use(keyboard);

keyboard.bindKey(['delete', 'backspace'], () => { ... }); // ❌ Error
```

**Cause of Error**:  
Plugin methods should be invoked through the `graph` instance, not the plugin instance.

**Corrected Code**:
```javascript
graph.use(new Keyboard({ enabled: true, global: true }));

graph.bindKey(['delete', 'backspace'], () => {
  const cells = graph.getSelectedCells();
  if (cells.length) graph.removeCells(cells);
});
```

### ❌ Error: The `batch` method does not exist in the History plugin

**Problematic Code**:
```javascript
graph.history.batch(() => {
  const node1 = graph.addNode(data[0]);
  const node2 = graph.addNode(data[1]);
  graph.addEdge({ source: node1, target: node2 });
});
```

**Cause of Error**:
The History plugin does not have a `batch` method. Use `graph.startBatch()` and `graph.stopBatch()` to control batch operations.

**Corrected Code**:
```javascript
graph.startBatch('custom-batch');

const node1 = graph.addNode(data[0]);
const node2 = graph.addNode(data[1]);
graph.addEdge({ source: node1, target: node2 });

graph.stopBatch('custom-batch');
```

---