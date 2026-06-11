---
id: "x6-core-transform-api"
title: "X6 Canvas Size and Transformation API"
description: |
  Comprehensive guide to canvas transformation APIs including zoom/scale, translate, rotate, fit to content (fitToContent/zoomToFit), and center (centerContent/centerCell).
library: x6
version: 3.x
category: "core"
tags:
  - transform
  - zoom
  - scale
  - resize
  - translate
  - fit
  - center
---

# Canvas Size and Transformation API

## Overview

X6's TransformManager provides canvas-level scaling, panning, rotating, resizing, and content adaptation capabilities. All transformation APIs are directly invoked through the `graph` instance.

## Canvas Size

### resize — Adjust Canvas Size

```javascript
// Set canvas width and height (in pixels)
graph.resize(1000, 600);
```

### autoResize — Automatically Follow Container Size

When constructing a Graph, configure `autoResize: true`, and the canvas will automatically follow the size changes of the parent container using ResizeObserver:

```javascript
const graph = new Graph({
  container: 'container',
  autoResize: true,  // Automatically follow parent container size
});
```

You can also pass a specified DOM element as the listening target:

```javascript
const graph = new Graph({
  container: 'container',
  autoResize: document.getElementById('wrapper'),
});
```

### getComputedSize — Get the current canvas size

```javascript
const { width, height } = graph.getComputedSize();
```

## Zoom / Scale

### zoom — Zoom Canvas

```javascript
// Relative zoom: Increase by 0.2 based on the current scale
graph.zoom(0.2);

// Absolute zoom: Set to 1.5 times
graph.zoom(1.5, { absolute: true });

// Zoom with a specified center point
graph.zoom(0.5, { absolute: true, center: { x: 400, y: 300 } });

// Limit zoom range
graph.zoom(2, { absolute: true, minScale: 0.5, maxScale: 4 });

// Grid-aligned zoom
graph.zoom(1.5, { absolute: true, scaleGrid: 0.25 });  // Zoom value aligns to multiples of 0.25
```

**zoom options parameters:**

| Parameter | Type | Description |
|------|------|------|
| `absolute` | boolean | `true` for absolute zoom, `false` (default) for relative increment |
| `minScale` | number | Minimum zoom scale |
| `maxScale` | number | Maximum zoom scale |
| `scaleGrid` | number | Zoom value alignment grid |
| `center` | `{ x, y }` | Zoom center point (canvas coordinates) |

### getZoom — Get the current zoom level

```javascript
const currentZoom = graph.getZoom();  // Returns a number, such as 1.0
```

### scale — Basic Scaling (Set sx/sy Separately)

```javascript
// Uniform scaling
graph.scale(1.5);

// Non-uniform scaling
graph.scale(2, 1.5);

// Specify scaling origin
graph.scale(1.5, 1.5, 400, 300);
```

### getScale — Get the current scale ratio (per axis)

```javascript
const { sx, sy } = graph.getScale();
```

### scaling Configuration — Restrict Scaling Range

Set the global scaling boundaries during Graph construction via the `scaling` option:

```javascript
const graph = new Graph({
  container: 'container',
  scaling: { min: 0.2, max: 4 },  // Global scaling range restriction
});
```

## Translate

(Note: The original content provided only contains a header in Chinese, which has been translated to English as "Translate". Since there is no additional content to translate, the output remains minimal.)

### translate — Set Canvas Translation

```javascript
// Set absolute translation amount
graph.translate(100, 50);
```

### getTranslation — Get the Current Translation

```javascript
const { tx, ty } = graph.getTranslation();
```

## Rotate

(Note: The original content provided only included a header. Below is the translation of that header, adhering to the strict instructions provided.)

## Rotate

### rotate — Rotate Canvas

```javascript
// Rotate 45 degrees (default origin is the center of the canvas content)
graph.rotate(45);

// Specify rotation center
graph.rotate(90, 400, 300);
```

### getRotation — Get the current rotation angle

```javascript
const angle = graph.getRotation();
```

## Content Adaptation

### zoomToFit — Zoom and pan to make all content visible

```javascript
// Basic usage: Automatically fit all content
graph.zoomToFit();

// With padding
graph.zoomToFit({ padding: 20 });

// Limit zoom range
graph.zoomToFit({ padding: 20, maxScale: 2, minScale: 0.5 });

// Different padding for each side
graph.zoomToFit({ padding: { top: 20, right: 30, bottom: 20, left: 30 } });
```

### zoomToRect — Zoom to a specified rectangular area

```javascript
graph.zoomToRect({ x: 100, y: 100, width: 500, height: 400 });

graph.zoomToRect(
  { x: 0, y: 0, width: 1000, height: 800 },
  { padding: 20, maxScale: 3 },
);
```

### fitToContent — Adjust Canvas Size to Fit Content

Adjust the canvas size to just fit all content (without scaling the content, but by changing the canvas dimensions):

```javascript
// Basic usage
graph.fitToContent();

// With grid alignment and padding
graph.fitToContent({ gridWidth: 10, gridHeight: 10, padding: 20 });

// Full parameters
graph.fitToContent({
  gridWidth: 10,
  gridHeight: 10,
  padding: { top: 20, right: 20, bottom: 20, left: 20 },
  minWidth: 400,
  minHeight: 300,
  maxWidth: 2000,
  maxHeight: 1500,
  allowNewOrigin: 'any',  // 'negative' | 'positive' | 'any'
  border: 10,
});
```

**fitToContent options:**

| Parameter | Type | Description |
|------|------|------|
| `gridWidth` | number | Width alignment grid (default 1) |
| `gridHeight` | number | Height alignment grid (default 1) |
| `padding` | number \| SideOptions | Padding |
| `minWidth` | number | Minimum canvas width |
| `minHeight` | number | Minimum canvas height |
| `maxWidth` | number | Maximum canvas width |
| `maxHeight` | number | Maximum canvas height |
| `border` | number | Content border expansion |
| `allowNewOrigin` | string | Whether to allow origin adjustment |
| `contentArea` | RectangleLike | Custom content area |
| `useCellGeometry` | boolean | Use geometric calculation (default true) |

### scaleContentToFit — Scale Content to Fit Canvas

Scale the canvas content to fit the current visible area of the canvas (uniform scaling):

```javascript
graph.scaleContentToFit();

graph.scaleContentToFit({
  padding: 20,
  maxScale: 2,
  minScale: 0.5,
  preserveAspectRatio: true,  // Preserve aspect ratio (default true)
});
```

**scaleContentToFit options:**

| Parameter | Type | Description |
|------|------|------|
| `padding` | number \| SideOptions | Padding |
| `minScale` / `maxScale` | number | Global scale limits |
| `minScaleX` / `maxScaleX` | number | X-axis scale limits |
| `minScaleY` / `maxScaleY` | number | Y-axis scale limits |
| `scaleGrid` | number | Scale alignment grid |
| `contentArea` | RectangleLike | Custom content area |
| `viewportArea` | RectangleLike | Custom viewport area |
| `preserveAspectRatio` | boolean | Preserve aspect ratio |

## Center Alignment

### centerContent — Center the content display

```javascript
graph.centerContent();
graph.centerContent({ useCellGeometry: true });
```

### centerCell — Center the specified node (scroll to node)

```javascript
const node = graph.addNode({ ... });
graph.centerCell(node);  // Scroll the canvas to center the node
```

> **⚠️ Note**: X6 does not have a `graph.scrollToCell()` method. To scroll to a specified node, use `graph.centerCell(cell)`.

### centerPoint — Center the specified coordinates

```javascript
graph.centerPoint(500, 300);
```

## Positioning

### positionContent — Position content to a specified location

```javascript
// Position content to the center of the canvas
graph.positionContent('center');

// Other positions: 'top' | 'top-right' | 'right' | 'bottom-right' | 'bottom' | 'bottom-left' | 'left' | 'top-left'
graph.positionContent('top-left');
```

### positionCell — Position a node to a specified location

```javascript
graph.positionCell(node, 'center');
```

### positionPoint — Position a specified point to a designated location on the canvas

```javascript
// Position the local coordinates (200, 150) to the 50% 50% of the canvas (i.e., center)
graph.positionPoint({ x: 200, y: 150 }, '50%', '50%');

// Position the point to the top-left corner of the canvas with an offset of 100px
graph.positionPoint({ x: 0, y: 0 }, 100, 100);
```

## Content Area Query

### getContentArea — Get Content Boundaries (Local Coordinates)

```javascript
const rect = graph.getContentArea();
// rect: { x, y, width, height }
```

### getContentBBox — Get Content Bounding Box (Canvas Coordinates)

```javascript
const bbox = graph.getContentBBox();
```

### getGraphArea — Get the visible area of the canvas (local coordinates)

```javascript
const area = graph.getGraphArea();
```

## Coordinate Transformation

### localToGraph — Local Coordinates to Canvas Coordinates

```javascript
const graphPoint = graph.localToGraph({ x: 100, y: 100 });
```

### graphToLocal — Canvas Coordinates to Local Coordinates

```javascript
const localPoint = graph.graphToLocal({ x: 200, y: 150 });
```

## Complete Example

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  autoResize: true,
  scaling: { min: 0.2, max: 5 },
  mousewheel: { enabled: true, modifiers: 'ctrl' },
  panning: true,
});

// Add some nodes
graph.addNode({ shape: 'rect', x: 50, y: 50, width: 100, height: 40, label: 'A' });
graph.addNode({ shape: 'rect', x: 300, y: 200, width: 100, height: 40, label: 'B' });
graph.addNode({ shape: 'rect', x: 600, y: 400, width: 100, height: 40, label: 'C' });

// Automatically fit all content to the center of the canvas
graph.zoomToFit({ padding: 50, maxScale: 1 });

// Listen for zoom events
graph.on('scale', ({ sx, sy }) => {
  console.log(`Current zoom: ${sx.toFixed(2)}x`);
});

// Listen for size change events
graph.on('resize', ({ width, height }) => {
  console.log(`Canvas size: ${width} x ${height}`);
});
```

## Common Errors

```javascript
// ❌ Error: When zoom does not pass absolute, it is a relative increment, not setting an absolute value
graph.zoom(1.5);  // This adds +1.5 to the current scale, not setting it to 1.5 times!

// ✅ Correct: Set absolute zoom scale
graph.zoom(1.5, { absolute: true });

// ❌ Error: Content disappears after fitToContent (returns an empty rectangle when content is empty)
graph.fitToContent();  // May shrink dimensions to a very small size when there are no elements in the canvas

// ✅ Correct: Set minimum size protection
graph.fitToContent({ minWidth: 400, minHeight: 300 });

// ❌ Error: Mixing scale and zoom leads to unexpected behavior
graph.scale(2, 1.5);  // Non-uniform scaling
graph.zoom(1);         // zoom internally uses scale(sx, sy) and will override to uniform scaling

// ✅ Correct: Use either zoom or scale consistently
graph.zoom(2, { absolute: true });  // Recommended to use zoom for uniform scaling
```