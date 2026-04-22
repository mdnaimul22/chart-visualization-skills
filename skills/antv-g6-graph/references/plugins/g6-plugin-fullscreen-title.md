---
id: "g6-plugin-fullscreen-title"
title: "G6 Fullscreen Plugin + Title Plugin (fullscreen / title)"
description: |
  fullscreen: Expands the graph visualization to the entire screen, supporting shortcut key triggers and programmatic control.
  title: Adds a main title and subtitle to the graph, supporting custom positioning, fonts, and styles.

library: "g6"
version: "5.x"
category: "plugins"
subcategory: "ui"
tags:
  - "fullscreen"
  - "title"
  - "全屏"
  - "标题"
  - "图标题"
  - "沉浸式"

related:
  - "g6-plugin-contextmenu-toolbar"
  - "g6-plugin-history-legend"

difficulty: "beginner"
completeness: "full"
created: "2026-04-16"
updated: "2026-04-16"
---

## Title Plugin (title)

Adds a main title and subtitle to the graph canvas, supporting custom styles such as font, color, and alignment.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
      { id: 'n1', label: 'Node 1' },
      { id: 'n2', label: 'Node 2' },
    ],
    edges: [{ source: 'n1', target: 'n2' }],
  },
  layout: { type: 'force' },
  behaviors: ['drag-canvas', 'zoom-canvas'],
  plugins: [
    {
      type: 'title',
      key: 'chart-title',
      title: 'Knowledge Graph',         // Main title text
      subtitle: 'Data Source: Internal System', // Subtitle text
      align: 'left',           // 'left' | 'center' | 'right'
      size: 48,                // Title area height (px), default 44
      padding: [16, 24, 0, 24], // [top, right, bottom, left]
      spacing: 8,              // Spacing between main and subtitle (px)
    },
  ],
});

graph.render();
```

### Title Configuration Parameters

**Container Configuration:**

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `type` | `string` | `'title'` | Plugin type |
| `key` | `string` | — | Unique identifier |
| `title` | `string` | — | **Required**: Main title text |
| `subtitle` | `string` | — | Subtitle text |
| `align` | `'left' \| 'center' \| 'right'` | `'left'` | Title alignment |
| `size` | `number` | `44` | Title area height (px) |
| `padding` | `number \| number[]` | `[16,24,0,24]` | Inner padding |
| `spacing` | `number` | `8` | Spacing between main and subtitle |

**Main Title Style (titleXxx):**

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `titleFontSize` | `number` | `16` | Font size |
| `titleFontWeight` | `number` | `bold` | Font weight |
| `titleFill` | `string` | `'#1D2129'` | Font color |
| `titleFillOpacity` | `number` | `0.9` | Font opacity |
| `titleFontFamily` | `string` | `'system-ui, sans-serif'` | Font family |

**Subtitle Style (subtitleXxx):**

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `subtitleFontSize` | `number` | `12` | Font size |
| `subtitleFontWeight` | `number` | `normal` | Font weight |
| `subtitleFill` | `string` | `'#1D2129'` | Font color |
| `subtitleFillOpacity` | `number` | `0.65` | Font opacity |

### Complete Style Example

```javascript
plugins: [
  {
    type: 'title',
    key: 'title',
    align: 'center',
    size: 60,
    spacing: 4,
    // Main Title
    title: 'Organizational Structure Chart',
    titleFontSize: 20,
    titleFontWeight: 600,
    titleFill: '#262626',
    // Subtitle
    subtitle: '2026 Q1 · Total 120 People',
    subtitleFontSize: 13,
    subtitleFill: '#8c8c8c',
  },
]
```

### Dynamic Title Update

```javascript
graph.updatePlugin({ key: 'title', title: 'New Title', subtitle: 'Updated on: 2026-04-16' });
```

---

## Fullscreen Plugin (fullscreen)

Expand the graph visualization to fullscreen, supporting both shortcut key triggers and programmatic control via API, with enter/exit callbacks.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: Array.from({ length: 20 }, (_, i) => ({ id: `n${i}` })),
  },
  layout: { type: 'force' },
  behaviors: ['drag-canvas', 'zoom-canvas'],
  plugins: [
    {
      type: 'fullscreen',
      key: 'fullscreen',
      autoFit: true,     // Auto-fit canvas size after entering fullscreen
      trigger: {
        request: 'F',    // Press F to enter fullscreen
        exit: 'Escape',  // Press Esc to exit fullscreen
      },
      onEnter: () => console.log('Enter fullscreen'),
      onExit: () => console.log('Exit fullscreen'),
    },
  ],
});

graph.render();
```

### fullscreen Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `type` | `string` | `'fullscreen'` | Plugin type |
| `key` | `string` | — | Unique identifier (required for programmatic control) |
| `autoFit` | `boolean` | `true` | Whether to automatically adapt canvas size after entering fullscreen |
| `trigger` | `{ request?: string; exit?: string }` | — | Trigger keyboard shortcuts |
| `onEnter` | `() => void` | — | Callback when entering fullscreen |
| `onExit` | `() => void` | — | Callback when exiting fullscreen |

### Programming Control for Fullscreen

```javascript
const graph = new Graph({
  plugins: [{ type: 'fullscreen', key: 'fs' }],
});

// Control via API
const fsPlugin = graph.getPluginInstance('fs');
fsPlugin.request();  // Enter fullscreen
fsPlugin.exit();     // Exit fullscreen
```

### Use with Toolbar

```javascript
plugins: [
  { type: 'fullscreen', key: 'fullscreen' },
  {
    type: 'toolbar',
    position: 'top-left',
    onClick: (item) => {
      const fs = graph.getPluginInstance('fullscreen');
      if (item === 'fullscreen') fs.request();
      if (item === 'exit-fullscreen') fs.exit();
    },
    getItems: () => [
      { id: 'fullscreen', value: 'fullscreen' },
      { id: 'exit-fullscreen', value: 'exit-fullscreen' },
    ],
  },
]
```

---

## Title + Fullscreen Combination Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 900,
  height: 600,
  data: {
    nodes: Array.from({ length: 15 }, (_, i) => ({
      id: `n${i}`,
      data: { label: `Node${i}` },
    })),
    edges: Array.from({ length: 12 }, (_, i) => ({
      source: `n${i % 10}`,
      target: `n${(i + 3) % 15}`,
    })),
  },
  node: {
    style: {
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
  },
  layout: { type: 'force', preventOverlap: true },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
  plugins: [
    {
      type: 'title',
      title: 'Relationship Network Graph',
      subtitle: 'Based on Force-Directed Layout',
      align: 'center',
    },
    {
      type: 'fullscreen',
      key: 'fs',
      autoFit: true,
      trigger: { request: 'F', exit: 'Escape' },
    },
    {
      type: 'toolbar',
      position: 'top-right',
      onClick: (item) => {
        if (item === 'fullscreen') graph.getPluginInstance('fs').request();
      },
      getItems: () => [{ id: 'fullscreen', value: 'fullscreen' }],
    },
  ],
});

graph.render();
```