---
id: "g6-node-html"
title: "G6 HTML Node"
description: |
  Use html type nodes to render arbitrary HTML content in the graph, suitable for rich text, buttons,
  forms, and other complex UI node scenarios.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "nodes"
tags:
  - "node"
  - "html"
  - "rich text"
  - "custom node"
  - "HTML"

related:
  - "g6-node-circle"
  - "g6-node-rect"
  - "g6-core-custom-element"

use_cases:
  - "Card-style nodes (with images, text, buttons)"
  - "Nodes with embedded input/select forms"
  - "Complex multi-line text display"

anti_patterns:
  - "HTML nodes perform poorly with a large number of nodes (>500), consider using canvas nodes + custom shapes instead"
  - "Do not use user input content in innerHTML (XSS risk)"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Core Concepts

The `html` node uses `foreignObject` (SVG) or DOM overlay to render HTML content.

**Key Properties:**
- `innerHTML`: Required, HTML string or `HTMLElement`
- `size`: Node dimensions `[width, height]`, default `[160, 80]`
- `dx`/`dy`: Horizontal/Vertical offset

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
      {
        id: 'card1',
        data: {
          name: 'Zhang San',
          role: 'Front-end Engineer',
          avatar: 'https://api.dicebear.com/7.x/miniavs/svg?seed=1',
        },
      },
      {
        id: 'card2',
        data: {
          name: 'Li Si',
          role: 'Back-end Engineer',
          avatar: 'https://api.dicebear.com/7.x/miniavs/svg?seed=2',
        },
      },
    ],
    edges: [{ source: 'card1', target: 'card2' }],
  },
  node: {
    type: 'html',
    style: {
      size: [160, 80],
      // innerHTML accepts a callback function to dynamically generate HTML
      innerHTML: (d) => `
        <div style="
          display: flex;
          align-items: center;
          padding: 8px 12px;
          background: #fff;
          border: 1px solid #e8e8e8;
          border-radius: 8px;
          box-shadow: 0 2px 8px rgba(0,0,0,0.08);
          width: 156px;
          box-sizing: border-box;
          gap: 8px;
        ">
          <img src="${d.data.avatar}" width="36" height="36"
               style="border-radius: 50%; flex-shrink: 0;" />
          <div>
            <div style="font-weight: 600; font-size: 13px; color: #333;">
              ${d.data.name}
            </div>
            <div style="font-size: 11px; color: #999; margin-top: 2px;">
              ${d.data.role}
            </div>
          </div>
        </div>
      `,
    },
  },
  layout: { type: 'dagre', rankdir: 'LR', nodesep: 40, ranksep: 80 },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

## Common Variants

### HTML Node with State Highlighting

```javascript
node: {
  type: 'html',
  style: {
    size: [180, 90],
    innerHTML: (d) => `
      <div id="node-${d.id}" style="
        padding: 12px 16px;
        background: #fff;
        border: 2px solid #d9d9d9;
        border-radius: 8px;
        font-size: 13px;
        transition: border-color 0.2s;
      ">
        <div style="font-weight: bold;">${d.data.title}</div>
        <div style="color: #666; margin-top: 4px;">${d.data.desc}</div>
      </div>
    `,
  },
},
```

### Node Embedded Button (Handling DOM Events)

```javascript
node: {
  type: 'html',
  style: {
    size: [200, 100],
    innerHTML: (d) => {
      const div = document.createElement('div');
      div.style.cssText = 'padding:12px;background:#fff;border:1px solid #eee;border-radius:8px;';
      div.innerHTML = `<div>${d.data.label}</div>`;
      
      const btn = document.createElement('button');
      btn.textContent = 'Details';
      btn.style.cssText = 'margin-top:8px;padding:2px 12px;cursor:pointer;';
      // Prevent event bubbling to the chart canvas to avoid triggering drag behavior, etc.
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        console.log('Node Details:', d.id);
      });
      div.appendChild(btn);
      return div;
    },
  },
},
```

## Parameter Reference

| Property | Type | Default Value | Description |
|----------|------|---------------|-------------|
| `innerHTML` | `string \| HTMLElement \| ((d: NodeData) => string \| HTMLElement)` | — | **Required**, HTML content |
| `size` | `[number, number]` | `[160, 80]` | Node width and height |
| `dx` | `number` | `0` | Horizontal offset |
| `dy` | `number` | `0` | Vertical offset |
| `pointerEvents` | `string` | `'auto'` | Mouse event penetration control |

## Common Errors

### Error 1: Using User Input in innerHTML (XSS)

```javascript
// ❌ Dangerous: Directly inserting user input
innerHTML: (d) => `<div>${d.data.userInput}</div>`

// ✅ Use textContent or escape
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
innerHTML: (d) => `<div>${escapeHtml(d.data.userInput)}</div>`
```

### Error 2: Forgetting to Set Size, Resulting in Nodes Being Too Small

```javascript
// ❌ Default size may not be sufficient to contain the content
node: {
  type: 'html',
  style: { innerHTML: '<div style="padding:20px">Large amount of content...</div>' },
}

// ✅ Explicitly set size
node: {
  type: 'html',
  style: {
    size: [240, 120],
    innerHTML: '<div style="padding:20px">Large amount of content...</div>',
  },
}
```