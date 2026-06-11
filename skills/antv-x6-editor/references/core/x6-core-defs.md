---
id: "x6-core-defs"
title: "X6 defs (Gradient / Marker / Filter Definitions)"
description: |
  X6 provides three methods: `graph.defineGradient`, `graph.defineMarker`, and `graph.defineFilter`,
  to register gradients, arrow markers, and SVG filters into the canvas's `<defs>` and return the reference id.
  This document is based on the actual implementation in `src/graph/defs.ts` and `src/registry/{marker,filter}/*`.

library: "x6"
version: "3.x"
category: "core"
subcategory: "defs"
tags:
  - "defs"
  - "defineGradient"
  - "defineMarker"
  - "defineFilter"
  - "linearGradient"
  - "radialGradient"
  - "marker"
  - "arrow"
  - "filter"
  - "dropShadow"
  - "outline"
  - "highlight"
  - "blur"

related:
  - "x6-core-marker"
  - "x6-core-filter"
  - "x6-core-attr-registry"
  - "x6-core-edge"

use_cases:
  - "Set gradient fill for nodes / edges"
  - "Reuse gradient fill for custom arrow markers"
  - "Add shadow / highlight / blur filters to nodes"
  - "Retrieve <defs> resource ids in custom attr"
  - "Dynamically add / remove global SVG resources"

anti_patterns:
  - "Manually create <defs> child nodes using `graph.svg` / `graph.defs` / `document.createElementNS`"
  - "Use gradient objects as string fill"
  - "Forget `tagName` in the object passed to `defineMarker`"
  - "Misspell filter names (e.g., `dropShadow` vs `drop-shadow`), X6 has 11 built-in names that must match exactly"

difficulty: "intermediate"
completeness: "full"
---

## Why defs is Needed

The SVG `<defs>` element is used to declare reusable "template resources" (gradients, filters, markers), which can be referenced via `url(#id)` in attributes like `fill / stroke / marker-end / filter`.

X6 encapsulates all `<defs>` operations in `DefsManager` (`src/graph/defs.ts`), exposing three Graph methods:

| Method | Returns | Internal Behavior |
|------|------|----------|
| `graph.defineGradient(options)` | `string` (id) | Creates `<linearGradient>` / `<radialGradient>` in `<defs>` |
| `graph.defineMarker(options)` | `string` (id) | Creates `<marker>` in `<defs>` |
| `graph.defineFilter(options)` | `string` (id) | Creates `<filter>` in `<defs>` |

All methods are **idempotent**: internally, `StringExt.hashcode(JSON.stringify(options))` is used to generate the id, ensuring that identical options result in a single creation.

> ⚠️ **Do not** directly read or write internal fields like `graph.defs` / `graph.svgDoc`; X6 3.x does not expose these properties, and attempting to access them will throw `Cannot read properties of undefined`.

## `graph.defineGradient`

### Type Definitions (Checked from `src/graph/defs.ts`)

```typescript
interface GradientOptions {
  id?: string
  type: string                              // 'linearGradient' | 'radialGradient'
  stops: { offset: number; color: string; opacity?: number }[]
  attrs?: SimpleAttrs                       // Additional attributes for the <linearGradient> tag itself
}
```

### Most scenarios do not require manual invocation—directly write the gradient object in `attrs.fill` / `attrs.stroke`

X6's built-in `fill` attr registrar (see `core/x6-core-attr-registry.md`) automatically calls `defineGradient` when the fill value is an object:

```javascript
attrs: {
  body: {
    fill: {
      type: 'linearGradient',
      stops: [
        { offset: 0,    color: '#1890ff' },
        { offset: 1,    color: '#13c2c2', opacity: 0.6 },
      ],
    },
  },
}
```

> `offset` can be either a number between `0` and `1` or a string from `'0%'` to `'100%'`. The source code will directly append it to `stop-offset`.

### Scenarios Requiring Explicit Calls to `defineGradient`

When a gradient needs to be **referenced by a custom marker or custom attr**, you must first obtain its `id` and then apply it to the marker's `fill: 'url(#xxx)'`:

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
});

const gradientId = graph.defineGradient({
  type: 'linearGradient',
  stops: [
    { offset: 0, color: '#ff7875' },
    { offset: 1, color: '#ff4d4f' },
  ],
});

graph.addEdge({
  source: { x: 80, y: 80 },
  target: { x: 320, y: 220 },
  attrs: {
    line: {
      stroke: '#ff4d4f',
      strokeWidth: 2,
      targetMarker: {
        // Custom marker, using the previously defined gradient id for filling
        tagName: 'path',
        d: 'M 12 -6 0 0 12 6 z',
        fill: `url(#${gradientId})`,
      },
    },
  },
});

graph.centerContent();
```

## `graph.defineMarker`

### Type Definition (Checked from `src/registry/marker/index.ts`)

```typescript
interface MarkerResult extends SimpleAttrs {
  id?: string
  tagName?: string                              // Default 'path'
  refX?: number
  refY?: number
  markerUnits?: 'userSpaceOnUse' | 'strokeWidth'  // Default 'userSpaceOnUse'
  markerOrient?: 'auto' | 'auto-start-reverse' | number  // Default 'auto'
  children?: { tagName: string; [attr: string]: any }[]
  // Other fields will be used as attrs for the internal path of the marker (fill / stroke / d / size, etc.)
}
```

### Most Scenarios: Directly Use Built-in Names in `targetMarker` / `sourceMarker` of Edge

X6 provides 7 built-in marker types (`src/registry/marker/`):

| name | Shape | Key Parameters |
|------|------|----------|
| `'classic'` | Classic Triangle Arrow (Default) | `size`, `width`, `height`, `offset`, `factor` |
| `'block'` | Solid Triangle Block | `size`, `width`, `height`, `offset`, `open` |
| `'diamond'` | Diamond | `size`, `width`, `height`, `offset` |
| `'cross'` | Cross | `size`, `width`, `height`, `offset` |
| `'circle'` | Circle | `r`, `size`, `offset` |
| `'ellipse'` | Ellipse | `rx`, `ry`, `offset` |
| `'async'` | Asynchronous Double Arrow | `size`, `width`, `height`, `offset` |
| `'path'` | Custom Path | `d`, `offset`, `attrs` |

```javascript
graph.addEdge({
  source: a, target: b,
  attrs: {
    line: {
      stroke: '#333',
      targetMarker: 'classic',                              // String shorthand
      sourceMarker: { name: 'circle', args: { r: 4 } },     // Object + args
    },
  },
});
```

### Scenarios Requiring `defineMarker`: Fully Customized Marker (with Filter / Children / Gradient)

```javascript
const arrowId = graph.defineMarker({
  tagName: 'path',
  refX: 6,
  refY: 4,
  markerUnits: 'userSpaceOnUse',
  markerOrient: 'auto',
  d: 'M 0 0 L 8 4 L 0 8 z',
  fill: '#1890ff',
});

graph.addEdge({
  source: a, target: b,
  attrs: {
    line: {
      stroke: '#1890ff',
      'marker-end': `url(#${arrowId})`,    // Directly reference SVG marker-end
    },
  },
});
```

With Children (suitable for composite markers, e.g., a bordered circular terminator):

```javascript
graph.defineMarker({
  tagName: 'circle',
  children: [
    { tagName: 'circle', r: 4, fill: '#fff', stroke: '#1890ff', 'stroke-width': 2 },
    { tagName: 'circle', r: 2, fill: '#1890ff' },
  ],
  refX: 5,
  refY: 0,
  markerOrient: 'auto-start-reverse',
});
```

> The source code `defs.ts:127` indicates: If `tagName !== 'path'`, the `d` attribute will be automatically removed to avoid contamination inherited from the standard edge.

## `graph.defineFilter`

### Type Definitions (Checked from `src/registry/filter/index.ts`)

```typescript
type FilterOptions = (FilterNativeItem | FilterManualItem) & {
  id?: string
  attrs?: SimpleAttrs        // Attributes of the <filter> tag itself, default { x:-1, y:-1, width:3, height:3, filterUnits:'objectBoundingBox' }
}

interface FilterNativeItem {
  name: 'outline' | 'highlight' | 'blur' | 'dropShadow'
      | 'grayScale' | 'sepia' | 'saturate' | 'hueRotate'
      | 'invert'   | 'brightness' | 'contrast'
  args?: { /* Different args correspond to different names, see the table below */ }
}
```

### X6 Built-in 11 Filters (Verified from `src/registry/filter/main.ts`)

| name | args Example | Effect |
|------|-----------|------|
| `'outline'`     | `{ color, width, margin, opacity }` | Outline |
| `'highlight'`   | `{ color, width, blur, opacity }`   | Glow Highlight |
| `'blur'`        | `{ x, y }`                           | Blur |
| `'dropShadow'`  | `{ dx, dy, color, blur, opacity }`   | Drop Shadow |
| `'grayScale'`   | `{ amount }`                         | Grayscale |
| `'sepia'`       | `{ amount }`                         | Sepia |
| `'saturate'`    | `{ amount }`                         | Saturation |
| `'hueRotate'`   | `{ angle }`                          | Hue Rotation |
| `'invert'`      | `{ amount }`                         | Invert |
| `'brightness'`  | `{ amount }`                         | Brightness |
| `'contrast'`    | `{ amount }`                         | Contrast |

> Case-sensitive: `dropShadow` is not `drop-shadow`, `grayScale` is not `grayscale`.

### Use Directly via attrs.filter (Recommended)

X6 recognizes the `filter` field in `attrs`, and passing an object will automatically call `defineFilter`:

```javascript
graph.addNode({
  shape: 'rect',
  x: 100, y: 100, width: 120, height: 60,
  attrs: {
    body: {
      fill: '#fff',
      stroke: '#8f8f8f',
      filter: {
        name: 'dropShadow',
        args: { dx: 2, dy: 2, blur: 4, color: 'rgba(0,0,0,0.2)' },
      },
    },
  },
});
```

### Explicitly Call defineFilter (Required When Sharing or Customizing Filters in Multiple Places)

```javascript
const shadowId = graph.defineFilter({
  name: 'dropShadow',
  args: { dx: 0, dy: 4, blur: 8, color: '#1890ff', opacity: 0.4 },
});

// Multiple nodes share the same filter reference
['n1', 'n2', 'n3'].forEach((id, i) => {
  graph.addNode({
    id, shape: 'rect',
    x: 60 + i * 160, y: 100, width: 100, height: 50,
    attrs: { body: { fill: '#fff', filter: `url(#${shadowId})` } },
  });
});
```

### Custom Filter Tag (`FilterManualItem`)

If the built-in 11 items are insufficient, you can pass a `name` not in the native list and then extend the filter factory function yourself through `Registry` (advanced usage, most scenarios do not require this, see `core/x6-core-filter.md` for details).

## Commonalities of the Three Methods

1. **All return a string id**, which needs to be concatenated as `url(#id)` for use
2. **Idempotent**: Repeated calls with the same options create only one DOM (based on `JSON.stringify` hash)
3. **DefsManager.remove(id)** can be used to proactively remove, but is usually not necessary

## Common Errors and Fixes

### ❌ Directly Manipulating DOM to Create defs

```javascript
// Error: graph.defs / graph.svgDoc are not public APIs, will throw Cannot read properties of undefined
const defs = graph.defs;
const grad = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
defs.appendChild(grad);

// Correct: Use defineGradient
const id = graph.defineGradient({
  type: 'linearGradient',
  stops: [{ offset: 0, color: '#f00' }, { offset: 1, color: '#0f0' }],
});
attrs.body.fill = `url(#${id})`;
```

### ❌ Gradient Directly Passed as String

```javascript
// Error: Gradient object cannot be parsed as a string by fromJSON
attrs: { body: { fill: 'linear-gradient(#f00, #0f0)' } }   // ❌ This is CSS syntax

// Correct: Pass gradient object
attrs: {
  body: {
    fill: {
      type: 'linearGradient',
      stops: [{ offset: 0, color: '#f00' }, { offset: 1, color: '#0f0' }],
    },
  },
}
```

### ❌ defineMarker Missing tagName

```javascript
// Error: tagName defaults to 'path', but the d attribute must be provided along with path
graph.defineMarker({ refX: 5, refY: 0 });  // Renders as empty

// Correct: path type
graph.defineMarker({ tagName: 'path', d: 'M0 0 L8 4 L0 8 z', fill: '#333' });

// Alternatively: Non-path elements must explicitly specify tagName and avoid d
graph.defineMarker({ tagName: 'circle', r: 4, fill: '#333' });
```

### ❌ Incorrect Case for Filter Names

```javascript
// Incorrect: Built-in names are case-sensitive, incorrect names will throw "Filter not found"
filter: { name: 'drop-shadow', args: { dx: 2, dy: 2 } }   // ❌
filter: { name: 'grayscale',  args: { amount: 1 } }       // ❌

// Correct
filter: { name: 'dropShadow', args: { dx: 2, dy: 2 } }    // ✅
filter: { name: 'grayScale',  args: { amount: 1 } }       // ✅
```

### ❌ Redundant Definition of the Same Gradient

```javascript
// Incorrect: Concatenating id every time, but X6 internally already de-duplicates, redundant effort
for (const node of nodes) {
  const id = graph.defineGradient({ type: 'linearGradient', stops: [...] });
  // ...
}

// Correct: Call once to get the id
const gradientId = graph.defineGradient({ type: 'linearGradient', stops: [...] });
nodes.forEach((n) => n.attr('body/fill', `url(#${gradientId})`));
```