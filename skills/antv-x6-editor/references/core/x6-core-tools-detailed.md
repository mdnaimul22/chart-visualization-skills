---
id: "x6-core-tools-detailed"
title: "Detailed Guide to X6 Built-in Tools"
description: |
  X6 3.x provides various built-in tools that can be attached to nodes or edges to enable interactive functionality.
  These include button, button-remove, editor, boundary, vertices, segments, arrowhead, and anchor tools.

library: "x6"
version: "3.x"
category: "core"
subcategory: "tools"
tags:
  - "tools"
  - "工具"
  - "button"
  - "button-remove"
  - "editor"
  - "boundary"
  - "vertices"
  - "segments"
  - "arrowhead"
  - "anchor"
  - "交互"

related:
  - "x6-intermediate-tools"
  - "x6-core-events"

use_cases:
  - "Add a delete button to a node"
  - "Double-click to edit node/edge text"
  - "Drag intermediate vertices of an edge"
  - "Drag edge segments"
  - "Display node bounding box"
  - "Drag arrowhead to change connection"
  - "Drag anchor to adjust connection position"

difficulty: "intermediate"
completeness: "full"
---

## Complete List of Built-in Tools

### Node Tools

| Tool Name | Description | Typical Use Case |
|-----------|-------------|-------------|
| `button` | Custom button | Add operation buttons to nodes |
| `button-remove` | Delete button | Click to delete a node |
| `boundary` | Boundary box | Display a dashed boundary around a node |
| `editor` | Text editor | Double-click to edit node label text |

### Edge Tools

| Tool Name | Description | Typical Use Case |
|----------|------|---------|
| `button` | Custom button | Add operation buttons on edges |
| `button-remove` | Remove button | Click to delete an edge |
| `boundary` | Boundary box | Display the bounding box of an edge |
| `vertices` | Vertex tool | Drag to add/move/delete edge vertices |
| `segments` | Segment tool | Drag orthogonal segments of an edge |
| `arrowhead` | Arrowhead tool | Drag start/end arrowheads to change connections |
| `anchor` | Anchor tool | Drag to adjust anchor positions on nodes |
| `editor` | Text editor | Double-click to edit edge label text |

---

## Button Tool

Displays a clickable button on a node or edge.

### Configuration Options

| Property | Type | Description |
|------|------|------|
| `x` | `number \| string` | Button X position (supports percentage, e.g., `'100%'`) |
| `y` | `number \| string` | Button Y position |
| `offset` | `{ x, y }` | Offset value |
| `rotate` | `boolean` | Whether to rotate with the node |
| `useCellGeometry` | `boolean` | Whether to position based on node geometry |
| `markup` | `Markup[]` | Custom button SVG structure |
| `onClick` | `function` | Click callback |

### Example: Custom Button

```javascript
node.addTools([
  {
    name: 'button',
    args: {
      x: '100%',
      y: 0,
      offset: { x: -10, y: 10 },
      markup: [
        {
          tagName: 'circle',
          selector: 'button',
          attrs: {
            r: 8,
            stroke: '#fe854f',
            'stroke-width': 2,
            fill: 'white',
            cursor: 'pointer',
          },
        },
        {
          tagName: 'text',
          textContent: '+',
          selector: 'icon',
          attrs: {
            fill: '#fe854f',
            'font-size': 12,
            'text-anchor': 'middle',
            'pointer-events': 'none',
            y: '0.3em',
          },
        },
      ],
      onClick({ cell }) {
        console.log('Button clicked on', cell.id);
      },
    },
  },
]);
```

---

## Button-Remove Tool

A predefined delete button that removes the node or edge it is located on when clicked.

### Configuration Options

Inherits all configuration options from Button, with a default red X icon.

| Property | Type | Default Value | Description |
|------|------|--------|------|
| `x` | `number` | `0` | X position |
| `y` | `number` | `0` | Y position |
| `offset` | `{ x, y }` | - | Offset |

### Example

```javascript
// Display delete button when hovering over a node
graph.on('node:mouseenter', ({ node }) => {
  node.addTools([
    {
      name: 'button-remove',
      args: { x: 0, y: 0, offset: { x: 4, y: 4 } },
    },
  ]);
});

graph.on('node:mouseleave', ({ node }) => {
  node.removeTools();
});
```

---

## Editor Tool (Text Editing)

Double-click on a node or edge label to pop up an in-place editor for modifying the text.

### Configuration Options

| Property | Type | Default Value | Description |
|----------|------|---------------|-------------|
| `attrs.fontSize` | `number` | `14` | Editor font size |
| `attrs.fontFamily` | `string` | `'Arial'` | Font family |
| `attrs.color` | `string` | `'#000'` | Text color |
| `attrs.backgroundColor` | `string` | `'#fff'` | Editor background color |
| `getText` | `function` | - | Function to get the current text |
| `setText` | `function` | - | Function to set new text |

### Example: Node Text Editing

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({ container: 'container' });

const node = graph.addNode({
  shape: 'rect',
  x: 100,
  y: 100,
  width: 120,
  height: 50,
  label: 'Double-click to edit',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', rx: 6, ry: 6 } },
});

// Add editor tool
node.addTools([
  {
    name: 'editor',
    args: {
      attrs: {
        fontSize: 14,
        color: '#333',
        backgroundColor: '#fafafa',
      },
      getText({ cell }) {
        return cell.attr('label/text') || '';
      },
      setText({ cell, value }) {
        cell.attr('label/text', value);
      },
    },
  },
]);
```

### Example: Edge Label Editing

```javascript
edge.addTools([
  {
    name: 'editor',
    args: {
      getText({ cell }) {
        return cell.getLabelAt(0)?.attrs?.label?.text || '';
      },
      setText({ cell, value }) {
        cell.setLabelAt(0, { attrs: { label: { text: value } } });
      },
    },
  },
]);
```

---

## Boundary Tool

Displays a dashed bounding box for nodes or edges.

### Configuration Options

| Property | Type | Default Value | Description |
|------|------|--------|------|
| `padding` | `number \| SideOptions` | `10` | Inner padding from the border to the node |
| `rotate` | `boolean` | - | Whether to rotate with the node |
| `useCellGeometry` | `boolean` | `true` | Based on node geometry calculation |
| `attrs` | `object` | Dashed rectangle | Boundary box style |

### Example

```javascript
node.addTools([
  {
    name: 'boundary',
    args: {
      padding: 8,
      attrs: {
        fill: 'none',
        stroke: '#1890ff',
        'stroke-width': 1,
        'stroke-dasharray': '4, 4',
      },
    },
  },
]);
```

---

## Vertices Tool (Edge Vertices)

Display draggable vertex control points on the edge, allowing you to add, move, or delete vertices to adjust the edge's path.

### Configuration Options

| Property | Type | Default Value | Description |
|------|------|--------|------|
| `snapRadius` | `number` | `20` | Snap radius |
| `addable` | `boolean` | `true` | Whether to allow adding vertices by clicking on edges |
| `removable` | `boolean` | `true` | Whether to allow removing vertices |
| `removeRedundancies` | `boolean` | `true` | Automatically remove collinear vertices |
| `stopPropagation` | `boolean` | `true` | Prevent event bubbling |
| `attrs` | `object` | Circular control point | Vertex style |
| `modifiers` | `ModifierKey` | - | Modifier key required when adding vertices |

### Example

```javascript
graph.on('edge:mouseenter', ({ edge }) => {
  edge.addTools([
    {
      name: 'vertices',
      args: {
        snapRadius: 15,
        attrs: {
          r: 5,
          fill: '#fff',
          stroke: '#1890ff',
          'stroke-width': 2,
          cursor: 'move',
        },
      },
    },
  ]);
});

graph.on('edge:mouseleave', ({ edge }) => {
  edge.removeTools();
});
```

### Interaction Methods

- **Add Vertex**: Click on the blank area of the edge path
- **Move Vertex**: Drag an existing vertex control point
- **Delete Vertex**: Double-click a vertex (or via `removable` configuration)

---

## Segments Tool (Line Segment Dragging)

On orthogonal edges, display draggable line segment controls. Dragging the segments allows adjustment of the orthogonal path.

### Configuration Options

| Property | Type | Default Value | Description |
|------|------|--------|------|
| `precision` | `number` | `0.5` | Line segment detection precision |
| `threshold` | `number` | `40` | Minimum line segment length threshold |
| `snapRadius` | `number` | `10` | Snap radius |
| `removeRedundancies` | `boolean` | `true` | Automatically remove redundant points |
| `stopPropagation` | `boolean` | `true` | Prevent event bubbling |
| `attrs` | `object` | Rectangle control bar | Line segment handle style |

### Example

```javascript
graph.on('edge:mouseenter', ({ edge }) => {
  edge.addTools([
    {
      name: 'segments',
      args: {
        snapRadius: 10,
        attrs: {
          width: 20,
          height: 8,
          x: -10,
          y: -4,
          rx: 4,
          ry: 4,
          fill: '#333',
          stroke: '#fff',
          'stroke-width': 2,
        },
      },
    },
  ]);
});

graph.on('edge:mouseleave', ({ edge }) => {
  edge.removeTools();
});
```

### Key Notes

- **Applicable to orthogonal routing** (`orth`, `manhattan`) edges
- Control bars are only displayed on horizontal or vertical line segments
- Automatically adjusts adjacent vertex coordinates during dragging

---

## Arrowhead Tool

Displays a draggable arrowhead at the start or end point of an edge. Dragging the arrowhead allows you to change the edge's connection target.

### Configuration Options

| Property | Type | Description |
|------|------|------|
| `type` | `'source' \| 'target'` | The end of the edge where the arrow is located |
| `attrs` | `object` | Arrow SVG style |

### Example

```javascript
edge.addTools([
  { name: 'source-arrowhead' },
  { name: 'target-arrowhead' },
]);
```

### Built-in Presets

- `'source-arrowhead'`：Source Arrowhead Tool
- `'target-arrowhead'`：Target Arrowhead Tool

---

## Anchor Tool

Displays anchor controllers at the connection ends of edges. Dragging allows adjustment of the edge's anchor position on the node.

### Configuration Options

| Property | Type | Description |
|------|------|------|
| `type` | `'source' \| 'target'` | Controls which end's anchor |
| `customAnchorAttrs` | `object` | Custom anchor style |
| `defaultAnchorAttrs` | `object` | Default anchor style |
| `resetAnchor` | `boolean \| AnchorConfig` | Reset anchor on double-click |

### Example

```javascript
edge.addTools([
  {
    name: 'anchor',
    args: {
      type: 'source',
      customAnchorAttrs: {
        'stroke-width': 4,
        stroke: '#33334F',
        fill: '#FFFFFF',
        r: 5,
      },
    },
  },
  {
    name: 'anchor',
    args: { type: 'target' },
  },
]);
```

---

## Tool Addition and Management

### Add Tools

```javascript
// Add a single tool
node.addTools([{ name: 'button-remove', args: { x: 0, y: 0 } }]);

// Add multiple tools
edge.addTools([
  { name: 'vertices' },
  { name: 'segments' },
  { name: 'source-arrowhead' },
  { name: 'target-arrowhead' },
]);
```

### Remove Tools

```javascript
// Remove all tools
node.removeTools();
```

### Inspection Tools

```javascript
if (node.hasTools()) {
  node.removeTools();
}
```

### Hover Display/Hide Mode

```javascript
graph.on('node:mouseenter', ({ node }) => {
  node.addTools([
    { name: 'boundary' },
    { name: 'button-remove', args: { x: 0, y: 0 } },
  ]);
});

graph.on('node:mouseleave', ({ node }) => {
  node.removeTools();
});

graph.on('edge:mouseenter', ({ edge }) => {
  edge.addTools([
    { name: 'vertices' },
    { name: 'button-remove', args: { distance: 20 } },
  ]);
});

graph.on('edge:mouseleave', ({ edge }) => {
  edge.removeTools();
});
```

---

## Common Errors and Fixes

### Error 1: Using Non-existent hideTools/showTools API

```javascript
// ❌ Incorrect: This API does not exist in X6 3.x
node.hideTools();
node.showTools();

// ✅ Correct: Control visibility using addTools/removeTools
node.addTools([...]);
node.removeTools();
```

### Error 2: Configuring Tools in Graph Options

```javascript
// ❌ Incorrect: Tools are not set in Graph configuration
const graph = new Graph({
  container: 'container',
  tools: ['button-remove'],  // This configuration does not exist
});

// ✅ Correct: Add through node/edge instances
const node = graph.addNode({ ... });
node.addTools([{ name: 'button-remove', args: { x: 0, y: 0 } }]);
```

### Error 3: Non-array Passed to addTools

```javascript
// ❌ Error: The addTools parameter should be an array
node.addTools({ name: 'boundary' });

// ✅ Correct: Pass an array
node.addTools([{ name: 'boundary' }]);
```