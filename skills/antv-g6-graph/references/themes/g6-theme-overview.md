---
id: "g6-theme-overview"
title: "G6 Theme System"
description: |
  The G6 5.x theme system, including usage methods for built-in light/dark themes and dynamic switching.

library: "g6"
version: "5.x"
category: "themes"
subcategory: "overview"
tags:
  - "theme"
  - "dark"
  - "light"

related:
  - "g6-state-overview"
  - "g6-core-graph-init"

use_cases:
  - "Graph visualization supporting both light and dark modes"
  - "Unified visual style for graphs"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/theme/overview"
---

## Core Concepts

G6 v5 themes are a subset of Graph Options, including:
- Background color (`background`)
- Default node style (`node`)
- Default edge style (`edge`)
- Default combo style (`combo`)

Each section contains: basic style, color palette, state style, and animation configuration.

**Important Limitation:** Only static values are supported in themes, callback functions are not supported.

## Using Built-in Themes

```javascript
import { Graph } from '@antv/g6';

// Light theme (default)
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: { nodes: [...], edges: [...] },
  theme: 'light',               // Default value
  layout: { type: 'force' },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

// Dark theme
const graphDark = new Graph({
  container: 'container-dark',
  theme: 'dark',
  // ...
});

graph.render();
```

## Dynamic Theme Switching

```javascript
// Initialization
const graph = new Graph({
  container: 'container',
  theme: 'light',
  // ...
});
await graph.render();

// Theme Switching
document.getElementById('theme-toggle').addEventListener('click', async () => {
  const currentTheme = graph.getTheme();
  await graph.setTheme(currentTheme === 'light' ? 'dark' : 'light');
  await graph.render();
});
```

## Palette

The palette in the theme is used to automatically assign colors based on the categorical field:

```javascript
node: {
  // Use palette to automatically color by category
  palette: {
    type: 'group',        // 'group'=categorical | 'value'=continuous mapping by value
    field: 'category',    // Field name in the data
    color: 'tableau10',   // Built-in palette name
    // Optional: Custom color list
    // color: ['#ff4d4f', '#1783FF', '#52c41a', '#fa8c16'],
  },
},
```

**Built-in Palettes:** `tableau10`、`spectral`、`blues`、`greens`、`oranges`、`reds`、`purples`

## Common Combinations

### Dark Theme + Force-Directed Graph

```javascript
const graph = new Graph({
  container: 'container',
  width: 900,
  height: 600,
  theme: 'dark',
  data: { nodes: [...], edges: [...] },
  node: {
    style: {
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
    palette: {
      type: 'group',
      field: 'type',
      color: 'tableau10',
    },
  },
  layout: { type: 'force', preventOverlap: true },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element-force', 'hover-activate'],
});
```