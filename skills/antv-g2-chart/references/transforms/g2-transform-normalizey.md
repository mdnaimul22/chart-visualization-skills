---
id: "g2-transform-normalizey"
title: "G2 NormalizeY Transformation"
description: |
  NormalizeY normalizes the y values within each x group to the range [0, 1],
  typically used after stackY to create percentage stacked charts,
  eliminating total quantity differences and focusing on proportion distribution.

library: "g2"
version: "5.x"
category: "transforms"
tags:
  - "normalizeY"
  - "normalization"
  - "percentage"
  - "transform"
  - "percentage stacking"
  - "proportion"
  - "spec"

related:
  - "g2-mark-interval-normalized"
  - "g2-transform-stacky"

use_cases:
  - "Creating percentage stacked bar charts"
  - "Creating percentage stacked area charts"
  - "Eliminating total quantity differences, focusing on proportion"

difficulty: "beginner"
completeness: "full"
created: "2024-01-01"
updated: "2025-03-01"
author: "antv-team"
source_url: "https://g2.antv.antgroup.com/manual/core/transform/normalize-y"
---

## Basic Usage (Must be Used with stackY)

```javascript
import { Chart } from '@antv/g2';

const chart = new Chart({ container: 'container', width: 640, height: 480 });

chart.options({
  type: 'interval',
  data,
  encode: { x: 'month', y: 'value', color: 'type' },
  transform: [
    { type: 'stackY' },       // Step 1: Stack
    { type: 'normalizeY' },   // Step 2: Normalize (Order cannot be reversed!)
  ],
  axis: {
    y: { labelFormatter: (v) => `${(v * 100).toFixed(0)}%` },
  },
});

chart.render();
```

## Configuration Options

```javascript
transform: [
  { type: 'stackY' },
  {
    type: 'normalizeY',
    basis: 'max',    // Normalization basis: 'max' (default, maximum value per group) | 'min' | 'first' | 'last' | 'mean' | 'median'
    series: 'y',     // Specifies the channel for normalization, default is 'y'
  },
],
```

## Percentage Stacked Area Chart

```javascript
chart.options({
  type: 'area',
  data,
  encode: { x: 'date', y: 'value', color: 'type' },
  transform: [
    { type: 'stackY' },
    { type: 'normalizeY' },
  ],
  axis: {
    y: { labelFormatter: (v) => `${(v * 100).toFixed(0)}%` },
  },
});
```

## Y-axis Percentage Formatting

After `normalizeY`, the y-value range is [0, 1], and it needs to be manually formatted to display as a percentage:

```javascript
axis: {
  y: { labelFormatter: (v) => `${(v * 100).toFixed(0)}%` },
}
```

## Common Errors and Fixes

### Error 1: normalizeY Executed Before stackY
```javascript
// ❌ Incorrect: Normalizing before stacking does not achieve the percentage stacking effect
transform: [{ type: 'normalizeY' }, { type: 'stackY' }],

// ✅ Correct: Stack first, then normalize
transform: [{ type: 'stackY' }, { type: 'normalizeY' }],
```

### Error 2: Missing stackY, Directly Using normalizeY
```javascript
// ❌ Incorrect: Only normalizeY does not produce a percentage stacking effect
chart.options({
  type: 'interval',
  data,
  encode: { x: 'month', y: 'value', color: 'type' },
  transform: [{ type: 'normalizeY' }],
});

// ✅ Correct: Combine stackY with normalizeY
chart.options({
  type: 'interval',
  data,
  encode: { x: 'month', y: 'value', color: 'type' },
  transform: [{ type: 'stackY' }, { type: 'normalizeY' }],
});
```

### Error 3: Y-axis Not Formatted as Percentage
```javascript
// ❌ Problem: After normalization, the Y-axis displays 0.0 - 1.0, which is unclear to users
chart.options({ transform: [{ type: 'stackY' }, { type: 'normalizeY' }] });

// ✅ Correct: Add percentage formatting
chart.options({
  transform: [{ type: 'stackY' }, { type: 'normalizeY' }],
  axis: { y: { labelFormatter: (v) => `${(v * 100).toFixed(0)}%` } },
});
```