---
id: "g6-plugin-contextmenu-toolbar"
title: "G6 Context Menu (contextmenu) and Toolbar (toolbar)"
description: |
  contextmenu: Right-click on an element to pop up the operation menu.
  toolbar: Display toolbar buttons (zoom, fit, undo, etc.) in the corner of the canvas.

library: "g6"
version: "5.x"
category: "plugins"
subcategory: "interaction"
tags:
  - "plugin"
  - "context menu"
  - "toolbar"
  - "contextmenu"
  - "toolbar"

related:
  - "g6-plugin-tooltip"
  - "g6-plugin-history"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Context Menu (contextmenu)

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'User A' } },
       { id: 'n2', data: { label: 'User B' } },
    ],
    edges: [{ source: 'n1', target: 'n2' }],
  },
  node: {
    type: 'circle',
    style: {
      size: 40,
      fill: '#1783FF',
      stroke: '#fff',
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
  },
  layout: { type: 'circular' },
  behaviors: ['drag-canvas', 'zoom-canvas'],
  plugins: [
    {
      type: 'contextmenu',
      trigger: 'contextmenu',          // 'click' | 'contextmenu' (default)
      // Return menu item list
      getItems: (event) => {
        // Return different menus based on the clicked element type
        if (event.targetType === 'node') {
          return [
             { id: 'view',   value: 'view',   name: 'View Details' },
             { id: 'edit',   value: 'edit',   name: 'Edit Node' },
             { id: 'delete', value: 'delete', name: 'Delete Node' },
          ];
        }
        if (event.targetType === 'edge') {
          return [
             { id: 'delete', value: 'delete', name: 'Delete Edge' },
          ];
        }
        // Click on canvas
        return [
           { id: 'fit',   value: 'fit',   name: 'Fit View' },
           { id: 'reset', value: 'reset', name: 'Reset View' },
        ];
      },
      // Menu item click callback
      onClick: (value, target, current) => {
        if (value === 'delete') {
          const id = current.id;
          if (current.targetType === 'node') {
            graph.removeNodeData([id]);
          } else {
            graph.removeEdgeData([id]);
          }
          graph.draw();
        }
        if (value === 'fit') {
          graph.fitView();
        }
      },
      // Offset [x, y]
      offset: [4, 4],
    },
  ],
});

graph.render();
```

### contextmenu Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `trigger` | `'click' \| 'contextmenu'` | `'contextmenu'` | Trigger method |
| `getItems` | `(event) => Item[] \| Promise<Item[]>` | — | Menu item generation function (either this or `getContent` must be provided) |
| `getContent` | `(event) => HTMLElement \| string` | — | Fully customized menu HTML |
| `onClick` | `(value, target, current) => void` | — | Callback for menu item click |
| `offset` | `[number, number]` | `[4, 4]` | Menu offset |
| `enable` | `boolean \| ((event) => boolean)` | `true` | Whether to enable |
| `className` | `string` | `'g6-contextmenu'` | Menu container CSS class name |

---

## Toolbar

```javascript
plugins: [
  {
    type: 'toolbar',
    position: 'top-right',             // Toolbar position
    getItems: () => [
       { id: 'zoom-in',   value: 'zoom-in',   name: 'Zoom In' },
       { id: 'zoom-out',  value: 'zoom-out',  name: 'Zoom Out' },
       { id: 'fit',       value: 'fit',       name: 'Fit View' },
       { id: 'undo',      value: 'undo',      name: 'Undo' },
       { id: 'redo',      value: 'redo',      name: 'Redo' },
       { id: 'download',  value: 'download',  name: 'Export Image' },
    ],
    onClick: async (value) => {
      if (value === 'zoom-in') await graph.zoomTo(graph.getZoom() * 1.2);
      if (value === 'zoom-out') await graph.zoomTo(graph.getZoom() / 1.2);
      if (value === 'fit') await graph.fitView();
    },
    // Custom style
    style: {
      display: 'flex',
      gap: '4px',
      padding: '4px',
      background: '#fff',
      boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
      borderRadius: '4px',
    },
  },
],
```

### toolbar Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `position` | `'top-left' \| 'top-right' \| 'bottom-left' \| 'bottom-right'` | `'top-left'` | Toolbar position |
| `getItems` | `() => ToolbarItem[] \| Promise<ToolbarItem[]>` | — | **Required**, list of toolbar items |
| `onClick` | `(value: string, target: Element) => void` | — | Click callback |
| `className` | `string` | — | Toolbar CSS class name |
| `style` | `Partial<CSSStyleDeclaration>` | — | Toolbar container style |

**ToolbarItem:**
```typescript
interface ToolbarItem {
  id: string;
  value: string;     // value parameter for click callback
  name?: string;     // display text or title
  icon?: string;     // SVG icon string
}
```