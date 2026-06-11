---
id: "x6-core-port-layout"
title: "X6 Port Layout"
description: |
  Positioning strategy for ports on nodes and layout strategy for port labels.
  Port layout controls the distribution of ports on the node boundary, while port label layout controls the display position and direction of port labels.

library: "x6"
version: "3.x"
category: "core"
subcategory: "port-layout"
tags:
  - "port"
  - "layout"
  - "port layout"
  - "port position"
  - "top"
  - "bottom"
  - "left"
  - "right"
  - "absolute"
  - "ellipse"
  - "line"
  - "label"

related:
  - "x6-core-ports"
  - "x6-core-node"
  - "x6-core-edge"

use_cases:
  - "Control the distribution of ports on the four sides of a node"
  - "Customize the absolute position of ports"
  - "Distribute ports in an elliptical pattern"
  - "Control the position and direction of port labels"

difficulty: "intermediate"
completeness: "full"
---

## Core Concepts

In X6, port layout is divided into two layers:

- **Port Layout**: Determines the coordinates of the port on the node's BBox.
- **Port Label Layout**: Determines the position, angle, and text anchor of the port label relative to the port.

Both are configured through the `position` and `label.position` fields of the port group (group).

## Port Layout (Port Layout)

### Configuration Method

Set the `position` field in the node's `ports.groups`:

```javascript
graph.addNode({
  shape: 'rect',
  x: 100,
  y: 100,
  width: 120,
  height: 60,
  ports: {
    groups: {
      in: {
        position: 'left',  // String shorthand
        attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
      out: {
        position: { name: 'right', args: { strict: true } },  // Object format with parameters
        attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
    },
    items: [
      { id: 'in1', group: 'in' },
      { id: 'in2', group: 'in' },
      { id: 'out1', group: 'out' },
    ],
  },
});
```

### Built-in Port Position Layout

| Name | Description |
|------|------|
| `'left'` | Evenly distributed along the left side of the node |
| `'right'` | Evenly distributed along the right side of the node |
| `'top'` | Evenly distributed along the top side of the node |
| `'bottom'` | Evenly distributed along the bottom side of the node |
| `'line'` | Evenly distributed along a custom line segment |
| `'absolute'` | Each port is independently assigned absolute coordinates |
| `'ellipse'` | Distributed along an elliptical arc |
| `'ellipseSpread'` | Evenly spread distribution along an ellipse |

### left / right / top / bottom Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `strict` | `boolean` | `false` | Whether to use strict equal spacing. `false`: Ports are evenly distributed in the middle area; `true`: Equal spacing distribution including margins on both ends |
| `dx` | `number` | `0` | X offset for each port |
| `dy` | `number` | `0` | Y offset for each port |

**Difference in `strict`**:
- `strict: false` (default): N ports divide the edge into N equal parts, with ports at the midpoint of each part. For example, 2 ports are at the 1/4 and 3/4 positions.
- `strict: true`: N ports divide the edge into N+1 equal parts, with ports at the division points. For example, 2 ports are at the 1/3 and 2/3 positions.

### line parameter

Distribute ports along a custom line segment.

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `start` | `{ x, y }` | Top-left corner of the node | Start point of the line segment (relative to node BBox) |
| `end` | `{ x, y }` | Bottom-right corner of the node | End point of the line segment (relative to node BBox) |
| `strict` | `boolean` | `false` | Whether to distribute ports with strict equal spacing |
| `dx` | `number` | `0` | X offset |
| `dy` | `number` | `0` | Y offset |

### absolute Parameter

Each port independently specifies its position. Set through the `args` of each port in the port items:

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `x` | `number \| string` | `0` | X coordinate, supports percentage like `'50%'` |
| `y` | `number \| string` | `0` | Y coordinate, supports percentage like `'50%'` |
| `angle` | `number` | `0` | Rotation angle |

### ellipse / ellipseSpread Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `start` | `number` | `0` | Starting angle (in degrees) |
| `step` | `number` | `20` (ellipse) / `360/N` (ellipseSpread) | Angle step |
| `compensateRotate` | `boolean` | `false` | Whether to compensate for rotation angle, keeping ports always facing outward |
| `dr` | `number` | `0` | Radial offset (positive value outward, negative value inward) |
| `dx` | `number` | `0` | X offset |
| `dy` | `number` | `0` | Y offset |

**ellipse vs ellipseSpread**:
- `ellipse`: Ports expand from the center at `start` angle, spreading to both sides by `step` angle
- `ellipseSpread`: Ports are evenly distributed along the ellipse, with step automatically calculated as `360/N`

## Port Label Layout (Port Label Layout)

### Configuration Method

Set in the `label.position` of the port group:

```javascript
ports: {
  groups: {
    in: {
      position: 'left',
      label: {
        position: 'left',  // Label displayed on the left side of the port
      },
      attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
    },
  },
}
```

### Built-in Label Layout

| Name | Description |
|------|------|
| `'left'` | Label on the left side of the port, right-aligned |
| `'right'` | Label on the right side of the port, left-aligned |
| `'top'` | Label above the port, centered |
| `'bottom'` | Label below the port, centered |
| `'outside'` | Label outside the port (relative to the node center) |
| `'outsideOriented'` | Same as outside, but text orientation follows the angle |
| `'inside'` | Label inside the port (closer to the node center) |
| `'insideOriented'` | Same as inside, but text orientation follows the angle |
| `'radial'` | Radial layout, label offset outward along the radial direction |
| `'radialOriented'` | Same as radial, but text orientation follows the radial angle |
| `'manual'` | Manually specify the position |

### outside / inside Parameters

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `offset` | `number` | `15` | Distance between the label and the port |

### radial Parameter

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `offset` | `number` | `20` | Offset distance of the label along the radial direction |

## Complete Example

### Four-Sided Ports (Most Commonly Used)

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  connecting: { allowBlank: false, router: 'orth', connector: 'rounded' },
});

graph.addNode({
  shape: 'rect',
  x: 200,
  y: 150,
  width: 160,
  height: 80,
  label: 'Processing Node',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
  ports: {
    groups: {
      in: {
        position: 'left',
        label: { position: 'left' },
        attrs: { circle: { r: 5, magnet: true, stroke: '#1890ff', fill: '#fff' } },
      },
      out: {
        position: 'right',
        label: { position: 'right' },
        attrs: { circle: { r: 5, magnet: true, stroke: '#52c41a', fill: '#fff' } },
      },
    },
    items: [
      { id: 'in1', group: 'in', attrs: { text: { text: 'Input 1' } } },
      { id: 'in2', group: 'in', attrs: { text: { text: 'Input 2' } } },
      { id: 'out1', group: 'out', attrs: { text: { text: 'Output' } } },
    ],
  },
});
```

### Absolute Positioning of Ports

```javascript
graph.addNode({
  shape: 'rect',
  x: 100,
  y: 100,
  width: 160,
  height: 80,
  label: 'Custom Port Position',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
  ports: {
    groups: {
      custom: {
        position: 'absolute',
        attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
    },
    items: [
      { id: 'p1', group: 'custom', args: { x: 0, y: '25%' } },
      { id: 'p2', group: 'custom', args: { x: '100%', y: '25%' } },
      { id: 'p3', group: 'custom', args: { x: '50%', y: '100%' } },
    ],
  },
});
```

### Elliptical Distribution Ports

```javascript
graph.addNode({
  shape: 'ellipse',
  x: 200,
  y: 150,
  width: 120,
  height: 120,
  label: 'Service',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f' } },
  ports: {
    groups: {
      around: {
        position: { name: 'ellipseSpread', args: { start: 0 } },
        label: { position: 'outside' },
        attrs: { circle: { r: 4, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
    },
    items: [
      { id: 'p1', group: 'around', attrs: { text: { text: 'API' } } },
      { id: 'p2', group: 'around', attrs: { text: { text: 'DB' } } },
      { id: 'p3', group: 'around', attrs: { text: { text: 'MQ' } } },
      { id: 'p4', group: 'around', attrs: { text: { text: 'RPC' } } },
    ],
  },
});
```

### Strict Mode Comparison

```javascript
// 2 ports on the left:
// strict: false → located at 1/4 and 3/4 (default, visually more centered)
// strict: true  → located at 1/3 and 2/3 (equally spaced, including end spacing)

graph.addNode({
  shape: 'rect',
  x: 100, y: 100, width: 120, height: 80,
  ports: {
    groups: {
      left: {
        position: { name: 'left', args: { strict: true } },
        attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
    },
    items: [
      { id: 'p1', group: 'left' },
      { id: 'p2', group: 'left' },
    ],
  },
});
```

## Common Errors

### ❌ Confusing port layout with port label layout

```javascript
// Incorrect: position is the port position layout, not the label position
ports: {
  groups: {
    in: {
      position: 'outside', // ❌ 'outside' is a label layout, not a port position layout
    },
  },
}

// Correct
ports: {
  groups: {
    in: {
      position: 'left',               // ✅ Port position layout
      label: { position: 'outside' }, // ✅ Label layout
    },
  },
}
```

### ❌ Forgot to pass args in items for absolute layout

```javascript
// Error: absolute requires each item to specify a position
ports: {
  groups: { custom: { position: 'absolute' } },
  items: [
    { id: 'p1', group: 'custom' }, // ❌ Missing args, defaults to (0,0)
  ],
}

// Correct
ports: {
  groups: { custom: { position: 'absolute' } },
  items: [
    { id: 'p1', group: 'custom', args: { x: '50%', y: 0 } }, // ✅
  ],
}
```