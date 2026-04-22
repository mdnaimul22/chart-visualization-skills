---
id: "g6-core-custom-element"
title: "G6 Custom Nodes and Custom Edges"
description: |
  By inheriting BaseNode / BaseEdge and calling register() to register custom element types,
  implement graph nodes and edges with complex business shapes.

library: "g6"
version: "5.x"
category: "core"
subcategory: "customization"
tags:
  - "custom node"
  - "custom edge"
  - "register"
  - "BaseNode"
  - "BaseEdge"
  - "extension"

related:
  - "g6-node-circle"
  - "g6-node-html"
  - "g6-edge-line"
  - "g6-core-graph-api"

use_cases:
  - "Business card nodes (nodes with charts)"
  - "Specially shaped edges with annotations"
  - "Custom connection point logic"

anti_patterns:
  - "Avoid customizing if it can be achieved with built-in nodes + style configurations"
  - "Avoid complex DOM operations in custom nodes when frequently updating data"

difficulty: "advanced"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
---

## Custom Nodes

### Basic Structure

```javascript
import {
  BaseNode,
  ExtensionCategory,
  Graph,
  register,
  Rect,
  Text,
  Circle,
} from '@antv/g6';

class StatusNode extends BaseNode {
  /**
   * Draw the node body
   * Override render() to gain full control, need to manage all child shapes manually
   */
  render(attributes, container) {
    super.render(attributes, container);
    
    const [width, height] = this.getSize(attributes);
    const { status, label } = attributes;
    
    // Use upsert method to create/update shapes (first parameter is key, second is constructor, third is attributes)
    // Main rectangle (replaces the default key shape)
    this.upsert('key', Rect, {
      x: -width / 2,
      y: -height / 2,
      width,
      height,
      fill: this.getStatusColor(status),
      stroke: '#fff',
      lineWidth: 2,
      radius: 6,
    }, container);
    
    // Status indicator dot
    this.upsert('status-dot', Circle, {
      cx: width / 2 - 8,
      cy: -height / 2 + 8,
      r: 5,
      fill: status === 'online' ? '#52c41a' : '#ff4d4f',
    }, container);
    
    // Label (overrides default label behavior)
    this.upsert('label', Text, {
      x: 0,
      y: 0,
      text: label || attributes.id,
      fill: '#fff',
      fontSize: 13,
      fontWeight: 'bold',
      textAlign: 'center',
      textBaseline: 'middle',
    }, container);
  }
  
  getStatusColor(status) {
    const colors = { online: '#52c41a', offline: '#ff4d4f', idle: '#faad14' };
    return colors[status] || '#1783FF';
  }
  
  // Return default node size
  getDefaultStyle() {
    return { size: [120, 50] };
  }
}

// Register custom node type
register(ExtensionCategory.NODE, 'status-node', StatusNode);

// Usage
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
       { id: 'server1', data: { label: 'Web Server', status: 'online' } },
       { id: 'server2', data: { label: 'DB Server', status: 'offline' } },
       { id: 'server3', data: { label: 'Cache', status: 'idle' } },
    ],
    edges: [
       { source: 'server1', target: 'server2' },
       { source: 'server1', target: 'server3' },
    ],
  },
  node: {
    type: 'status-node',
    style: {
      size: [130, 50],
      // Custom attributes mapped through style callback
      status: (d) => d.data.status,
      label: (d) => d.data.label,
    },
  },
  layout: { type: 'dagre', rankdir: 'LR' },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

### Key APIs

```typescript
// upsert(key, Shape, attrs, container) - Create or update child shapes
this.upsert('shape-key', Rect, { x, y, width, height, fill }, container);

// Get node dimensions
const [width, height] = this.getSize(attributes);

// Get shapeMap (all rendered shapes)
const allShapes = this.shapeMap;

// Node center coordinates (world coordinate system)
const { x, y } = this.getPosition();
```

---

## Inheriting Built-in Node Extensions (Recommended)

For simple style extensions (such as adding animations or halo effects), it is recommended to inherit from built-in nodes (like `Circle`, `Rect`) rather than `BaseNode`, to reuse the built-in node's rendering logic:

```javascript
import { Circle, ExtensionCategory, Graph, register } from '@antv/g6';

// Inherit from built-in Circle node, adding a breathing animation halo
class BreathingCircle extends Circle {
  // onCreate is called after the element is created and its entrance animation is complete
  // Suitable for starting loop animations, avoiding conflicts with entrance animations
  onCreate() {
    const halo = this.shapeMap.halo;
    if (halo) {
      halo.animate([{ lineWidth: 0 }, { lineWidth: 20 }], {
        duration: 1000,
        iterations: Infinity,
        direction: 'alternate',
      });
    }
  }
}

register(ExtensionCategory.NODE, 'breathing-circle', BreathingCircle);

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
      { id: 'node-0' },
      { id: 'node-1' },
      { id: 'node-2' },
      { id: 'node-3' },
    ],
  },
  node: {
    type: 'breathing-circle',
    style: {
      size: 50,
      halo: true,  // Enable halo shape
    },
    palette: ['#3875f6', '#efb041', '#ec5b56', '#72c240'],
  },
  layout: {
    type: 'grid',
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});

graph.render();
```

### Lifecycle Hooks

Custom nodes/edges support the following lifecycle hooks:

```typescript
class MyNode extends BaseNode {
  /**
   * Called after the element is created and its entrance animation is complete.
   * Suitable for one-time initialization operations such as starting loop animations, binding events, etc.
   */
  onCreate() {
    const keyShape = this.shapeMap['key'];
    // Start breathing animation
    keyShape.animate(
      [{ r: 20 }, { r: 25 }, { r: 20 }],
      { duration: 2000, iterations: Infinity }
    );
  }

  /**
   * Called after the element is updated and its transition animation is complete.
   */
  onUpdate() {
    console.log('Node updated:', this.id);
  }

  /**
   * Called after the element completes its exit animation and is destroyed.
   */
  onDestroy() {
    console.log('Node destroyed:', this.id);
  }
}
```

---

## Custom Edge

```javascript
import {
  BaseEdge,
  ExtensionCategory,
  Graph,
  register,
  Path,
} from '@antv/g6';

class ArrowEdge extends BaseEdge {
  /**
   * Returns the SVG Path data for the edge (must be implemented)
   * Use this.getEndpoints(attributes) to get the start and end coordinates
   */
  getKeyPath(attributes) {
    // Get start and end coordinates (considering connection points, node boundaries, etc.)
    const [sourcePoint, targetPoint] = this.getEndpoints(attributes, false);
    
    if (!sourcePoint || !targetPoint) return [['M', 0, 0]];
    
    const [sx, sy] = sourcePoint;
    const [tx, ty] = targetPoint;
    
    // Polyline path: horizontal -> vertical -> horizontal
    const midX = (sx + tx) / 2;
    
    return [
      ['M', sx, sy],
      ['L', midX, sy],
      ['L', midX, ty],
      ['L', tx, ty],
    ];
  }
}

register(ExtensionCategory.EDGE, 'arrow-edge', ArrowEdge);

const graph = new Graph({
  // ...
  edge: {
    type: 'arrow-edge',
    style: {
      stroke: '#aaa',
      lineWidth: 1.5,
      endArrow: true,
    },
  },
});
```

### Custom Edge Animation (Ant Line)

After `super.render()`, obtain the main shape through `this.shapeMap['key']`, and then call the Web Animations API:

```javascript
import { BaseEdge, ExtensionCategory, Graph, register } from '@antv/g6';

class DashEdge extends BaseEdge {
  getKeyPath(attributes) {
    const [sourcePoint, targetPoint] = this.getEndpoints(attributes);
    if (!sourcePoint || !targetPoint) return [['M', 0, 0]];
    const [sx, sy] = sourcePoint;
    const [tx, ty] = targetPoint;
    return [['M', sx, sy], ['L', tx, ty]];
  }

  render(attributes, container) {
    super.render(attributes, container);

    const keyShape = this.shapeMap['key'];
    if (keyShape) {
      keyShape.style.lineDash = [10, 10];
      // Ant Line: Achieve flowing effect through lineDashOffset offset
      keyShape.animate(
        [{ lineDashOffset: 0 }, { lineDashOffset: -20 }],
        { duration: 1000, iterations: Infinity },
      );
    }
  }
}

register(ExtensionCategory.EDGE, 'line-dash', DashEdge);

const graph = new Graph({
  container: 'container',
  width: 800, height: 600,
  data: {
    nodes: [
      { id: 'n1', data: { label: 'Start' } },
      { id: 'n2', data: { label: 'End' } },
    ],
    edges: [{ source: 'n1', target: 'n2' }],
  },
  edge: {
    type: 'line-dash',
    style: { stroke: '#999', lineWidth: 2 },
  },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});
graph.render();
```

---

## Summary of Registered Types

```javascript
import { ExtensionCategory, register } from '@antv/g6';

// Register custom node
register(ExtensionCategory.NODE, 'my-node', MyNodeClass);

// Register custom edge
register(ExtensionCategory.EDGE, 'my-edge', MyEdgeClass);

// Register custom combo
register(ExtensionCategory.COMBO, 'my-combo', MyComboClass);

// Register custom layout
register(ExtensionCategory.LAYOUT, 'my-layout', MyLayoutClass);

// Register custom behavior
register(ExtensionCategory.BEHAVIOR, 'my-behavior', MyBehaviorClass);

// Register custom plugin
register(ExtensionCategory.PLUGIN, 'my-plugin', MyPluginClass);
```

---

## Common Errors and Fixes

### Error: Starting Loop Animation in render() Causes White Screen or Abnormal Animation

```javascript
// ❌ render() is called both when the element is created and updated. Starting the animation here can lead to:
//    1. Repeated animation starts, causing performance issues
//    2. Conflicts with entrance animations, potentially causing a white screen
//    3. Animation reset during updates
class BreathingNode extends BaseNode {
  render(attributes, container) {
    super.render(attributes, container);
    const circle = this.upsert('key', Circle, { cx: 0, cy: 0, r: 30 }, container);
    
    // Error: Starting animation in render
    circle.animate(
      [{ r: 30 }, { r: 40 }, { r: 30 }],
      { duration: 2000, iterations: Infinity }
    );
  }
}

// ✅ Use the onCreate lifecycle hook to start the loop animation after the entrance animation is complete
class BreathingNode extends BaseNode {
  render(attributes, container) {
    super.render(attributes, container);
    this.upsert('key', Circle, { cx: 0, cy: 0, r: 30 }, container);
  }
  
  onCreate() {
    const keyShape = this.shapeMap['key'];
    keyShape.animate(
      [{ r: 30 }, { r: 40 }, { r: 30 }],
      { duration: 2000, iterations: Infinity }
    );
  }
}

// ✅ Alternatively, inherit from a built-in node and use the built-in halo shape to achieve the breathing effect (recommended)
class BreathingCircle extends Circle {
  onCreate() {
    const halo = this.shapeMap.halo;
    if (halo) {
      halo.animate(
        [{ lineWidth: 0 }, { lineWidth: 20 }, { lineWidth: 0 }],
        { duration: 2000, iterations: Infinity }
      );
    }
  }
}
```

### Error: Using the Removed `extend` API

```javascript
// ❌ `extend` has been officially removed from G6 v5, causing "extend is not a function" error
import { Graph, extend } from '@antv/g6';
const ExtGraph = extend(Graph, { nodes: { 'my-node': MyNodeFn } });

// ✅ Use `BaseNode` + `register`
import { BaseNode, ExtensionCategory, register } from '@antv/g6';
class MyNode extends BaseNode { /* ... */ }
register(ExtensionCategory.NODE, 'my-node', MyNode);
```

### Error: Using a Custom Type Without Calling `register`

```javascript
// ❌ Without register, G6 does not recognize 'my-node'
const graph = new Graph({
  node: { type: 'my-node' },
});

// ✅ Register first, then use
register(ExtensionCategory.NODE, 'my-node', MyNode);
const graph = new Graph({
  node: { type: 'my-node' },
});
```

### Error: Directly Manipulating DOM in render (Should Use upsert)

```javascript
// ❌ Direct DOM manipulation is not managed by G6 rendering cycle
render(attributes, container) {
  const div = document.createElement('div');
  container.appendChild(div);
}

// ✅ Use upsert to manage shape lifecycle
render(attributes, container) {
  this.upsert('my-shape', Rect, { x: 0, y: 0 }, container);
}
```

### Error: Reading Node Business Data via `attributes.data` in `render` → Blank Screen

```javascript
// ❌ attributes is a collection of computed style properties, does not contain the node's data field
// attributes.data is undefined, accessing data.color throws TypeError → Blank Screen
render(attributes, container) {
  const { data } = attributes;        // undefined!
  const color = data.color;           // TypeError: Cannot read properties of undefined
}

// ✅ Map data to style properties via node.style callback, read directly from attributes
// Step 1: Map data to custom properties in node.style configuration of Graph
node: {
  type: 'my-node',
  style: {
    color: (d) => d.data.color,   // Mapped to attributes.color
    label: (d) => d.data.label,   // Mapped to attributes.label
  },
},
// Step 2: Directly destructure attributes in render()
render(attributes, container) {
  const { color = '#1783FF', label } = attributes;  // ✅ Correctly read
}
```

### Error: Conflict between upsert key and default shape causes double rendering

```javascript
// ❌ key is not 'key', super.render() has created a default 'key' shape,
//    calling upsert('circle', ...) will overlay an additional circle
render(attributes, container) {
  super.render(attributes, container);
  this.upsert('circle', Circle, { cx: 0, cy: 0, r: 20 }, container);  // Double circles!
}

// ✅ Replace the default main shape with 'key'
render(attributes, container) {
  super.render(attributes, container);
  this.upsert('key', Circle, { cx: 0, cy: 0, r: 20 }, container);  // Replace default shape
}
```

### Error: Animation uses CSS property (scale) instead of shape property

```javascript
// ❌ scale is a CSS transform, @antv/g shape animate() uses the shape's own property names
circle.animate(
  [{ scale: 1 }, { scale: 1.1 }, { scale: 1 }],  // Silently ignored, no effect
  { duration: 2000, iterations: Infinity }
);

// ✅ Use shape properties like r / fill / stroke when animating Circle shapes
circle.animate(
  [{ r: 20 }, { r: 25 }, { r: 20 }],
  { duration: 2000, iterations: Infinity }
);
```

### Error: Direct Access to `attributes.sourcePoint` in Custom Edge → White Screen

```javascript
// ❌ `sourcePoint` / `targetPoint` properties do not exist in `attributes`
// Direct access returns `undefined`, and destructuring assignment throws an exception, causing a white screen
class MyEdge extends BaseEdge {
  getKeyPath(attributes) {
    const { sourcePoint, targetPoint } = attributes;  // undefined!
    const [sx, sy] = sourcePoint;  // TypeError: Cannot read properties of undefined
    return [['M', sx, sy], ['L', tx, ty]];
  }
}

// ✅ Use `this.getEndpoints(attributes)` to retrieve start and end points
class MyEdge extends BaseEdge {
  getKeyPath(attributes) {
    const [sourcePoint, targetPoint] = this.getEndpoints(attributes, false);
    const [sx, sy] = sourcePoint;
    const [tx, ty] = targetPoint;
    return [['M', sx, sy], ['L', tx, ty]];
  }
}
```