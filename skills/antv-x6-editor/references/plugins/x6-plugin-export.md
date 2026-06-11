---
id: "x6-plugin-export"
title: "X6 Export"
description: |
  A comprehensive guide to exporting X6 canvas content as SVG/PNG/JPEG images.
  Includes usage of the Export plugin, exportSVG, exportPNG, exportJPEG, toSVG, toPNG, toJPEG APIs.

library: "x6"
version: "3.x"
category: "plugins"
subcategory: "export"
tags:
  - "export"
  - "SVG"
  - "PNG"
  - "JPEG"
  - "image"
  - "screenshot"
  - "download"
  - "toSVG"
  - "toPNG"
  - "exportPNG"
  - "exportSVG"
  - "dataUri"

related:
  - "x6-core-graph-init"
  - "x6-plugins"

use_cases:
  - "Export canvas as an SVG file"
  - "Export canvas as a PNG image"
  - "Export canvas as a JPEG image"
  - "Get the canvas DataURI for preview"
  - "Control the resolution and background color of exported images"

anti_patterns:
  - "Don't forget to register the plugin by calling graph.use(new Export()) first"
  - "Be cautious of CORS issues when exporting images with cross-domain resources"
---

# X6 Export

(Note: The original content provided only contains a header. Below is the translation of the given content, adhering to the strict instructions.)

# X6 Export

## Register Plugin

The Export plugin needs to be registered before using the export functionality:

```javascript
import { Graph, Export } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
});

// Register the Export plugin
graph.use(new Export());
```

## Export to File (Auto Download)

### exportSVG — Export SVG File

```javascript
// Basic usage: Automatically download a file named "my-graph.svg"
graph.exportSVG('my-graph');

// With configuration
graph.exportSVG('my-graph', {
  preserveDimensions: true,  // SVG dimensions match the actual graph size
  copyStyles: true,          // Copy external styles
  serializeImages: true,     // Convert images to DataURI
});
```

### exportPNG — Export PNG File

```javascript
// Basic Usage
graph.exportPNG('my-graph');

// High-Resolution Export (2x Resolution)
graph.exportPNG('my-graph', {
  ratio: 2,
  backgroundColor: '#ffffff',
  padding: 20,
});
```

### exportJPEG — Export JPEG File

```javascript
graph.exportJPEG('my-graph', {
  ratio: 2,
  backgroundColor: '#ffffff',
  quality: 0.92,  // Image quality 0-1
});
```

## Get DataURI (Without Downloading)

When you need to obtain image data for preview, upload, and other scenarios, use the `to*` series of methods:

### toSVG

```javascript
graph.toSVG((dataUri) => {
  // dataUri is a data URI in SVG format
  console.log(dataUri);
}, {
  preserveDimensions: true,
});
```

### toPNG

```javascript
graph.toPNG((dataUri) => {
  // dataUri is a base64 data URI in PNG format
  // Can be used in img tags or for uploading
  const img = new Image();
  img.src = dataUri;
  document.body.appendChild(img);
}, {
  ratio: 2,
  backgroundColor: '#ffffff',
  padding: { top: 20, right: 20, bottom: 20, left: 20 },
});
```

### toJPEG

```javascript
graph.toJPEG((dataUri) => {
  console.log(dataUri);
}, {
  quality: 0.85,
  backgroundColor: '#ffffff',
});
```

## Configuration Options

### ToSVGOptions

| Configuration | Type | Default Value | Description |
|--------------|------|---------------|-------------|
| `preserveDimensions` | boolean \| Size | - | SVG dimensions: `true` for actual size, or pass `{ width, height }` |
| `viewBox` | RectangleLike | - | Custom viewBox |
| `copyStyles` | boolean | `true` | Whether to copy styles from external stylesheets |
| `stylesheet` | string | - | Custom CSS stylesheet |
| `serializeImages` | boolean | `true` | Whether to convert image href to DataURI |
| `beforeSerialize` | Function | - | Callback to modify SVG elements before export |

### ToImageOptions (Inherits from ToSVGOptions)

| Configuration | Type | Default | Description |
|---------------|------|---------|-------------|
| `width` | number | - | Exported image width |
| `height` | number | - | Exported image height |
| `ratio` | number | 1 | Scaling ratio (device pixel ratio) |
| `backgroundColor` | string | - | Background color |
| `padding` | number \| SideOptions | - | Inner padding |
| `quality` | number | 0.92 | JPEG quality (0-1) |

## Complete Example

```javascript
import { Graph, Export } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  background: { color: '#F2F7FA' },
  grid: { visible: true },
});

graph.use(new Export());

// Add nodes and edges
const source = graph.addNode({
  shape: 'rect',
  x: 40,
  y: 40,
  width: 120,
  height: 50,
  label: 'Source',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 } },
});

const target = graph.addNode({
  shape: 'rect',
  x: 300,
  y: 200,
  width: 120,
  height: 50,
  label: 'Target',
  attrs: { body: { fill: '#fff', stroke: '#8f8f8f', strokeWidth: 1, rx: 6, ry: 6 } },
});

graph.addEdge({
  source,
  target,
  router: 'orth',
  connector: 'rounded',
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1, targetMarker: 'classic' } },
});

// Export as PNG (2x resolution)
graph.exportPNG('flowchart', {
  ratio: 2,
  backgroundColor: '#ffffff',
  padding: 20,
});
```

## ⚠️ Key Constraints (Must Comply)

**All export methods (toPNG / toSVG / toJPEG / exportPNG / exportSVG / exportJPEG) require the Export plugin to be registered first**, otherwise it will throw `graph.toPNG is not a function`.

```javascript
// ✅ Correct export code template (these two lines must be included every time export code is generated)
import { Graph, Export } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Export());  // Must be called before any export method
```

**Prohibited Actions:**
- Do not call toPNG/toSVG/exportPNG methods without registering the Export plugin
- Do not use `graph.use(Export)` — must use `graph.use(new Export())`
- Do not call export methods before `graph.use(new Export())`

## Common Errors and Fixes

### ❌ Calling Export Method Without Registering the Export Plugin

```javascript
// Error: graph.toPNG is not a function / graph.exportPNG is not a function
import { Graph } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.toPNG((dataUri) => { console.log(dataUri); }); // TypeError

// Correct: Must import and register Export first
import { Graph, Export } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Export());
graph.toPNG((dataUri) => { console.log(dataUri); }); // ✅
```

### ❌ Missing Background Color During Export

```javascript
// Error: Exported image has no background (transparent)
graph.exportPNG('test');

// Correct: Specify background color
graph.exportPNG('test', { backgroundColor: '#ffffff' });
```

### ❌ No Callback Function Passed When Using toPNG/toSVG

```javascript
// Error: Direct call returns undefined
const dataUri = graph.toPNG(); // undefined

// Correct: Pass a callback function to receive the result (Async version can also be used)
graph.toPNG((dataUri) => { console.log(dataUri); });
// or
const dataUri = await graph.toPNGAsync({ backgroundColor: '#fff' });
```

### ❌ Initialize the Canvas Using DOM Container Reference Instead of ID String

```javascript
// Error: May cause container re-declaration in certain environments
const container = document.getElementById('container');
const graph = new Graph({ container });

// Recommended: Use string ID
const graph = new Graph({ container: 'container' });
```

### ❌ Calling graph.render() Causes an Error

```javascript
// Error: graph.render is not a function
graph.render();

// Correct: X6 Graph instances do not require manual calls to render()
// All nodes and edges are automatically rendered after being added
```

### ❌ Export method called before ensuring the plugin is registered

```javascript
// Error: Even if Export is imported, it will still throw an error if the plugin is not registered
import { Graph, Export } from '@antv/x6';
const graph = new Graph({ container: 'container' });
// Forgot to call graph.use(new Export());
graph.toPNG((dataUri) => { console.log(dataUri); }); // ❌ TypeError

// Correct: Ensure the plugin is registered
import { Graph, Export } from '@antv/x6';
const graph = new Graph({ container: 'container' });
graph.use(new Export()); // ✅ Must register the plugin
graph.toPNG((dataUri) => { console.log(dataUri); }); // ✅ Correct call
```

</skill>