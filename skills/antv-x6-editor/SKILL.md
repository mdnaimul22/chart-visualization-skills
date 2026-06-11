---
name: antv-x6-editor
description: X6 graph editor engine code generation capability, supporting node/edge/port/interaction/plugin configuration for graph editing scenarios such as flowcharts, DAGs, ER diagrams, and lineage graphs
version: 3.x
---

# X6 Graph Editing Engine Code Generation Skills

## Core Constraints (Must Comply)

<!-- CONSTRAINTS:START -->

### X6 3.x Key Constraints (Mandatory)

- **`graph.render()` does not exist**: In X6 3.x, `new Graph()` / `addNode` / `addEdge` / `fromJSON` automatically render, and `graph.render()` must not appear in the code.
- **Do not declare `container` variable**: The runtime environment injects `container` as a function parameter. Graph initialization should only use the string literal `container: 'container'`. Prohibited: `const/let/var container = ...` and `document.getElementById('container')`.
- **Plugins must be registered with `graph.use(new Plugin(...))` before using their methods**: `graph.toPNG / toSVG / toJPEG` depend on `Export`; `graph.select / unselect` depend on `Selection`; `graph.undo / redo` depend on `History`; `graph.copy / paste / cut` depend on `Clipboard`; `graph.bindKey` depends on `Keyboard`. Methods do not exist if the corresponding plugin is not registered.
- **Custom shapes must be registered before use**: `Graph.registerNode(name, def)` / `Graph.registerEdge(name, def)` / `Shape.HTML.register({ shape, ... })` must be completed before the first `addNode / addEdge`.
- **`@antv/x6` exports only 11 plugin classes**: `Clipboard`, `Dnd`, `Export`, `History`, `Keyboard`, `MiniMap`, `Scroller`, `Selection`, `Snapline`, `Stencil`, `Transform`. `mousewheel`, `embedding`, `panning`, `connecting`, `translating`, `interacting`, `background`, `grid` are **constructor options** for `new Graph()`, not plugins. **Do not** import classes with the same name or use `graph.use(new XxxClass())`. Example: Wheel zoom is configured in the Graph constructor as `mousewheel: { enabled: true, zoomAtMousePosition: true, modifiers: ['ctrl'] }`.
- **Node/edge animations use `cell.animate(keyframes, options)` (Web Animations API style)**: X6 3.x **does not have the `node.transition(path, target, options)` method**. In the source code, `transition` exists only as an **options field** (`boolean | KeyframeEffectOptions`) in `node.translate(tx, ty, { transition })` / `node.rotate(deg, { transition })`, not as an independent method. Example:
  ```javascript
  // General animation
  node.animate(
    { fill: ['#fff', '#1890ff'], transform: ['scale(1)', 'scale(1.2)'] },
    { duration: 500, iterations: 1, fill: 'forwards' },
  );
  // Translation transition only
  node.translate(120, 0, { transition: { duration: 500, easing: 'ease-in-out' } });
  ```
  Multi-step attribute changes can be wrapped with `graph.startBatch('animate'); cell.attr(...); graph.stopBatch('animate');`.

### Initialization Standards
- The `container` parameter is **required** and **must be a string**, e.g., `container: 'container'`. The runtime environment will automatically parse it into a DOM element.
- **Background color must be set**: `background: { color: '#F2F7FA' }`. All canvases require a uniform light blue-gray background.
- **Do not add `grid` configuration** unless the user explicitly requests grid display.
- **Do not set `width` / `height`** unless the user explicitly specifies canvas dimensions. The canvas defaults to adaptive container sizing.
- Import method: `import { Graph } from '@antv/x6'`. **Import only the classes actually used**.
- **Prohibited**: Unconditional import of `Shape`. Import `Shape` only when using static methods like `Shape.HTML.register()`.
- Plugins are imported directly from `'@antv/x6'`, e.g., `import { Graph, Selection, History } from '@antv/x6'`.
- **Prohibited**: Using `@antv/x6-plugin-xxx` standalone packages (deprecated).
- Standard initialization template:
  ```javascript
  import { Graph } from '@antv/x6';
  const graph = new Graph({
    container: 'container',
    background: { color: '#F2F7FA' },
  });
  ```

### Node Operation Specifications
- **Prefer using `graph.addNode()`** to add nodes one by one, rather than `graph.fromJSON()` for batch import (unless the user explicitly requests batch data loading)
- Built-in shapes: `'rect'`, `'circle'`, `'ellipse'`, `'polygon'`, `'polyline'`, `'path'`, `'text'`, `'text-block'`, `'image'`, `'html'`
- Node styles are configured through `attrs`, following SVG attribute naming conventions
- Node position is set via `x`, `y` (top-left coordinates), and size is set via `width`, `height`
- **Default node style** (unless the user specifies another style, all nodes uniformly use this default style):
  ```javascript
  attrs: {
    body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 },
  }
  ```
- **Prohibited** to use CSS property names (e.g., `background-color`) in `attrs`; must use SVG attributes (e.g., `fill`)

### Edge Operation Specifications
- Use `graph.addEdge({ source, target, ... })` to add an edge
- `source`/`target` can be: node instance, node ID string, `{ cell: node, port: 'portId' }` object, or coordinates `{ x, y }`
- Edge style: `attrs: { line: { stroke, strokeWidth, strokeDasharray, targetMarker, sourceMarker } }`
- **Default edge style** (unless the user specifies another style): `attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1 } }`
- Arrows: `targetMarker: 'classic'` (classic arrow), `'block'`, `'circle'`, `'diamond'`
- Routers: `router: 'orth'` (orthogonal), `'manhattan'`, `'metro'`, `'er'`
- Connectors: `connector: 'rounded'` (rounded), `'smooth'` (Bezier curve), `'jumpover'`

### Ports Specification
- Ports are defined in the `ports` field of the node configuration
- Port group: `ports: { groups: { groupName: { position, attrs, ... } }, items: [{ id, group }] }`
- `position` values: `'top'`, `'bottom'`, `'left'`, `'right'`
- Ports serve as anchor points for edges. Setting `attrs: { circle: { magnet: true } }` allows edges to be dragged from the port
- **Must set `magnet: true`** to enable initiating or receiving edges from the port

### Interaction Configuration Specifications
- Line connection interaction is set in the Graph configuration via the `connecting` field
- `connecting: { allowBlank: false, router: 'orth', connector: 'rounded', createEdge() {...} }`
- Node movement restriction: `translating: { restrict: true }` or pass a function to restrict the area
- Embedding: `embedding: { enabled: true }` allows nodes to be dragged into groups

### Plugin Usage Specifications
- Plugins are imported from `@antv/x6` and registered via `graph.use(new Plugin(options))`
- Available plugins: `Selection`, `Snapline`, `History`, `Clipboard`, `Keyboard`, `Scroller`, `MiniMap`, `Transform`, `Export`, `Stencil`, `Dnd`
- Selection: `graph.use(new Selection({ enabled: true, rubberband: true }))`
- Snapline: `graph.use(new Snapline({ enabled: true }))`
- History: `graph.use(new History({ enabled: true }))`
- Clipboard: `graph.use(new Clipboard({ enabled: true }))`
- Keyboard: `graph.use(new Keyboard({ enabled: true }))`
- Scroller: `graph.use(new Scroller({ enabled: true }))`
- MiniMap: `graph.use(new MiniMap({ enabled: true, container: minimapContainer }))`
- Transform: `graph.use(new Transform({ resizing: { enabled: true }, rotating: { enabled: true } }))`
- Export: `graph.use(new Export())` (After registration, `graph.toPNG()` / `graph.toSVG()` can be called)
- Dynamic control: `graph.enablePlugins('selection')` / `graph.disablePlugins('selection')`
- **Do not** directly pass options like `selecting`, `snapline` in the Graph constructor (not supported in 3.x)

### Serialization Specification
- Export: `const data = graph.toJSON()` returns `{ cells: [...] }` object
- Import: `graph.fromJSON(data)` loads the entire graph data
- Clear: `graph.clearCells()` clears all elements
- **Prohibited** manual construction of internal fields in the cells array (e.g., `zIndex`, `parent`), should be operated through API

### Event Specifications
- Node events: `graph.on('node:click', ({ node, e }) => {...})`
- Edge events: `graph.on('edge:click', ({ edge, e }) => {...})`
- Canvas events: `graph.on('blank:click', ({ e }) => {...})`
- Change events: `graph.on('node:moved', ({ node }) => {...})`
- **Event callback parameters are objects**, not positional arguments: `({ node, e })` instead of `(node, e)`

### Import Standards
- **All used classes must appear in the import statement**: For example, if using `Selection`, it must be `import { Graph, Selection } from '@antv/x6'`.
- **Prohibited** use of namespace notation such as `Graph.Selection`, `Graph.Keyboard`, etc. (does not exist).
- **Prohibited** use of unimported classes: `new Selection(...)` must correspond to `import { Selection } from '@antv/x6'`.
- **Import self-check checklist (mandatory, must be verified line by line before outputting code)**: For **every** `new XxxYyy(...)` call in the code, `XxxYyy` must **literally appear** within the curly braces of the first line `import { ..., XxxYyy } from '@antv/x6'`. Common omissions: `Selection`, `Keyboard`, `History`, `Clipboard`, `Snapline`, `MiniMap`, `Transform`, `Scroller`, `Export`, `Stencil`, `Dnd`, `Shape` (when using `Shape.HTML.register`).
- **Why import omissions result in runtime errors like `Illegal constructor`**: The evaluation/Playground environment uses **UMD build** (`window.X6`) to execute the code, not actual ES Modules. Classes like `Selection`, `Keyboard`, etc., are **destructured from `window.X6` based on the import list**; if an import is omitted, the identifier `Selection` will **fall back to `window.Selection`** (the browser's native Selection interface), and `new Selection({...})` will throw `Failed to construct 'Selection': Illegal constructor`. The same applies to `Keyboard` / `History`, etc. (will result in `is not a constructor`).
- **Standard fix for import omissions**: Combine all used plugin classes into a single line `import { Graph, Selection, Keyboard, History, ... } from '@antv/x6';`, without splitting into multiple lines or omitting any.

### Node Tools (Tools) Specification
- Add tools: `node.addTools([{ name: 'button-remove', args: { x: 0, y: 0 } }])` or `graph.addTools(node, [...])`
- Remove tools: `node.removeTools()` or `graph.removeTools(node)`
- Check tools: `node.hasTools()`
- **Do not use** `node.hideTools()` / `node.showTools()` (these APIs do not exist in 3.x)
- Correct way to show/hide tools on hover:
  ```javascript
  graph.on('node:mouseenter', ({ node }) => {
    node.addTools([{ name: 'button-remove', args: { x: 0, y: 0 } }]);
  });
  graph.on('node:mouseleave', ({ node }) => {
    node.removeTools();
  });
  ```

### Gradient Color Specifications
- X6 `attrs` supports gradient object syntax in `fill`, **prohibiting** direct manipulation of `graph.defs` or `document.createElementNS` to create SVG gradients
- Correct syntax for linear gradient:
  ```javascript
  attrs: {
    body: {
      fill: {
        type: 'linearGradient',
        stops: [
          { offset: '0%', color: '#0000ff' },
          { offset: '100%', color: '#00ff00' },
        ],
      },
    },
  }
  ```

### Code Output Standards
- **Must output pure JavaScript**, TypeScript syntax is prohibited (e.g., `private`, type annotations `: string`, `as` type assertions)
- For HTML custom nodes, use `Shape.HTML.register({ shape, html, effect })` to register custom shapes, **do not** use `class extends Node`
- **Do not** use `Graph.registerHTMLComponent(name, factory)` —— This is an old X6 2.x API, and the 3.x source code no longer contains this method. All HTML nodes must be registered uniformly through `Shape.HTML.register` (see `references/core/x6-core-html-shape.md` for details)
- The `effect` array specifies which property changes trigger re-rendering (e.g., `['data']`); **do not add effect for purely static display nodes**
- Correct usage of HTML nodes:
  ```javascript
  import { Graph, Shape } from '@antv/x6';
  Shape.HTML.register({
    shape: 'my-html',
    effect: ['data'],
    html(node) {
      const div = document.createElement('div');
      div.style.width = '100%';
      div.style.height = '100%';
      div.innerHTML = node.getData().content || '';
      return div;
    },
  });
  const graph = new Graph({ container: 'container' });
  graph.addNode({ shape: 'my-html', x: 100, y: 100, width: 200, height: 80, data: { content: '<div>Hello</div>' } });
  ```

### Stencil Plugin Specification
- Stencil is registered via `graph.use(new Stencil({ target: graph, groups: [...] }))`
- After registration, the instance is obtained through `graph.getPlugin('stencil')`, and `stencil.container` is mounted to the DOM
- Node templates within Stencil are created using `graph.createNode(...)` (not `graph.addNode`), and then loaded via `stencil.load(nodes, groupName)`

### Dynamic Port Specification
- When dynamically adding ports using `node.addPort()`, **you must predefine the corresponding `ports.groups` during node initialization**.
- If the group is not predefined, the port cannot be positioned correctly, which may lead to rendering anomalies.
- Correct usage:
  ```javascript
  const node = graph.addNode({
    ...,
    ports: {
      groups: {
        in: { position: 'left', attrs: { circle: { r: 4, magnet: true, stroke: '#8f8f8f', fill: '#fff' } } },
        out: { position: 'right', attrs: { circle: { r: 4, magnet: true, stroke: '#8f8f8f', fill: '#fff' } } },
      },
    },
  });
  node.addPort({ id: 'port1', group: 'out' });
  ```

- **`registerNode` + `addNode` Ports Merging Pitfall (Strong Constraint)**: After `Graph.registerNode(name, { ports: { items: [{ id: 'in1', group: 'in' }] } })`, if you then call `graph.addNode({ shape: name, ports: { items: [{ id: 'in1', group: 'in' }] } })`, the internal X6 `Cell` constructor's `ObjectExt.merge(defaults, metadata)` will merge by array index, and `node.addPorts` will simply concatenate using `[...current, ...new]`, **without deduplication**. This will throw `Error: Duplicitied port id.` at runtime. Correct approaches (choose one):
  - Declare only `ports.groups` in `registerNode`, leaving `ports.items` for `addNode` or subsequent `node.addPort` calls.
  - Fully declare `ports.items` in `registerNode`, and **do not pass `ports.items` in `addNode`** (if additional ports are needed, call `node.addPort({ id: 'newId', group: 'xxx' })`, ensuring the new id does not conflict with those already declared in the registry).

### DOM/CSS Operation Specifications (HTML Nodes / Stencil / Custom Tools)
- When setting styles for DOM in the `html(node)` callback of an HTML node, **do not** directly write hyphenated properties: `el.style.box-sizing = '...'` or `el.style.font-size = '...'` will be parsed by JS as `el.style.box - sizing = ...`, throwing an `Invalid left-hand side in assignment` error. Choose one of the correct methods:
  - Camel case: `el.style.boxSizing = 'border-box'`, `el.style.fontSize = '14px'`, `el.style.backgroundColor = '#fff'`;
  - Square brackets: `el.style['box-sizing'] = 'border-box'`, `el.style['font-size'] = '14px'`;
  - For multiple styles, prioritize using `el.style.cssText = 'box-sizing:border-box;font-size:14px;'` or `Object.assign(el.style, { boxSizing: 'border-box', fontSize: '14px' })`.
- Similarly, `el.classList.add('...')` / `el.setAttribute('data-x', '...')` are valid APIs; **do not** use `el.class = '...'` / `el['class-name'] = ...`.

### Non-existent APIs (Prohibited)
- **Prohibited** `graph.scrollToCell()` → Correct approach: `graph.centerCell(cell)` to scroll and center on the specified cell
- **Prohibited** `graph.highlightCell()` / `graph.highlightNode()` → Correct approach: Use `node.attr('body/stroke', '#f00')` or add a CSS class to achieve highlighting
- **Prohibited** `Shape.Cylinder` / `Shape.Diamond` and other non-existent built-in Shapes → Use `'rect'` + `rx/ry` or `'polygon'` for customization
- **Prohibited** `Shape.Edge.define()` / `Shape.Node.define()` → Correct approach: `Graph.registerEdge()` / `Graph.registerNode()`
- **Prohibited** `Shape.Group` / `Shape.Group.define()` / `new Shape.Group()` → The `Shape` namespace in X6 3.x **does not** export `Group` (only `Circle / Edge / Ellipse / HTML / Image / Path / Polygon / Polyline / Rect / TextBlock` are available, runtime error: `Cannot read properties of undefined (reading 'define')`). Correct approach for parent-child grouping: Directly create a regular node as the parent using `graph.addNode({ shape: 'rect', ... })`, then establish the parent-child relationship via `parent.addChild(child)` / `parent.embed(child)`; or register a custom group shape using `Graph.registerNode('my-group', { inherit: 'rect', markup: [...], attrs: {...} })` and then `addNode({ shape: 'my-group' })`.
- **Prohibited** Importing `Embedding` as a plugin / `new Embedding(...)` / `graph.use(new Embedding(...))` → X6 3.x **does not** have an `Embedding` plugin class (runtime error: `Embedding is not a constructor`). Node embedding is a **Graph constructor option**: `new Graph({ container, embedding: { enabled: true, findParent: 'bbox', frontOnly: false, validate: ({ child, parent }) => true } })`. Hover highlighting is configured via `highlighting.embedding`, and embedding/unembedding events are `node:embedding` / `node:embedded`.
- **Prohibited** `history.batch()` → Correct approach: `graph.startBatch('custom'); ...; graph.stopBatch('custom');` or `graph.batchUpdate(() => { ... })`
- **Prohibited** `graph.defs` / `graph.svgDoc` / `document.createElementNS('...', 'linearGradient' | 'defs' | 'marker')` → X6 3.x does not expose `graph.defs` / `graph.svgDoc`, runtime error: `Cannot read properties of undefined`. Correct approach:
  - Node/edge regular `fill` gradient: Directly use gradient object syntax in attrs (`fill: { type: 'linearGradient', stops: [...] }`)
  - Custom marker requiring gradient fill: First define the gradient using `const id = graph.defineGradient({ type: 'linearGradient', stops: [{ offset: 0, color: '#f00' }, { offset: 1, color: '#0f0' }] })`, then in the marker object write `fill: \`url(#${id})\``
  - Custom markers/filters similarly use `graph.defineMarker(options)` / `graph.defineFilter(options)`

### Rendering Output Specifications (Must Comply)
- **After canvas initialization, there must be at least one `graph.addNode` / `graph.addEdge` / `graph.fromJSON` call**, ensuring the canvas has visible content. Even if the user query only describes interaction configurations (panning / mousewheel / plugins, etc.), you must manually add 2~3 example nodes + 1 edge as the rendering carrier; otherwise, visual validation will be judged as a "white screen".
- **After all nodes/edges are added, `graph.centerContent()` must be called at the end** (or use `graph.zoomToFit({ padding: 20, maxScale: 1 })` when the canvas needs to scale with content). X6 does not center content automatically by default; omitting this call will cause content to be positioned in the top-left corner, resulting in visual scoring failure. Choose one of the two methods; they cannot be called simultaneously.
- When multiple interactions (`panning` + `mousewheel` + `Selection` rubberband) are enabled simultaneously, **use `modifiers` to stagger trigger conditions** (e.g., panning uses `'shift'`, mousewheel uses `'ctrl'`, and rubberband remains empty). **Do not** place `'mouseWheel'` in `panning.eventTypes` while also enabling `mousewheel`, as both will compete for the wheel event.

<!-- CONSTRAINTS:END -->

---

## Prohibited Error Patterns

### ❌ Using Deprecated Standalone Plugin Packages

```javascript
// Wrong: Standalone plugin packages are deprecated
import { Selection } from '@antv/x6-plugin-selection';
import { History } from '@antv/x6-plugin-history';

// Correct: Import directly from @antv/x6
import { Graph, Selection, History } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Selection({ enabled: true, rubberband: true }));
graph.use(new History({ enabled: true }));
```

### ❌ Passing Plugin Options in the Constructor

```javascript
// Error: 3.x does not support constructor options pattern
const graph = new Graph({
  container: 'container',
  selecting: { enabled: true },  // ❌
  snapline: { enabled: true },   // ❌
  history: { enabled: true },    // ❌
});

// Correct: Use graph.use() to register plugins
import { Graph, Selection, Snapline, History } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Selection({ enabled: true }));
graph.use(new Snapline({ enabled: true }));
graph.use(new History({ enabled: true }));
```

### ❌ Confusing CSS Properties with SVG Attributes

```javascript
// Incorrect: Using CSS property names
attrs: {
  body: {
    'background-color': '#fff',  // ❌
    'border-radius': '6px',      // ❌
  }
}

// Correct: Using SVG attribute names
attrs: {
  body: {
    fill: '#fff',               // ✅ Background color
    rx: 6,                      // ✅ Border radius (x-axis)
    ry: 6,                      // ✅ Border radius (y-axis)
    stroke: '#8f8f8f',          // ✅ Border color
    strokeWidth: 1,             // ✅ Border width
  }
}
```

### ❌ Missing container

```javascript
// Error: Missing container
const graph = new Graph({});

// Correct: container is required
const graph = new Graph({ container: 'container' });
```

### ❌ Magnet Not Set for Connection Port

```javascript
// Error: Port cannot be connected
ports: {
  items: [{ id: 'port1', group: 'out' }],
  groups: {
    out: { position: 'right', attrs: { circle: { r: 5 } } }
  }
}

// Correct: Set magnet: true
ports: {
  items: [{ id: 'port1', group: 'out' }],
  groups: {
    out: { position: 'right', attrs: { circle: { r: 5, magnet: true, stroke: '#8f8f8f' } } }
  }
}
```

### ❌ Event Callback Using Positional Parameters

```javascript
// Incorrect: Parameters are not passed positionally
graph.on('node:click', (node, e) => { ... });

// Correct: Destructure object parameters
graph.on('node:click', ({ node, e }) => { ... });
```

---

## Basic Structure Template

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
});

const source = graph.addNode({
  shape: 'rect',
  x: 40,
  y: 40,
  width: 100,
  height: 40,
  label: 'Source',
  attrs: {
    body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 },
  },
});

const target = graph.addNode({
  shape: 'rect',
  x: 300,
  y: 200,
  width: 100,
  height: 40,
  label: 'Target',
  attrs: {
    body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 },
  },
});

graph.addEdge({
  source,
  target,
  attrs: {
    line: { stroke: '#8f8f8f', strokeWidth: 1 },
  },
});

// Center content: Call after all nodes/edges are added to center the canvas content relative to the container
// To zoom to fit the container, use graph.zoomToFit({ padding: 20, maxScale: 1 }) instead
graph.centerContent();
```

---

## Scenario Selection Guide

| Scenario | Recommended Configuration | Key Features |
|------|----------|----------|
| DAG Data Pipeline | ports + orth router + connecting | Directed Acyclic Graph, Port Connections |
| ER Entity Relationship Diagram | HTML nodes + er router | Tabular Nodes, Field Display |
| Flowchart/Approval Flow | Diamond Decision Nodes + Branching Edges | Conditional Branching, Multiple Paths |
| Organizational Chart | orth router + Tree Layout | Hierarchical Relationships, Collapse |
| Lineage Analysis | Left-Right Layout + Smooth Connector | Multi-Layer Flow, Ports |
| Network Topology | Circular Nodes + Star Structure | Device Types, Connection Status |
| State Machine | Circular Nodes + Edge Labels | State Transitions, Event Triggers |

---

## Built-in Node Types

| shape | Shape | Applicable Scenarios |
|-------|------|----------|
| `rect` | Rectangle | General nodes, process steps |
| `circle` | Circle | State nodes, endpoints |
| `ellipse` | Ellipse | General emphasis |
| `polygon` | Polygon | Rhombus (decision), hexagon |
| `text` | Plain text | Label, annotation |
| `image` | Image | Icon node |
| `html` | HTML | Rich text, tabular nodes |

---

## Router and Connector

### Router — Determines the Path of Edges
| Type | Effect | Applicable Scenarios |
|------|------|----------|
| `normal` | Straight line (default) | Simple graphs |
| `orth` | Orthogonal polyline | Flowcharts, DAGs |
| `manhattan` | Smart orthogonal (obstacle avoidance) | Complex layouts |
| `metro` | Metro line style | Metro maps |
| `er` | ER diagram specific | Entity-relationship diagrams |

### Connector — Determines the Edge Line Style
| Type | Effect | Applicable Scenarios |
|------|------|----------|
| `normal` | Straight line segment (default) | Simple graphs |
| `rounded` | Rounded corner polyline | Flowcharts (recommended) |
| `smooth` | Bézier curve | Lineage graphs, relationship graphs |
| `jumpover` | Line jumping | Complex crossings |

---

## Plugin Quick Reference

| Plugin | Registration Method | Functionality |
|------|----------|------|
| Selection | `graph.use(new Selection({ enabled: true, rubberband: true }))` | Box select nodes |
| Snapline | `graph.use(new Snapline({ enabled: true }))` | Alignment guides |
| History | `graph.use(new History({ enabled: true }))` | Undo/Redo |
| Clipboard | `graph.use(new Clipboard({ enabled: true }))` | Copy/Paste |
| Keyboard | `graph.use(new Keyboard({ enabled: true }))` | Keyboard shortcut binding |
| Scroller | `graph.use(new Scroller({ enabled: true }))` | Canvas scrolling |
| MiniMap | `graph.use(new MiniMap({ enabled: true, container }))` | Mini-map navigation |
| Transform | `graph.use(new Transform({ resizing: { enabled: true }, rotating: { enabled: true } }))` | Node scaling/rotation |
| Export | `graph.use(new Export())` | Export PNG/SVG |
| Stencil | `graph.use(new Stencil({ target: graph, groups: [...] }))` | Sidebar drag panel |
| Dnd | `graph.use(new Dnd({ target: graph }))` | Drag to create nodes |