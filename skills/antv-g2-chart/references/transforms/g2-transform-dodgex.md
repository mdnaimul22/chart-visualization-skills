---
id: "g2-transform-dodgex"
title: "G2 DodgeX Group Transform"
description: |
  DodgeX is a Transform in G2 v5 used for grouped displays,
  arranging multiple series elements at the same x-position in a staggered manner horizontally.
  It is the core dependency for grouped bar charts.

library: "g2"
version: "5.x"
category: "transforms"
tags:
  - "dodgeX"
  - "group"
  - "side-by-side"
  - "transform"
  - "grouped bar chart"
  - "spec"

related:
  - "g2-mark-interval-grouped"
  - "g2-transform-stacky"

use_cases:
  - "Creating grouped bar charts (side-by-side display of multiple series)"
  - "Grouped scatter plots"

difficulty: "beginner"
completeness: "full"
created: "2024-01-01"
updated: "2025-03-01"
author: "antv-team"
source_url: "https://g2.antv.antgroup.com/manual/core/transform/dodge-x"
---

## Basic Usage

```javascript
import { Chart } from '@antv/g2';

const chart = new Chart({ container: 'container', width: 640, height: 480 });

chart.options({
  type: 'interval',
  data,
  encode: { x: 'month', y: 'value', color: 'type' },
  transform: [{ type: 'dodgeX' }],
});

chart.render();
```

## Configuration Options

```javascript
chart.options({
  type: 'interval',
  data: [...],
  encode: { x: 'month', y: 'value', color: 'type' },
  transform: [
    {
      type: 'dodgeX',
      padding: 0,          // Spacing between bars within a group (relative to group width, 0-1), default 0
      paddingOuter: 0.1,   // Outer margin between entire groups and adjacent groups
      reverse: false,      // Whether to reverse the group order
    },
  ],
});
```

## Difference from stackY

```javascript
// dodgeX: Each series is displayed side by side, facilitating direct comparison of absolute values
chart.options({ transform: [{ type: 'dodgeX' }] });

// stackY: Each series is stacked, facilitating comparison of totals and proportions
chart.options({ transform: [{ type: 'stackY' }] });
```

## Grouping + Stacking Combination

Simultaneously group and stack: dodgeX first, then stackY, achieving "stacking within groups and side-by-side between groups".

```javascript
chart.options({
  type: 'interval',
  data,
  encode: { x: 'quarter', y: 'value', color: 'type', series: 'group' },
  transform: [
    { type: 'dodgeX', groupBy: 'x' },   // Group by series, specify groupBy: 'x' to exclude color from grouping
    { type: 'stackY' },                 // Stack within groups by color
  ],
});
```

## Horizontal Grouped Bar Chart

```javascript
chart.options({
  type: 'interval',
  data,
  encode: { x: 'category', y: 'value', color: 'type' },
  transform: [{ type: 'dodgeX' }],
  coordinate: { transform: [{ type: 'transpose' }] },
});
```

## Common Errors and Fixes

### Error 1: transform written as an object
```javascript
// ❌ chart.options({ transform: { type: 'dodgeX' } });
// ✅ chart.options({ transform: [{ type: 'dodgeX' }] });
```

### Error 2: Multiple Series Interval Without Grouping/Stacking Transform
```javascript
// ❌ Incorrect: Multiple series data without transform, bars overlap in the same position
chart.options({
  type: 'interval',
  data: multiSeriesData,
  encode: { x: 'month', y: 'value', color: 'type' },
});

// ✅ Correct: Add dodgeX for grouped display
chart.options({
  type: 'interval',
  data: multiSeriesData,
  encode: { x: 'month', y: 'value', color: 'type' },
  transform: [{ type: 'dodgeX' }],
});
```

### Error 3: dodgeX placed in data.transform
```javascript
// ❌ Incorrect: dodgeX is a Mark Transform, not a Data Transform
chart.options({
  data: { type: 'inline', value: data, transform: [{ type: 'dodgeX' }] },
});

// ✅ Correct: At the same level as data/encode
chart.options({
  data,
  encode: { x: 'x', y: 'y', color: 'type' },
  transform: [{ type: 'dodgeX' }],
});
```