---
id: "x6-core-attr-registry"
title: "X6 Custom Attribute Registration (Attr Registry)"
description: |
  X6's attribute registration mechanism is used to extend the attrs configuration options for nodes/edges. It supports three types of custom attribute processors: set, position, and offset.
library: x6
version: 3.x
category: "core"
tags:
  - attr
  - registry
  - custom-attr
  - attrs
---

# Custom Attribute Registration (Attr Registry)

## Overview

X6 manages all special attributes available in `attrs` through the Attribute Registry (Attr Registry). In addition to standard SVG attributes (such as `fill`, `stroke`) that are directly applied to DOM elements, X6 also includes a set of advanced attributes (e.g., `refX`, `refWidth`, `connection`, etc.) and supports user-defined registration of new attributes.

## Built-in Special Properties

### Relative Positioning Attributes (ref Series)

Perform relative positioning and size calculations based on the BBox of a reference element (usually the node body):

| Attribute | Description | Value Range |
|------|------|--------|
| `ref` | Selector specifying the reference element | CSS selector string |
| `refX` | Relative X coordinate | 0~1 for percentage, otherwise absolute offset |
| `refY` | Relative Y coordinate | Same as above |
| `refDx` | X offset relative to the right side of the reference element | Pixel value |
| `refDy` | Y offset relative to the bottom of the reference element | Pixel value |
| `refWidth` | Relative width | 0~1 for percentage, otherwise absolute adjustment |
| `refHeight` | Relative height | Same as above |
| `refRx` | Relative corner radius rx | 0~1 for percentage |
| `refRy` | Relative corner radius ry | Same as above |
| `refCx` | Relative center cx | 0~1 for percentage |
| `refCy` | Relative center cy | Same as above |
| `refR` | Relative radius (inscribed) | 0~1 for percentage |
| `refRCircumscribed` | Relative radius (circumscribed) | 0~1 for percentage |
| `refD` | Relative path d (scale adaptation) | SVG path string |
| `refPoints` | Relative polygon points (scale adaptation) | Point coordinate string |

```javascript
graph.addNode({
  shape: 'rect',
  x: 100, y: 100, width: 200, height: 80,
  attrs: {
    body: { fill: '#fff', stroke: '#333' },
    icon: {
      ref: 'body',       // Reference body element
      refX: 0.5,         // Horizontally centered (50%)
      refY: 0.5,         // Vertically centered (50%)
      refWidth: 0.3,     // Width is 30% of body
      refHeight: 0.3,    // Height is 30% of body
    },
  },
});
```

### Gradient Color Properties

`fill` and `stroke` support passing in gradient objects, and X6 will automatically create gradient definitions in the SVG `<defs>`:

```javascript
attrs: {
  body: {
    fill: {
      type: 'linearGradient',
      stops: [
        { offset: '0%', color: '#31d0c6' },
        { offset: '100%', color: '#7c68fc' },
      ],
    },
  },
}
```

### Edge Connection Attributes

Only effective in the `attrs` of an Edge:

| Attribute | Description |
|-----------|-------------|
| `connection` | Automatically follow the edge path (set to `true` or `{ stubs }` object) |
| `atConnectionLength` | Position at a specified length along the edge path (maintain tangent direction) |
| `atConnectionRatio` | Position at a specified ratio along the edge path (maintain tangent direction) |
| `atConnectionLengthIgnoreGradient` | Position along the path but do not rotate |
| `atConnectionRatioIgnoreGradient` | Position at a ratio along the path but do not rotate |

```javascript
graph.addEdge({
  source: node1,
  target: node2,
  attrs: {
    line: { connection: true, stroke: '#333', strokeWidth: 2 },
    label: {
      atConnectionRatio: 0.5,  // Label positioned at 50% of the edge
      text: 'Hello',
      textAnchor: 'middle',
      textVerticalAnchor: 'middle',
    },
  },
});
```

### Other Built-in Attributes

| Attribute | Description |
|-----------|-------------|
| `text` | Sets the text content (supports multi-line, text-path, and other advanced typesetting) |
| `textWrap` | Text auto-wrap configuration |
| `title` | Sets the SVG `<title>` child element (tooltip) |
| `html` | Sets the element's innerHTML |
| `style` | Sets the CSS style object (via `elem.style`) |
| `filter` | SVG filter (supports object-based shorthand syntax) |

## Custom Attribute Registration

### Register API

Register custom attributes using `Graph.registerAttr(name, definition)`:

```javascript
import { Graph } from '@antv/x6';

Graph.registerAttr('myAttr', {
  // qualify: Determine whether to apply this attribute processor (optional)
  qualify(value, { elem, attrs, cell, view }) {
    return typeof value === 'number';
  },
  // set: Return the SVG attribute object to be set
  set(value, { elem, refBBox, cell, view }) {
    return { opacity: value / 100 };
  },
});
```

### Three Types of Attribute Definitions

#### 1. Set Attribute — Calculate and Set SVG Attributes

```javascript
Graph.registerAttr('highlightWidth', {
  qualify(value) {
    return typeof value === 'number';
  },
  set(value, { refBBox }) {
    // Return the attributes to be set on the DOM element
    return {
      strokeWidth: value,
      stroke: value > 2 ? 'red' : '#333',
    };
  },
});
```

#### 2. Position Attribute — Calculate Element Position Offset

```javascript
Graph.registerAttr('centerInParent', {
  position(value, { refBBox }) {
    if (value) {
      return {
        x: refBBox.x + refBBox.width / 2,
        y: refBBox.y + refBBox.height / 2,
      };
    }
    return null;
  },
});
```

#### 3. Offset Attribute — Calculate Additional Displacement

```javascript
Graph.registerAttr('circularOffset', {
  offset(value, { refBBox }) {
    const angle = (value * Math.PI) / 180;
    const radius = Math.min(refBBox.width, refBBox.height) / 2;
    return {
      x: Math.cos(angle) * radius,
      y: Math.sin(angle) * radius,
    };
  },
});
```

### qualify Function

The `qualify` function is used to determine whether an attribute value should be processed by this custom handler. If it returns `false`, the attribute will be set directly on the element as a regular SVG attribute.

```javascript
Graph.registerAttr('fill', {
  // Only process gradient handling when the fill value is an object; string values are directly set as SVG fill
  qualify(value) {
    return typeof value === 'object' && value !== null;
  },
  set(fill, { view }) {
    return `url(#${view.graph.defineGradient(fill)})`;
  },
});
```

## Complete Example: Customizing Progress Bar Attributes

```javascript
import { Graph } from '@antv/x6';

// Register a 'progress' attribute to dynamically set width and color based on percentage
Graph.registerAttr('progress', {
  qualify(value) {
    return typeof value === 'number';
  },
  set(value, { refBBox }) {
    const percent = Math.max(0, Math.min(1, value));
    const color = percent > 0.7 ? '#52c41a' : percent > 0.3 ? '#faad14' : '#f5222d';
    return {
      width: refBBox.width * percent,
      fill: color,
    };
  },
});

const graph = new Graph({ container: 'container', width: 800, height: 600 });

graph.addNode({
  shape: 'rect',
  x: 100, y: 100, width: 200, height: 30,
  markup: [
    { tagName: 'rect', selector: 'body' },
    { tagName: 'rect', selector: 'progress' },
    { tagName: 'text', selector: 'label' },
  ],
  attrs: {
    body: { width: 200, height: 30, fill: '#f0f0f0', stroke: '#d9d9d9' },
    progress: { progress: 0.65, height: 30, rx: 0, ry: 0 },
    label: { text: '65%', refX: 0.5, refY: 0.5, textAnchor: 'middle', textVerticalAnchor: 'middle' },
  },
});
```

## Common Errors

```javascript
// ❌ Error: refX/refY uses pixel values but expects percentage effect
attrs: { icon: { refX: 100, refY: 50 } }
// When refX > 1, it is treated as an absolute offset (pixels), not a percentage

// ✅ Correct: Use decimals between 0~1 to represent percentages
attrs: { icon: { refX: 0.5, refY: 0.5 } }  // Centered

// ❌ Error: Using connection property on non-edge elements
graph.addNode({
  attrs: { body: { connection: true } }  // connection is only valid for edges
});

// ✅ Correct: connection is used in edge attrs
graph.addEdge({
  attrs: { line: { connection: true, stroke: '#333' } },
});
```