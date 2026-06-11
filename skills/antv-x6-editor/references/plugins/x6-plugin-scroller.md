---
id: "x6-plugin-scroller"
title: "X6 Scroller Canvas Scrolling Plugin"
description: |
  The Scroller plugin embeds the canvas in a scrollable container, supporting canvas panning (Pan), infinite scrolling, paginated display, and more.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "scroller"
tags:
  - "Scroller"
  - "scrolling"
  - "panning"
  - "pan"
  - "scroll"
  - "canvas panning"
  - "infinite canvas"

related:
  - "x6-plugins"
  - "x6-plugin-minimap"
  - "x6-core-graph-init"

use_cases:
  - "Large canvas scrolling navigation"
  - "Canvas drag panning"
  - "Display page boundaries"
  - "Center canvas content"
  - "Zoom canvas to fit size"

difficulty: "intermediate"
completeness: "full"
---

## Basic Usage

```javascript
import { Graph, Scroller } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Scroller({
  enabled: true,
  pannable: true,  // Canvas can be dragged and panned
}));
```

**Note**: After using the Scroller plugin, the canvas container will be wrapped in a scroll container. The Graph's `container` is no longer the outermost container; instead, `scroller.container` is.

## Configuration Options

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `enabled` | boolean | `true` | Whether to enable scrolling |
| `pannable` | boolean \| object | `false` | Whether panning is enabled. Object format: `{ enabled: true, eventTypes: ['leftMouseDown'] }` |
| `modifiers` | string \| string[] | - | Pan modifier keys, e.g., `'ctrl'`, `['ctrl', 'meta']` |
| `className` | string | - | Custom CSS class name for the scroll container |
| `width` | number | - | Scroll container width (defaults to the same width as the canvas container) |
| `height` | number | - | Scroll container height (defaults to the same height as the canvas container) |
| `pageVisible` | boolean | `false` | Whether to display page boundaries |
| `pageBreak` | boolean | `false` | Whether to display page breakpoints |
| `pageWidth` | number | - | Page width |
| `pageHeight` | number | - | Page height |
| `padding` | number \| object | - | Additional scroll area around the canvas |
| `autoResize` | boolean | `true` | Automatically adjust when container size changes |

### pannable Object Configuration

```javascript
graph.use(new Scroller({
  enabled: true,
  pannable: {
    enabled: true,
    eventTypes: ['leftMouseDown'],  // Only left-click drag to pan
    // Optional values: 'leftMouseDown', 'rightMouseDown'
  },
}));
```

## Programmatic API

After registering Scroller, the following graph methods will delegate their behavior to the Scroller implementation:

```javascript
// Panning control (handled by Scroller)
graph.enablePanning();
graph.disablePanning();
graph.togglePanning(true);
graph.isPannable();  // boolean

// Centering (automatically uses Scroller implementation after registration)
graph.centerPoint(x, y);      // Centers the canvas coordinates (x, y)
graph.centerCell(cell);        // Centers the specified cell
graph.centerContent();         // Centers the canvas content

// Zooming (automatically uses Scroller implementation after registration)
graph.zoom(1.5, { absolute: true });   // Zooms to 150%
graph.zoomToFit({ padding: 20 });      // Auto-fits zoom to make all content visible
graph.zoomToRect(rect);                // Zooms to the specified rectangle area
```

### Scroller Plugin Exclusive API

The following methods are exclusive to the Scroller plugin after registration:

```javascript
// Lock/Unlock scrolling
graph.lockScroller();     // Disable scrolling
graph.unlockScroller();   // Restore scrolling

// Update Scroller (manually refresh after canvas content changes)
graph.updateScroller();

// Get/Set scrollbar position
graph.getScrollbarPosition();              // { left: number, top: number }
graph.setScrollbarPosition(left, top);     // Set scrollbar position

// Get Scroller DOM container
const scroller = graph.getPlugin('scroller');
const scrollerContainer = scroller.container;
```

## Complete Example

```javascript
import { Graph, Scroller, MiniMap } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

graph.use(new Scroller({
  enabled: true,
  pannable: true,
  pageVisible: true,
  pageBreak: false,
  modifiers: 'ctrl',  // Hold Ctrl and drag to pan (to avoid conflicts with node dragging)
}));

// Add multiple nodes distributed across a large area
for (let i = 0; i < 20; i++) {
  graph.addNode({
    x: Math.random() * 2000,
    y: Math.random() * 1500,
    width: 80,
    height: 40,
    label: `Node ${i + 1}`,
  });
}

// Zoom to fit, ensuring all nodes are visible
graph.zoomToFit({ padding: 40 });
```

## Use with MiniMap

When Scroller and MiniMap are used together, MiniMap automatically reflects the viewport area of Scroller:

```javascript
import { Graph, Scroller, MiniMap } from '@antv/x6';

const graph = new Graph({ container: 'container' });

graph.use(new Scroller({ enabled: true, pannable: true }));
graph.use(new MiniMap({
  enabled: true,
  container: document.getElementById('minimap'),
  width: 200,
  height: 160,
}));
```

## Scroller vs panning Configuration

X6 Graph itself has a `panning` configuration (no plugin required), but Scroller provides a more complete scrolling experience:

| Feature | `panning: true` | Scroller Plugin |
|---------|-----------------|-----------------|
| Canvas Drag Panning | ✅ | ✅ |
| Scrollbar | ❌ | ✅ |
| Paginated Display | ❌ | ✅ |
| MiniMap Integration | Partial | ✅ |
| Infinite Scroll Area | ❌ | ✅ |

If you only need simple panning, use `panning: true`; if you require scrollbars and pagination, use the Scroller plugin.

## Common Errors

### ❌ Using panning and Scroller Simultaneously

```javascript
// Error: Both conflict
const graph = new Graph({
  container: 'container',
  panning: true,  // ❌ Conflicts with Scroller
});
graph.use(new Scroller({ enabled: true, pannable: true }));
```

```javascript
// Correct: Do not configure panning when using Scroller
const graph = new Graph({ container: 'container' });
graph.use(new Scroller({ enabled: true, pannable: true }));  // ✅
```

### ❌ Configure scroller in the constructor

```javascript
// Error: Not supported in 3.x
const graph = new Graph({
  container: 'container',
  scroller: { enabled: true, pannable: true },  // ❌
});
```

```javascript
// Correct
import { Graph, Scroller } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Scroller({ enabled: true, pannable: true }));  // ✅
```