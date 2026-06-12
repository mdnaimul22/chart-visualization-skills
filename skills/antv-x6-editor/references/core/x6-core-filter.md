---
id: "x6-core-filter"
title: "X6 SVG Filter"
description: |
  X6 built-in SVG filters: outline, highlight, blur, dropShadow, grayScale, sepia, saturate, hueRotate, invert, brightness, contrast.

library: "x6"
version: "3.x"
category: "core"
subcategory: "filter"
tags:
  - "filter"
  - "filter"
  - "shadow"
  - "blur"
  - "highlight"
  - "outline"
  - "drop-shadow"
  - "blur"
  - "grayScale"
  - "SVG filter"

related:
  - "x6-core-node"
  - "x6-core-edge"
  - "x6-core-highlighter"

use_cases:
  - "Adding shadow effects to nodes"
  - "Highlighting node outlines"
  - "Applying blur effects to nodes"
  - "Grayscale/disabled state for nodes"
  - "Mouse hover highlights"

difficulty: "intermediate"
completeness: "full"
---
## Basic Usage

Use built-in filters through the `filter` property in the `attrs` of nodes/edges:

```javascript
graph.addNode({
  x: 100,
  y: 100,
  width: 120,
  height: 60,
  attrs: {
    body: {
      fill: '#fff',
      stroke: '#5F95FF',
      filter: {
        name: 'dropShadow',
        args: { dx: 2, dy: 2, blur: 3, color: 'rgba(0,0,0,0.2)' },
      },
    },
  },
});
```

## Built-in Filter List

### dropShadow (Shadow)

Add a drop shadow to an element:

```javascript
attrs: {
  body: {
    filter: {
      name: 'dropShadow',
      args: {
        dx: 2,        // Horizontal offset, default 0
        dy: 2,        // Vertical offset, default 0
        blur: 4,      // Blur radius, default 4
        color: 'black',  // Shadow color, default 'black'
        opacity: 0.3, // Shadow opacity, default 1
      },
    },
  },
}
```

### outline (Outer Stroke)

Add a stroke around the outer edge of an element (does not affect the element itself):

```javascript
attrs: {
  body: {
    filter: {
      name: 'outline',
      args: {
        color: 'blue',   // Stroke color, default 'blue'
        width: 2,        // Stroke width, default 1
        margin: 3,       // Distance between stroke and element, default 2
        opacity: 1,      // Stroke opacity, default 1
      },
    },
  },
}
```

### highlight (Glow Effect)

Adds a glowing effect around the element:

```javascript
attrs: {
  body: {
    filter: {
      name: 'highlight',
      args: {
        color: 'red',    // Highlight color, default 'red'
        width: 2,        // Highlight expansion width, default 1
        blur: 5,         // Blur radius, default 0
        opacity: 0.8,    // Highlight opacity, default 1
      },
    },
  },
}
```

### blur (Gaussian Blur)

```javascript
attrs: {
  body: {
    filter: {
      name: 'blur',
      args: {
        x: 3,  // Horizontal blur amount, default is 2
        y: 3,  // Vertical blur amount (optional, defaults to the same as x)
      },
    },
  },
}
```

### grayScale (Grayscale)

```javascript
attrs: {
  body: {
    filter: {
      name: 'grayScale',
      args: {
        amount: 1,  // Grayscale level, 0~1, 1 for complete grayscale
      },
    },
  },
}
```

### Sepia (Brown/Vintage)

```javascript
attrs: {
  body: {
    filter: {
      name: 'sepia',
      args: {
        amount: 1,  // 0~1
      },
    },
  },
}
```

### saturate (Saturation)

```javascript
attrs: {
  body: {
    filter: {
      name: 'saturate',
      args: {
        amount: 0.5,  // < 1 decreases saturation, > 1 increases saturation
      },
    },
  },
}
```

### hueRotate (Hue Rotation)

```javascript
attrs: {
  body: {
    filter: {
      name: 'hueRotate',
      args: {
        angle: 90,  // Rotation angle (degrees)
      },
    },
  },
}
```

### invert (Inversion)

```javascript
attrs: {
  body: {
    filter: {
      name: 'invert',
      args: {
        amount: 1,  // 0~1, 1 for complete inversion
      },
    },
  },
}
```

### brightness

```javascript
attrs: {
  body: {
    filter: {
      name: 'brightness',
      args: {
        amount: 1.5,  // < 1 darkens, > 1 brightens
      },
    },
  },
}
```

### contrast (Contrast)

```javascript
attrs: {
  body: {
    filter: {
      name: 'contrast',
      args: {
        amount: 2,  // < 1 decreases contrast, > 1 increases contrast
      },
    },
  },
}
```

## Dynamically Adding/Removing Filters

```javascript
const node = graph.addNode({
  x: 100, y: 100, width: 120, height: 60,
  attrs: { body: { fill: '#EFF4FF', stroke: '#5F95FF' } },
});

// Add shadow on mouse hover
graph.on('node:mouseenter', ({ node }) => {
  node.attr('body/filter', {
    name: 'dropShadow',
    args: { dx: 0, dy: 4, blur: 8, color: 'rgba(0,0,0,0.15)' },
  });
});

// Remove filter on mouse leave
graph.on('node:mouseleave', ({ node }) => {
  node.attr('body/filter', null);
});
```

## Disabled State Example

Use a grayscale filter to represent a node as "disabled":

```javascript
function setNodeDisabled(node, disabled) {
  if (disabled) {
    node.attr('body/filter', { name: 'grayScale', args: { amount: 1 } });
    node.attr('body/opacity', 0.6);
  } else {
    node.attr('body/filter', null);
    node.attr('body/opacity', 1);
  }
}
```

## Common Errors

### ❌ filter directly writes CSS filter string

```javascript
// Error: CSS filter string syntax is not supported
attrs: {
  body: {
    filter: 'drop-shadow(2px 2px 4px rgba(0,0,0,0.3))',  // ❌
  },
}
```

```javascript
// Correct: Use X6's object syntax
attrs: {
  body: {
    filter: {
      name: 'dropShadow',
      args: { dx: 2, dy: 2, blur: 4, color: 'rgba(0,0,0,0.3)' },
    },  // ✅
  },
}
```

### ❌ Incorrect Spelling of Filter Names

```javascript
// Incorrect: Misspelled filter names
filter: { name: 'drop-shadow', args: {...} }  // ❌ Should be 'dropShadow'
filter: { name: 'grayscale', args: {...} }    // ❌ Should be 'grayScale'
filter: { name: 'hue-rotate', args: {...} }   // ❌ Should be 'hueRotate'
```

Correct filter names (camelCase): `dropShadow`, `grayScale`, `hueRotate`