---
id: "x6-core-connector-params"
title: "X6 Connector Full Parameters"
description: |
  Full parameter descriptions for X6's five built-in connectors (normal/rounded/smooth/jumpover/loop), including key configuration items such as radius for rounded and direction for smooth.
library: x6
version: 3.x
category: "core"
tags:
  - connector
  - rounded
  - smooth
  - normal
  - jumpover
  - loop
  - radius
  - direction
---

# Connector Complete Parameters

```markdown

# Connector Complete Parameters
```

**Note:** The provided content only contains a header in Chinese and its English translation. Since there is no additional content to translate, the output remains the same as the input with the header translated. If you have more content to translate, please provide it, and I will ensure it adheres to the strict instructions.

```markdown
# Connector Complete Parameters
```
# Connector Complete Parameters
```

## Overview

The Connector determines the edge line style—how to draw curves between the path points calculated by the router. X6 3.x comes with 5 built-in connectors.

## Usage

```javascript
// String shorthand (using default parameters)
graph.addEdge({ source, target, connector: 'rounded' });

// Object form (passing parameters)
graph.addEdge({
  source, target,
  connector: { name: 'rounded', args: { radius: 20 } },
});
```

## normal — Line Segment (Default)

Connects path points with a straight line segment, no additional parameters required.

```javascript
graph.addEdge({ source, target, connector: 'normal' });
```

**Parameters:** No special parameters.

---

## rounded — Rounded Corners

Draws rounded corners at the bends of the polyline using Bézier curves.

```javascript
graph.addEdge({
  source, target,
  router: 'orth',
  connector: { name: 'rounded', args: { radius: 10 } },
});
```

**Parameters:**

| Parameter | Type | Default Value | Description |
|-----------|------|---------------|-------------|
| `radius`  | number | `10` | Radius of the rounded corners (px). Larger values result in larger rounded corners. The actual radius will not exceed half the length of the adjacent line segments. |

**Example Comparison:**

```javascript
// Small radius
connector: { name: 'rounded', args: { radius: 5 } }

// Large radius
connector: { name: 'rounded', args: { radius: 30 } }
```

---

## smooth — Bézier Curve

Connects the start and end points using a cubic Bézier curve. If route points exist, it uses Catmull-Rom spline fitting.

```javascript
graph.addEdge({
  source, target,
  connector: { name: 'smooth', args: { direction: 'H' } },
});
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `direction` | `'H'` \| `'V'` | Auto | Direction of the Bézier curve control points. `'H'` for horizontal (suitable for left-right layouts), `'V'` for vertical (suitable for top-bottom layouts). If not provided, it is automatically determined based on the distance between the start and end points. |

**Direction Explanation:**
- `'H'` (Horizontal): Control points are centered on the X-axis, producing an S-shaped horizontal curve. Suitable for DAG charts, lineage graphs, and other left-right flow layouts.
- `'V'` (Vertical): Control points are centered on the Y-axis, producing an S-shaped vertical curve. Suitable for organizational charts and other top-bottom flow layouts.
- Not provided: Automatically selects `'H'` if `|dx| >= |dy|`, otherwise selects `'V'`.

**Note:** When route points (`routePoints`) exist, the `direction` parameter is ignored, and a Catmull-Rom spline curve is used to pass through all route points.

```javascript
// Lineage graph with horizontal layout
graph.addEdge({
  source: { cell: leftNode, port: 'out' },
  target: { cell: rightNode, port: 'in' },
  connector: { name: 'smooth', args: { direction: 'H' } },
});

// Organizational chart with vertical layout
graph.addEdge({
  source: { cell: parentNode, port: 'bottom' },
  target: { cell: childNode, port: 'top' },
  connector: { name: 'smooth', args: { direction: 'V' } },
});
```

---

## jumpover

When two edges intersect on the canvas, draw an arc-shaped jumpover at the intersection point to distinguish different paths.

```javascript
graph.addEdge({
  source, target,
  connector: { name: 'jumpover', args: { size: 5, type: 'arc' } },
});
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | `'arc'` \| `'gap'` \| `'cubic'` | `'arc'` | Jumpover style: arc/gap/cubic curve |
| `size` | number | `5` | Jumpover size (radius or gap width) |

---

## loop — Self-Loop Connector

Used when the source and target of an edge are the same node, drawing a circular path that starts and ends at the same node.

```javascript
graph.addEdge({
  source: node,
  target: node,
  connector: { name: 'loop', args: { width: 50, height: 80, direction: 'top' } },
});
```

**Parameters:**

| Parameter | Type | Default Value | Description |
|-----------|------|---------------|-------------|
| `width` | number | | Width of the loop |
| `height` | number | | Height of the loop |
| `direction` | string | | Direction of the loop |

---

## Custom Connector

Register a custom connector using `Graph.registerConnector`:

```javascript
import { Graph, Path } from '@antv/x6';

Graph.registerConnector('wobble', (sourcePoint, targetPoint, routePoints, options) => {
  const path = new Path();
  path.appendSegment(Path.createSegment('M', sourcePoint));
  // Custom path logic
  path.appendSegment(Path.createSegment('L', targetPoint));
  return options.raw ? path : path.serialize();
});

graph.addEdge({
  source, target,
  connector: { name: 'wobble', args: {} },
});
```

**Connector Function Signature:**

```typescript
(
  sourcePoint: PointLike,      // Source point coordinates
  targetPoint: PointLike,      // Target point coordinates
  routePoints: PointLike[],    // Intermediate route points calculated by the router
  options: T,                  // User-provided args
  edgeView: EdgeView,          // Edge view instance
) => Path | string             // Returns a Path object or SVG path string
```

## Complete Example

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  connecting: {
    router: 'orth',
    connector: { name: 'rounded', args: { radius: 8 } },
  },
});

const n1 = graph.addNode({ shape: 'rect', x: 50, y: 50, width: 80, height: 40, label: 'A' });
const n2 = graph.addNode({ shape: 'rect', x: 300, y: 50, width: 80, height: 40, label: 'B' });
const n3 = graph.addNode({ shape: 'rect', x: 300, y: 250, width: 80, height: 40, label: 'C' });

// rounded rounded polyline
graph.addEdge({ source: n1, target: n2, router: 'orth', connector: { name: 'rounded', args: { radius: 15 } } });

// smooth Bezier curve
graph.addEdge({ source: n1, target: n3, connector: { name: 'smooth', args: { direction: 'H' } } });

// self-loop edge
graph.addEdge({ source: n2, target: n2, connector: 'loop' });
```

## Common Errors

```javascript
// ❌ Error: rounded has no effect when used without a router as there are no corners to round
graph.addEdge({ source, target, connector: 'rounded' });
// Only a straight line between two points, rounded has no effect

// ✅ Correct: Use with orth/manhattan router to produce corners
graph.addEdge({ source, target, router: 'orth', connector: 'rounded' });

// ❌ Error: Incorrect spelling of direction for smooth
connector: { name: 'smooth', args: { direction: 'horizontal' } }  // Invalid

// ✅ Correct: Only accepts 'H' or 'V'
connector: { name: 'smooth', args: { direction: 'H' } }
```