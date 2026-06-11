---
id: "x6-pattern-lineage"
title: "X6 Lineage Graph (Data Lineage)"
description: |
  Best practices for building data lineage graphs using X6: multiple input/output ports, hierarchical layout, table field-level lineage relationships, collapse/expand functionality, and more.

library: "x6"
version: "3.x"
category: "patterns"
subcategory: "lineage"
tags:
  - "lineage graph"
  - "lineage"
  - "data lineage"
  - "data lineage"
  - "table relationships"
  - "field-level lineage"
  - "DAG"

related:
  - "x6-pattern-dag"
  - "x6-core-ports"
  - "x6-core-edge"
  - "x6-intermediate-custom-node"
  - "x6-intermediate-layout"

use_cases:
  - "Data warehouse table-level lineage"
  - "Field-level lineage tracking"
  - "ETL data flow"
  - "Data asset lineage relationships"

difficulty: "advanced"
completeness: "full"
---

## Scene Characteristics

Core features of the data lineage graph:
- **Table Nodes**: Each node represents a table/dataset, displaying a list of fields internally
- **Field-Level Connections**: Connections precisely link source table fields to target table fields (port to port)
- **Left-to-Right Layout**: Data flow from upstream to downstream, typically using LR (Left-to-Right) layout
- **Multi-Ports**: Each node has multiple input/output ports (corresponding to fields)
- **Orthogonal Routing**: Connections use orthogonal routing to avoid crossing

## Register Custom Table Node

```javascript
const { Graph } = X6;

// Register lineage table node
Graph.registerNode('lineage-table', {
  inherit: 'rect',
  width: 220,
  height: 60,
  attrs: {
    body: {
      fill: '#fff',
      stroke: '#d9d9d9',
      strokeWidth: 1,
      rx: 4,
      ry: 4,
    },
    label: {
      fontSize: 14,
      fontWeight: 'bold',
      fill: '#333',
      refY: 14,
      refX: 0.5,
    },
  },
  ports: {
    groups: {
      in: {
        position: 'left',
        label: { position: 'inside' },
        attrs: {
          circle: { r: 4, magnet: true, stroke: '#31d0c6', fill: '#fff', strokeWidth: 1.5 },
        },
      },
      out: {
        position: 'right',
        label: { position: 'inside' },
        attrs: {
          circle: { r: 4, magnet: true, stroke: '#ff6347', fill: '#fff', strokeWidth: 1.5 },
        },
      },
    },
  },
}, true);
```

## Complete Example: Three-Table Lineage

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>X6 Data Lineage Diagram Example</title>
  <style>
    #container {
      width: 1000px;
      height: 600px;
      border: 1px solid #d9d9d9;
    }
  </style>
</head>
<body>
  <div id="container"></div>
  <script src="https://unpkg.com/@antv/x6/dist/x6.js"></script>
  <script>
    const { Graph } = X6;

    const graph = new Graph({
      container: document.getElementById('container'),
      width: 1000,
      height: 600,
      background: { color: '#F2F7FA' },
      grid: { visible: true, size: 10 },
      panning: { enabled: true, modifiers: 'ctrl' },
      mousewheel: { enabled: true, modifiers: 'ctrl' },
      connecting: {
        allowBlank: false,
        router: 'orth',
        connector: 'rounded',
      },
    });

    // Source Table
    const sourceTable = graph.addNode({
      shape: 'rect',
      x: 50,
      y: 100,
      width: 200,
      height: 130,
      label: 'user_orders',
      attrs: {
        body: { fill: '#fff', stroke: '#5F95FF', strokeWidth: 1.5, rx: 6, ry: 6 },
        label: { fontSize: 14, fontWeight: 'bold', fill: '#333', refY: 16, refX: 0.5 },
      },
      ports: {
        groups: {
          out: {
            position: 'right',
            attrs: { circle: { r: 4, magnet: true, stroke: '#5F95FF', fill: '#EFF4FF' } },
          },
        },
        items: [
          { id: 'user_id', group: 'out', attrs: { text: { text: 'user_id' } } },
          { id: 'order_id', group: 'out', attrs: { text: { text: 'order_id' } } },
          { id: 'amount', group: 'out', attrs: { text: { text: 'amount' } } },
          { id: 'order_date', group: 'out', attrs: { text: { text: 'order_date' } } },
        ],
      },
    });

    // Intermediate ETL Node
    const etlNode = graph.addNode({
      shape: 'rect',
      x: 380,
      y: 130,
      width: 200,
      height: 100,
      label: 'agg_user_stats',
      attrs: {
        body: { fill: '#fff', stroke: '#73d13d', strokeWidth: 1.5, rx: 6, ry: 6 },
        label: { fontSize: 14, fontWeight: 'bold', fill: '#333', refY: 16, refX: 0.5 },
      },
      ports: {
        groups: {
          in: {
            position: 'left',
            attrs: { circle: { r: 4, magnet: true, stroke: '#73d13d', fill: '#f6ffed' } },
          },
          out: {
            position: 'right',
            attrs: { circle: { r: 4, magnet: true, stroke: '#73d13d', fill: '#f6ffed' } },
          },
        },
        items: [
          { id: 'in_user_id', group: 'in', attrs: { text: { text: 'user_id' } } },
          { id: 'in_amount', group: 'in', attrs: { text: { text: 'amount' } } },
          { id: 'out_user_id', group: 'out', attrs: { text: { text: 'user_id' } } },
          { id: 'out_total', group: 'out', attrs: { text: { text: 'total_amount' } } },
        ],
      },
    });

    // Target Table
    const targetTable = graph.addNode({
      shape: 'rect',
      x: 700,
      y: 150,
      width: 200,
      height: 80,
      label: 'report_summary',
      attrs: {
        body: { fill: '#fff', stroke: '#ff7a45', strokeWidth: 1.5, rx: 6, ry: 6 },
        label: { fontSize: 14, fontWeight: 'bold', fill: '#333', refY: 16, refX: 0.5 },
      },
      ports: {
        groups: {
          in: {
            position: 'left',
            attrs: { circle: { r: 4, magnet: true, stroke: '#ff7a45', fill: '#fff7e6' } },
          },
        },
        items: [
          { id: 'in_uid', group: 'in', attrs: { text: { text: 'user_id' } } },
          { id: 'in_total', group: 'in', attrs: { text: { text: 'total' } } },
        ],
      },
    });

    // Field-Level Connections
    graph.addEdge({
      source: { cell: sourceTable.id, port: 'user_id' },
      target: { cell: etlNode.id, port: 'in_user_id' },
      attrs: { line: { stroke: '#5F95FF', strokeWidth: 1.5 } },
      router: 'orth',
      connector: 'rounded',
    });

    graph.addEdge({
      source: { cell: sourceTable.id, port: 'amount' },
      target: { cell: etlNode.id, port: 'in_amount' },
      attrs: { line: { stroke: '#5F95FF', strokeWidth: 1.5 } },
      router: 'orth',
      connector: 'rounded',
    });

    graph.addEdge({
      source: { cell: etlNode.id, port: 'out_user_id' },
      target: { cell: targetTable.id, port: 'in_uid' },
      attrs: { line: { stroke: '#73d13d', strokeWidth: 1.5 } },
      router: 'orth',
      connector: 'rounded',
    });

    graph.addEdge({
      source: { cell: etlNode.id, port: 'out_total' },
      target: { cell: targetTable.id, port: 'in_total' },
      attrs: { line: { stroke: '#73d13d', strokeWidth: 1.5 } },
      router: 'orth',
      connector: 'rounded',
    });
  </script>
</body>
</html>
```

## Highlight Lineage Path

When clicking on a field, highlight its complete upstream and downstream linkage:

```javascript
graph.on('node:port:click', ({ node, port }) => {
  // Reset the style of all edges
  graph.getEdges().forEach((edge) => {
    edge.attr('line/stroke', '#d9d9d9');
    edge.attr('line/strokeWidth', 1);
  });

  // Highlight edges related to the port
  const relatedEdges = graph.getEdges().filter((edge) => {
    const source = edge.getSource();
    const target = edge.getTarget();
    return (source.cell === node.id && source.port === port) ||
           (target.cell === node.id && target.port === port);
  });

  relatedEdges.forEach((edge) => {
    edge.attr('line/stroke', '#1890ff');
    edge.attr('line/strokeWidth', 3);
  });
});
```

## Layout Recommendations

Use the dagre algorithm from `@antv/layout` to implement automatic LR layout:

```html
<script src="https://unpkg.com/@antv/layout@latest/dist/layout.min.js"></script>
<script>
  const { DagreLayout } = Layout;

  const dagreLayout = new DagreLayout({
    type: 'dagre',
    rankdir: 'LR',
    nodesep: 40,
    ranksep: 100,
  });

  const layoutData = dagreLayout.layout({
    nodes: graph.getNodes().map((n) => ({
      id: n.id,
      size: { width: n.getSize().width, height: n.getSize().height },
    })),
    edges: graph.getEdges().map((e) => ({
      source: e.getSourceCellId(),
      target: e.getTargetCellId(),
    })),
  });

  layoutData.nodes.forEach((n) => {
    const node = graph.getCellById(n.id);
    if (node) node.setPosition(n.x, n.y);
  });
</script>
```

## Best Practices

1. **Port ID Using Field Name**: Facilitates lineage tracking logic
2. **Orthogonal Routing + Rounded Connector**: `router: 'orth'`, `connector: 'rounded'`
3. **Layer-Based Coloring**: Source tables, intermediate tables, and target tables use different colors
4. **Dynamic Node Height Calculation**: Set `height = 40 + fields.length * 24` based on the number of fields
5. **Enable Virtual Rendering for Large-Scale Scenarios**: Configure `virtual: true` when there are more than 200 nodes

## Common Errors and Fixes

### Error 1: Using an Unregistered Node Type

**Error Code:**
```javascript
const node = graph.addNode({
  shape: 'dag-node', // Error: Unregistered node type
  label: 'Source Table',
});
```

**Error Message:**
```
Node with name 'dag-node' does not exist.
```

**Solution:**
Before using a custom node, you must register the node type. It is recommended to use `Graph.registerNode` to register custom nodes:

```javascript
Graph.registerNode('lineage-node', {
  inherit: 'rect',
  width: 130,
  height: 40,
  attrs: {
    body: { fill: '#fff', stroke: '#d9d9d9', strokeWidth: 1, rx: 4, ry: 4 },
    label: { fontSize: 12 },
  },
  ports: {
    groups: {
      in: { position: 'left', attrs: { circle: { r: 4, magnet: true, stroke: '#8f8f8f', fill: '#fff' } } },
      out: { position: 'right', attrs: { circle: { r: 4, magnet: true, stroke: '#8f8f8f', fill: '#fff' } } },
    },
  },
}, true);

const node = graph.addNode({
  shape: 'lineage-node', // Correct: Registered node type
  label: 'Source Table',
});
```

### Error 2: Incorrect API Usage for Layout

**Error Code:**
```javascript
import { DagreLayout } from '@antv/x6';
const layout = new DagreLayout({...});
const model = layout.layout(graph.toJSON());
graph.fromJSON(model);
```

**Error Message:**
```
TypeError: layout.layout is not a function
```

**Correction Method:**
Import `DagreLayout` from `@antv/layout` and use the correct layout approach:

```javascript
import { DagreLayout } from '@antv/layout';

const dagreLayout = new DagreLayout({
  type: 'dagre',
  rankdir: 'LR',
  align: 'UL',
  ranksep: 80,
  nodesep: 30,
});

const layoutData = dagreLayout.layout({
  nodes: graph.getNodes().map((n) => ({
    id: n.id,
    size: { width: n.getSize().width, height: n.getSize().height },
  })),
  edges: graph.getEdges().map((e) => ({
    source: e.getSourceCellId(),
    target: e.getTargetCellId(),
  })),
});

layoutData.nodes.forEach((n) => {
  const node = graph.getCellById(n.id);
  if (node) node.setPosition(n.x, n.y);
});
```

### Error 3: Using ES Module Import Syntax in Browser Environment

**Error Code:**
```javascript
import { Graph } from '@antv/x6'
import { DagreLayout } from '@antv/layout'
```

**Error Message:**
```
Cannot use import statement outside a module
```

**Solution:**
In a browser environment, use `<script>` tags to include the X6 and layout libraries, or use a bundler (such as Webpack, Vite) to handle module dependencies. If using script tags, ensure the correct import order and access APIs via global variables:

```html
<script src="https://unpkg.com/@antv/x6/dist/x6.js"></script>
<script src="https://unpkg.com/@antv/layout@latest/dist/layout.min.js"></script>
<script>
  const { Graph } = X6;
  const { DagreLayout } = Layout;

  Graph.registerNode('lineage-node', {
    inherit: 'rect',
    width: 130,
    height: 40,
    attrs: {
      body: { fill: '#fff', stroke: '#d9d9d9', strokeWidth: 1, rx: 4, ry: 4 },
      label: { fontSize: 12 },
    },
    ports: {
      groups: {
        in: { position: 'left', attrs: { circle: { r: 4, magnet: true, stroke: '#8f8f8f', fill: '#fff' } } },
        out: { position: 'right', attrs: { circle: { r: 4, magnet: true, stroke: '#8f8f8f', fill: '#fff' } } },
      },
    },
  }, true);

  const graph = new Graph({
    container: document.getElementById('container'),
    width: 800,
    height: 450,
    background: { color: '#F2F7FA' },
    panning: true,
    mousewheel: { enabled: true, modifiers: 'ctrl' },
  });

  // Add nodes and edges...
</script>
```

### Error 4: Module System Not Properly Configured in Browser Environment

**Error Code:**
```html
<script type="text/javascript">
  import { Graph } from '@antv/x6';
</script>
```

**Error Message:**
```
Cannot use import statement outside a module
```

**Solution:**
To use ES Module syntax in a browser, mark the script tag with `type="module"` and use the ESM version provided by CDN:

```html
<script type="module">
  import { Graph } from 'https://unpkg.com/@antv/x6?module';
  import { DagreLayout } from 'https://unpkg.com/@antv/layout?module';

  const graph = new Graph({
    container: document.getElementById('container'),
    width: 800,
    height: 450,
    background: { color: '#F2F7FA' },
  });

  // Add nodes and edges...
</script>
```

Alternatively, use the traditional IIFE method to include the library:

```html
<script src="https://unpkg.com/@antv/x6/dist/x6.js"></script>
<script>
  const { Graph } = X6;

  const graph = new Graph({
    container: document.getElementById('container'),
    width: 800,
    height: 450,
    background: { color: '#F2F7FA' },
  });

  // Add nodes and edges...
</script>
```

### Error 5: Container Element Not Properly Specified

**Error Code:**
```javascript
const graph = new Graph({
  container, // Error: `container` variable is undefined
  width: 800,
  height: 450,
});
```

**Error Message:**
```
Uncaught TypeError: Cannot read property 'appendChild' of undefined
```

**Fix:**
Ensure `container` is either a DOM element or a valid selector string:

```javascript
const graph = new Graph({
  container: document.getElementById('container'), // Correct: Retrieve DOM element
  width: 800,
  height: 450,
});
```

or:

```javascript
const graph = new Graph({
  container: 'container', // Correct: Use selector string
  width: 800,
  height: 450,
});
```

### Error 6: Incorrect Port Reference Usage

**Error Code:**
```javascript
graph.addEdge({
  source: { cell: sourceTable, port: 'out1' }, // Error: sourceTable is a Node instance, not an ID
  target: { cell: etl1, port: 'in1' },
});
```

**Error Message:**
```
Invalid source or target cell reference
```

**Correction Method:**
When creating an edge, `source.cell` and `target.cell` should be the node ID strings, not the node objects themselves:

```javascript
graph.addEdge({
  source: { cell: sourceTable.id, port: 'out1' }, // Correct: Use node ID
  target: { cell: etl1.id, port: 'in1' },
});
```

Alternatively, store the node IDs when adding nodes:

```javascript
const sourceTableId = graph.addNode({...}).id;
const etl1Id = graph.addNode({...}).id;

graph.addEdge({
  source: { cell: sourceTableId, port: 'out1' },
  target: { cell: etl1Id, port: 'in1' },
});
```