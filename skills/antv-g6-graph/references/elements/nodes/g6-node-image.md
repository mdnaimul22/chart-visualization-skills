---
id: "g6-node-image"
title: "G6 Image Node"
description: |
  Use image nodes to display avatars, icons, and other image content.
  Supports circular cropping, labels, states, etc.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "nodes"
tags:
  - "node"
  - "image"
  - "avatar"
  - "icon"

related:
  - "g6-node-circle"
  - "g6-node-rect"
  - "g6-core-data-structure"

use_cases:
  - "Social relationship graph with user avatars"
  - "Enterprise relationship graph with logos"
  - "Icon-based system architecture diagram"

anti_patterns:
  - "Pay attention to performance when using too many images, avoid loading large images"
  - "Image nodes may display blank when offline, fallback styles need to be set"

difficulty: "beginner"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
source_url: "https://g6.antv.antgroup.com/manual/element/node/image"
---

## Core Concepts

Image nodes (`image`) render nodes as images, supporting URL images, Base64 images, etc.

**Main Properties:**
- `src`: Image URL (callback function retrieves from data)
- `size`: Node size
- `labelText`: Label text

## Minimum Viable Example

```javascript
import { Graph } from '@antv/g6';

const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
      {
        id: 'n1',
        data: {
          name: 'Zhang San',
          avatar: 'https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png',
        },
      },
      {
        id: 'n2',
        data: {
          name: 'Li Si',
          avatar: 'https://gw.alipayobjects.com/zos/antfincdn/YXH2wo1%26Kb/Avatar.png',
        },
      },
    ],
    edges: [
      { source: 'n1', target: 'n2' },
    ],
  },
  node: {
    type: 'image',
    style: {
      size: 60,
      src: (d) => d.data.avatar,         // Retrieve image URL from data
      labelText: (d) => d.data.name,
      labelPlacement: 'bottom',
    },
  },
  layout: { type: 'circular' },
  behaviors: ['drag-canvas', 'zoom-canvas', 'drag-element'],
});

graph.render();
```

## Common Variants

### Circular Avatar (Cropped to Circle)

```javascript
node: {
  type: 'image',
  style: {
    size: 60,
    src: (d) => d.data.avatar,
    // Circular cropping: achieved by setting clipCfg
    clipType: 'circle',
    clipR: 30,           // Same as size/2
    labelText: (d) => d.data.name,
    labelPlacement: 'bottom',
    stroke: '#91caff',
    lineWidth: 2,
  },
},
```

### Image Node with Status Indicator

```javascript
node: {
  type: 'image',
  style: {
    size: 60,
    src: (d) => d.data.avatar,
    labelText: (d) => d.data.name,
    labelPlacement: 'bottom',
    // Badge (status indicator) in the upper-right corner
    badges: [
      {
        text: (d) => d.data.online ? '●' : '○',
        placement: 'right-bottom',
        fill: (d) => d.data.online ? '#52c41a' : '#d9d9d9',
        textFill: '#fff',
      },
    ],
  },
},
```

### Mixed Local and Remote Images

```javascript
const graph = new Graph({
  container: 'container',
  width: 640,
  height: 480,
  data: {
    nodes: [
      {
        id: 'github',
        data: {
          name: 'GitHub',
          // Use online icon
          icon: 'https://github.githubassets.com/favicons/favicon.svg',
        },
      },
      {
        id: 'npm',
        data: {
          name: 'NPM',
          icon: 'https://static.npmjs.com/favicon-32x32.png',
        },
      },
    ],
    edges: [{ source: 'github', target: 'npm' }],
  },
  node: {
    type: 'image',
    style: {
      size: 50,
      src: (d) => d.data.icon,
      labelText: (d) => d.data.name,
      labelPlacement: 'bottom',
    },
  },
  layout: { type: 'force', linkDistance: 150 },
  behaviors: ['drag-canvas', 'zoom-canvas'],
});
```

## Common Errors

### Error 1: `src` Written as a Static String

```javascript
// ❌ All nodes display the same image
node: {
  type: 'image',
  style: {
    src: 'https://example.com/avatar.png',  // Static value, same for all nodes
  },
}

// ✅ Use a callback function to retrieve from data
node: {
  type: 'image',
  style: {
    src: (d) => d.data.avatar,  // Each node uses its own image
  },
}
```

### Error 2: Blank Space Due to Image Loading Failure

```javascript
// ✅ Provide a default fallback image
node: {
  type: 'image',
  style: {
    src: (d) => d.data.avatar || 'https://example.com/default-avatar.png',
    size: 60,
  },
},
```