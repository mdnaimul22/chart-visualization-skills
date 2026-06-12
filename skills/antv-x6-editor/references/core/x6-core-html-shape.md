---
id: "x6-core-html-shape"
title: "Complete Guide to X6 HTML Shape (Shape.HTML.register)"
description: |
  Specialized guide for X6 3.x Rich HTML Nodes: Shape.HTML.register is the only registration entry point. This document is based on the source code in src/shape/html.ts, covering the HTML shape registration API, three types of return values for the html callback (string / HTMLElement / function), effect re-rendering mechanism (e.g., effect: ['data']), and business scenario templates: HTML card nodes, HTML form nodes (input/select/textarea), HTML status badge nodes, HTML user cards (avatar + name + position), and HTML data table nodes. It also clarifies that the deprecated X6 2.x API Graph.registerHTMLComponent is no longer available in 3.x.

library: "x6"
version: "3.x"
category: "core"
subcategory: "shapes"
tags:
  - "HTML shape"
  - "Shape.HTML"
  - "Shape.HTML.register"
  - "html-node"
  - "html node"
  - "HTML 节点"
  - "HTML 卡片"
  - "HTML 表单节点"
  - "HTML 状态节点"
  - "HTML 状态徽标"
  - "HTML 用户卡片"
  - "用户卡片节点"
  - "可编辑表单节点"
  - "富节点"
  - "富 HTML 节点"
  - "foreignObject"
  - "data 重渲染"
  - "data 自动重新渲染"
  - "effect"
  - "effect: ['data']"
  - "registerHTMLComponent"
  - "Graph.registerHTMLComponent"
  - "DOM 节点"
  - "innerHTML"
  - "createElement"

related:
  - "x6-core-shapes"
  - "x6-core-node"
  - "x6-core-cell-data"
  - "x6-intermediate-custom-node"

use_cases:
  - "Render rich UI nodes such as cards, forms, status badges, and data tables using HTML/CSS"
  - "Automatically re-render node content when data changes"
  - "Embed arbitrary DOM elements (including input, select, img) within SVG nodes"
  - "User card nodes (avatar + name + position)"
  - "Editable form nodes (input/select fields)"
  - "State-switchable nodes (online/offline/idle)"

anti_patterns:
  - "Using Graph.registerHTMLComponent —— Deprecated in X6 3.x, does not exist in the source code"
  - "Directly passing html in addNode({ shape: 'html', html: '...' }) —— Must first register a named shape"
  - "Returning undefined / null in the html callback"
  - "Overusing effect: ['data'] for static display nodes"

difficulty: "intermediate"
completeness: "full"
---
## 1. Unique Registration Entry Point: `Shape.HTML.register`

In X6 3.x, **all rich HTML nodes are registered via `Shape.HTML.register` as a named shape**, and then added using `graph.addNode({ shape: 'xxx' })`. **There is no other registration method**.

Source code location: `src/shape/html.ts:38`

```ts
public static register(config: HTMLShapeConfig) {
  const { shape, html, effect, inherit, ...others } = config
  if (!shape) {
    throw new Error('HTML.register should specify `shape` in config.')
  }
  HTMLShapeMaps[shape] = { html, effect }
  Graph.registerNode(shape, { inherit: inherit || 'html', ...others }, true)
}
```

### `HTMLShapeConfig` Fields (Complete List)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `shape` | `string` | ✅ | Registered shape id, used in `addNode({ shape })` |
| `html` | `string \| HTMLElement \| (cell) => HTMLElement \| string` | ✅ | HTML content generation function or static HTML |
| `effect` | `(keyof NodeProperties)[]` | ❌ | List of props to listen for changes and re-invoke `html(cell)` rendering; defaults to initial render only if not provided (Note: Internal `change:*` listeners will still trigger, but re-rendering occurs only when the prop is in the effect list) |
| `inherit` | `string` | ❌ | Inherited built-in shape, defaults to `'html'` |
| `width` / `height` | `number` | ❌ | Default dimensions (can be overridden in `addNode`) |
| Other NodeProperties | — | ❌ | Consistent with `Graph.registerNode` options |

## 2. Minimum Viable Templates (Progressively by Complexity)

### 2.1 Static HTML (Simplest)

Directly pass a string to the `html` field:

```javascript
import { Graph, Shape } from '@antv/x6';

Shape.HTML.register({
  shape: 'static-html',
  width: 160,
  height: 80,
  html: '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;border:1px solid #8f8f8f;border-radius:6px;background:#fff;">Hello</div>',
});

const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
});

graph.addNode({ shape: 'static-html', x: 80, y: 60 });
```

### 2.2 Function Returns HTMLElement (Recommended)

`html(node)` returns a DOM element, and business data is read using `node.getData()`:

```javascript
import { Graph, Shape } from '@antv/x6';

Shape.HTML.register({
  shape: 'card',
  width: 200,
  height: 80,
  html(node) {
    const data = node.getData() || {};
    const div = document.createElement('div');
    div.style.cssText =
      'width:100%;height:100%;padding:8px;box-sizing:border-box;' +
      'border:1px solid #8f8f8f;border-radius:6px;background:#fff;';
    div.innerHTML = `
      <div style="font-size:14px;font-weight:500;">${data.title || ''}</div>
      <div style="font-size:12px;color:#666;">${data.desc || ''}</div>
    `;
    return div;
  },
});

const graph = new Graph({ container: 'container', background: { color: '#F2F7FA' } });

graph.addNode({
  shape: 'card',
  x: 80, y: 60,
  data: { title: 'Hello', desc: 'World' },
});
```

### 2.3 Add effect: Automatic Re-rendering on Data Changes

`effect: ['data']` allows the `html(cell)` function to be **automatically re-invoked when the node's `data` prop changes**, eliminating the need for manual `view.render()`:

```javascript
Shape.HTML.register({
  shape: 'status-badge',
  width: 200, height: 50,
  effect: ['data'],
  html(node) {
    const { name, status } = node.getData() || {};
    const colors = { online: '#52c41a', offline: '#ff4d4f', idle: '#faad14' };
    const color = colors[status] || '#d9d9d9';
    const div = document.createElement('div');
    div.style.cssText = `width:100%;height:100%;display:flex;align-items:center;
      padding:0 10px;border:2px solid ${color};border-radius:8px;background:#fff;`;
    div.innerHTML = `
      <div style="width:8px;height:8px;border-radius:50%;background:${color};margin-right:8px;"></div>
      <span style="font-size:13px;">${name || ''}</span>
      <span style="font-size:11px;color:${color};margin-left:auto;">${status || ''}</span>
    `;
    return div;
  },
});

const node = graph.addNode({
  shape: 'status-badge',
  x: 80, y: 60,
  data: { name: 'API Server', status: 'online' },
});

// Modifying data automatically triggers html(cell) re-execution → view refresh
setTimeout(() => node.setData({ name: 'API Server', status: 'offline' }), 1000);
```

> **When to add `effect: ['data']`**：Dynamic changes in business data (status switches, count updates, etc.).  
> **When not to add**：Purely static node displays (hardcoded card titles, no modifications via `setData`). Unnecessary effects increase re-rendering overhead.

### 2.4 Form / Interactive Node with Input / Select

```javascript
Shape.HTML.register({
  shape: 'form-node',
  width: 220, height: 130,
  html(node) {
    const data = node.getData() || {};
    const div = document.createElement('div');
    div.style.cssText =
      'width:100%;height:100%;padding:12px;box-sizing:border-box;' +
      'border:1px solid #d9d9d9;border-radius:8px;background:#fff;';
    div.innerHTML = `
      <div style="font-size:13px;font-weight:500;margin-bottom:8px;">${data.title || ''}</div>
      <div style="margin-bottom:6px;">
        <label style="font-size:11px;color:#666;">Name:</label>
        <input style="width:100%;padding:3px 6px;border:1px solid #d9d9d9;border-radius:4px;font-size:12px;box-sizing:border-box;" value="${data.name || ''}" />
      </div>
      <div>
        <label style="font-size:11px;color:#666;">Type:</label>
        <select style="width:100%;padding:3px 6px;border:1px solid #d9d9d9;border-radius:4px;font-size:12px;">
          <option ${data.type === 'string' ? 'selected' : ''}>string</option>
          <option ${data.type === 'number' ? 'selected' : ''}>number</option>
        </select>
      </div>
    `;
    return div;
  },
});

graph.addNode({
  shape: 'form-node',
  x: 80, y: 40,
  data: { title: 'Variable Config', name: 'userName', type: 'string' },
});
```

### 2.5 User Card (Avatar + Text)

```javascript
Shape.HTML.register({
  shape: 'user-card',
  width: 200, height: 60,
  html(node) {
    const data = node.getData() || {};
    const div = document.createElement('div');
    div.style.cssText =
      'width:100%;height:100%;display:flex;align-items:center;padding:8px;' +
      'box-sizing:border-box;border:1px solid #e8e8e8;border-radius:8px;background:#fff;';
    div.innerHTML = `
      <div style="width:36px;height:36px;border-radius:50%;background:#1890ff;
        display:flex;align-items:center;justify-content:center;
        color:#fff;font-weight:bold;margin-right:10px;">
        ${(data.name || 'U')[0]}
      </div>
      <div>
        <div style="font-size:14px;font-weight:500;">${data.name || ''}</div>
        <div style="font-size:12px;color:#999;">${data.role || ''}</div>
      </div>
    `;
    return div;
  },
});
```

## 3. Three Valid Returns for the `html` Field (Source Code `src/shape/html.ts:124-134`)

```ts
let { html } = content;
if (typeof html === 'function') {
  html = html(this.cell);
}
if (html) {
  if (typeof html === 'string') {
    container.innerHTML = html;
  } else {
    Dom.append(container, html);   // Must be an HTMLElement
  }
}
```

| Return Type | Rendering Method | Applicable Scenarios |
|---------|---------|---------|
| `string` | `container.innerHTML = html` | Static structure, template string concatenation |
| `HTMLElement` | `Dom.append(container, html)` | Requires addEventListener / ref holding |
| `(cell) => string \| HTMLElement` | Same as above, can read cell state | Content depends on data / props |

Returning `null` / `undefined` / empty string will **render as an empty div**.

## 4. Style Guidelines (for writing according to expected)

The HTML shape in the official X6 demo usually **keeps it minimalistic**:

1. **Node width and height** are written in `Shape.HTML.register({ width, height })` as the default values for the shape; can be omitted when `addNode`
2. **`addNode`** only passes `shape` / `x` / `y` / `data` (if needed), **do not repeat width/height** (unless you really want to override)
3. **Styles are written in one line using `cssText`** or concise `style.xxx` assignments, avoiding long strings of decorative properties like `box-shadow / fontFamily / padding`
4. **Do not add `effect: ['data']` to static nodes** - only needed when dynamically modifying with setData
5. **Do not include connecting / addEdge / centerContent in HTML shape demos** - unless explicitly required
6. **`background: { color: '#F2F7FA' }`** is the commonly used light blue background color in X6 demos, consistent with expected

## 5. X6 2.x Legacy APIs Deprecated (Important)

⚠️ **`Graph.registerHTMLComponent(name, factory)` does not exist in X6 3.x**:

```javascript
// ❌ Incorrect: X6 2.x legacy API, removed from 3.x source code (grep src/ yields no matches)
Graph.registerHTMLComponent('user-card', (node) => { /* ... */ });
graph.addNode({ shape: 'html', html: 'user-card', data: {...} });

// ✅ Correct: X6 3.x uses Shape.HTML.register uniformly
Shape.HTML.register({
  shape: 'user-card',
  html(node) { /* ... */ },
});
graph.addNode({ shape: 'user-card', data: {...} });
```

If you encounter `Graph.registerHTMLComponent` in online resources or old demos, **replace it with `Shape.HTML.register`**:
- No longer need to specify shape as the string `'html'` and reference with `html: 'component-name'`
- Directly use the registered shape name in `addNode({ shape })`

## 6. Common Errors and Fixes

### ❌ Directly writing `'html'` for `shape` when using `addNode`

```javascript
// Error: 'html' is a built-in basic shape in X6, without HTML content definition
graph.addNode({ shape: 'html', html: '<div>x</div>' });
// → Throws "shape not found" or renders blank
```

```javascript
// Correct: First register a named shape
Shape.HTML.register({ shape: 'card', html: '<div>x</div>' });
graph.addNode({ shape: 'card', x: 0, y: 0, width: 100, height: 40 });
```

### ❌ Forgot to return value in `html` callback

```javascript
Shape.HTML.register({
  shape: 'card',
  html(node) {
    const div = document.createElement('div');
    div.textContent = 'hi';
    // ❌ Forgot to return → foreignObject is empty
  },
});
```

```javascript
// Correct: Must return
html(node) {
  const div = document.createElement('div');
  div.textContent = 'hi';
  return div;
}
```

### ❌ Using `Graph.registerHTMLComponent` (X6 2.x remnant)

Refer to Section 5.

### ❌ Incorrect `effect` prop name

```javascript
// Error: 'datas' is not a valid NodeProperty key
Shape.HTML.register({ shape: 'x', effect: ['datas'], html(n) { /* ... */ } });
// → setData will not trigger re-rendering
```

```javascript
// Correct: effect elements must be keys of NodeProperties (e.g., 'data' / 'attrs' / 'size' / 'position')
Shape.HTML.register({ shape: 'x', effect: ['data'], html(n) { /* ... */ } });
```

### ❌ HTML Node Size Not Taking Effect

```javascript
// Error: div size is hardcoded in px, but the outer foreignObject size is determined by width/height
html(node) {
  const div = document.createElement('div');
  div.style.width = '300px';   // ⚠️ Node itself is only 200x80
  div.style.height = '200px';  // → Exceeds foreignObject and gets clipped
  return div;
}
```

```javascript
// Correct: Use 100% internally to fill the foreignObject, node size controlled by register/addNode
html(node) {
  const div = document.createElement('div');
  div.style.cssText = 'width:100%;height:100%;...';
  return div;
}
graph.addNode({ shape: 'card', width: 300, height: 200 });
```

## 7. Related Documentation

- `core/x6-core-shapes.md` — Overview of all 10 built-in shapes
- `core/x6-core-node.md` — Node API (addNode / setData / events)
- `core/x6-core-cell-data.md` — Reading, writing, and listening to cell.data
- `intermediate/x6-intermediate-custom-node.md` — Registering custom SVG nodes using Graph.registerNode