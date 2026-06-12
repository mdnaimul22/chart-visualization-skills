---
id: "x6-core-background"
title: "X6 Canvas Background Configuration"
description: |
  X6 Canvas Background Configuration: solid color background, background image, tiling mode (repeat/flip-x/flip-y/flip-xy/watermark), opacity, etc.

library: "x6"
version: "3.x"
category: "core"
subcategory: "background"
tags:
  - "background"
  - "背景"
  - "背景色"
  - "背景图片"
  - "水印"
  - "watermark"

related:
  - "x6-core-graph-init"
  - "x6-core-grid"

use_cases:
  - "Set canvas background color"
  - "Set canvas background image"
  - "Add watermark to canvas"
  - "Background image tiling/flipping"
  - "Dynamically switch background"

difficulty: "beginner"
completeness: "full"
---
## Basic Usage

The background is configured in the Graph constructor via the `background` field:

```javascript
import { Graph } from '@antv/x6';

// Solid color background
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
});
```

## Configuration Options

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `color` | string | - | Background color (CSS color value) |
| `image` | string | - | Background image URL |
| `position` | string \| object | `'center'` | Background image position. String: CSS background-position; Object: `{ x, y }` |
| `size` | string \| object | `'auto auto'` | Background image size. String: `'auto'`/`'contain'`/`'cover'`; Object: `{ width, height }` |
| `repeat` | string | `'no-repeat'` | Tiling mode: `'repeat'`, `'no-repeat'`, `'repeat-x'`, `'repeat-y'`, `'flip-x'`, `'flip-y'`, `'flip-xy'`, `'watermark'` |
| `opacity` | number | `1` | Background opacity (0~1) |

## Solid Color Background

```javascript
const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
});
```

## Background Image

```javascript
const graph = new Graph({
  container: 'container',
  background: {
    image: 'https://example.com/bg.png',
    size: 'cover',
    position: 'center',
    opacity: 0.5,
  },
});
```

## Tiled Mode

### repeat (Standard Tiling)

```javascript
const graph = new Graph({
  container: 'container',
  background: {
    image: 'https://example.com/tile.png',
    repeat: 'repeat',
    size: { width: 100, height: 100 },
  },
});
```

### flip-x / flip-y / flip-xy (Flip Tiling)

The image alternates and flips in the horizontal/vertical direction, creating a mirrored tiling effect:

```javascript
const graph = new Graph({
  container: 'container',
  background: {
    image: 'https://example.com/pattern.png',
    repeat: 'flip-xy',  // Flip both horizontally and vertically
    size: { width: 200, height: 200 },
  },
});
```

### Watermark

Tile an image as a watermark with a rotation angle:

```javascript
const graph = new Graph({
  container: 'container',
  background: {
    image: 'https://example.com/watermark.png',
    repeat: 'watermark',
    opacity: 0.1,
  },
});
```

## Programmatic API

```javascript
// Dynamically set background
graph.drawBackground({ color: '#fff' });

// Set background image
graph.drawBackground({
  image: 'https://example.com/bg.png',
  repeat: 'repeat',
  size: { width: 100, height: 100 },
});

// Clear background
graph.clearBackground();
```

## Complete Example: Background Color + Grid

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
  grid: { visible: true, size: 10, type: 'dot' },
});

graph.addNode({
  x: 200,
  y: 150,
  width: 120,
  height: 60,
  label: 'Hello',
  attrs: { body: { fill: '#fff', stroke: '#5F95FF' } },
});
```

## Common Errors

### ❌ Confusion Between `background` and `grid` Colors

```javascript
// Note: The color of `grid` refers to the color of grid lines/points, not the background color
const graph = new Graph({
  container: 'container',
  grid: { visible: true, args: { color: '#F2F7FA' } },  // ❌ This does not set the background color
});

// Correct: Use `background` for background color and `grid.args.color` for grid color
const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },  // ✅ Background color
  grid: { visible: true, args: { color: '#ddd' } },  // ✅ Grid point color
});
```

### ❌ Image Path Issues

```javascript
// Note: image must be an accessible URL or Data URL
background: {
  image: './bg.png',  // ⚠️ Relative paths may fail to load in certain environments
}

// Recommended: Use absolute URLs or imported resources
background: {
  image: 'https://cdn.example.com/bg.png',  // ✅
}
```