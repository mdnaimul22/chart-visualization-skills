---
id: "x6-core-geometry"
title: "X6 Geometry Tools"
description: |
  X6's built-in geometry toolkit, including Point / Line / Rectangle / Ellipse / Polyline / Path / Curve,
  as well as Angle and util utility functions. This document is based on the actual source code in src/geometry/*.ts,
  organizing commonly used APIs and typical scenarios (calculating node positions, path lengths, intersection judgments, angle conversions, etc.).

library: "x6"
version: "3.x"
category: "core"
subcategory: "geometry"
tags:
  - "geometry"
  - "Point"
  - "Rectangle"
  - "Line"
  - "Ellipse"
  - "Polyline"
  - "Path"
  - "Curve"
  - "Angle"
  - "toDeg"
  - "toRad"
  - "snapToGrid"
  - "containsPoint"
  - "intersect"
  - "BBox"

related:
  - "x6-core-coord"
  - "x6-core-node"
  - "x6-core-edge"
  - "x6-core-router-advanced"

use_cases:
  - "Calculate path geometry in custom routers / connectors"
  - "Determine if a point falls within a node's BBox"
  - "Calculate distance / midpoint / angle between two points"
  - "Find intersection points / containment relationships using Rectangle"
  - "Align mouse coordinates to a grid"
  - "Convert between angles and radians"

anti_patterns:
  - "Mixing Geometry classes with DOM elements"
  - "Directly reading/writing properties of Point / Rectangle instances without calling graph.refresh()"
  - "Manually calculating angles using Math.atan2 instead of utilizing X6's built-in Angle.toDeg"

difficulty: "intermediate"
completeness: "full"
---

## Overview

X6 abstracts all geometric calculations in the `src/geometry/` module, uniformly exported through the `@antv/x6` top-level namespace. These classes are **decoupled from the DOM**—they are purely mathematical objects and can be used in any callback, such as custom routers, connectors, connection points, attributes, tools, etc.

```javascript
import { Point, Line, Rectangle, Ellipse, Polyline, Path, Curve, Angle } from '@antv/x6';
```

> All Geometry subclasses inherit from the `Geometry` base class, supporting method chaining (most methods return `this`).

## Angle (Angle Utility, Functional Export)

Source code: `src/geometry/angle.ts`. Direct namespace import:

```javascript
import { Angle } from '@antv/x6';

Angle.toDeg(Math.PI);          // 180   Radians → Degrees
Angle.toRad(180);              // π     Degrees → Radians
Angle.toRad(720, true);        // 4π    Second parameter over360=true disables modulo 360
Angle.normalize(-30);          // 330   Normalize any angle to [0, 360)
```

| API | Description |
|-----|------|
| `Angle.toDeg(rad)` | Radians → Degrees, result modulo 360 |
| `Angle.toRad(deg, over360?)` | Degrees → Radians, defaults to `deg % 360` |
| `Angle.normalize(angle)` | Normalize any value to `[0, 360)` |

## Point (2D Point)

Source code: `src/geometry/point.ts`.

### Creation

```javascript
import { Point } from '@antv/x6';

new Point(10, 20);
Point.create(10, 20);                  // Equivalent
Point.create({ x: 10, y: 20 });        // From PointLike
Point.create([10, 20]);                // From array
Point.fromPolar(100, Math.PI / 4);     // Polar → Cartesian
```

### Common Instance Methods (Chaining)

```javascript
const p = new Point(10, 20);

p.translate(5, 5);                     // (15, 25), modifies itself and returns this
p.scale(2, 2);                         // (30, 50), third parameter origin defaults to (0,0)
p.rotate(90, new Point(0, 0));         // Rotates counterclockwise by 90° around the origin (degrees, not radians)
p.distance({ x: 0, y: 0 });            // Distance to another point
p.equals({ x: 30, y: 50 });            // Checks if equal
const q = p.clone();                   // Deep copy
p.round(2);                            // Rounds to 2 decimal places
p.toJSON();                            // { x, y }
```

> ⚠️ The angle for `rotate` is in **degrees**, not radians.

### Typical Scenario: Calculating Endpoints in a Custom Connection Strategy

```javascript
import { Graph, Point } from '@antv/x6';

Graph.registerConnectionStrategy('snap-by-distance', (args) => {
  const { sourcePoint, targetPoint, type, terminal } = args;
  // Align the endpoint to a 10px grid
  const aligned = new Point(targetPoint.x, targetPoint.y).round();
  return { ...terminal, x: aligned.x, y: aligned.y };
});
```

## Line

Source code: `src/geometry/line.ts`.

### Creation

```javascript
import { Line, Point } from '@antv/x6';

new Line(0, 0, 100, 100);                       // (x1, y1, x2, y2)
new Line({ x: 0, y: 0 }, { x: 100, y: 100 });   // Two PointLike objects
```

### Common Methods

```javascript
const l = new Line(0, 0, 100, 0);

l.start;                            // Point(0,0)
l.end;                              // Point(100,0)
l.center;                           // Point(50,0) (getter)
l.getCenter();                      // Same as above

l.length();                         // 100
l.angle();                          // 0 (angle with the positive X-axis, in degrees)
l.vector();                         // Point(100, 0)

l.pointAt(0.5);                     // Point(50, 0), ratio 0~1
l.pointAtLength(30);                // Point(30, 0), by pixel length

l.containsPoint({ x: 50, y: 0 });   // true
l.intersect(new Line(50, -10, 50, 10));  // [Point(50, 0)]
l.translate(0, 10);
l.scale(2, 2);
l.rotate(90, new Point(0, 0));
l.clone();
l.equals(other);
```

## Rectangle (Rectangle / BBox, Most Commonly Used)

Source code: `src/geometry/rectangle.ts`. Most X6 APIs (`cell.getBBox()`, `node.getBBox()`, `graph.getContentBBox()`) return a `Rectangle`.

### Creation

```javascript
import { Rectangle } from '@antv/x6';

new Rectangle(10, 20, 100, 60);                   // (x, y, width, height)
Rectangle.create(10, 20, 100, 60);
Rectangle.create({ x: 10, y: 20, width: 100, height: 60 });
Rectangle.create([10, 20, 100, 60]);
Rectangle.fromEllipse(ellipse);
```

### Center / Corner / Size

```javascript
const r = new Rectangle(10, 20, 100, 60);

r.getCenter();           // Point(60, 50)
r.getCenterX();          // 60
r.getCenterY();          // 50
r.getOrigin();           // Point(10, 20)
r.getCorner();           // Point(110, 80) Bottom-right
r.getTopLeft();
r.getTopRight();
r.getBottomLeft();
r.getBottomRight();
r.getTopMiddle();
r.getBottomMiddle();
r.getLeftMiddle();
r.getRightMiddle();
r.toJSON();              // { x, y, width, height }
```

### Geometric Transformations

```javascript
r.translate(5, 5);
r.scale(2, 2);                                  // The third parameter origin defaults to (0,0)
r.rotate(45);                                   // Rotate around the center, return the rotated BBox
r.rotate90();                                   // 90° rotation (special shortcut)
r.inflate(10);                                  // Expand 10px in all directions
r.inflate(10, 20);                              // x +10, y +20
r.normalize();                                  // Convert negative width/height to positive
r.round(2);
```

### Judgment

```javascript
r.containsPoint(50, 50);
r.containsPoint({ x: 50, y: 50 });
r.containsRect(other);
r.intersectsWithLine(line);                      // Returns intersection array | null
r.intersectsWithRect(other);                     // Returns intersecting Rectangle | null
r.intersectsWithLineFromCenterToPoint(target);   // Intersection of the ray from center to target with the edge
r.equals(other);
r.clone();
```

### Typical Scenario: Determining if a Node is Within the Canvas Visible Area

```javascript
import { Rectangle } from '@antv/x6';

const viewport = Rectangle.create(graph.getGraphArea());  // Current viewport
const visibleNodes = graph.getNodes().filter((n) => {
  return viewport.intersectsWithRect(n.getBBox()) != null;
});
```

## Ellipse

Source code: `src/geometry/ellipse.ts`.

```javascript
import { Ellipse, Rectangle } from '@antv/x6';

new Ellipse(centerX, centerY, semiAxisA, semiAxisB);
Ellipse.fromRect(rect);              // from inscribed rectangle

const e = new Ellipse(50, 50, 40, 20);
e.bbox();                            // bounding box Rectangle
e.center();                          // Point(50, 50)
e.containsPoint({ x: 50, y: 50 });   // true
e.intersectionWithLine(line);        // intersection with line segment
e.tangentTheta(point);               // tangent angle
e.clone();
```

## Polyline

Source code: `src/geometry/polyline.ts`.

```javascript
import { Polyline, Point } from '@antv/x6';

const pl = new Polyline([new Point(0, 0), new Point(50, 50), new Point(100, 0)]);
// Also supports PointLike[] / [number, number][]
new Polyline([[0, 0], [50, 50], [100, 0]]);
new Polyline([{x:0,y:0}, {x:50,y:50}, {x:100,y:0}]);

pl.length();                         // Total length of the polyline
pl.pointAt(0.5);                     // Proportional positioning
pl.pointAtLength(60);                // Positioning by length
pl.bbox();                           // Bounding Rectangle
pl.simplify();                       // Remove collinear points
pl.clone();
```

## Path / Curve (SVG Path and Cubic Bezier)

Source code: `src/geometry/path/*` and `src/geometry/curve.ts`.

```javascript
import { Path, Curve } from '@antv/x6';

const path = new Path();
path
  .moveTo(0, 0)
  .lineTo(100, 0)
  .quadTo(150, 50, 100, 100)
  .curveTo(80, 120, 20, 120, 0, 100)
  .close();

path.length();                       // Arc length (approximate)
path.bbox();                         // Bounding box
path.pointAtLength(50);              // Point at length along path
path.serialize();                    // Output standard SVG d string

// Cubic Bezier
const c = new Curve(
  { x: 0, y: 0 },
  { x: 30, y: 100 },
  { x: 70, y: 100 },
  { x: 100, y: 0 },
);
c.pointAt(0.5);
c.length();
c.divide(0.5);                       // Split into two segments
```

Path is commonly used in custom connectors / markers:

```javascript
// Custom connector
import { Graph, Path, Point } from '@antv/x6';

Graph.registerConnector('curve-connector', (sourcePoint, targetPoint) => {
  const path = new Path();
  path.moveTo(sourcePoint.x, sourcePoint.y);
  path.curveTo(
    sourcePoint.x + 80, sourcePoint.y,
    targetPoint.x - 80, targetPoint.y,
    targetPoint.x, targetPoint.y,
  );
  return path.serialize();
}, true);
```

## util (Numerical Utilities)

Source code: `src/geometry/util.ts`, not exported via the `Geometry` class name, needs to be imported from the top-level of `@antv/x6`:

```javascript
import { round, random, clamp, snapToGrid, containsPoint, squaredLength } from '@antv/x6';

round(3.14159, 2);                    // 3.14
random();                             // 0~1
random(10);                           // 0~10 integer
random(5, 15);                        // 5~15 integer
clamp(150, 0, 100);                   // 100
snapToGrid(73, 10);                   // 70
containsPoint({ x:0, y:0, width:100, height:100 }, { x: 50, y: 50 });  // true
squaredLength({ x:0, y:0 }, { x:3, y:4 });   // 25
```

> `snapToGrid` is extremely common when implementing the "mouse drag alignment to grid" feature.

## End-to-End Example: Implementing a "Center Nodes and Edges" Button Using the Geometry Tool

```javascript
import { Graph, Rectangle, Point } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
  panning: true,
  mousewheel: { enabled: true, modifiers: 'ctrl' },
});

// Add sample content
const a = graph.addNode({ shape: 'rect', x: 40,  y: 40,  width: 80, height: 40, label: 'A' });
const b = graph.addNode({ shape: 'rect', x: 320, y: 220, width: 80, height: 40, label: 'B' });
graph.addEdge({ source: a, target: b });

graph.centerContent();

// Business method: Align all node centers to the horizontal centerline of the canvas
function centerHorizontally() {
  const area = Rectangle.create(graph.getGraphArea());
  const cy = area.getCenterY();
  graph.getNodes().forEach((node) => {
    const bbox = node.getBBox();
    const newY = cy - bbox.height / 2 - area.y; // Convert to node coordinates
    node.position(node.position().x, newY);
  });
}

// Usage:
// centerHorizontally();
```

## Common Errors and Fixes

### ❌ Passing Degrees as Radians to Point.rotate

```javascript
// Error: rotate accepts "degrees"
new Point(10, 0).rotate(Math.PI / 2);   // Actually rotates only 1.57°

// Correct
new Point(10, 0).rotate(90);
// Or convert from radians
import { Angle } from '@antv/x6';
new Point(10, 0).rotate(Angle.toDeg(Math.PI / 2));
```

### ❌ Treating Geometry Objects as DOM Elements

```javascript
// Error: Rectangle is a mathematical object without DOM reference
const r = new Rectangle(0, 0, 100, 100);
r.style.background = 'red';            // ❌ TypeError

// Correct: To style canvas elements, use cell.attr(...) or cell.setProp(...)
node.attr('body/fill', 'red');
```

### ❌ Forgot to Sync Back to Cell After Modifying Rectangle Instance Properties

```javascript
// Error: node.getBBox() returns a new Rectangle copy, modifying it does not affect the node
const bbox = node.getBBox();
bbox.x += 50;                          // ❌ Node position remains unchanged

// Correct: Use node API
node.translate(50, 0);
// Or
node.position(node.position().x + 50, node.position().y);
```

### ❌ Setting `gridSize` to 0 when using `snapToGrid`

```javascript
// Error: Will result in NaN
snapToGrid(73, 0);

// Correct: grid must be > 0
snapToGrid(73, graph.getGridSize() || 10);
```