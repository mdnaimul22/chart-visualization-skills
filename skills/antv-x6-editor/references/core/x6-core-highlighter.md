---
id: "x6-core-highlighter"
title: "X6 Highlighter"
description: |
  Configuration for highlighting effects on nodes and edges.
  Used to highlight connectable nodes/ports during edge interaction, or to customize visual feedback for selected states.
  Built-in highlight strategies include stroke, className, and opacity.

library: "x6"
version: "3.x"
category: "core"
subcategory: "highlighter"
tags:
  - "highlighter"
  - "highlight"
  - "stroke"
  - "className"
  - "opacity"
  - "highlighting"
  - "magnetAvailable"
  - "nodeAvailable"
  - "edge highlighting"

related:
  - "x6-core-graph-init"
  - "x6-core-ports"
  - "x6-core-edge"

use_cases:
  - "Highlight connectable ports during edge interaction"
  - "Highlight connectable nodes during edge interaction"
  - "Customize highlight styles for selected elements"
  - "Provide visual feedback on mouse hover"

difficulty: "intermediate"
completeness: "full"
---

## Core Concepts

**Highlighter** provides visual highlighting effects for nodes/edges. X6 automatically triggers highlighting during edge interactions:

- **magnetAvailable**: When dragging an edge, highlight connectable ports (magnets)
- **nodeAvailable**: When dragging an edge, highlight connectable nodes
- **default**: Default highlight style (used when manually triggered, e.g., `graph.highlightCell()`)

## Configuration Method

Configure in the `highlighting` field of the Graph constructor:

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  connecting: {
    highlight: true,  // Must be enabled to trigger highlighting during connection
  },
  highlighting: {
    default: {
      name: 'stroke',
      args: { padding: 3 },
    },
    magnetAvailable: {
      name: 'className',
      args: { className: 'available-magnet' },
    },
    nodeAvailable: {
      name: 'className',
      args: { className: 'available-node' },
    },
  },
});
```

## Built-in Highlighter

### stroke

Draws a stroke highlight box (SVG path) around the element, the most commonly used highlighting method.

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `padding` | `number` | `3` | The spacing between the highlight box and the element |
| `rx` | `number` | `0` | Highlight box rounded corner X |
| `ry` | `number` | `0` | Highlight box rounded corner Y |
| `attrs` | `object` | `{ 'stroke-width': 3, stroke: '#FEB663' }` | SVG attributes of the highlight box |

```javascript
highlighting: {
  default: {
    name: 'stroke',
    args: {
      padding: 5,
      rx: 4,
      ry: 4,
      attrs: {
        'stroke-width': 2,
        stroke: '#1890ff',
        'stroke-dasharray': '5 3',
      },
    },
  },
}
```

### className

Highlighting is achieved by adding a CSS class name, which is suitable for implementing complex effects using CSS animations.

| Parameter | Type | Default Value | Description |
|------|------|--------|------|
| `className` | `string` | `'x6-highlighted'` | CSS class name added to the element |

```javascript
highlighting: {
  magnetAvailable: {
    name: 'className',
    args: { className: 'port-available' },
  },
}
```

Accompanying CSS:

```css
.port-available circle {
  fill: #52c41a;
  stroke: #52c41a;
  transition: all 0.2s;
}
```

### opacity

Highlighting is achieved by adding a CSS class name that reduces opacity (the actual effect is that non-highlighted elements become faded).

No parameters are required; use directly:

```javascript
highlighting: {
  nodeAvailable: {
    name: 'opacity',
    args: {},
  },
}
```

## highlighting Configuration

| Field | Trigger Timing | Description |
|-------|----------------|-------------|
| `default` | When `graph.highlightCell()` is manually called | Default highlight style |
| `magnetAvailable` | When dragging a line and passing over a connectable magnet during connection | Port/element highlight |
| `nodeAvailable` | When dragging a line and passing over a connectable node during connection | Node highlight |

**Note**: `highlight: true` must be set in `connecting` for `magnetAvailable` and `nodeAvailable` highlights to be triggered during line interaction.

## Graph Default Configuration

Default highlighting configuration for X6 Graph (source code):

```javascript
highlighting: {
  default: {
    name: 'stroke',
    args: { padding: 3 },
  },
  nodeAvailable: {
    name: 'className',
    args: { className: 'x6-available-node' },
  },
  magnetAvailable: {
    name: 'className',
    args: { className: 'x6-available-magnet' },
  },
}
```

## Complete Example

### Highlight Available Ports When Connecting

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  connecting: {
    highlight: true,
    allowBlank: false,
    router: 'orth',
    connector: 'rounded',
  },
  highlighting: {
    magnetAvailable: {
      name: 'stroke',
      args: {
        padding: 4,
        attrs: { 'stroke-width': 2, stroke: '#52c41a' },
      },
    },
  },
});

const node1 = graph.addNode({
  shape: 'rect',
  x: 100,
  y: 100,
  width: 120,
  height: 60,
  label: 'Source',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
  ports: {
    groups: {
      out: {
        position: 'right',
        attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
    },
    items: [{ id: 'out1', group: 'out' }],
  },
});

const node2 = graph.addNode({
  shape: 'rect',
  x: 400,
  y: 100,
  width: 120,
  height: 60,
  label: 'Target',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
  ports: {
    groups: {
      in: {
        position: 'left',
        attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f', fill: '#fff' } },
      },
    },
    items: [{ id: 'in1', group: 'in' }],
  },
});

// When dragging a connection from node1's out1 port, node2's in1 port will be highlighted
```

### Manual Highlight/Unhighlight

Manually trigger highlighting using the `highlight()` / `unhighlight()` methods of `CellView`:

```javascript
// Get the node view
const nodeView = graph.findViewByCell(node1);

// Manual highlight (uses highlighting.default configuration when no options are provided)
nodeView.highlight();

// Highlight a specific child element using a custom highlighter
nodeView.highlight(nodeView.container.querySelector('rect'), {
  highlighter: { name: 'stroke', args: { padding: 5, attrs: { stroke: '#f5222d' } } },
});

// Unhighlight
nodeView.unhighlight();
```

## Common Errors

### ❌ Ports Do Not Highlight During Connection

```javascript
// Error: Forgot to enable connecting.highlight
const graph = new Graph({
  container: 'container',
  connecting: {
    allowBlank: false,
    // highlight defaults to false!
  },
  highlighting: {
    magnetAvailable: { name: 'stroke', args: { padding: 4 } },
  },
});
// Ports will not highlight during connection

// Correct: Must set highlight: true
const graph = new Graph({
  container: 'container',
  connecting: {
    allowBlank: false,
    highlight: true, // ✅ Enable connection highlighting
  },
  highlighting: {
    magnetAvailable: { name: 'stroke', args: { padding: 4 } },
  },
});
```

### ❌ Using className but Forgetting to Write CSS

```javascript
// Problem: className highlighter only adds a class name, without built-in styles
highlighting: {
  magnetAvailable: {
    name: 'className',
    args: { className: 'my-highlight' }, // Only adds a class name
  },
}
// If there are no corresponding CSS rules, there will be no visual changes

// Solution: Add CSS or switch to the stroke highlighter
```