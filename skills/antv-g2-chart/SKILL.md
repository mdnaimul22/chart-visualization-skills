

---
name: antv-g2-chart
description: Generate G2 v5 chart code. Use when user asks for G2 charts, bar charts, line charts, pie charts, scatter plots, area charts, or any data visualization with G2 library.
---

# G2 v5 Chart Code Generator

You are an expert in AntV G2 v5 charting library. Generate accurate, runnable code following G2 v5 best practices.

---

## 1. Core Constraints / Core Constraints (MUST follow)

1. **`container` is mandatory**: `new Chart({ container: 'container', ... })`
2. **Use Spec Mode ONLY**: `chart.options({ type: 'interval', data, encode: {...} })` (V4 chain API see Forbidden Patterns)
3. **`chart.options()` can only be called once**: Multiple calls will completely override the previous configuration, only the last one takes effect. Multiple mark overlay must use `type: 'view'` + `children` array, not multiple calls to `chart.options()`.
4. **`encode` object**: `encode: { x, y }` (Forbidden V4's `.position('x*y')`)
5. **`transform` must be array**: `transform: [{ type: 'stackY' }]`
6. **`labels` is plural**: Use `labels: [{ text: 'field' }]` not `label: {}`
7. **`coordinate` rules**:
   - Coordinate system type write directly: `coordinate: { type: 'theta' }`, `coordinate: { type: 'polar' }`
   - transpose is **transform** not coordinate system type, must be written in `transform` array: `coordinate: { transform: [{ type: 'transpose' }] }`
   - ❌ Forbidden: `coordinate: { type: 'transpose' }`
8. **Range encoding** (Gantt chart, candlestick, etc.): `encode: { y: 'start', y1: 'end' }`, forbidden `y: ['start', 'end']`
9. **Style principles**: Styles mentioned in user description (radius, fillOpacity, color, fontSize, etc.) must be fully preserved; decorative styles not mentioned by user (`shadowBlur`, `shadowColor`, `shadowOffsetX/Y`, etc.) should not be added arbitrarily.
10. **`animate` rules**: Do not add `animate` configuration when user does not explicitly require animation (G2 has built-in default animation), only add when user explicitly describes animation requirements.
11. **`scale.color.palette` can only use valid values**: palette found via d3-scale-chromatic, illegal names will throw `Unknown palette` error. **Do not infer or create non-existent names** (e.g., `'blueOrange'`, `'redGreen'`, `'hot'`, `'jet'`, `'coolwarm'` are all illegal). Legal common values: sequential scales `'blues'|'greens'|'reds'|'ylOrRd'|'viridis'|'plasma'|'turbo'`; diverging scales `'rdBu'|'rdYlGn'|'spectral'`; when unsure use `range: ['#startColor', '#endColor']` custom alternative.
12. **Do not use `d3.*` in user code**: G2 uses d3 internally, but `d3` object is not exposed to user code scope, calling `d3.sum()` etc. will throw `ReferenceError: d3 is not defined`. If aggregation is needed, prioritize G2 built-in options (e.g. `sortX` reducer: 'sum'), if must customize use native JS: `d3.sum(arr, d=>d.v)` → `arr.reduce((s,d)=>s+d.v,0)`; `d3.max(arr, d=>d.v)` → `Math.max(...arr.map(d=>d.v))`
13. **When user does not specify color scheme, forbidden to use white or near-white as graphic fill color**: `style: { fill: '#fff' }`, `style: { fill: 'white' }`, `style: { fill: '#ffffff' }` etc. will make graphics completely invisible on white background. When color scheme not specified rely on G2's `encode.color` to auto-assign theme colors, or use colors with clear visual distinction (e.g., `'#5B8FF9'`). Below are legal exceptions: label text `fill: '#fff'` (labels inside dark background), separator lines `stroke: '#fff'` (stacked/pack/treemap separator white lines)
15. **When user does not specify container**: `container` defaults to `'container'`, do not create via `document.createElement('div')`, code end must have `chart.render();`

### 1.1 Forbidden Patterns / Forbidden Usage

**Do not use V4 syntax**, must use V5 Spec mode:

```javascript
// ❌ Forbidden: V4 createView
const view = chart.createView();
view.options({...});
// ❌ Forbidden: V4 chain API call
chart.interval()
  .data([...])
  .encode('x', 'genre')
  .encode('y', 'sold')
  .style({ radius: 4 });
// ❌ Forbidden: V4 chain encode
chart.line().encode('x', 'date').encode('y', 'value');
// ❌ Forbidden: V4 source
chart.source(data);
// ❌ Forbidden: V4 position
chart.interval().position('genre*sold');
// ✅ Correct: V5 Spec mode
chart.options({
  type: 'interval',
  data: [...],
  encode: { x: 'genre', y: 'sold' },
  style: { radius: 4 },
});
```

**Reason**: V5 uses Spec mode, structure is clear, easy to serialize, dynamically generate and debug.

#### Correct V5 alternative for `createView`

`chart.createView()` in V4 is used for "multiple views sharing container but different data", in V5 corresponds to two scenarios:

**Scenario A: Overlay multiple marks within the same coordinate system (most common)** → use `type: 'view'` + `children` array, `children` cannot nest `view` or `children` again:

```javascript
// ✅ Multiple mark overlay (line + point)
chart.options({
  type: 'view',
  data,
  children: [
    { type: 'line', encode: { x: 'date', y: 'value' } },
    { type: 'point', encode: { x: 'date', y: 'value' } },
  ],
});
```

**Scenario B: Multiple independent coordinate systems side-by-side/overlaid (e.g., population pyramid, butterfly chart)** → use `type: 'spaceLayer'` + `children` (each child view has independent data and coordinate system):

```javascript
// ✅ Population pyramid: left and right side independent views overlaid, share Y axis
chart.options({
  type: 'spaceLayer',
  children: [
    {
      type: 'interval',
      data: leftData, // Left side data (negative or flipped)
      coordinate: { transform: [{ type: 'transpose' }, { type: 'reflectX' }] },
      encode: { x: 'age', y: 'male' },
      axis: { y: { position: 'right' } },
    },
    {
      type: 'interval',
      data: rightData, // Right side data
      coordinate: { transform: [{ type: 'transpose' }] },
      encode: { x: 'age', y: 'female' },
      axis: { y: false },
    },
  ],
});
// ✅ Simpler solution: Single view + negative value trick (data can be in one array)
chart.options({
  type: 'interval',
  data: combinedData, // Merged data, use negative values to distinguish direction
  coordinate: { transform: [{ type: 'transpose' }] },
  encode: {
    x: 'age',
    y: (d) => d.sex === 'male' ? -d.population : d.population,
    color: 'sex',
  },
  axis: { y: { labelFormatter: (d) => Math.abs(d) } }, // Show absolute value
});
```

**Selection principles**:
- Both sides data structure same, just direction opposite → **Prioritize negative value trick** (single `interval`, code is most concise)
- Both sides need completely independent coordinate systems/scales → use `spaceLayer`

### 1.2 Forbidden Hallucinated Mark Types / Hallucinated Mark Types

The following types come from other chart libraries (e.g., ECharts, Vega), **do not exist in G2**, using them will cause runtime errors:

| ❌ Wrong Usage | ✅ Correct Replacement |
|------------|-----------|
| `type: 'ruleX'` | `type: 'lineX'` (Vertical reference line) |
| `type: 'ruleY'` | `type: 'lineY'` (Horizontal reference line) |
| `type: 'regionX'` | `type: 'rangeX'` (X axis interval highlight) |
| `type: 'regionY'` | `type: 'rangeY'` (Y axis interval highlight) |
| `type: 'venn'` | `type: 'path'` + `data.transform: [{ type: 'venn' }]` |

**G2 legal mark type complete list** (do not create other type out of thin air):
- Basic: `interval`, `line`, `area`, `point`, `rect`, `cell`, `text`, `image`, `path`, `polygon`, `shape`
- Connection: `link`, `connector`, `vector`
- Reference lines/areas: `lineX`, `lineY`, `rangeX`, `rangeY`; `range` (rarely used, only when x/y both need limit 2D rectangle, and data's x/y fields must be `[start,end]` array)
- Statistical: `box`, `boxplot`, `density`, `heatmap`, `beeswarm`
- Hierarchy/Relation: `treemap`, `pack`, `partition`, `tree`, `sankey`, `chord`, `forceGraph`
- Special: `wordCloud`, `gauge`, `liquid`
- Requires extension package: `sunburst` (needs `@antv/g2-extension-plot`, see [Sunburst](references/marks/g2-mark-sunburst.md))

---

## 2. Common Mistakes / Common Errors

Code examples:

```javascript
// ❌ Wrong: missing container
const chart = new Chart({ width: 640, height: 480 });
// ✅ Correct: container required
const chart = new Chart({ container: 'container', width: 640, height: 480 });

// ❌ Wrong: transform as object
chart.options({ transform: { type: 'stackY' } });
// ✅ Correct: transform as array
chart.options({ transform: [{ type: 'stackY' }] });

// ❌ Wrong: label (singular)
chart.options({ label: { text: 'value' } });
// ✅ Correct: labels (plural)
chart.options({ labels: [{ text: 'value' }] });

// ❌ Wrong: Multiple calls to chart.options() —— each call completely replaces previous, only last one takes effect
chart.options({ type: 'interval', data, encode: { x: 'x', y: 'y' } });
// ❌ Overridden, not rendered
chart.options({ type: 'line', data, encode: { x: 'x', y: 'y' } });
// ❌ Overridden, not rendered
chart.options({ type: 'text', data, encode: { x: 'x', y: 'y', text: 'label' } });
// Only this one takes effect
// ✅ Correct: Multiple mark overlay must use type: 'view' + children
chart.options({
  type: 'view',
  data, // Shared data (child mark can override)
  children: [
    { type: 'interval', encode: { x: 'x', y: 'y' } },
    { type: 'line', encode: { x: 'x', y: 'y' } },
    { type: 'text', encode: { x: 'x', y: 'y', text: 'label' } },
  ],
});
// ✅ Child marks need different data, specify data separately in children
chart.options({
  type: 'view',
  data: mainData,
  children: [
    { type: 'interval', encode: { x: 'x', y: 'y' } }, // Use parent mainData
    { type: 'text', data: labelData, encode: { x: 'x', text: 'label' } }, // Use independent data
  ],
});
// ⚠️ Multiple mark combination rules:
// 1. Can only use children, forbidden to use marks, layers etc. config
// 2. children cannot nest (children inside cannot have children again)
// 3. Complex combinations use spaceLayer/spaceFlex
// ❌ Wrong: Use marks (Forbidden)
chart.options({ type: 'view', data, marks: [...], // ❌ Forbidden! });
// ❌ Wrong: Use layers (Forbidden)
chart.options({ type: 'view', data, Layers: [...], // ❌ Forbidden! });
// ✅ Correct: Use children
chart.options({
  type: 'view',
  data,
  children: [ // ✅ Correct
    { type: 'line', encode: { x: 'year', y: 'value' } },
    { type: 'point', encode: { x: 'year', y: 'value' } },
  ],
});
// ❌ Wrong: children nesting (Forbidden)
chart.options({
  type: 'view',
  children: [
    { type: 'view', children: [...], // ❌ Forbidden! children cannot nest },
  ],
});
// ✅ Correct: Use spaceLayer/spaceFlex to handle complex combinations
chart.options({
  type: 'spaceLayer',
  children: [
    { type: 'view', children: [...] }, // ✅ Under spaceLayer can have view + children
    { type: 'line', ... },
  ],
});
// ❌ Wrong: unnecessary scale type specification
chart.options({
  scale: {
    x: { type: 'linear' }, // ❌ Not needed, default is linear
    y: { type: 'linear' }, // ❌ Not needed
  },
});
// ✅ Correct: Let G2 infer scale type automatically
chart.options({
  scale: {
    y: { domain: [0, 100] }, // ✅ Only configure needed properties
  },
});
```

---

## 3. Basic Structure / Basic Structure

```javascript
import { Chart } from '@antv/g2';
const chart = new Chart({ container: 'container', width: 640, height: 480 });
chart.options({
  type: 'interval', // Mark type
  data: [...], // Data array
  encode: { x: 'field', y: 'field', color: 'field' },
  transform: [], // Data transforms
  scale: {}, // Scale config
  coordinate: {}, // Coordinate system
  style: {}, // Style config
  labels: [], // Data labels
  tooltip: {}, // Tooltip config
  axis: {}, // Axis config
  legend: {}, // Legend config
});
chart.render();
```

---

## 4. Core / Core Concepts

Core concepts are the foundation of G2, understanding these concepts is the prerequisite for correctly using G2.

### 4.1 Chart Initialization

Chart is the core class of G2, all charts start from Chart instance.

```javascript
import { Chart } from '@antv/g2';
const chart = new Chart({
  container: 'container', // Required: DOM container ID or element
  width: 640, // Optional: width
  height: 480, // Optional: height
  autoFit: true, // Optional: adapt to container size
  padding: 'auto', // Optional: padding
  theme: 'light', // Optional: theme
});
```

> **Detailed Documentation**: [Chart Initialization](references/core/g2-core-chart-init.md)

### 4.2 encode Channel System

encode maps data fields to visual channels, is the core concept of G2.

| Channel | Purpose | Example |
|------|------|------|
| `x` | X axis position | `encode: { x: 'month' }` |
| `y` | Y axis position | `encode: { y: 'value' }` |
| `color` | Color | `encode: { color: 'category' }` |
| `size` | Size | `encode: { size: 'population' }` |
| `shape` | Shape | `encode: { shape: 'type' }` |

> **Detailed Documentation**: [encode Channel System](references/core/g2-core-encode-channel.md)

### 4.3 View Composition (view + children)

Use `view` type with `children` array to combine multiple marks.

```javascript
chart.options({
  type: 'view',
  data,
  children: [
    { type: 'line', encode: { x: 'date', y: 'value' } },
    { type: 'point', encode: { x: 'date', y: 'value' } },
  ],
});
```

> **Detailed Documentation**: [View Composition](references/core/g2-core-view-composition.md)

---

## 5. Concepts / Concept Guide

Concept guide helps choose the correct chart type and configuration scheme.

### 5.1 Chart Type Selection / Chart Selection

Select appropriate chart type based on data characteristics and visualization goals:

| Data Relationship | Recommended Chart | Mark |
|---------|---------|------|
| Comparison | Bar Chart, Bar Chart | `interval` |
| Trend | Line Chart, Area Chart | `line`, `area` |
| Proportion | Pie Chart, Donut Chart | `interval` + `theta` |
| Distribution | Histogram, Box Plot | `rect`, `boxplot` |
| Correlation | Scatter Plot, Bubble Chart | `point` |
| Hierarchy | Treemap, Sunburst | `treemap`, `sunburst` (requires extension package) |

> **Detailed Documentation**: [Chart Type Selection Guide](references/concepts/g2-concept-chart-selection.md)

### 5.2 Visual Channels / Visual Channels

Visual channels are the mapping method from data to visual attributes:

| Channel Type | Suitable Data | Perception Accuracy |
|---------|---------|---------|
| Position | Continuous/Discrete | Highest |
| Length | Continuous | High |
| Color (Hue) | Discrete | Medium |
| Color (Lightness) | Continuous | Medium |
| Size | Continuous | Medium-Low |
| Shape | Discrete | Low |

> **Detailed Documentation**: [Visual Channels](references/concepts/g2-concept-visual-channels.md)

### 5.3 Color Theory / Color Theory

Select appropriate color scheme to improve chart readability:

| Scenario | Recommended Scheme | Example |
|------|---------|------|
| Categorical Data | Discrete Palette | `category10`, `category20` |
| Continuous Data | Sequential Palette | `Blues`, `RdYlBu` |
| Positive/Negative Contrast | Diverging Palette | `RdYlGn` |

> **Detailed Documentation**: [Color Theory](references/concepts/g2-concept-color-theory.md)

---

## 6. Marks / Chart Types

Marks are the core visualization elements of G2, determining the visual representation of data. Each Mark is suitable for specific data types and visualization scenarios.

### 6.1 Bar Chart Series / Interval

Bar charts are used to compare the size of categorical data, is the most commonly used chart type. Basic bar chart uses `interval` mark, stacked bar chart needs to add `stackY` transform, grouped bar chart uses `dodgeX` transform.

| Type | Mark | Key Configuration |
|------|------|----------|
| Basic Bar Chart | `interval` | - |
| Stacked Bar Chart | `interval` | `transform: [{ type: 'stackY' }]` |
| Grouped Bar Chart | `interval` | `transform: [{ type: 'dodgeX' }]` |
| Percentage Bar Chart | `interval` | `transform: [{ type: 'normalizeY' }]` |
| Horizontal Bar Chart | `interval` | `coordinate: { transform: [{ type: 'transpose' }] }` |

> **Detailed Documentation**: [Basic Bar Chart](references/marks/g2-mark-interval-basic.md) | [Stacked Bar Chart](references/marks/g2-mark-interval-stacked.md) | [Grouped Bar Chart](references/marks/g2-mark-interval-grouped.md) | [Percentage Bar Chart](references/marks/g2-mark-interval-normalized.md)

### 6.2 Line Chart Series / Line

Line charts are used to show data trends over time or ordered categories. Supports single line, multi-line comparison, and different interpolation methods.

| Type | Mark | Key Configuration |
|------|------|----------|
| Basic Line Chart | `line` | - |
| Multi-series Line | `line` | `encode: { color: 'category' }` |
| Smooth Curve | `line` | `encode: { shape: 'smooth' }` |
| Step Line | `line` | `encode: { shape: 'step' }` |

> **Detailed Documentation**: [Basic Line Chart](references/marks/g2-mark-line-basic.md) | [Multi-series Line](references/marks/g2-mark-line-multi.md) | [LineX/LineY](references/marks/g2-mark-linex-liney.md)

### 6.3 Area Chart Series / Area

Area charts fill the area on top of line charts, emphasizing the degree of change in quantity over time. Stacked area charts are used to show the contribution of each part to the whole.

| Type | Mark | Key Configuration |
|------|------|----------|
| Basic Area Chart | `area` | - |
| Stacked Area Chart | `area` | `transform: [{ type: 'stackY' }]` |

> **Detailed Documentation**: [Basic Area Chart](references/marks/g2-mark-area-basic.md) | [Stacked Area Chart](references/marks/g2-mark-area-stacked.md)

### 6.4 Pie/Donut Chart / Arc (Pie/Donut)

Pie charts are used to show the proportional relationship of each part to the whole. Use `theta` coordinate system with `interval` mark implementation.

| Type | Mark | Key Configuration |
|------|------|----------|
| Pie Chart | `interval` | `coordinate: { type: 'theta' }` + `stackY` |
| Donut Chart | `interval` | `coordinate: { type: 'theta', innerRadius: 0.6 }` |

> **Detailed Documentation**: [Pie Chart](references/marks/g2-mark-arc-pie.md) | [Donut Chart](references/marks/g2-mark-arc-donut.md)

### 6.5 Scatter/Bubble Chart / Point

Scatter plots are used to show the relationship between two numerical variables, bubble charts show the third dimension through point size.

| Type | Mark | Key Configuration |
|------|------|----------|
| Scatter Plot | `point` | `encode: { x, y }` |
| Bubble Chart | `point` | `encode: { x, y, size }` |

> **Detailed Documentation**: [Scatter Plot](references/marks/g2-mark-point-scatter.md) | [Bubble Chart](references/marks/g2-mark-point-bubble.md)

### 6.6 Histogram / Histogram

Histograms are used to show the distribution of continuous numerical data, use `rect` mark with `binX` transform implementation. Unlike bar charts, histogram bars have no gaps between them, indicating data continuity.

| Type | Mark | Key Configuration |
|------|------|----------|
| Basic Histogram | `rect` | `transform: [{ type: 'binX', y: 'count' }]` |
| Multi-distribution Comparison | `rect` | `groupBy` grouping |

> **Detailed Documentation**: [Histogram](references/marks/g2-mark-histogram.md)

### 6.7 Rose/Jade Chart / Polar Charts

Charts under polar coordinate system, represent numerical size through radius or arc length, visually more beautiful.

| Type | Mark | Key Configuration |
|------|------|----------|
| Rose Chart | `interval` | `coordinate: { type: 'polar' }` |
| Radial Bar Chart | `interval` | `coordinate: { type: 'radial' }` |

> **Detailed Documentation**: [Rose Chart](references/marks/g2-mark-rose.md) | [Radial Bar Chart](references/marks/g2-mark-radial-bar.md)

### 6.8 Statistical Distribution Charts / Distribution

Charts showing data distribution characteristics, suitable for statistical analysis and exploratory data analysis.

| Type | Mark | Purpose |
|------|------|------|
| Box Plot | `boxplot` | Data distribution statistics |
| Box Chart (Box) | `box` | Manually specified five-number summary box plot |
| Density Plot | `density` | Kernel density estimation curve |
| Violin Plot | `density` + `boxplot` | Density distribution + statistical info |
| Polygon | `polygon` | Custom polygon area |

> **Detailed Documentation**: [Box Plot](references/marks/g2-mark-boxplot.md) | [Box Chart (Box)](references/marks/g2-mark-box-boxplot.md) | [Density Plot](references/marks/g2-mark-density.md) | [Violin Plot](references/marks/g2-mark-violin.md) | [Polygon](references/marks/g2-mark-polygon.md)

### 6.9 Relation Charts / Relation

Charts showing relationships between data, suitable for network analysis and set relationship display.

| Type | Mark | Purpose |
|------|------|------|
| Sankey Diagram | `sankey` | Flow/transfer relationship |
| Chord Diagram | `chord` | Matrix flow relationship |
| Venn Diagram | `path` + venn data transform | Set intersection relationship (venn is data transform, not mark type) |
| Arc Diagram | `line` + `point` | Node link relationship |

> **Detailed Documentation**: [Sankey Diagram](references/marks/g2-mark-sankey.md) | [Chord Diagram](references/marks/g2-mark-chord.md) | [Venn Diagram](references/marks/g2-mark-venn.md) | [Arc Diagram](references/marks/g2-mark-arc-diagram.md)

### 6.10 Project Management Charts / Project

Charts suitable for project management and progress tracking.

| Type | Mark | Purpose |
|------|------|------|
| Gantt Chart | `interval` | Task time scheduling |
| Bullet Chart | `interval` + `point` | KPI indicator display |

> **Detailed Documentation**: [Gantt Chart](references/marks/g2-mark-gantt.md) | [Bullet Chart](references/marks/g2-mark-bullet.md)

### 6.11 Financial Charts / Finance

Professional charts suitable for financial data analysis.

| Type | Mark | Purpose |
|------|------|------|
| K-Line Chart | `link` + `interval` | Stock four-price data |

> **Detailed Documentation**: [K-Line Chart](references/marks/g2-mark-k-chart.md)

### 6.12 Multivariate Data Charts / Multivariate

Charts showing multivariate data relationships.

| Type | Mark | Purpose |
|------|------|------|
| Parallel Coordinates | `line` | Multivariate data relationship analysis |
| Radar Chart | `line` | Multivariate data comparison |

> **Detailed Documentation**: [Parallel Coordinates](references/marks/g2-mark-parallel.md) | [Radar Chart](references/marks/g2-mark-radar.md)

### 6.13 Comparison Charts / Comparison

Charts suitable for data comparison.

| Type | Mark | Purpose |
|------|------|------|
| Bidirectional Bar Chart | `interval` | Positive/negative data comparison |

> **Detailed Documentation**: [Bidirectional Bar Chart](references/marks/g2-mark-bi-directional-bar.md)

### 6.14 Basic Marks / Basic Marks

Basic marks are the underlying building blocks of G2, can be used independently or combined to build complex charts.

| Type | Mark | Purpose |
|------|------|------|
| Rectangle | `rect` | Rectangular area, histogram/heatmap basis |
| Text | `text` | Text annotation and labels |
| Image | `image` | Image mark, data points represented by images |
| Path | `path` | Custom path drawing |
| Link | `link` | Connecting line between two points |
| Connector | `connector` | Connecting line between data points |
| Shape | `shape` | Custom shape drawing |
| Vector | `vector` | Vector/arrow mark, wind field charts etc. |

> **Detailed Documentation**: [rect](references/marks/g2-mark-rect.md) | [text](references/marks/g2-mark-text.md) | [image](references/marks/g2-mark-image.md) | [path](references/marks/g2-mark-path.md) | [link](references/marks/g2-mark-link.md) | [connector](references/marks/g2-mark-connector.md) | [shape](references/marks/g2-mark-shape.md) | [vector](references/marks/g2-mark-vector.md)

### 6.15 Range Marks / Range

Range marks are used to show data interval ranges.

| Type | Mark | Purpose |
|------|------|------|
| Time Period/Interval Highlight (X direction) | `rangeX` | X axis interval, `encode: { x: 'start', x1: 'end' }` |
| Value Range Highlight (Y direction) | `rangeY` | Y axis interval, `encode: { y: 'min', y1: 'max' }` |
| 2D Rectangular Area | `range` | x/y fields are `[start,end]` array, `encode: { x:'x', y:'y' }`, rarely used |

> **Detailed Documentation**: [range/rangeY](references/marks/g2-mark-range-rangey.md) | [rangeX](references/marks/g2-mark-rangex.md)

### 6.16 Distribution & Pack Charts / Distribution & Pack

| Type | Mark | Purpose |
|------|------|------|
| Beeswarm Chart | `point` + `pack` | Data points tightly arranged to show distribution |
| Pack Chart | `pack` | Circular packing of hierarchical data |

> **Detailed Documentation**: [Beeswarm Chart](references/marks/g2-mark-beeswarm.md) | [Pack Chart](references/marks/g2-mark-pack.md)

### 6.17 Hierarchy Charts / Hierarchy

Charts showing hierarchical data, represent numerical proportion through area or radius.

| Type | Mark | Purpose |
|------|------|------|
| Treemap | `treemap` | Hierarchical data proportion |
| Sunburst | `sunburst`⚠️ | Multi-level concentric circle display (requires importing @antv/g2-extension-plot) |
| Partition | `partition` | Hierarchical data partition display |
| Tree | `tree` | Tree hierarchical structure |

> **Detailed Documentation**: [Treemap](references/marks/g2-mark-treemap.md) | [Sunburst](references/marks/g2-mark-sunburst.md) | [Partition](references/marks/g2-mark-partition.md) | [Tree](references/marks/g2-mark-tree.md)

### 6.18 Other Charts / Others

| Type | Mark | Purpose |
|------|------|------|
| Heatmap | `cell` | 2D matrix data visualization |
| Density Heatmap | `heatmap` | Continuous density heatmap |
| Gauge | `gauge` | Indicator progress display |
| Word Cloud | `wordCloud` | Text frequency visualization |
| Liquid | `liquid` | Percentage progress |

> **Detailed Documentation**: [Heatmap](references/marks/g2-mark-cell-heatmap.md) | [Density Heatmap](references/marks/g2-mark-heatmap.md) | [Gauge](references/marks/g2-mark-gauge.md) | [Word Cloud](references/marks/g2-mark-wordcloud.md) | [Liquid](references/marks/g2-mark-liquid.md)

---

## 7. Data / Data Transforms

Data transforms are executed at the data loading stage, configured in `data.transform`, affecting all marks using that data.

### 7.1 Data Transform Types (configured in `data.transform`)

| Transform | Type | Purpose | Example Scenario |
|------|------|------|---------|
| **fold** | `fold` | Wide table to long table | Multi-column data to multi-series |
| **filter** | `filter` | Filter data by condition | Filter invalid data |
| **sort** | `sort` | Sort using callback function | Custom sorting logic |
| **sortBy** | `sortBy` | Sort by field | Sort by field value |
| **map** | `map` | Data mapping conversion | Add calculated fields |
| **join** | `join` | Merge data tables | Associate external data |
| **pick** | `pick` | Select specified fields | Simplify fields |
| **rename** | `rename` | Rename fields | Field renaming |
| **slice** | `slice` | Slice data range | Pagination/slicing |
| **ema** | `ema` | Exponential moving average | Time series smoothing |
| **kde** | `kde` | Kernel density estimation | Density chart/Violin chart |
| **log** | `log` | Print data to console | Debugging |
| **custom** | `custom` | Custom data processing | Complex transformation |

### 7.2 Data Formats and Patterns

| Type | Purpose |
|------|------|
| Tabular Data Format | Standard tabular data format description accepted by G2 |
| Data Transform Patterns | Combination usage patterns of Data Transform and Mark Transform |

> **Detailed Documentation**: [filter](references/data/g2-data-filter.md) | [sort](references/data/g2-data-sort.md) | [sortBy](references/data/g2-data-sortby.md) | [fold](references/data/g2-data-fold.md) | [slice](references/data/g2-data-slice.md) | [ema](references/data/g2-data-ema.md) | [kde](references/data/g2-data-kde.md) | [log](references/data/g2-data-log.md) | [fetch](references/data/g2-data-fetch.md) | [Tabular Data Format](references/data/g2-data-format-tabular.md) | [Data Transform Patterns](references/data/g2-data-transform-patterns.md)

### 7.3 Common Mistake: Data Transform in Wrong Position

```javascript
// ❌ Error: fold is data transform, cannot be placed in mark transform
chart.options({
  type: 'interval',
  data: wideData,
  transform: [{ type: 'fold', fields: ['a', 'b'] }], // ❌ Error!
});
// ✅ Correct: fold placed in data.transform
chart.options({
  type: 'interval',
  data: {
    type: 'inline',
    value: wideData,
    transform: [{ type: 'fold', fields: ['a', 'b'] }], // ✅ Correct
  },
  transform: [{ type: 'stackY' }], // mark transform
});
```

### 7.4 Combination Example: Wide Table Data + Stacked Chart

```javascript
// Wide table data: multiple type data columns for each month
const wideData = [
  { year: '2000', 'Type A': 21, 'Type B': 16, 'Type C': 8 },
  { year: '2001', 'Type A': 25, 'Type B': 16, 'Type C': 8 },
  // ...
];
chart.options({
  type: 'interval',