---
id: "g6-node-circle"
title: "G6 Circle Node"
description: |
  Create graph visualizations using circle nodes. The circle is the most common node shape,
  supporting labels, icons, badges, ports, and multiple states.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "nodes"
tags:
  - "node"
  - "circle"
  - "network graph"
  - "social network"

related:
  - "g6-node-rect"
  - "g6-node-image"
  - "g6-state-overview"
  - "g6-core-graph-init"

use_cases:
  - "Network topology"
  - "Social relationship graph"
  - "Knowledge graph"
  - "General node scenarios"

anti_patterns:
  - "When the number of nodes is extremely large (>1000), consider performance optimization and avoid complex styles"
  - "Use html or react nodes when displaying complex content"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/element/node/circle"
---

## Core Concepts

Circular nodes (`circle`) are the default node type in G6, with a symmetrical shape suitable for representing undirected entities.

**Main Style Attributes:**
- `size`: Node diameter (px), default 32
- `fill`: Fill color
- `stroke`: Stroke color
- `lineWidth`: Stroke width
- `labelText`: Label text (callback function)
- `labelPlacement`: Label position (`'center'` | `'top'` | `'bottom'` | `'left'` | `'right'`)

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
       { id: 'n1', data: { label: 'User A' } },
       { id: 'n2', data: { label: 'User B' } },
       { id: 'n3', data: { label: 'User C' } },
    ],
    edges: [
       { source: 'n1', target: 'n2' },
       { source: 'n2', target: 'n3' },
       { source: 'n1', target: 'n3' },
    ],
  },
  node: {
    type: 'circle',
    style: {
      size: 40,
      fill: '#1783FF',
      stroke: '#fff',
      lineWidth: 2,
      labelText: (d) => d.data.label,
      labelPlacement: 'bottom',
      labelFill: '#333',
    },
  },
  layout: { type: 'circular' },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

## Common Variants

### Color by Category (Palette)

```javascript
node: {
  type: 'circle',
  style: {
    size: 40,
    labelText: (d) => d.data.name,
    labelPlacement: 'bottom',
  },
  palette: {
    type: 'group',
    field: 'category',        // Category field in the data
    color: 'tableau10',       // Built-in color palette
  },
},
```

### Mapping Node Size to Numerical Values

```javascript
// Using transform to map node size
transforms: [
  {
    type: 'map-node-size',
    field: 'value',           // Numerical field in the data
    range: [20, 80],          // Size range to map to
  },
],
node: {
  type: 'circle',
  style: {
    labelText: (d) => d.data.name,
  },
},
```

### Nodes with Icons

```javascript
node: {
  type: 'circle',
  style: {
    size: 48,
    fill: '#1783FF',
    // Icon (requires importing iconfont or using Unicode)
    iconText: '\ue6a7',          // iconfont unicode
    iconFontFamily: 'iconfont',  // font family name
    iconFill: '#fff',
    iconFontSize: 20,
    labelText: (d) => d.data.label,
    labelPlacement: 'bottom',
  },
},
```

### With Badge

```javascript
node: {
  type: 'circle',
  style: {
    size: 40,
    fill: '#1783FF',
    labelText: (d) => d.data.label,
    // Badge configuration
    badges: [
      {
        text: '!',
        placement: 'right-top',  // Badge position
        fill: '#ff4d4f',
        textFill: '#fff',
        fontSize: 10,
      },
    ],
  },
},
```

### With Ports (Port)

```javascript
// Ports are used to precisely control the connection positions of edges
node: {
  type: 'circle',
  style: {
    size: 40,
    fill: '#1783FF',
    ports: [
       { key: 'top', placement: 'top' },
       { key: 'bottom', placement: 'bottom' },
       { key: 'left', placement: 'left' },
       { key: 'right', placement: 'right' },
    ],
  },
},
```

### Node State Styles

```javascript
node: {
  type: 'circle',
  style: {
    size: 40,
    fill: '#1783FF',
    labelText: (d) => d.data.label,
  },
  state: {
    selected: {
      fill: '#ff7875',
      stroke: '#ff4d4f',
      lineWidth: 3,
      // Halo effect
      haloFill: '#ff7875',
      haloLineWidth: 12,
      haloOpacity: 0.25,
    },
    hover: {
      fill: '#40a9ff',
      cursor: 'pointer',
    },
    inactive: {
      opacity: 0.3,
    },
  },
},
// Works with hover-activate behavior
behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element', 'hover-activate'],
```

## Complete Style Property Reference

```typescript
// Common Node Style Properties
interface CircleNodeStyle {
  // Shape
  size?: number;                    // Node size (diameter)
  
  // Fill and Stroke
  fill?: string;                    // Fill color
  fillOpacity?: number;             // Fill opacity 0~1
  stroke?: string;                  // Stroke color
  lineWidth?: number;               // Stroke width
  lineDash?: number[];              // Dashed stroke [solid length, gap length]
  opacity?: number;                 // Overall opacity 0~1
  
  // Shadow
  shadowColor?: string;
  shadowBlur?: number;
  shadowOffsetX?: number;
  shadowOffsetY?: number;
  
  // Halo (hover/select effect)
  halo?: boolean;                   // Whether to display halo
  haloFill?: string;
  haloLineWidth?: number;
  haloOpacity?: number;
  
  // Label
  labelText?: string | ((d: NodeData) => string);
  labelPlacement?: 'center' | 'top' | 'bottom' | 'left' | 'right';
  labelFill?: string;
  labelFontSize?: number;
  labelFontWeight?: string | number;
  labelBackground?: boolean;        // Whether to display label background
  labelBackgroundFill?: string;
  labelBackgroundOpacity?: number;
  labelOffsetX?: number;
  labelOffsetY?: number;
  labelMaxWidth?: number;           // Maximum label width (truncate if exceeded)
  labelWordWrap?: boolean;          // Whether to automatically wrap text
  
  // Icon
  iconText?: string;                // Icon text/unicode
  iconFontFamily?: string;          // Icon font family
  iconFill?: string;
  iconFontSize?: number;
  iconWidth?: number;
  iconHeight?: number;
  
  // Badges
  badges?: BadgeStyle[];
  
  // Ports
  ports?: PortStyle[];
  
  // Interaction
  cursor?: string;                  // Mouse cursor style
}
```

## Common Errors

### Error 1: Using the label property from v4

```javascript
// ❌ Incorrect: v4 syntax
node: {
  labelCfg: {
    style: { fill: '#333', fontSize: 14 }
  }
}

// ✅ Correct: v5 syntax
node: {
  style: {
    labelText: (d) => d.data.label,
    labelFill: '#333',
    labelFontSize: 14,
  }
}
```

### Error 2: Directly Setting `label` in Data and Forgetting to Configure `labelText`

```javascript
// ❌ Label exists in node data, but forgotten to reference it in style
const nodes = [{ id: 'n1', data: { label: 'Node 1' } }];
// Without configuring `node.style.labelText`, the node label will not be displayed

// ✅ Correct
node: {
  style: {
    labelText: (d) => d.data.label,  // Read label from data
  },
},
```

### Error 3: Array size set for unsupported node type

```javascript
// ❌ Setting [width, height] array for circle node
node: {
  type: 'circle',
  style: { size: [60, 40] },  // circle only accepts a single value
}

// ✅ Using a single value for circle node
node: {
  type: 'circle',
  style: { size: 60 },
}

// rect node can use an array
node: {
  type: 'rect',
  style: { size: [120, 60] },  // [width, height]
}
```