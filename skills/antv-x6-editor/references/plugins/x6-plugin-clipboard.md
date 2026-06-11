---
id: "x6-plugin-clipboard"
title: "X6 Clipboard Copy-Paste Plugin"
description: |
  The Clipboard plugin provides copy (Copy), cut (Cut), and paste (Paste) capabilities for canvas elements, supporting cross-canvas pasting and localStorage persistence.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "clipboard"
tags:
  - "Clipboard"
  - "复制"
  - "粘贴"
  - "剪切"
  - "copy"
  - "paste"
  - "cut"

related:
  - "x6-plugins"
  - "x6-plugin-selection"
  - "x6-plugin-keyboard"

use_cases:
  - "Copy selected nodes and edges"
  - "Cut selected elements"
  - "Paste to canvas (with offset)"
  - "Cross-page copy-paste"
  - "Ctrl+C/Ctrl+V shortcuts"

difficulty: "beginner"
completeness: "full"
---

## Basic Usage

```javascript
import { Graph, Clipboard } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Clipboard({ enabled: true }));

// Copy
graph.copy(cells);

// Paste
graph.paste();

// Cut
graph.cut(cells);
```

## Configuration Options

| Option | Type | Default Value | Description |
|--------|------|--------|------|
| `enabled` | boolean | `false` | Whether to enable clipboard |
| `useLocalStorage` | boolean | `false` | Whether to use localStorage for storage (supports cross-page pasting) |

## Programmatic API

### copy(cells, options?)

Copy the specified elements to the clipboard:

```javascript
// Copy selected elements
const cells = graph.getSelectedCells();
graph.copy(cells);

// Deep copy (including child elements)
graph.copy(cells, { deep: true });

// Use localStorage (cross-page)
graph.copy(cells, { useLocalStorage: true });
```

### cut(cells, options?)

Cut: Copy and then delete from the canvas:

```javascript
const cells = graph.getSelectedCells();
graph.cut(cells);
```

### paste(options?)

Paste clipboard content to the canvas:

```javascript
// Default paste (offset by 20px)
graph.paste();

// Custom offset
graph.paste({ offset: 40 });

// Specify offset direction
graph.paste({ offset: { dx: 30, dy: 30 } });

// Modify node properties during paste
graph.paste({
  offset: 20,
  nodeProps: { zIndex: 10 },
  edgeProps: { zIndex: 5 },
});

// Paste from localStorage
graph.paste({ useLocalStorage: true });
```

### getCellsInClipboard()

Get the elements currently in the clipboard:

```javascript
const cells = graph.getCellsInClipboard();
console.log('There are', cells.length, 'elements in the clipboard');
```

### isClipboardEmpty()

Determine if the clipboard is empty:

```javascript
if (!graph.isClipboardEmpty()) {
  graph.paste();
}
```

## Event Listening

```javascript
graph.on('clipboard:changed', ({ cells }) => {
  console.log('Clipboard content changed:', cells.length, 'elements');
});
```

## Complete Example: Copy and Paste + Keyboard Shortcuts

```javascript
import { Graph, Selection, Clipboard, Keyboard } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

graph.use(new Selection({ enabled: true, rubberband: true }));
graph.use(new Clipboard({ enabled: true }));
graph.use(new Keyboard({ enabled: true, global: true }));

// Ctrl+C Copy
graph.bindKey('ctrl+c', () => {
  const cells = graph.getSelectedCells();
  if (cells.length) {
    graph.copy(cells);
  }
});

// Ctrl+X Cut
graph.bindKey('ctrl+x', () => {
  const cells = graph.getSelectedCells();
  if (cells.length) {
    graph.cut(cells);
  }
});

// Ctrl+V Paste
graph.bindKey('ctrl+v', () => {
  if (!graph.isClipboardEmpty()) {
    const cells = graph.paste({ offset: 20 });
    graph.cleanSelection();
    graph.select(cells);  // Select the pasted elements
  }
});

// Add example node
graph.addNode({ x: 100, y: 100, width: 100, height: 50, label: 'Copy me' });
```

## Cross-Page Copy and Paste

After enabling `useLocalStorage`, the copied data is stored in the browser's localStorage, allowing it to be pasted across different pages under the same domain:

```javascript
graph.use(new Clipboard({
  enabled: true,
  useLocalStorage: true,  // Enable cross-page
}));

// Copy on Page A
graph.copy(graph.getSelectedCells(), { useLocalStorage: true });

// Paste on Page B
graph.paste({ useLocalStorage: true });
```

## Common Errors

### ❌ Passing an Empty Array During Copy

```javascript
// Error: No check for selected elements
graph.bindKey('ctrl+c', () => {
  graph.copy(graph.getSelectedCells());  // If no elements are selected, an empty array is passed
  // The clipboard will be cleared at this point!
});
```

```javascript
// Correct: Check first
graph.bindKey('ctrl+c', () => {
  const cells = graph.getSelectedCells();
  if (cells.length) {
    graph.copy(cells);
  }
});
```

### ❌ Calling copy/paste without registering Clipboard

```javascript
// Error: Plugin not registered
const graph = new Graph({ container: 'container' });
graph.copy(cells);   // ❌ Invalid
graph.paste();       // ❌ Invalid
```

```javascript
// Correct: Register plugin first
import { Graph, Clipboard } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Clipboard({ enabled: true }));
graph.copy(cells);   // ✅
graph.paste();       // ✅
```