---
id: "g6-plugin-timebar-gridline"
title: "G6 Timebar and Grid Line"
description: |
  timebar: Filter or play the temporal changes of graph data through a time axis.
  grid-line: Draw grid auxiliary lines on the canvas background, supporting canvas zoom and pan.

library: "g6"
version: "5.x"
category: "plugins"
subcategory: "display"
tags:
  - "plugin"
  - "timebar"
  - "grid"
  - "timebar"
  - "grid-line"

related:
  - "g6-plugin-minimap"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Timebar

The timebar allows filtering nodes/edges by time range or automatically playing sequential data.

```javascript
import { Graph } from '@antv/g6';

// Node/edge data contains timestamp field
const data = {
  nodes: [
    { id: 'n1', data: { label: 'A', timestamp: 1000 } },
    { id: 'n2', data: { label: 'B', timestamp: 2000 } },
    { id: 'n3', data: { label: 'C', timestamp: 3000 } },
    { id: 'n4', data: { label: 'D', timestamp: 4000 } },
  ],
  edges: [
    { source: 'n1', target: 'n2', data: { timestamp: 1500 } },
    { source: 'n2', target: 'n3', data: { timestamp: 2500 } },
    { source: 'n3', target: 'n4', data: { timestamp: 3500 } },
  ],
};

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data,
  node: {
    type: 'circle',
    style: {
      size: 40,
      fill: '#1783FF',
      stroke: '#fff',
      labelText: (d) => d.data.label,
    },
  },
  layout: { type: 'dagre', rankdir: 'LR' },
  behaviors: ['drag-canvas', 'zoom-canvas'],
  plugins: [
    {
      type: 'timebar',
      // Time data: equally spaced ticks
      ticks: [1000, 1500, 2000, 2500, 3000, 3500, 4000],
      // Function to extract time value from data
      getTime: (datum) => datum.data.timestamp,
      // Initial visible time range
      values: [1000, 2500],
      // Affected element types
      elementTypes: ['node', 'edge'],
      // Filtering mode
      mode: 'modify',          // 'modify' (change visibility) | 'visibility' (display none)
      // Timebar type
      timebarType: 'time',     // 'time' | 'chart' (trend line chart)
      // Position
      position: 'bottom',      // 'bottom' | 'top'
      // Dimensions
      width: 600,
      height: 60,
      // Time label formatting
      labelFormatter: (t) => new Date(t).toLocaleDateString(),
      // Change callback
      onChange: (values) => {
        console.log('Time range:', values);
      },
    },
  ],
});

graph.render();
```

### timebar Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `data` | `number[] \| { time, value }[]` | — | **Required**, time scale data |
| `getTime` | `(datum) => number` | — | **Required**, extract time value from element data |
| `values` | `number \| [number, number]` | — | Initial time range |
| `elementTypes` | `ElementType[]` | `['node']` | Filtered element types |
| `mode` | `'modify' \| 'visibility'` | `'modify'` | Filtering mode |
| `timebarType` | `'time' \| 'chart'` | `'time'` | Time axis style type |
| `position` | `'bottom' \| 'top'` | `'bottom'` | Position |
| `width` | `number` | `450` | Width |
| `height` | `number` | `60` | Height |
| `labelFormatter` | `(time) => string` | — | Time label formatter |
| `loop` | `boolean` | `false` | Loop during playback |

### Timebar Playback Control API

```javascript
const timebar = graph.getPluginInstance('timebar-key');
timebar.play();      // Auto play
timebar.pause();     // Pause
timebar.forward();   // Move forward one frame
timebar.backward();  // Move backward one frame
timebar.reset();     // Reset to start
```

---

## Grid Line (grid-line)

Draws a reference grid on the canvas background to assist with alignment and layout.

```javascript
plugins: [
  {
    type: 'grid-line',
    size: 20,                  // Grid cell size (px)
    stroke: '#0001',           // Grid line color (default very light)
    lineWidth: 1,
    // Whether to follow canvas translation/zoom
    follow: {
      translate: true,         // Follow translation
      zoom: false,             // Do not follow zoom (maintain pixel size)
    },
    // Border
    border: true,
    borderStroke: '#e8e8e8',
    borderLineWidth: 1,
    borderStyle: 'solid',
  },
],
```

### grid-line Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `size` | `number` | `20` | Grid cell size (px) |
| `stroke` | `string` | `'#0001'` | Grid line color |
| `lineWidth` | `number \| string` | `1` | Grid line width |
| `follow` | `boolean \| { translate?, zoom? }` | `false` | Whether to follow canvas transformations |
| `border` | `boolean` | `true` | Whether to draw the border |
| `borderStroke` | `string` | `'#eee'` | Border color |
| `borderLineWidth` | `number` | `1` | Border width |

> **Note:** `follow: true` is equivalent to `{ translate: true, zoom: true }`, the grid will scale with the canvas,  
> ensuring the grid always covers the visible area with fixed spacing. `follow: false` (default) fixes the grid at its initial position.