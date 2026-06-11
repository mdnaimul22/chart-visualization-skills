---
id: "x6-plugin-keyboard"
title: "X6 Keyboard Shortcut Plugin"
description: |
  The Keyboard plugin provides keyboard shortcut support for the canvas.
  It is implemented based on the Mousetrap library, supporting key combinations, key sequences, and scope control.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "keyboard"
tags:
  - "keyboard"
  - "shortcut"
  - "hotkey"
  - "bindKey"
  - "Mousetrap"
  - "ctrl"
  - "undo"
  - "redo"
  - "delete"
  - "copy"
  - "paste"

related:
  - "x6-plugins"
  - "x6-core-events"

use_cases:
  - "Bind Ctrl+Z/Ctrl+Y for undo and redo"
  - "Bind Delete/Backspace to delete selected elements"
  - "Bind Ctrl+C/Ctrl+V for copy and paste"
  - "Customize shortcut operations on the canvas"

difficulty: "beginner"
completeness: "full"
---

## Core Concepts

The **Keyboard** plugin, based on the [Mousetrap](https://github.com/ccampbell/mousetrap) library, provides shortcut key binding capabilities for the canvas. It supports:
- Single keys: `'delete'`, `'backspace'`, `'escape'`
- Combination keys: `'ctrl+z'`, `'ctrl+shift+z'`, `'command+c'`
- Sequence keys: `'g i'` (press g followed by i)
- Multiple key bindings: array form to bind multiple keys simultaneously

## Basic Usage

```javascript
import { Graph, Keyboard } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

// Register Keyboard plugin
const keyboard = new Keyboard({ enabled: true });
graph.use(keyboard);

// Bind shortcut keys
keyboard.bindKey('ctrl+z', () => {
  // Undo operation
});

keyboard.bind(Keyboard.events.KEYDOWN, (e) => {
  console.log('keydown', e);
});

keyboard.bindKey('ctrl+shift+z', () => {
  // Redo operation
});

keyboard.bindKey(['delete', 'backspace'], () => {
  // Delete selected elements
  const cells = graph.getSelectedCells();
  if (cells.length) {
    graph.removeCells(cells);
  }
});
```

## Configuration Options

### KeyboardOptions

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `enabled` | `boolean` | `true` | Whether to enable |
| `global` | `boolean` | `false` | Whether to bind to `document` (`true`) or the canvas container (`false`) |
| `format` | `(key: string) => string` | None | Key formatting function |
| `guard` | `(e: KeyboardEvent) => boolean` | None | Guard function, returns `true` to prevent shortcut triggering |

### Global Parameter Description

- `false` (default): Shortcuts only take effect when the canvas container is focused. The container automatically sets `tabindex="-1"` to ensure focusability.  
- `true`: Shortcuts are bound to the `document`, taking effect globally without requiring the canvas to be focused.

## API Methods

| Method | Description |
|--------|-------------|
| `keyboard.bindKey(keys, callback, action?)` | Bind shortcut key |
| `keyboard.unbindKey(keys, action?)` | Unbind shortcut key |
| `keyboard.trigger(key, action?)` | Manually trigger shortcut key callback |
| `keyboard.clear()` | Clear all bindings |
| `keyboard.enable()` | Enable keyboard |
| `keyboard.disable()` | Disable keyboard |
| `keyboard.isEnabled()` | Get enabled status |
| `keyboard.toggleEnabled(enabled?)` | Toggle enabled status |

### bindKey Parameter

| Parameter | Type | Description |
|------|------|------|
| `keys` | `string \| string[]` | Key or array of keys |
| `callback` | `(e: KeyboardEvent) => void` | Callback function |
| `action` | `'keypress' \| 'keydown' \| 'keyup'` | Optional, trigger timing, default `'keydown'` |

### Key Syntax (Mousetrap Format)

| Type | Example | Description |
|------|------|------|
| Single Key | `'a'`, `'1'`, `'delete'` | Single key |
| Modifier Combination | `'ctrl+s'`, `'command+c'` | Modifier key + key |
| Multiple Modifiers | `'ctrl+shift+z'` | Multiple modifier keys |
| Multi-key Binding | `['ctrl+z', 'command+z']` | Array, compatible with Win/Mac |
| Sequence Keys | `'g i'` (space-separated) | Press in sequence |

## Complete Example

### Common Editor Shortcuts

```javascript
import { Graph, Keyboard, Selection, Clipboard, History } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

graph.use(new Selection({ enabled: true, rubberband: true }));
graph.use(new Clipboard({ enabled: true }));
graph.use(new History({ enabled: true }));

const keyboard = new Keyboard({ enabled: true });
graph.use(keyboard);

// Undo/Redo
keyboard.bindKey(['ctrl+z', 'command+z'], () => {
  if (graph.canUndo()) {
    graph.undo();
  }
});

keyboard.bindKey(['ctrl+shift+z', 'command+shift+z'], () => {
  if (graph.canRedo()) {
    graph.redo();
  }
});

// Delete
keyboard.bindKey(['delete', 'backspace'], () => {
  const cells = graph.getSelectedCells();
  if (cells.length) {
    graph.removeCells(cells);
  }
});

// Copy/Paste
keyboard.bindKey(['ctrl+c', 'command+c'], () => {
  const cells = graph.getSelectedCells();
  if (cells.length) {
    graph.copy(cells);
  }
});

keyboard.bindKey(['ctrl+v', 'command+v'], () => {
  if (!graph.isClipboardEmpty()) {
    const cells = graph.paste({ offset: 32 });
    graph.cleanSelection();
    graph.select(cells);
  }
});

// Select All
keyboard.bindKey(['ctrl+a', 'command+a'], (e) => {
  e.preventDefault();
  graph.select(graph.getCells());
});
```

### Global Mode (No Canvas Focus Required)

```javascript
const keyboard = new Keyboard({
  enabled: true,
  global: true,  // Bind to document
  guard(e) {
    // Do not trigger in input/textarea
    const tagName = (e.target as HTMLElement)?.tagName?.toLowerCase();
    return tagName === 'input' || tagName === 'textarea';
  },
});
graph.use(keyboard);
```

## Common Errors

### ❌ Shortcuts Not Working (Canvas Not Focused)

```javascript
// Issue: In default mode, shortcuts do not trigger when the canvas container is not focused
const keyboard = new Keyboard({ enabled: true });
graph.use(keyboard);
// Shortcuts only work after clicking on the canvas

// Solution 1: Use global mode
const keyboard = new Keyboard({ enabled: true, global: true });

// Solution 2: Manually focus the container
graph.container.focus();
```

### ❌ Mac/Windows Compatibility Issues

```javascript
// Error: Only binds ctrl, Mac users cannot use
keyboard.bindKey('ctrl+z', handler); // ❌ Does not work on Mac

// Correct: Binds both ctrl and command
keyboard.bindKey(['ctrl+z', 'command+z'], handler); // ✅
```

### ❌ Incorrect Usage of `graph.bindKey` or `graph.bind`

```javascript
// Incorrect: Using graph.bindKey (non-existent method)
graph.bindKey('ctrl+s', handler); // ❌ Error: graph.bindKey is not a function

// Correct: Using bindKey with a keyboard instance
const keyboard = new Keyboard({ enabled: true });
graph.use(keyboard);
keyboard.bindKey('ctrl+s', handler); // ✅

// Incorrect: Using graph.bind to listen to Keyboard.events (deprecated or non-existent)
graph.bind(Keyboard.events.KEYDOWN, handler); // ❌ Error: Cannot read properties of undefined

// Correct: Using keyboard.bindKey to bind key combinations
keyboard.bindKey('ctrl+d', () => {
  const cells = graph.getSelectedCells();
  if (cells.length) {
    const cloned = graph.cloneCells(cells);
    Object.values(cloned).forEach((cell) => {
      if (cell.isNode()) {
        cell.translate(30, 30);
        graph.addCell(cell);
      }
    });
  }
});
```

### ❌ Shortcut Key Conflicts or Default Behavior Not Prevented

```javascript
// Error: Browser default behavior not prevented, may cause side effects like page navigation
keyboard.bindKey('ctrl+s', () => {
  const data = graph.toJSON();
  console.log(data);
}); // ❌ Browser will prompt a save dialog

// Correct: Prevent default behavior in the callback
keyboard.bindKey('ctrl+s', (e) => {
  e.preventDefault();
  const data = graph.toJSON();
  console.log(data);
  return false; // Optional: Return false to prevent further bubbling
});
```

### ❌ Runtime Error Caused by Undefined Variable

```javascript
// Error: Incorrect declaration of the keyboard variable results in runtime error "keyboard is not defined"
const keyboard = new Keyboard({ enabled: true });
graph.use(keyboard);

keyboard.bindKey(['ctrl+c', 'command+c'], () => {
  const cells = graph.getSelectedCells();
  if (cells.length) {
    graph.copy(cells);
  }
});

// Correct: Ensure the keyboard variable is declared and used correctly
const keyboard = new Keyboard({ enabled: true });
graph.use(keyboard);

keyboard.bindKey(['ctrl+c', 'command+c'], () => {
  const cells = graph.getSelectedCells();
  if (cells.length) {
    graph.copy(cells);
  }
});
```

### ❌ Use keyboard.bindKey instead of graph.bindKey

```javascript
// Error: Using graph.bindKey (non-existent method)
graph.bindKey('ctrl+s', handler); // ❌ Error: graph.bindKey is not a function

// Correct: Use bindKey by calling the keyboard instance
const keyboard = new Keyboard({ enabled: true });
graph.use(keyboard);
keyboard.bindKey('ctrl+s', handler); // ✅
```

</skill>