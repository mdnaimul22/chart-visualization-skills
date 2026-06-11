---
id: "x6-plugin-snapline"
title: "X6 Snapline Alignment Plugin"
description: |
  The Snapline plugin automatically displays alignment guides when nodes are dragged and moved, helping users precisely align node positions.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "snapline"
tags:
  - "Snapline"
  - "Alignment Line"
  - "Guide Line"
  - "Snapping"
  - "Alignment"
  - "snap"

related:
  - "x6-plugins"
  - "x6-core-node"

use_cases:
  - "Display alignment lines during node dragging"
  - "Precisely align multiple nodes"
  - "Adjust snapping tolerance"

difficulty: "beginner"
completeness: "full"
---

## Basic Usage

```javascript
import { Graph, Snapline } from '@antv/x6';

const graph = new Graph({ container: 'container' });
graph.use(new Snapline({ enabled: true }));
```

When dragging a node, a red auxiliary line will automatically appear and snap to the aligned position when the node's edge or center aligns with another node.

## Configuration Options

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `enabled` | boolean | `true` | Whether to enable alignment lines |
| `tolerance` | number | `10` | Snap tolerance (pixels), triggers snapping when the distance from the node edge/center to the alignment position is less than this value |
| `sharp` | boolean | `false` | Whether to display truncated alignment lines (only shown between aligned nodes) |
| `resizing` | boolean | `false` | Whether to display alignment lines during node resizing |
| `clean` | boolean \| number | `true` | Automatic clearing of alignment lines. `true` clears immediately, a number represents the delay in milliseconds |
| `filter` | function \| string[] | - | Filters nodes that do not participate in alignment calculations |

## Programmatic API

```javascript
// Enable/Disable
graph.enableSnapline();
graph.disableSnapline();
graph.toggleSnapline(true);
graph.isSnaplineEnabled();  // boolean

// Hide currently displayed snaplines
graph.hideSnapline();

// Set filter
graph.setSnaplineFilter((node) => {
  return node.getData()?.snapable !== false;
});

// Tolerance control
graph.getSnaplineTolerance();      // number, current tolerance value
graph.setSnaplineTolerance(20);    // Set tolerance

// Sharp (truncation style) control
graph.isSharpSnapline();           // boolean
graph.enableSharpSnapline();       // Enable truncation style
graph.disableSharpSnapline();      // Disable truncation style
graph.toggleSharpSnapline(true);

// Whether to display snaplines during resizing
graph.isSnaplineOnResizingEnabled();   // boolean
graph.enableSnaplineOnResizing();
graph.disableSnaplineOnResizing();
graph.toggleSnaplineOnResizing(true);
```

## Complete Example

```javascript
import { Graph, Snapline } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  grid: { visible: true, size: 10 },
});

graph.use(new Snapline({
  enabled: true,
  tolerance: 15,   // 15px tolerance
  sharp: true,     // sharp style
  resizing: true,  // align during resizing
}));

// Add example nodes
graph.addNode({ x: 100, y: 100, width: 120, height: 60, label: 'Node A' });
graph.addNode({ x: 350, y: 200, width: 120, height: 60, label: 'Node B' });
graph.addNode({ x: 200, y: 350, width: 120, height: 60, label: 'Node C' });
// When dragging Node C to align left with Node A, a vertical alignment line will appear
```

## Filter Examples

```javascript
// Filter by shape name: Only specific shapes participate in alignment
graph.use(new Snapline({
  enabled: true,
  filter: ['rect', 'circle'],  // Only rect and circle nodes participate in alignment
}));

// Filter by function
graph.use(new Snapline({
  enabled: true,
  filter(node) {
    // Nodes with the 'group' tag do not participate in alignment
    return node.getData()?.type !== 'group';
  },
}));
```

## Common Errors

### ❌ Configure snapline in the constructor

```javascript
// Error: Not supported in 3.x
const graph = new Graph({
  container: 'container',
  snapline: { enabled: true },  // ❌
});
```

```javascript
// Correct
import { Graph, Snapline } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Snapline({ enabled: true }));  // ✅
```