---
id: "x6-core-shape-advanced"
title: "X6 Advanced Built-in Shapes"
description: |
  In addition to basic shapes like rect, circle, and ellipse, X6 provides advanced shapes such as path, polyline, polygon, and text-block.
  These are suitable for scenarios like custom path graphics, polyline connections, polygons, and rich text nodes.

library: "x6"
version: "3.x"
category: "core"
subcategory: "shape"
tags:
  - "shape"
  - "path"
  - "polyline"
  - "polygon"
  - "text-block"
  - "custom shape"
  - "SVG path"
  - "polyline"
  - "rich text"

related:
  - "x6-core-node"
  - "x6-intermediate-custom-node"

use_cases:
  - "Drawing custom SVG path nodes"
  - "Drawing polyline shape nodes"
  - "Creating rich text nodes"
  - "Drawing polygon nodes"

difficulty: "intermediate"
completeness: "full"
---

## Complete List of Built-in Shapes

X6 3.x provides the following built-in shapes:

| Shape | Description | Primary Use |
|-------|-------------|-------------|
| `rect` | Rectangle | Most commonly used node shape |
| `circle` | Circle | Status node, start/end node |
| `ellipse` | Ellipse | Decision node |
| `polygon` | Polygon | Custom polygons (rhombus, hexagon, etc.) |
| `polyline` | Polyline | Polyline path shape |
| `path` | SVG Path | Any SVG path shape |
| `text` | Plain Text | Text label node |
| `text-block` | Rich Text Block | Auto-wrapping text node |
| `image` | Image | Image node |
| `html` | HTML | Custom HTML content node |

---

## Path Node

The `path` shape uses SVG path data to define arbitrary shapes. Set the path data via the `path` attribute (shortcut) or `attrs.body.refD`.

### Basic Usage

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({ container: 'container' });

// Using the path shortcut property
graph.addNode({
  shape: 'path',
  x: 100,
  y: 50,
  width: 120,
  height: 60,
  path: 'M 0 5 10 0 C 20 0 20 20 10 20 L 0 15 Z',
  attrs: {
    body: {
      fill: '#efdbff',
      stroke: '#9254de',
      strokeWidth: 2,
    },
  },
});

// Using attrs.body.refD (the path will automatically scale to the node size)
graph.addNode({
  shape: 'path',
  x: 300,
  y: 50,
  width: 100,
  height: 80,
  attrs: {
    body: {
      refD: 'M 0 0 L 1 0.5 L 0 1 Z',
      fill: '#d9f7be',
      stroke: '#52c41a',
      strokeWidth: 2,
    },
  },
});
```

### Key Notes

- The `path` attribute is a shorthand for `attrs.body.refD`
- The path coordinates in `refD` are scaled proportionally based on the node's `width`/`height`
- Markup structure: `rect(bg)` + `path(body)` + `text(label)`
- `bg` is a transparent background rectangle used for event capturing

---

## Polyline Node

The `polyline` shape inherits from `polygon` and is used to draw polyline/polygon shapes.

### Basic Usage

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({ container: 'container' });

// Polyline shape (not closed)
graph.addNode({
  shape: 'polyline',
  x: 100,
  y: 50,
  width: 120,
  height: 60,
  attrs: {
    body: {
      refPoints: '0,0 1,0 1,1 0,1',
      fill: '#fff1b8',
      stroke: '#faad14',
      strokeWidth: 2,
    },
  },
});
```

### Differences from Polygon

- `polygon`: Closed polygon, automatically closes the path
- `polyline`: Polyline shape, does not automatically close (unless the start and end points are the same)

### Polygon Example (Rhombus)

```javascript
graph.addNode({
  shape: 'polygon',
  x: 100,
  y: 50,
  width: 100,
  height: 60,
  attrs: {
    body: {
      refPoints: '0.5,0 1,0.5 0.5,1 0,0.5',
      fill: '#e6f7ff',
      stroke: '#1890ff',
      strokeWidth: 2,
    },
  },
});
```

---

## Text-Block Node

The `text-block` shape supports rich text content with automatic line breaks. It renders text using an HTML div in browsers that support `foreignObject`, otherwise it falls back to SVG text.

### Basic Usage

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({ container: 'container' });

graph.addNode({
  shape: 'text-block',
  x: 100,
  y: 50,
  width: 200,
  height: 80,
  text: 'This is a long text content with automatic line breaks. The text-block will automatically wrap the text based on the node width.',
  attrs: {
    body: {
      fill: '#f0f0f0',
      stroke: '#8f8f8f',
      strokeWidth: 1,
      rx: 4,
      ry: 4,
    },
    label: {
      style: {
        fontSize: 14,
      },
    },
  },
});
```

### Key Notes

- Use the `text` property (shortcut) to set the text content
- Text automatically wraps based on node width
- `attrs.label.style` sets the font style (CSS style, as HTML rendering is used)
- Suitable for scenarios requiring multi-line text display

---

## Custom Arrow Markers

In X6, custom SVG paths can be used as arrow markers by directly defining `sourceMarker` and `targetMarker` in the `attrs.line` of an edge.

### Basic Usage

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  background: {
    color: '#F2F7FA',
  },
});

graph.addEdge({
  source: [100, 140],
  target: [400, 140],
  label: 'custom-marker',
  attrs: {
    line: {
      sourceMarker: {
        tagName: 'path',
        d: 'M 20 -10 0 0 20 10 Z',
      },
      targetMarker: {
        tagName: 'path',
        stroke: '#D94111',
        strokeWidth: 2,
        fill: '#90C54C',
        d: 'M 20 -10 0 0 20 10 Z',
      },
      stroke: '#8f8f8f',
      strokeWidth: 1,
    },
  },
});
```

### Key Notes

- `sourceMarker` and `targetMarker` can be strings (preset markers) or objects (custom markers)
- Custom marker objects must include `tagName` and `d` properties
- The `d` property defines the SVG path
- Styles can be set via properties such as `stroke`, `fill`, etc.

---

## Common Errors and Fixes

### Error 1: Using `d` Instead of `refD` for Path Nodes

```javascript
// ❌ Incorrect: Using `d` attribute, the path does not scale
attrs: { body: { d: 'M 0 0 L 100 50 L 0 100 Z' } }

// ✅ Correct: Using `refD`, the path scales according to the node size
attrs: { body: { refD: 'M 0 0 L 1 0.5 L 0 1 Z' } }

// ✅ Correct: Using the `path` shorthand property
graph.addNode({ shape: 'path', path: 'M 0 0 L 100 50 L 0 100 Z', ... })
```

### Error 2: Confusing Polygon and Polyline

```javascript
// Polygon automatically closes, no need to repeat the first point
attrs: { body: { refPoints: '0,0 1,0 1,1 0,1' } }  // Automatically closes to form a rectangle

// Polyline does not automatically close, manual closure requires adding the first point
attrs: { body: { refPoints: '0,0 1,0 1,1 0,1 0,0' } }  // Manually closed
```

### Error 3: Using `label` instead of `text` for `text-block`

```javascript
// ❌ Incorrect: `label` property is invalid for `text-block`
graph.addNode({ shape: 'text-block', label: 'Text Content' })

// ✅ Correct: Use `text` property
graph.addNode({ shape: 'text-block', text: 'Text Content' })
```

### Error 4: Incorrect Use of `graph.markers.register` to Register Custom Arrows

```javascript
// ❌ Incorrect: There is no `graph.markers.register` method in X6
const customMarker = { tagName: 'path', attrs: { d: 'M 0 -6 L 12 0 L 0 6 Z' } }
graph.markers.register('custom-marker', customMarker)

// ✅ Correct: Define the marker directly in `attrs.line`
graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: {
      sourceMarker: 'classic',
      targetMarker: {
        tagName: 'path',
        d: 'M 0 -6 L 12 0 L 0 6 Z',
        fill: 'green',
        stroke: 'red',
      },
    },
  },
})
```