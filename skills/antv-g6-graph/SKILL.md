---
name: antv-g6-graph
description: G6 v5 graph visualization code generation skill, supporting initialization, layout, interaction, and plugin configuration for various graph types such as network graphs, tree graphs, and flowcharts
---

# G6 v5 Graph Visualization Code Generation Skills

## Core Constraints (Must Comply)

### Initialization Specifications
- `container` parameter is required, pass in a DOM element ID string or a DOM element object
- Use `new Graph({...})` constructor, **do not use** `new G6.Graph()` (v4 syntax)
- All configurations must be completed in the constructor at once, do not override them later with multiple configuration method calls
- `graph.render()` returns a Promise, rendering asynchronously; if you need to wait for completion, use `await graph.render()`

### Data Structure Specification
- Data format: `{ nodes: [...], edges: [...], combos?: [...] }`
- Each node must have a unique `id` (string); business data is stored in the `data` field
- Edges must have `source` and `target`, with values being node `id`s
- **Prohibited**: Using the v4 `graph.data()` method to pass data

### Node/Edge Style Specifications
- Styles are configured via `node.style` / `edge.style`, supporting both static values and callback functions
- Callback function signature: `(datum: NodeData | EdgeData) => value`
- Label text is set via `style.labelText` (**not** `label` or `labelCfg`)
- Node size is set via `style.size` (a single numeric value or a `[width, height]` array)

### Layout Specifications
- `layout` configuration is placed in Graph options: `{ type: 'force', ... }`
- `force` layout **does not support** `preventOverlap` / `nodeSize` (G6 v4 parameters, silently ignored in v5); for overlap prevention, use `d3-force` + `collide` instead
- Tree layouts (mindmap, compact-box, dendrogram, indented) require tree data or `treeToGraphData()` conversion
- Force-directed layout runs asynchronously and continues iterating after `graph.render()`

### Interaction Behavior Specifications
- `behaviors` is an array of strings or configuration objects
- Common behavior string abbreviations: `'drag-canvas'`, `'zoom-canvas'`, `'drag-element'`, `'click-select'`
- G6 v5 **removed the Mode concept**, all behaviors are configured directly in the array
- Complex configurations use object form: `{ type: 'click-select', multiple: true }`

### Plugin Specifications
- `plugins` is an array, similar to `behaviors`
- Shorthand: `'minimap'`, `'grid-line'`, `'tooltip'`
- Complex configuration: `{ type: 'tooltip', getContent: (e, items) => '...' }`

---

## Prohibited Error Patterns

### ❌ Using v4 API

```javascript
// Error: v4 chainable API
const graph = new G6.Graph({ ... });
graph.data(data);
graph.render();
graph.node((node) => ({ ... }));  // v4 callback

// Correct: v5 constructor
const graph = new Graph({
  container: 'container',
  data: { nodes: [...], edges: [...] },
  node: { style: { ... } },
});
graph.render();
```

### ❌ Incorrect Node Data Structure

```javascript
// Incorrect: Business attributes directly at the top level
{ id: 'node1', label: 'Node 1', value: 100 }

// Correct: Business attributes placed in the data field
{ id: 'node1', data: { label: 'Node 1', value: 100 } }
```

### ❌ Incorrect Label Configuration

```javascript
// Incorrect: v4 labelCfg
node: {
  labelCfg: { style: { fill: '#333' } }
}

// Correct: v5 style.labelText
node: {
  style: {
    labelText: (d) => d.data.label,
    labelFill: '#333',
    labelFontSize: 14,
  }
}
```

### ❌ behaviors Using the Mode Concept

```javascript
// Incorrect: v4 modes
modes: {
  default: ['drag-canvas', 'zoom-canvas'],
  edit: ['create-edge'],
}

// Correct: v5 directly uses behaviors array
behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
```

### ❌ Reading attributes.data in Custom Node render() → Blank Screen

```javascript
// Error: attributes is a computed style object, does not contain node data, accessing data.color throws TypeError
render(attributes, container) {
  const { data } = attributes;       // undefined
  const fill = data.color;           // TypeError → Blank Screen
}

// Correct: Map data fields to custom style properties via node.style callback
// ① Graph Configuration
node: {
  type: 'my-node',
  style: { color: (d) => d.data.color },
},
// ② Directly read from attributes in render()
render(attributes, container) {
  const { color = '#1783FF' } = attributes;  // ✅
}
```

### ❌ Using extend to Register Custom Nodes

```javascript
// Error: extend has been officially removed from G6 v5, and calling it after import will result in "extend is not a function"
import { Graph, extend } from '@antv/g6';
const extendedGraph = extend(Graph, {
  nodes: { 'my-node': MyNodeFn },
});

// Error: v4's group.addShape() API
const MyNode = (node) => (model) => {
  const group = node.group();
  group.addShape('circle', { attrs: { r: 20 } });
};

// Correct: BaseNode class + register()
import { BaseNode, Circle, ExtensionCategory, Graph, register } from '@antv/g6';
class MyNode extends BaseNode {
  render(attributes, container) {
    super.render(attributes, container);
    this.upsert('key', Circle, { cx: 0, cy: 0, r: 20, fill: '#1783FF' }, container);
  }
}
register(ExtensionCategory.NODE, 'my-node', MyNode);
const graph = new Graph({ node: { type: 'my-node' } });
```

### ❌ Missing container

```javascript
// Error: Missing container
const graph = new Graph({ width: 800, height: 600 });

// Correct: container is required, value should be a string ID or DOM element
const graph = new Graph({ container: 'container', width: 800, height: 600 });
// Or pass a DOM element
const graph = new Graph({ container: document.getElementById('container'), width: 800, height: 600 });
```

> Common variant error: `container: container` (using a string ID as a variable name, variable is undefined → ReferenceError → blank screen)

### ❌ autoFit: 'view' with Asynchronous Force-Directed Layout Causes Blank Screen

```javascript
// Error: Layouts like combo-combined / force / d3-force are asynchronous iterations
// autoFit executes before layout iteration starts, all nodes are stacked at the origin, bounding box is zero → abnormal scaling → blank screen
const graph = new Graph({
  autoFit: 'view',          // ❌ Cannot set this under asynchronous layout
  layout: { type: 'combo-combined' },
});
graph.render();

// Correct: Do not set autoFit, call fitView after the AFTER_LAYOUT event
import { Graph, GraphEvent } from '@antv/g6';
const graph = new Graph({
  layout: { type: 'combo-combined' },
});
graph.on(GraphEvent.AFTER_LAYOUT, () => graph.fitView({ padding: 20 }));
graph.render();
```

> Synchronous layouts (`dagre`, `grid`, `circular`, etc.) are not affected by this issue and can directly use `autoFit: 'view'`.

---

## Basic Structure Template

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  // 1. Container
  container: 'container',       // DOM id or HTMLElement
  width: 800,
  height: 600,
  autoFit: 'view',              // Optional: 'center' | 'view' | false

  // 2. Data
  data: {
    nodes: [
       { id: 'n1', data: { label: 'Node 1' } },
       { id: 'n2', data: { label: 'Node 2' } },
    ],
    edges: [
       { source: 'n1', target: 'n2' },
    ],
  },

  // 3. Node Style
  node: {
    type: 'circle',             // Node type
    style: {
      size: 40,
      fill: '#1783FF',
      stroke: '#fff',
      lineWidth: 2,
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
    },
  },

  // 4. Edge Style
  edge: {
    type: 'line',
    style: {
      stroke: '#aaa',
      lineWidth: 1,
      endArrow: true,
    },
  },

  // 5. Layout
  layout: {
    type: 'force',
    preventOverlap: true,
    nodeSize: 40,
  },

  // 6. Interactions
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],

  // 7. Plugins (Optional)
  plugins: ['grid-line'],

  // 8. Theme (Optional)
  theme: 'light',               // 'light' | 'dark'
});

graph.render();
```

---

## Chart Type Selection Guide

| Chart Type | Recommended Layout | Typical Scenarios |
|------------|----------|----------|
| Network/Relationship Graph | `force` / `fruchterman` | Social Networks, Knowledge Graphs |
| Hierarchical/Flow Chart | `dagre` / `antv-dagre` | Organizational Structures, Workflows |
| Tree Graph | `compact-box` / `mindmap` | File Trees, Mind Maps |
| Circular Graph | `circular` | Circular Dependencies, Circular Relationships |
| Grid Graph | `grid` | Chessboard Layouts, Matrix Relationships |
| Concentric Circles | `concentric` | Center-Radiating Relationships |
| Radial Layout | `radial` | Radiation Centered on a Specific Node |

---

## Built-in Node Types

| Type Name | Shape | Applicable Scenarios |
|--------|------|----------|
| `circle` | Circle | General nodes, network graphs |
| `rect` | Rectangle | Flowcharts, UML |
| `ellipse` | Ellipse | General, emphasizing vertical orientation |
| `diamond` | Diamond | Decision nodes |
| `hexagon` | Hexagon | Honeycomb layouts |
| `triangle` | Triangle | Special markers |
| `star` | Star | Special markers, ratings |
| `donut` | Donut | Nodes with progress |
| `image` | Image | Avatars, icon nodes |
| `html` | HTML | Rich text custom nodes |

---

## Built-in Edge Types

| Type Name | Shape | Applicable Scenarios |
|--------|------|----------|
| `line` | Straight Line | Simple Graphs, Topology Diagrams |
| `cubic` | Cubic Bezier Curve | General, Arc Effect |
| `cubic-horizontal` | Horizontal Cubic Curve | Horizontal Flowcharts |
| `cubic-vertical` | Vertical Cubic Curve | Vertical Flowcharts |
| `quadratic` | Quadratic Bezier Curve | Lightweight Arc Edge |
| `polyline` | Polyline | Orthogonal Layout |
| `loop` | Self-Loop | Node's Own Loop |

---

## Built-in Layout Algorithms

| Layout Name | Type | Features |
|-------------|------|----------|
| `force` | Force-directed | Physical simulation, natural distribution |
| `d3-force` | Force-directed | Based on D3, configurable force types |
| `fruchterman` | Force-directed | Fast, supports GPU acceleration |
| `force-atlas2` | Force-directed | Large-scale graphs, good clustering effect |
| `dagre` | Hierarchical | DAG, automatic layering |
| `antv-dagre` | Hierarchical | AntV optimized version of Dagre |
| `circular` | Circular | Nodes arranged in a circle |
| `concentric` | Concentric | Rings divided by attribute values |
| `grid` | Grid | Regular grid arrangement |
| `radial` | Radial | Radiates from a specific node |
| `mds` | Dimensionality Reduction | Preserves relative node distances |
| `random` | Random | For debugging |
| `compact-box` | Tree | Compact tree, space-saving |
| `mindmap` | Tree | Mind map style |
| `dendrogram` | Tree | Dendrogram |
| `indented` | Tree | Indented tree |

---

## Built-in Interaction Behaviors

| Behavior Name | Description |
|---------------|-------------|
| `drag-canvas` | Drag canvas |
| `zoom-canvas` | Zoom canvas with mouse wheel |
| `scroll-canvas` | Pan canvas with mouse wheel |
| `drag-element` | Drag node/edge/combo |
| `drag-element-force` | Drag node in force-directed graph |
| `click-select` | Click to select element |
| `brush-select` | Box select elements |
| `lasso-select` | Lasso select |
| `hover-activate` | Hover to activate element |
| `collapse-expand` | Collapse/expand node (tree graph) |
| `create-edge` | Interactively create edge |
| `focus-element` | Focus on element (zoom to specified element) |
| `fix-element-size` | Maintain element size during zoom |
| `auto-adapt-label` | Automatically show/hide labels (prevent overlap) |
| `optimize-viewport-transform` | Large-scale graph viewport optimization |

---

## Built-in Plugins

| Plugin Name | Description |
|-------------|-------------|
| `grid-line` | Grid background lines |
| `background` | Background color/image |
| `watermark` | Watermark |
| `minimap` | Mini-map navigation |
| `legend` | Legend |
| `tooltip` | Element tooltip |
| `toolbar` | Toolbar (zoom, undo, etc.) |
| `contextmenu` | Context menu |
| `history` | Undo/Redo |
| `timebar` | Timeline filter |
| `fisheye` | Fisheye magnification effect |
| `edge-bundling` | Edge bundling |
| `edge-filter-lens` | Edge filter lens |
| `hull` | Element contour hull |
| `bubble-sets` | Bubble sets |
| `snapline` | Alignment guide lines |
| `fullscreen` | Fullscreen |

---

## Element States (States)

G6 v5 comes with 5 built-in states: `selected`, `active`, `highlight`, `inactive`, `disabled`

```javascript
// Set styles for states in Graph configuration
node: {
  style: {
    fill: '#1783FF',
  },
  state: {
    selected: {
      fill: '#ff6b6b',
      stroke: '#ff4d4d',
      lineWidth: 3,
    },
    hover: {
      fill: '#40a9ff',
    },
  },
},

// Dynamically set states
graph.setElementState('node1', 'selected');
graph.setElementState('node1', ['selected', 'highlight']);
graph.setElementState('node1', []);  // Clear all states
```

---

## Theme System

```javascript
// Built-in Themes
const graph = new Graph({
  theme: 'light',   // Default
  // theme: 'dark',
});

// Dynamically Switch Themes
graph.setTheme('dark');
graph.render();
```

---

## Data Manipulation API

```javascript
// Add elements
graph.addNodeData([{ id: 'n3', data: { label: 'New Node' } }]);
graph.addEdgeData([{ source: 'n1', target: 'n3' }]);

// Update elements
graph.updateNodeData([{ id: 'n1', style: { fill: 'red' } }]);

// Remove elements
graph.removeNodeData(['n3']);

// Re-render after updating data
graph.draw();
```

---

## Common Usage Patterns

### Data-Driven Styles (Recommended)

```javascript
node: {
  style: {
    size: (d) => d.data.size || 30,
    fill: (d) => {
      const colorMap = { type1: '#1783FF', type2: '#FF6B6B', type3: '#52C41A' };
      return colorMap[d.data.type] || '#ccc';
    },
    labelText: (d) => d.data.name,
  },
},
```

### Palette Mapping

```javascript
node: {
  palette: {
    type: 'group',       // Map colors by category
    field: 'category',   // Category field in the data
    color: 'tableau10',  // Built-in palette name
  },
},
```

### Continuous Numerical Mapping of Node Size

```javascript
transforms: [
  {
    type: 'map-node-size',
    field: 'value',
    range: [16, 60],
  },
],
```

### Parallel Edge Processing

```javascript
transforms: [
  {
    type: 'process-parallel-edges',
    offset: 15,
  },
],
edge: {
  type: 'quadratic',
},
```

---

## Data Operation API Quick Reference

```javascript
// Add
graph.addNodeData([{ id: 'n3', data: { label: 'New Node' } }]);
graph.addEdgeData([{ source: 'n1', target: 'n3' }]);
graph.draw();

// Remove
graph.removeNodeData(['n3']);   // Associated edges are automatically deleted
graph.draw();

// Update
graph.updateNodeData([{ id: 'n1', data: { label: 'Updated' } }]);
graph.draw();

// Query
const node = graph.getNodeData('n1');
const selected = graph.getElementDataByState('node', 'selected');
const zoom = graph.getZoom();

// Viewport
await graph.fitView({ padding: 20 });
await graph.focusElement('n1', { duration: 500 });
await graph.zoomTo(1.5);

// State
graph.setElementState('n1', 'selected');
graph.setElementState('n1', []);          // Clear

// Destroy
graph.destroy();
```

---

## Event Listening Quick Reference

```javascript
// Element events (node/edge/combo + event type)
graph.on('node:click', (e) => console.log(e.target.id));
graph.on('edge:pointerover', (e) => graph.setElementState(e.target.id, 'active'));
graph.on('canvas:click', () => { /* Click on blank area */ });

// Lifecycle events
import { GraphEvent } from '@antv/g6';
graph.on(GraphEvent.AFTER_RENDER, () => console.log('Rendering complete'));
graph.on(GraphEvent.AFTER_LAYOUT, () => console.log('Layout complete'));
```

---

## Reference Document Index

### Core
- [`g6-core-graph-init`](references/core/g6-core-graph-init.md)：Complete configuration for Graph initialization
- [`g6-core-data-structure`](references/core/g6-core-data-structure.md)：Data structure specifications
- [`g6-core-graph-api`](references/core/g6-core-graph-api.md)：Graph instance API (CRUD, viewport, states)
- [`g6-core-events`](references/core/g6-core-events.md)：Event system (element events, canvas events, lifecycle)
- [`g6-core-custom-element`](references/core/g6-core-custom-element.md)：Custom nodes/edges (register + BaseNode/BaseEdge)
- [`g6-core-transforms-animation`](references/core/g6-core-transforms-animation.md)：Data transformations (map-node-size) and animation configurations

### Node Types
- [`g6-node-circle`](references/elements/nodes/g6-node-circle.md): Circle (General)
- [`g6-node-rect`](references/elements/nodes/g6-node-rect.md): Rectangle (Flowchart)
- [`g6-node-image`](references/elements/nodes/g6-node-image.md): Image Node
- [`g6-node-diamond-ellipse-hexagon`](references/elements/nodes/g6-node-diamond-ellipse-hexagon.md): Diamond/Ellipse/Hexagon
- [`g6-node-star-triangle-donut`](references/elements/nodes/g6-node-star-triangle-donut.md): Star/Triangle/Donut Progress
- [`g6-node-html`](references/elements/nodes/g6-node-html.md): HTML Rich Text Node
- [`g6-node-react`](references/elements/nodes/g6-node-react.md): React/Vue Custom Node (@antv/g6-extension-react)

### Combo
- [`g6-combo-overview`](references/elements/combos/g6-combo-overview.md)：Combo Grouping (circle/rect, collapse/expand)

### Edge Types
- [`g6-edge-line`](references/elements/edges/g6-edge-line.md)：Straight line edge
- [`g6-edge-cubic`](references/elements/edges/g6-edge-cubic.md)：Cubic Bézier curve edge
- [`g6-edge-cubic-directional`](references/elements/edges/g6-edge-cubic-directional.md)：Directed cubic curve (cubic-horizontal horizontal / cubic-vertical vertical)
- [`g6-edge-polyline`](references/elements/edges/g6-edge-polyline.md)：Polyline edge
- [`g6-edge-quadratic-loop`](references/elements/edges/g6-edge-quadratic-loop.md)：Quadratic curve and loop edge

### Layout
- [`g6-layout-force`](references/layouts/g6-layout-force.md)：Force-directed (force/d3-force)
- [`g6-layout-dagre`](references/layouts/g6-layout-dagre.md)：Hierarchical/Flowchart (dagre)
- [`g6-layout-circular`](references/layouts/g6-layout-circular.md)：Circular
- [`g6-layout-grid`](references/layouts/g6-layout-grid.md)：Grid
- [`g6-layout-mindmap`](references/layouts/g6-layout-mindmap.md)：Mind Map
- [`g6-layout-advanced`](references/layouts/g6-layout-advanced.md)：Concentric/Radial/MDS/Fruchterman
- [`g6-layout-combo-fishbone`](references/layouts/g6-layout-combo-fishbone.md)：Combo Layout (combo-combined) + Fishbone Layout (fishbone)

### Data Transformations
- [`g6-core-transforms-animation`](references/core/g6-core-transforms-animation.md): map-node-size and animation configuration
- [`g6-transform-parallel-edges-radial`](references/transforms/g6-transform-parallel-edges-radial.md): process-parallel-edges + place-radial-labels

### Interaction Behaviors
- [`g6-behavior-click-select`](references/behaviors/g6-behavior-click-select.md)：Click to Select
- [`g6-behavior-drag-element`](references/behaviors/g6-behavior-drag-element.md)：Drag Node
- [`g6-behavior-canvas-nav`](references/behaviors/g6-behavior-canvas-nav.md)：Canvas Drag + Zoom
- [`g6-behavior-hover-activate`](references/behaviors/g6-behavior-hover-activate.md)：Hover to Activate
- [`g6-behavior-lasso-collapse`](references/behaviors/g6-behavior-lasso-collapse.md)：Lasso Select + Collapse/Expand
- [`g6-behavior-create-edge-focus`](references/behaviors/g6-behavior-create-edge-focus.md)：Create Edge + Focus Element
- [`g6-behavior-advanced`](references/behaviors/g6-behavior-advanced.md)：fix-element-size / auto-adapt-label / drag-element-force

### Plugins
- [`g6-plugin-tooltip`](references/plugins/g6-plugin-tooltip.md)：Tooltip
- [`g6-plugin-minimap`](references/plugins/g6-plugin-minimap.md)：Minimap
- [`g6-plugin-contextmenu-toolbar`](references/plugins/g6-plugin-contextmenu-toolbar.md)：Context Menu + Toolbar
- [`g6-plugin-history-legend`](references/plugins/g6-plugin-history-legend.md)：Undo/Redo + Legend
- [`g6-plugin-fisheye-hull-watermark`](references/plugins/g6-plugin-fisheye-hull-watermark.md)：Fish Eye + Hull + Watermark
- [`g6-plugin-timebar-gridline`](references/plugins/g6-plugin-timebar-gridline.md)：Time Bar + Grid Line
- [`g6-plugin-background-snapline`](references/plugins/g6-plugin-background-snapline.md)：Background + Snapline
- [`g6-plugin-edge-bundling-bubble`](references/plugins/g6-plugin-edge-bundling-bubble.md)：Edge Bundling + Bubble Sets
- [`g6-plugin-fullscreen-title`](references/plugins/g6-plugin-fullscreen-title.md)：Fullscreen + Title

### State and Theme
- [`g6-state-overview`](references/states/g6-state-overview.md)：Element State System
- [`g6-theme-overview`](references/themes/g6-theme-overview.md)：Theme System

### Scene Templates
- [`g6-pattern-network-graph`](references/patterns/g6-pattern-network-graph.md)：Network Graph
- [`g6-pattern-tree-graph`](references/patterns/g6-pattern-tree-graph.md)：Tree Graph/Organizational Structure
- [`g6-pattern-flow-chart`](references/patterns/g6-pattern-flow-chart.md)：Flow Chart