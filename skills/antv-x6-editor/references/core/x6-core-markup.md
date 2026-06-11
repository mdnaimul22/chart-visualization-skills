---
id: "x6-core-markup"
title: "X6 Markup (DOM Structure Definition)"
description: |
  The DOM structure of X6 nodes, edges, and ports is described using markup.
  This document is based on the actual implementation in src/view/markup.ts and src/shape/util.ts,
  systematically explaining the MarkupJSONMarkup field, selector/groupSelector mechanism,
  default markup for built-in shapes, custom shape markup writing conventions, and string markup compatibility syntax.

library: "x6"
version: "3.x"
category: "core"
subcategory: "markup"
tags:
  - "markup"
  - "selector"
  - "groupSelector"
  - "tagName"
  - "DOM"
  - "custom shape"
  - "registerNode"
  - "label"
  - "body"
  - "lines"

related:
  - "x6-core-shapes"
  - "x6-core-node"
  - "x6-core-edge"
  - "x6-intermediate-custom-node"
  - "x6-intermediate-custom-edge"

use_cases:
  - "Custom node shapes (declaring markup when using registerNode)"
  - "Custom edge shapes (double lines, bold hit-area, etc.)"
  - "Understanding the origin of selectors in attrs (body/label/line)"
  - "Independently setting styles on multiple child elements in markup via selector"
  - "Setting the same attribute for multiple child elements at once using groupSelector"

anti_patterns:
  - "Reusing the same selector in markup"
  - "Writing attrs keys as CSS selectors (should be the name of selector/groupSelector in markup)"
  - "Mixing SVG tagName in the markup of HTML nodes"
  - "Omitting lines groupSelector in edge markup, causing attrs.lines to fail"

difficulty: "intermediate"
completeness: "full"
---

## Core Concepts

**Markup** is the **underlying DOM structure description** for nodes / edges / ports / labels in X6. The `attrs` configuration of the same cell must reference the specific DOM element through the `selector` or `groupSelector` declared in the markup to take effect correctly.

> Source code location: `src/view/markup.ts` — `parseJSONMarkup` is responsible for recursively constructing the JSON description into SVG / XHTML nodes.

## MarkupJSONMarkup Field Quick Reference

| Field | Type | Description | Required |
|------|------|------|------|
| `tagName` | `string` | DOM element tag name (e.g., `'rect'`, `'circle'`, `'path'`, `'text'`, `'g'`, `'image'`) | ✓ |
| `selector` | `string` | Unique selector, used to precisely locate elements via `attrs[selector] = {...}` | |
| `groupSelector` | `string \| string[]` | Group selector, applies the same set of `attrs` to multiple elements; **name must not conflict with `selector`** | |
| `ns` | `string` | Namespace, defaults to `http://www.w3.org/2000/svg`; for HTML elements, use `Dom.ns.xhtml` | |
| `attrs` | `SimpleAttrs` | DOM attributes (automatically converted to kebab-case); merged with `cell.attrs[selector]`, with the latter taking precedence | |
| `style` | `Record<string, string \| number>` | Inline CSS (set via `Dom.css`) | |
| `className` | `string \| string[]` | DOM `class` attribute | |
| `textContent` | `string` | Element's `textContent` (Note: dynamic text should be placed in `attrs.text/text`) | |
| `children` | `MarkupJSONMarkup[]` | Child elements, recursively constructed | |

If `tagName` is missing, `parseJSONMarkup` will throw `TypeError: Invalid tagName`.

## Difference Between `selector` and `groupSelector` (Key)

- `selector` **must be unique** within a markup. Duplicates will throw `TypeError: Selector must be unique`.
- `groupSelector` allows multiple elements to share the same name. When referencing this name in `attrs`, the attributes will be applied to **all members**.
- If a `groupSelector` shares the same name as a `selector`, it will throw `Error: Ambiguous group selector`.

```javascript
// Built-in edge markup (excerpt from src/shape/edge.ts)
markup: [
  { tagName: 'path', selector: 'wrap', groupSelector: 'lines', attrs: {...} },
  { tagName: 'path', selector: 'line', groupSelector: 'lines', attrs: {...} },
]
attrs: {
  lines: { connection: true, strokeLinejoin: 'round' }, // ← Applies to both wrap and line
  wrap:  { strokeWidth: 10 },                            // ← Applies only to the first path (invisible hit area)
  line:  { stroke: '#333', strokeWidth: 2, targetMarker: 'classic' }, // ← The actual visible line
}
```

## Default markup for built-in shapes (verified from `src/shape/util.ts`)

`createShape(shape, config)` generates default markup for all basic shapes:

```javascript
// Equivalent to
markup: [
  { tagName: shape, selector: 'body' },  // shape: rect / circle / ellipse / polygon / polyline / path / image / text-block
  { tagName: 'text', selector: 'label' },
]
attrs: {
  [shape]: { /* BaseBodyAttr: fill #ffffff, stroke #333333, strokeWidth 2 */ },
  text:    { /* BaseLabelAttr: fontSize 14, fill #000, refX/refY 0.5, anchor middle */ },
}
```

This leads to several key rules to avoid pitfalls:

1. The `body` selector in built-in node `attrs` **directly corresponds to the shape's own tagName** (e.g., `rect`'s body is `<rect>`, `circle`'s body is `<circle>`), so only SVG attributes supported by that tagName can be used in `attrs`.
2. The text selector for built-in nodes is **`label`** (not `text`), but `attrs.text` is also retained as an alias, and both can be used.
3. By default, edges (`edge`) have a markup consisting of two `path` elements (`wrap` + `line`), controlled together via the `lines` group. When customizing edges and overriding the markup, the `lines` group must be preserved or the `attrs` must be rewritten accordingly.

## Custom Node: Complete Markup Example

```javascript
import { Graph } from '@antv/x6';

Graph.registerNode(
  'card-node',
  {
    inherit: 'rect',
    width: 180,
    height: 64,
    markup: [
      { tagName: 'rect',  selector: 'body' },
      { tagName: 'image', selector: 'icon' },
      { tagName: 'text',  selector: 'title' },
      { tagName: 'text',  selector: 'subtitle' },
    ],
    attrs: {
      body: {
        refWidth: '100%',       // Follow node width
        refHeight: '100%',
        fill: '#fff',
        stroke: '#8f8f8f',
        strokeWidth: 1,
        rx: 6,
        ry: 6,
      },
      icon: {
        ref: 'body',
        refX: 8,
        refY: 0.5,             // 50% of body height
        refY2: -10,            // Then subtract 10 pixels
        width: 20,
        height: 20,
        'xlink:href': '',
      },
      title: {
        ref: 'body',
        refX: 36,
        refY: 16,
        textAnchor: 'start',
        textVerticalAnchor: 'middle',
        fontSize: 14,
        fill: '#262626',
      },
      subtitle: {
        ref: 'body',
        refX: 36,
        refY: 40,
        textAnchor: 'start',
        textVerticalAnchor: 'middle',
        fontSize: 12,
        fill: '#8c8c8c',
      },
    },
  },
  true,
);

const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
});

graph.addNode({
  shape: 'card-node',
  x: 40, y: 40,
  attrs: {
    icon:     { 'xlink:href': 'https://gw.alipayobjects.com/zos/antfincdn/FLrTNDvlna/antv.png' },
    title:    { text: 'AntV X6' },
    subtitle: { text: 'Graph editor' },
  },
});

graph.centerContent();
```

## Custom Edge: Markup with Hit-Area

```javascript
import { Graph } from '@antv/x6';

Graph.registerEdge(
  'thick-edge',
  {
    inherit: 'edge',
    markup: [
      // First invisible thick path used as the hit-area
      { tagName: 'path', selector: 'wrap',  groupSelector: 'lines',
        attrs: { fill: 'none', stroke: 'transparent', strokeWidth: 12, cursor: 'pointer' } },
      // Second visible thin path is the actual edge
      { tagName: 'path', selector: 'line',  groupSelector: 'lines',
        attrs: { fill: 'none', pointerEvents: 'none' } },
    ],
    attrs: {
      lines: { connection: true, strokeLinejoin: 'round' }, // ← Must be retained
      line:  { stroke: '#1890ff', strokeWidth: 2, targetMarker: 'classic' },
    },
  },
  true,
);
```

## String markup (compatible syntax)

`markup` can also be a string (HTML/SVG fragment), but it is **not recommended** for use in custom shapes:
- String mode lacks the `selector` concept, making it impossible to precisely target with attrs
- Typically appears only in internal scenarios like `getPortContainerMarkup()`, where a "single g container" is used
- Always use JSON markup in application code

```javascript
// ❌ Not recommended
markup: '<rect class="body"/><text class="label"/>'

// ✅ Recommended
markup: [
  { tagName: 'rect', selector: 'body' },
  { tagName: 'text', selector: 'label' },
]
```

## Port Markup

Port markup is configured via `ports.groups[name].markup`, with the default markup being a `<circle>` (see `Markup.getPortMarkup()`):

```javascript
ports: {
  groups: {
    in: {
      position: 'left',
      markup: [{ tagName: 'circle', selector: 'circle' }], // ← Default value
      attrs: {
        circle: { r: 4, magnet: true, stroke: '#8f8f8f', fill: '#fff' },
      },
    },
  },
}
```

> The top-level `tagName` of port markup must be an SVG element. If an HTML-based port is required, use `Shape.HTML.register` to register the entire HTML node instead of modifying the port markup.

## Label Markup (Side Label)

The default markup for `labels` in `graph.addEdge` is `<rect> + <text>`, which can be overridden via `defaultLabel` or individual labels:

```javascript
graph.addEdge({
  source: a, target: b,
  defaultLabel: {
    markup: [
      { tagName: 'rect',  selector: 'body' },
      { tagName: 'text',  selector: 'label' },
    ],
    attrs: {
      body:  { fill: '#fff', stroke: '#8f8f8f', rx: 4, ry: 4 },
      label: { fontSize: 12, fill: '#262626', textAnchor: 'middle', textVerticalAnchor: 'middle' },
    },
  },
  labels: [{ position: 0.5, attrs: { label: { text: 'connected' } } }],
});
```

## Common Errors and Fixes

### ❌ Duplicate selector

```javascript
// Error: Both elements use 'body', throws TypeError: Selector must be unique at runtime
markup: [
  { tagName: 'rect', selector: 'body' },
  { tagName: 'rect', selector: 'body' },
]

// Correct: Each selector is unique
markup: [
  { tagName: 'rect', selector: 'body' },
  { tagName: 'rect', selector: 'header' },
]
```

### ❌ groupSelector and selector have the same name

```javascript
// Error: Throws Error: Ambiguous group selector
markup: [
  { tagName: 'path', selector: 'lines' },
  { tagName: 'path', groupSelector: 'lines' },
]

// Correct: Use different names
markup: [
  { tagName: 'path', selector: 'line', groupSelector: 'lines' },
  { tagName: 'path', selector: 'wrap', groupSelector: 'lines' },
]
```

### ❌ Missing `tagName`

```javascript
// Error: Throws TypeError: Invalid tagName
markup: [{ selector: 'body' }]

// Correct
markup: [{ tagName: 'rect', selector: 'body' }]
```

### ❌ Using CSS Selectors as Keys in attrs

```javascript
// Incorrect: Keys in attrs must be selectors or groupSelectors from the markup
attrs: {
  '.body': { fill: '#fff' },        // ❌ Not a CSS selector
  'rect.body': { fill: '#fff' },    // ❌
}

// Correct
markup: [{ tagName: 'rect', selector: 'body' }],
attrs: {
  body: { fill: '#fff' },           // ✅ Aligned with the selector name
}
```

### ❌ Custom Edge Missing `lines` `groupSelector`

```javascript
// Error: Overriding markup without the lines group, attrs.lines.connection = true becomes invalid,
// the edge path will not update with source/target changes
markup: [{ tagName: 'path', selector: 'line' }],
attrs: { lines: { connection: true } },

// Correct: Either retain groupSelector, or move connection to the line
markup: [{ tagName: 'path', selector: 'line', groupSelector: 'lines' }],
attrs: { lines: { connection: true }, line: { stroke: '#333' } },
// or
markup: [{ tagName: 'path', selector: 'line' }],
attrs: { line: { connection: true, stroke: '#333' } },
```

### ❌ Wrap HTML Content with SVG Markup

```javascript
// Error: Rendering will fail when using a div as a child node of SVG
markup: [
  { tagName: 'rect', selector: 'body' },
  { tagName: 'div',  selector: 'content' },     // ❌ No div in SVG namespace
]

// Correct: Use Shape.HTML.register
import { Shape } from '@antv/x6';
Shape.HTML.register({
  shape: 'my-card',
  effect: ['data'],
  html(node) {
    const el = document.createElement('div');
    el.style.cssText = 'width:100%;height:100%;border:1px solid #8f8f8f;';
    el.innerHTML = node.getData()?.html || '';
    return el;
  },
});
```