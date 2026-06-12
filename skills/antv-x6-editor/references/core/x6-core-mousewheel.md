---
id: "x6-core-mousewheel"
title: "X6 Mousewheel Zoom"
description: |
  X6 mousewheel zoom configuration: zoom factor, minimum/maximum zoom ratio, modifier key control, mouse position zoom, etc.

library: "x6"
version: "3.x"
category: "core"
subcategory: "mousewheel"
tags:
  - "mousewheel"
  - "缩放"
  - "zoom"
  - "滚轮"
  - "scale"

related:
  - "x6-core-graph-init"
  - "x6-core-panning"
  - "x6-core-coord"

use_cases:
  - "Zoom canvas with mousewheel"
  - "Ctrl+mousewheel zoom"
  - "Limit zoom range"
  - "Zoom centered at mouse position"

difficulty: "beginner"
completeness: "full"
---
## Basic Usage

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  mousewheel: {
    enabled: true,
    modifiers: 'ctrl',  // Ctrl+wheel zoom
  },
});
```

## Configuration Options

| Option | Type | Default Value | Description |
|--------|------|--------|------|
| `enabled` | boolean | `false` | Whether to enable scroll zoom |
| `global` | boolean | `false` | Whether to listen globally (`true`: listen to document, `false`: listen only to the canvas container) |
| `factor` | number | `1.2` | Zoom factor, the zoom multiplier per scroll |
| `minScale` | number | - | Minimum zoom scale |
| `maxScale` | number | - | Maximum zoom scale |
| `modifiers` | string \| string[] \| null | `null` | Modifier keys: `'ctrl'`, `'alt'`, `'shift'`, `'meta'` |
| `guard` | function | - | Custom judgment function, returns `false` to prevent zoom |
| `zoomAtMousePosition` | boolean | `true` | Whether to zoom centered at the mouse position |

## Modifier Key Control

It is recommended to use `modifiers` to avoid conflicts with page scrolling:

```javascript
mousewheel: {
  enabled: true,
  modifiers: 'ctrl',  // Only Ctrl + wheel triggers zooming
}
```

Multiple modifier keys are supported (any one can satisfy the condition):

```javascript
mousewheel: {
  enabled: true,
  modifiers: ['ctrl', 'meta'],  // Ctrl or Meta modifier key
}
```

## Limit Zoom Range

```javascript
mousewheel: {
  enabled: true,
  modifiers: 'ctrl',
  minScale: 0.5,   // Minimum zoom to 50%
  maxScale: 3,     // Maximum zoom to 300%
}
```

## Zoom Centered at Mouse Position

The default behavior (`zoomAtMousePosition: true`) is to zoom centered at the mouse position, similar to the experience in design tools:

```javascript
mousewheel: {
  enabled: true,
  zoomAtMousePosition: true,  // Default value, centered at the mouse
}
```

When disabled, zooming is centered at the canvas center:

```javascript
mousewheel: {
  enabled: true,
  zoomAtMousePosition: false,  // Zoom centered at the canvas center
}
```

## Custom Filtering with guard

```javascript
mousewheel: {
  enabled: true,
  guard(e) {
    // Disable zooming when the mouse is over a specific area
    if (e.target.closest('.no-zoom-area')) {
      return false;
    }
    return true;
  },
}
```

## Programmatic Zoom API

```javascript
// Set absolute zoom ratio
graph.zoom(1.5, { absolute: true });  // Zoom to 150%

// Relative zoom
graph.zoom(0.2);    // Zoom in by 20%
graph.zoom(-0.2);   // Zoom out by 20%

// Zoom with a specific point as the center
graph.zoom(2, { absolute: true, center: { x: 400, y: 300 } });

// Get the current zoom ratio
graph.zoom();  // number, current zoom value

// Fit to zoom (display all content)
graph.zoomToFit({ padding: 20 });

// Zoom to a specified area
graph.zoomToRect({ x: 100, y: 100, width: 400, height: 300 });
```

## Complete Example

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  grid: { visible: true },
  panning: { enabled: true, modifiers: 'ctrl' },
  mousewheel: {
    enabled: true,
    modifiers: 'ctrl',
    minScale: 0.3,
    maxScale: 5,
    zoomAtMousePosition: true,
  },
});

graph.addNode({ x: 200, y: 200, width: 120, height: 60, label: 'Zoom me' });

// Display current zoom level
graph.on('scale', ({ sx }) => {
  console.log(`Current Zoom: ${Math.round(sx * 100)}%`);
});
```

## Common Errors and Fixes

### ❌ Page Cannot Scroll Due to Missing Modifiers

```javascript
// Issue: Without modifier keys, the wheel event is intercepted by the canvas, preventing page scrolling
mousewheel: { enabled: true }  // ⚠️ Any wheel event triggers zooming
```

```javascript
// Correct: Set modifier keys to allow normal wheel behavior
mousewheel: { enabled: true, modifiers: 'ctrl' }  // ✅
```

### ❌ Confusing Relative and Absolute Modes in zoom()

```javascript
// Note the distinction:
graph.zoom(2);                         // Relative: current scale + 2 (becomes 3x)
graph.zoom(2, { absolute: true });     // Absolute: sets to 2x
```

### ❌ White Screen Due to Incorrectly Specified Container or Unready DOM

```javascript
// Error Example: Container variable is undefined or DOM is not fully loaded
const graph = new Graph({
  container,  // ❌ container variable is undefined
  panning: true,
  mousewheel: {
    enabled: true,
    modifiers: 'ctrl',
    minScale: 0.5,
    maxScale: 3,
  }
});
```

```javascript
// Correct Example: Ensure DOM element exists and is mounted
const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
  panning: {
    enabled: true,
    modifiers: 'shift',
  },
  mousewheel: {
    enabled: true,
    modifiers: 'ctrl',
    minScale: 0.5,
    maxScale: 3,
  },
});

// Add nodes to ensure the canvas has content
graph.addNode({ shape: 'rect', x: 60, y: 60, width: 120, height: 50, label: 'Shift+Drag to pan' });
graph.addNode({ shape: 'rect', x: 260, y: 160, width: 120, height: 50, label: 'Ctrl+Wheel to zoom' });
```

### ❌ Incorrect panning Configuration Causes Dragging to Fail

```javascript
// Antipattern: Neither panning nor mousewheel specifies modifiers,
// and 'mouseWheel' is included in panning.eventTypes, leading to conflicts
// between panning (translation) and mousewheel (zoom) events, resulting in
// a perceived "blank screen / failure".
const graph = new Graph({
  container: 'container',
  panning: {
    enabled: true,
    eventTypes: ['leftMouseDown', 'mouseWheel'], // ❌ Conflicts with mousewheel zoom
  },
  mousewheel: {
    enabled: true,
    modifiers: ['ctrl'],
    minScale: 0.5,
    maxScale: 3,
  },
});
```

```javascript
// Correct: Use modifiers to separate the two interactions
// - Normal left-click drag = Pan (or Shift+drag, depending on product definition)
// - Ctrl + Wheel = Zoom
const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
  panning: {
    enabled: true,
    modifiers: 'shift', // or leave empty: 'leftMouseDown' + no modifiers
  },
  mousewheel: {
    enabled: true,
    modifiers: 'ctrl',
    minScale: 0.5,
    maxScale: 3,
  },
});
```

> Note: `panning` supports boolean shorthand (`panning: true`, equivalent to `{ enabled: true, eventTypes: ['leftMouseDown'] }`), not "does not support boolean values". However, when panning is enabled alongside mousewheel, Selection rubberband, etc., **modifiers must be used to distinguish trigger conditions** to avoid event conflicts.

### ❌ Blank Screen Due to No Content Added After Canvas Initialization

```javascript
// Incorrect Example: Only panning / mousewheel configured, no nodes or edges
const graph = new Graph({
  container: 'container',
  panning: { enabled: true, modifiers: 'shift' },
  mousewheel: { enabled: true, modifiers: 'ctrl', minScale: 0.5, maxScale: 3 },
});
// ❌ Render validation will flag as "blank screen": Canvas exists, but visually no content is present
```

```javascript
// Correct Example: Even if the user query only describes interaction configurations, at least add visible content using addNode/addEdge
const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
  grid: { visible: true, size: 10 },
  panning: { enabled: true, modifiers: 'shift' },
  mousewheel: { enabled: true, modifiers: 'ctrl', minScale: 0.5, maxScale: 3 },
});

graph.addNode({
  shape: 'rect', x: 60, y: 60, width: 120, height: 50, label: 'Shift+Drag to pan',
  attrs: { body: { fill: '#e6f7ff', stroke: '#1890ff', rx: 6, ry: 6 } },
});
graph.addNode({
  shape: 'rect', x: 260, y: 160, width: 120, height: 50, label: 'Ctrl+Wheel to zoom',
  attrs: { body: { fill: '#f6ffed', stroke: '#52c41a', rx: 6, ry: 6 } },
});
graph.addEdge({
  source: { x: 180, y: 85 },
  target: { x: 260, y: 185 },
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
});
```