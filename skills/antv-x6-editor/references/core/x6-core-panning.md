---
id: "x6-core-panning"
title: "X6 Canvas Panning"
description: |
  X6 canvas panning configuration: mouse drag panning, modifier key control, supports various trigger methods including left-click, right-click, mouse wheel, and mouse wheel press.

library: "x6"
version: "3.x"
category: "core"
subcategory: "panning"
tags:
  - "panning"
  - "pan"
  - "canvas drag"
  - "canvas move"

related:
  - "x6-core-graph-init"
  - "x6-core-mousewheel"
  - "x6-plugin-scroller"

use_cases:
  - "Drag blank area to pan canvas"
  - "Hold modifier key and drag to pan"
  - "Right-click drag to pan"
  - "Mouse wheel to pan canvas"
  - "Spacebar + drag to pan"

difficulty: "beginner"
completeness: "full"
---
## Basic Usage

Canvas panning is configured in the Graph constructor via the `panning` field:

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  panning: true,  // Shorthand: Enable left-click drag panning
});
```

## Configuration Options

| Option | Type | Default Value | Description |
|--------|------|--------|------|
| `enabled` | boolean | `false` | Whether to enable panning |
| `modifiers` | string \| string[] \| null | `null` | Modifier keys: `'ctrl'`, `'alt'`, `'shift'`, `'meta'`, or an array combination |
| `eventTypes` | string[] | `['leftMouseDown']` | Trigger methods: `'leftMouseDown'`, `'rightMouseDown'`, `'mouseWheel'`, `'mouseWheelDown'` |

## Abbreviated Form

```javascript
// Boolean shorthand
panning: true
// Equivalent to
panning: { enabled: true, eventTypes: ['leftMouseDown'] }
```

## Object Configuration

```javascript
const graph = new Graph({
  container: 'container',
  panning: {
    enabled: true,
    modifiers: 'ctrl',  // Hold Ctrl to enable panning
    eventTypes: ['leftMouseDown'],
  },
});
```

## Trigger Method Description

| eventType | Description |
|-----------|------|
| `'leftMouseDown'` | Left mouse button drag on blank area to pan |
| `'rightMouseDown'` | Right mouse button drag to pan |
| `'mouseWheel'` | Mouse wheel scroll to pan (not zoom) |
| `'mouseWheelDown'` | Press and drag mouse wheel (middle button) to pan |

Combination of multiple methods:

```javascript
panning: {
  enabled: true,
  eventTypes: ['leftMouseDown', 'rightMouseDown'],  // Both left and right buttons can pan
}
```

## Modifier Key Control

Use `modifiers` to avoid conflicts between panning and rubberband selection:

```javascript
import { Graph, Selection } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  panning: {
    enabled: true,
    modifiers: 'ctrl',  // Ctrl+drag = panning
  },
});

// Drag without modifier key = rubberband selection
graph.use(new Selection({ enabled: true, rubberband: true }));
```

## Space Key Panning

X6 provides built-in support for temporary panning using the space key (similar to design tools). Simply hold down the space key and drag to pan the canvas, with no additional configuration required:

```javascript
const graph = new Graph({
  container: 'container',
  panning: { enabled: true },
  // Hold space key + mouse drag = pan (automatically supported)
});
```

## Programmatic API

```javascript
// Enable panning
graph.enablePanning();

// Disable panning
graph.disablePanning();

// Check if panning is enabled
graph.isPannable();  // boolean

// Canvas panning (programmatic)
graph.translateBy(dx, dy);   // Relative translation
graph.translate(tx, ty);     // Set absolute offset
```

## Complete Example: Panning + Box Selection + Zooming

```javascript
import { Graph, Selection } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
  grid: { visible: true },
  // Ctrl+Drag to pan (avoid conflict with box selection)
  panning: { enabled: true, modifiers: 'ctrl' },
  // Ctrl+Mouse wheel to zoom
  mousewheel: { enabled: true, modifiers: 'ctrl' },
});

// Drag without modifiers = Box selection
graph.use(new Selection({ enabled: true, rubberband: true }));

graph.addNode({ x: 100, y: 100, width: 120, height: 60, label: 'Node A' });
graph.addNode({ x: 400, y: 300, width: 120, height: 60, label: 'Node B' });
```

## Panning and Mousewheel Coexistence

If `'mouseWheel'` is included in `panning.eventTypes`, X6 will use the mouse wheel for **panning**, which directly conflicts with the **zooming** behavior of `mousewheel: { enabled: true }`, causing zoom to be unresponsive or behave abnormally. When configuring both, use `modifiers` to offset the trigger conditions:

```javascript
// ✅ Recommended: Left-click drag to pan + Ctrl+wheel to zoom (no interference)
const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
  panning: { enabled: true },                       // Equivalent to eventTypes: ['leftMouseDown']
  mousewheel: { enabled: true, modifiers: 'ctrl' }, // Only Ctrl+wheel to zoom
});

// ✅ Recommended: Shift+drag to pan + Ctrl+wheel to zoom (even with Selection rubberband, no conflict)
const graph2 = new Graph({
  container: 'container',
  panning: { enabled: true, modifiers: 'shift' },
  mousewheel: { enabled: true, modifiers: 'ctrl', minScale: 0.5, maxScale: 3 },
});
```

```javascript
// ❌ Anti-pattern: mouseWheel in panning.eventTypes with mousewheel zoom enabled simultaneously
const graph = new Graph({
  container: 'container',
  panning: { enabled: true, eventTypes: ['leftMouseDown', 'mouseWheel'] }, // ❌
  mousewheel: { enabled: true, modifiers: ['ctrl'], minScale: 0.5, maxScale: 3 },
});
```

## Panning vs Scroller

| Feature | `panning` Configuration | Scroller Plugin |
|---------|--------------------------|-----------------|
| Drag to Pan | ✅ | ✅ |
| Scrollbar | ❌ | ✅ |
| Paged Display | ❌ | ✅ |
| Infinite Scroll Area | ❌ | ✅ |
| Configuration Method | Graph Constructor | `graph.use()` |

Use `panning` for simple needs, and use the Scroller plugin when scrollbars and paging are required. **Both cannot be used simultaneously**.

## Common Errors

### ❌ Using panning and Scroller Simultaneously

```javascript
// Error: Conflict
const graph = new Graph({
  container: 'container',
  panning: true,  // ❌
});
graph.use(new Scroller({ enabled: true, pannable: true }));
```

```javascript
// Correct: Choose One
// Option A: Use panning
const graph = new Graph({ container: 'container', panning: true });

// Option B: Use Scroller
const graph = new Graph({ container: 'container' });
graph.use(new Scroller({ enabled: true, pannable: true }));
```

### ❌ Conflict Between Panning and Rubberband

```javascript
// Issue: Without modifier keys, is dragging for panning or rubberband selection?
const graph = new Graph({
  container: 'container',
  panning: { enabled: true },  // No modifier key
});
graph.use(new Selection({ enabled: true, rubberband: true }));  // Also no modifier key
// Result: Rubberband selection has higher priority, panning does not take effect
```

```javascript
// Correct: Use modifier keys to differentiate
const graph = new Graph({
  container: 'container',
  panning: { enabled: true, modifiers: 'ctrl' },  // ✅ Ctrl+drag for panning
});
graph.use(new Selection({ enabled: true, rubberband: true }));  // Normal drag for rubberband selection
```