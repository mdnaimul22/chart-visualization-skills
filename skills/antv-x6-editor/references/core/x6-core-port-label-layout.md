---
id: "x6-core-port-label-layout"
title: "X6 Port Label Layout"
description: |
  X6 port label layout strategies: side (fixed position), outside/inside (node external/internal), radial (radial), etc., control the position and direction of port text.

library: "x6"
version: "3.x"
category: "core"
subcategory: "port-label-layout"
tags:
  - "port"
  - "label"
  - "port-label-layout"
  - "port label"
  - "label position"
  - "outside"
  - "inside"
  - "radial"

related:
  - "x6-core-ports"
  - "x6-core-port-layout"
  - "x6-core-node"

use_cases:
  - "Port label displayed on the left/right/top/bottom of the port"
  - "Port label automatically displayed outward"
  - "Port label displayed inside the node"
  - "Radial layout of port labels for circular nodes"
  - "Custom port label offset"

difficulty: "intermediate"
completeness: "full"
---

## Concept Explanation

Port Label Layout controls the offset and alignment of port text relative to the port position. Unlike Port Layout (which controls the position of ports on a node), label layout only affects the display position of the text.

## Basic Usage

Configure in the port group (`groups`) using `label.position`:

```javascript
graph.addNode({
  x: 100,
  y: 100,
  width: 160,
  height: 80,
  ports: {
    groups: {
      in: {
        position: 'left',
        label: {
          position: 'left',  // Label displayed on the left side of the port
        },
        attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
      out: {
        position: 'right',
        label: {
          position: 'right',  // Label displayed on the right side of the port
        },
        attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
    },
    items: [
      { id: 'in-1', group: 'in', attrs: { text: { text: 'Input' } } },
      { id: 'out-1', group: 'out', attrs: { text: { text: 'Output' } } },
    ],
  },
});
```

## Built-in Layout Strategies

### Side Class (Fixed Position)

| Name | Description |
|------|------|
| `'left'` | Label is on the left side of the port, right-aligned |
| `'right'` | Label is on the right side of the port, left-aligned |
| `'top'` | Label is above the port, center-aligned |
| `'bottom'` | Label is below the port, center-aligned |
| `'manual'` | Manually specify the position (via x/y in args) |

```javascript
label: {
  position: 'right',  // String shorthand
}

// Equivalent to object form
label: {
  position: {
    name: 'right',
    args: {},  // Can pass x/y/angle/attrs to override default values
  },
}
```

### InOut Class (Automatic Node In/Out Determination)

Automatically determines whether the label faces inward or outward based on the port's position on the node's edge:

| Name | Description |
|------|------|
| `'outside'` | Label is outside the node (away from the node center) |
| `'outsideOriented'` | Same as above, with text automatically rotated parallel to the edge |
| `'inside'` | Label is inside the node (toward the node center) |
| `'insideOriented'` | Same as above, with text automatically rotated parallel to the edge |

```javascript
ports: {
  groups: {
    default: {
      position: 'left',
      label: {
        position: {
          name: 'outside',
          args: { offset: 15 },  // Offset of the label from the port (in pixels)
        },
      },
    },
  },
}
```

Determination logic for `outside` and `inside`: Based on the angle of the port's position relative to the node center, automatically decides whether to place the label outside or inside the node.

### Radial Class (Radial Layout)

Suitable for scenarios where circular nodes or ports are distributed along an arc:

| Name | Description |
|------|------|
| `'radial'` | Labels are placed in the radial direction (away from the node center) |
| `'radialOriented'` | Same as above, with text automatically rotated to the radial direction |

```javascript
ports: {
  groups: {
    default: {
      position: {
        name: 'ellipse',  // Ports distributed along an ellipse
        args: { dr: 0, compensateRotate: false },
      },
      label: {
        position: {
          name: 'radial',
          args: { offset: 20 },  // Radial offset of the label from the port
        },
      },
    },
  },
}
```

## Configuration Parameters

All layout strategies support the following common parameters:

| Parameter | Type | Description |
|------|------|------|
| `x` | number | Overrides the label x offset |
| `y` | number | Overrides the label y offset |
| `angle` | number | Label rotation angle |
| `attrs` | object | Overrides the label's SVG attributes |

InOut and Radial additionally support:

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `offset` | number | `15`/`20` | Offset distance of the label from the port |

## Complete Example: Input and Output Ports

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});

graph.addNode({
  x: 200,
  y: 150,
  width: 200,
  height: 100,
  label: 'Process',
  ports: {
    groups: {
      in: {
        position: 'left',
        label: { position: 'outside' },
        attrs: {
          circle: { r: 5, magnet: true, stroke: '#31d0c6', fill: '#fff', strokeWidth: 2 },
        },
      },
      out: {
        position: 'right',
        label: { position: 'outside' },
        attrs: {
          circle: { r: 5, magnet: true, stroke: '#ff6347', fill: '#fff', strokeWidth: 2 },
        },
      },
    },
    items: [
      { id: 'in-1', group: 'in', attrs: { text: { text: 'data' } } },
      { id: 'in-2', group: 'in', attrs: { text: { text: 'config' } } },
      { id: 'out-1', group: 'out', attrs: { text: { text: 'result' } } },
      { id: 'out-2', group: 'out', attrs: { text: { text: 'error' } } },
    ],
  },
});
```

## Manual Label Positioning

Use the `manual` strategy to fully control the label position:

```javascript
label: {
  position: {
    name: 'manual',
    args: {
      x: 10,
      y: -10,
      angle: 0,
      attrs: {
        '.': { 'text-anchor': 'start', fontSize: 12, fill: '#666' },
      },
    },
  },
}
```

## Common Errors

### ❌ Confusing Port Layout (`position`) and Label Layout (`label.position`)

```javascript
// Incorrect Understanding: `label.position` does not control the port's position on the node
ports: {
  groups: {
    in: {
      position: 'left',         // Port on the left side of the node ← Port layout
      label: {
        position: 'left',       // Label on the left side of the port ← Label layout (different concept!)
      },
    },
  },
}
```

### ❌ Label Not Displayed

```javascript
// Error: Port items lack the text property
items: [{ id: 'p1', group: 'in' }]  // ❌ Label has no content

// Correct: Set label text via attrs.text.text
items: [{ id: 'p1', group: 'in', attrs: { text: { text: 'Port 1' } } }]  // ✅
```