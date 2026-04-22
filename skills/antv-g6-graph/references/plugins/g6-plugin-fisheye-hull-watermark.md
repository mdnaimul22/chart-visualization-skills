---
id: "g6-plugin-fisheye-hull-watermark"
title: "G6 Fisheye, Hull, and Watermark"
description: |
  fisheye: Focus at mouse position + context magnifier effect.
  hull: Draw a bounding contour (convex/concave hull) around a set of nodes.
  watermark: Add text or image watermark to the canvas.

library: "g6"
version: "5.x"
category: "plugins"
subcategory: "display"
tags:
  - "plugin"
  - "fisheye"
  - "hull"
  - "watermark"

related:
  - "g6-plugin-minimap"
  - "g6-plugin-tooltip"

difficulty: "advanced"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Fisheye Magnification (fisheye)

The fisheye lens magnifies a local area near the mouse while keeping the global context visible.

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: Array.from({ length: 50 }, (_, i) => ({
      id: `n${i}`,
      label: `N${i}`,
    })),
    edges: Array.from({ length: 60 }, (_, i) => ({
      source: `n${i % 25}`,
      target: `n${(i * 3 + 7) % 50}`,
    })),
  },
  node: {
    type: 'circle',
    style: {
      size: 20,
      fill: '#1783FF',
      stroke: '#fff',
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
      labelFontSize: 10,
    },
  },
  layout: { type: 'force', preventOverlap: true, nodeSize: 20 },
  behaviors: ['drag-canvas', 'zoom-canvas'],
  plugins: [
    {
      type: 'fisheye',
      trigger: 'pointermove',        // 'pointermove' | 'drag' | 'click'
      r: 120,                        // Fisheye lens radius (px)
      d: 1.5,                        // Magnification distortion factor (higher values result in stronger magnification)
      // Adjust radius via mouse wheel
      scaleRBy: 'wheel',
      // Lens style
      style: {
        fill: 'rgba(255,255,255,0.1)',
        stroke: '#1783FF',
        lineWidth: 1,
      },
      // Node style override within magnified area
      nodeStyle: {
        labelFontSize: 14,
        labelFontWeight: 'bold',
      },
    },
  ],
});

graph.render();
```

### fisheye Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `trigger` | `string` | `'pointermove'` | Event that triggers the fisheye movement |
| `r` | `number` | `120` | Lens radius (px) |
| `d` | `number` | `1.5` | Distortion coefficient, higher values result in greater magnification |
| `scaleRBy` | `'wheel' \| 'drag'` | — | Adjust radius by wheel/drag |
| `scaleDBy` | `'wheel' \| 'drag'` | — | Adjust distortion by wheel/drag |
| `style` | `Partial<CircleStyleProps>` | — | Lens appearance style |
| `nodeStyle` | `NodeStyle \| ((d) => NodeStyle)` | — | Node style within the magnified area |

---

## Hull

Draws convex or concave hulls around specified node sets, suitable for group visualization.

```javascript
plugins: [
  {
    type: 'hull',
    // Define one or more hulls
    hulls: [
      {
        id: 'hull-team-a',
        members: ['n1', 'n2', 'n3'],   // List of node IDs
        type: 'smooth-convex',          // 'convex' | 'smooth-convex' | 'concave'
        padding: 20,                    // Hull expansion distance
        style: {
          fill: 'rgba(23, 131, 255, 0.1)',
          stroke: '#1783FF',
          lineWidth: 2,
        },
        labelText: 'Team A',
        labelPlacement: 'top',
      },
      {
        id: 'hull-team-b',
        members: ['n4', 'n5', 'n6'],
        type: 'smooth-convex',
        padding: 20,
        style: {
          fill: 'rgba(82, 196, 26, 0.1)',
          stroke: '#52c41a',
          lineWidth: 2,
        },
        labelText: 'Team B',
      },
    ],
  },
],
```

### Hull Type Description

| Type | Description |
|------|------|
| `convex` | Minimum convex hull, fits the boundary |
| `smooth-convex` | Smooth convex hull (default, recommended) |
| `concave` | Concave hull, can bypass internal holes |

---

## Watermark

```javascript
plugins: [
  // Text Watermark
  {
    type: 'watermark',
    text: 'Internal Document · Confidential',
    textFill: '#ccc',
    textFontSize: 14,
    textFontFamily: 'Arial',
    opacity: 0.3,
    rotate: -Math.PI / 6,   // Rotation angle (in radians)
    width: 200,
    height: 100,
  },
  // Image Watermark (choose one of the two)
  // {
  //   type: 'watermark',
  //   imageURL: 'https://example.com/logo.png',
  //   width: 120,
  //   height: 40,
  //   opacity: 0.15,
  // },
],
```

### watermark Configuration Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `text` | `string` | — | Text watermark content (either `text` or `imageURL` must be provided) |
| `imageURL` | `string` | — | Image watermark URL |
| `textFill` | `string` | `'#000'` | Text color |
| `textFontSize` | `number` | `14` | Font size |
| `opacity` | `number` | `0.2` | Watermark opacity |
| `rotate` | `number` | `Math.PI/12` | Rotation angle (in radians) |
| `width` | `number` | `200` | Width of a single watermark |
| `height` | `number` | `100` | Height of a single watermark |