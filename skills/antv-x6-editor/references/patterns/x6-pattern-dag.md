---
id: "x6-pattern-dag"
title: "X6 DAG (Directed Acyclic Graph)"
description: |
  Best practices for building DAG (Directed Acyclic Graph) using X6.
  Suitable for data pipelines, CI/CD pipelines, task dependencies, and more.

library: "x6"
version: "3.x"
category: "patterns"
subcategory: "dag"
tags:
  - "DAG"
  - "Directed Acyclic Graph"
  - "Data Pipeline"
  - "pipeline"
  - "CI/CD"
  - "Task Dependencies"
  - "Data Lineage"
  - "ETL"
  - "Port Connections"

related:
  - "x6-core-ports"
  - "x6-core-edge"
  - "x6-core-node"
  - "x6-plugins"

use_cases:
  - "Creating data processing pipeline diagrams"
  - "CI/CD pipeline visualization"
  - "Task dependency graphs"
  - "Data lineage analysis diagrams"

difficulty: "intermediate"
completeness: "full"
---

## DAG Core Features

- **Directed**: Edges have a direction, flowing from upstream to downstream
- **Acyclic**: No cyclic dependencies exist
- **Port Connection**: Connections are established through in/out Ports
- **Horizontal/Vertical Layout**: Typically flows horizontally (left→right) or vertically (top→bottom)

## DAG Node Registration

```javascript
import { Graph } from '@antv/x6';

Graph.registerNode('dag-node', {
  inherit: 'rect',
  width: 140,
  height: 50,
  attrs: {
    body: { stroke: '#8f8f8f', strokeWidth: 1, fill: '#fff', rx: 6, ry: 6 },
  },
  ports: {
    groups: {
      in: {
        position: 'left',
        attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
      },
      out: {
        position: 'right',
        attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
      },
    },
  },
}, true);
```

## Complete DAG Example

Below is a standard, directly executable DAG data pipeline example. Regardless of whether the user provides a reference JSON, the output should be complete, runnable code, with each node assigned an independent variable name.

```javascript
import { Graph } from '@antv/x6';

Graph.registerNode('dag-node', {
  inherit: 'rect',
  width: 140,
  height: 48,
  attrs: {
    body: { fill: '#fff', stroke: '#5F95FF', strokeWidth: 1, rx: 6, ry: 6 },
    label: { fontSize: 13, fill: '#333' },
  },
  ports: {
    groups: {
      in: { position: 'left', attrs: { circle: { r: 5, magnet: true, stroke: '#5F95FF', fill: '#fff', strokeWidth: 1 } } },
      out: { position: 'right', attrs: { circle: { r: 5, magnet: true, stroke: '#5F95FF', fill: '#fff', strokeWidth: 1 } } },
    },
  },
}, true);

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 500,
  background: { color: '#F2F7FA' },
  grid: { visible: true, size: 10 },
  connecting: {
    allowBlank: false,
    allowLoop: false,
    allowMulti: false,
    router: 'orth',
    connector: 'rounded',
    createEdge() {
      return this.createEdge({
        attrs: { line: { stroke: '#5F95FF', strokeWidth: 1, targetMarker: 'classic' } },
      });
    },
    validateConnection({ sourcePort, targetPort }) {
      return sourcePort !== targetPort;
    },
  },
});

const extract = graph.addNode({ shape: 'dag-node', x: 40, y: 100, label: 'MySQL Source', ports: { items: [{ id: 'out-1', group: 'out' }] } });
const transform = graph.addNode({ shape: 'dag-node', x: 260, y: 60, label: 'Data Clean', ports: { items: [{ id: 'in-1', group: 'in' }, { id: 'out-1', group: 'out' }] } });
const aggregate = graph.addNode({ shape: 'dag-node', x: 260, y: 160, label: 'Aggregate', ports: { items: [{ id: 'in-1', group: 'in' }, { id: 'out-1', group: 'out' }] } });
const load = graph.addNode({ shape: 'dag-node', x: 500, y: 120, label: 'Write to DW', ports: { items: [{ id: 'in-1', group: 'in' }, { id: 'in-2', group: 'in' }] } });

graph.addEdge({ source: { cell: extract, port: 'out-1' }, target: { cell: transform, port: 'in-1' }, attrs: { line: { stroke: '#5F95FF', strokeWidth: 1, targetMarker: 'classic' } } });
graph.addEdge({ source: { cell: extract, port: 'out-1' }, target: { cell: aggregate, port: 'in-1' }, attrs: { line: { stroke: '#5F95FF', strokeWidth: 1, targetMarker: 'classic' } } });
graph.addEdge({ source: { cell: transform, port: 'out-1' }, target: { cell: load, port: 'in-1' }, attrs: { line: { stroke: '#5F95FF', strokeWidth: 1, targetMarker: 'classic' } } });
graph.addEdge({ source: { cell: aggregate, port: 'out-1' }, target: { cell: load, port: 'in-2' }, attrs: { line: { stroke: '#5F95FF', strokeWidth: 1, targetMarker: 'classic' } } });
```

## Generate DAG from User Data

When users provide node/edge reference data (e.g., JSON arrays), **do not directly copy JSON fields**, as user data often mistakenly uses port IDs as node IDs or lacks complete `ports` configuration. The correct approach is:

1. Create separate variables for each node based on semantics (e.g., `source1`, `etl`, `warehouse`).
2. Explicitly add `shape: 'dag-node'` and `ports.items` in `addNode`.
3. Use the `{ cell: nodeVar, port: '...' }` object format for edges, and avoid using string IDs.
4. Always output complete, executable code, and avoid returning empty or pseudocode.

```javascript
// Counterexample: Do not directly iterate over user JSON as node configuration
// Positive example: Rebuild nodes and edges based on semantics
const etl = graph.addNode({
  shape: 'dag-node',
  x: 260,
  y: 90,
  label: 'ETL Transform',
  ports: {
    items: [
      { id: 'in1', group: 'in' },
      { id: 'in2', group: 'in' },
      { id: 'out1', group: 'out' },
    ],
  },
});
```

## DAG Node with Status

```javascript
const statusColors = {
  pending: { stroke: '#8f8f8f', fill: '#fff' },
  running: { stroke: '#1890ff', fill: '#e6f7ff' },
  success: { stroke: '#52c41a', fill: '#f6ffed' },
  failed: { stroke: '#f5222d', fill: '#fff1f0' },
};

function setNodeStatus(node, status) {
  const colors = statusColors[status];
  node.attr('body/stroke', colors.stroke);
  node.attr('body/fill', colors.fill);
  node.setData({ status });
}
```

## Connection Validation (Preventing Loops)

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    allowBlank: false,
    allowLoop: false,
    router: 'orth',
    connector: 'rounded',
    validateConnection({ sourceCell, targetCell }) {
      // Prevent self-connection
      if (sourceCell === targetCell) return false;
      // Check if a loop would be formed (simple implementation)
      const edges = graph.getEdges();
      // ... Topological sorting to detect loops
      return true;
    },
  },
});
```

## Data Lineage Graph (Multi-Layer DAG)

Data lineage is a typical application of DAG, showcasing the flow of data from source tables to final reports:

```javascript
// Use smooth connector instead of orth, more suitable for multi-layer fan-out scenarios
graph.addEdge({
  source: { cell: srcNode, port: 'out1' },
  target: { cell: tgtNode, port: 'in1' },
  connector: 'smooth',
  attrs: { line: { stroke: '#8f8f8f', strokeWidth: 1 } },
});
```

Layer recommendations:
- **ODS Layer**: Original data source (white background)
- **DWD Layer**: Detailed data (light blue `#e6f7ff`)
- **DWS Layer**: Aggregated data (light green `#f6ffed`)
- **ADS Layer**: Application data (light orange `#fff7e6`)

## Common Errors and Fixes

### 1. Returns empty code (no code)

**Error Manifestation**: After the user provides reference JSON data, the model does not output any code.  
**Cause**: The model is confused by incomplete fields or port/node IDs in the data, leading to abandonment of code generation.  
**Fix**: Always output complete, runnable code based on the standard DAG template. Ignore potentially incorrect `id` fields in the user's JSON, create independent variables based on node semantics, and explicitly configure `ports.items`.

```javascript
// ❌ Error: No code generated, or only data comments are output
// ✅ Correct: Directly output complete code
const source1 = graph.addNode({
  shape: 'dag-node', x: 40, y: 40, label: 'MySQL Source',
  ports: { items: [{ id: 'out1', group: 'out' }] },
});
```

### 2. Incorrect Edge Connection Format

**Error Manifestation**: `source: 'source1'` or `source: { cell: 'source1' }` (string ID).  
**Correction**: Must use node variable reference + port ID object.

```javascript
// ❌ Incorrect
graph.addEdge({ source: 'source1', target: 'etl' });

// ✅ Correct
graph.addEdge({
  source: { cell: source1, port: 'out1' },
  target: { cell: etl, port: 'in1' },
  attrs: { line: { stroke: '#1890ff', strokeWidth: 1, targetMarker: 'classic' } },
});
```

### 3. Missing Port Configuration in Nodes

**Error Description**: Only `shape` and `label` are specified when using `addNode`, without `ports`.  
**Fix**: DAGs must be connected through ports. Each node must declare `ports: { items: [...] }` when using `addNode`, and specify either `group: 'in'` or `group: 'out'`.

```javascript
// ❌ Incorrect
graph.addNode({ shape: 'dag-node', label: 'ETL' });

// ✅ Correct
graph.addNode({
  shape: 'dag-node',
  label: 'ETL',
  ports: {
    items: [
      { id: 'in1', group: 'in' },
      { id: 'out1', group: 'out' },
    ],
  },
});
```

### 4. Port ID and Node Variable Name Confusion

**Error Manifestation**: Mistaking `"id": "out1"` in the user's JSON as the node ID, resulting in all node IDs being duplicated or losing their semantic meaning.  
**Correction**: `out1`/`in1` should be used as **port IDs** within `ports.items`; the node itself should use a meaningful variable name (e.g., `source1`, `etl`, `warehouse`).

```javascript
// ✅ Correct Distinction
const warehouse = graph.addNode({
  shape: 'dag-node',
  label: 'Data Warehouse',
  ports: { items: [{ id: 'in1', group: 'in' }, { id: 'out1', group: 'out' }] },
});
```

### 5. Incorrect Use of the addPorts Method

**Error Manifestation**: Calling `addPorts` to add ports after `addNode`, instead of declaring `ports.items` all at once during the `addNode` stage.  
**Correction**: Declare `ports.items` directly when calling `addNode` to avoid manually adding ports later.

```javascript
// ❌ Incorrect
const node = graph.addNode({ shape: 'dag-node', label: 'Node' });
node.addPorts([{ id: 'in1', group: 'in' }]);

// ✅ Correct
const node = graph.addNode({
  shape: 'dag-node',
  label: 'Node',
  ports: { items: [{ id: 'in1', group: 'in' }] },
});
```

### 6. Using String IDs as Cell References

**Incorrect Behavior**: Using string IDs instead of node variable references in edge connections.  
**Correction**: Must use node variable references + port ID objects.

```javascript
// ❌ Incorrect
graph.addEdge({ source: { cell: 'source1', port: 'out1' }, target: { cell: 'etl', port: 'in1' } });

// ✅ Correct
graph.addEdge({ source: { cell: source1, port: 'out1' }, target: { cell: etl, port: 'in1' } });
```

### 7. Error Caused by Introducing Extra Dependencies

**Error Manifestation**: Introducing `Shape` or other non-essential modules, resulting in loading failure.  
**Fix**: Only import `Graph` to avoid unnecessary module imports.

```javascript
// ❌ Incorrect
import { Graph, Shape } from '@antv/x6'

// ✅ Correct
import { Graph } from '@antv/x6';
```

### 8. Incorrect Usage of addNode + addPorts Pattern

**Error Manifestation**: Using `addNode` first and then `addPorts`, instead of declaring `ports.items` directly within `addNode`.  
**Correction**: Declare `ports.items` directly when calling `addNode`.

```javascript
// ❌ Incorrect
const node = graph.addNode({ shape: 'dag-node', label: 'Node' });
node.addPorts([{ id: 'in1', group: 'in' }]);

// ✅ Correct
const node = graph.addNode({
  shape: 'dag-node',
  label: 'Node',
  ports: { items: [{ id: 'in1', group: 'in' }] },
});
```

### 9. Incorrect Use of `ports` Array Instead of `items` Object

**Error Manifestation**: Using `ports: [{ id: 'out', group: 'out' }]` in `addNode` instead of `ports: { items: [...] }`.  
**Correction**: Must use the `ports: { items: [...] }` format; otherwise, ports will not render correctly.

```javascript
// ❌ Incorrect
graph.addNode({
  shape: 'dag-node',
  label: 'Node',
  ports: [{ id: 'out', group: 'out' }]
});

// ✅ Correct
graph.addNode({
  shape: 'dag-node',
  label: 'Node',
  ports: { items: [{ id: 'out', group: 'out' }] }
});
```

### 10. Incorrect Use of createEdge Method Introducing Extra Dependencies

**Error Manifestation**: Using `Shape.Edge` in `connecting.createEdge` results in introducing extra dependencies.  
**Correction**: Avoid using `Shape.Edge` and directly use the default edge configuration.

```javascript
// ❌ Incorrect
connecting: {
  createEdge() {
    return new Shape.Edge({
      attrs: { line: { stroke: '#A2B1C3' } }
    });
  }
}

// ✅ Correct
connecting: {
  // No need to customize createEdge
}
```

### 11. Incorrect use of ports array format instead of items object format

**Error Manifestation**: Using `ports: [{ id: 'out1', group: 'out' }]` in `addNode` instead of `ports: { items: [...] }`.  
**Correction**: Must use `ports: { items: [...] }` format, otherwise ports cannot be rendered correctly.

```javascript
// ❌ Incorrect
graph.addNode({
  shape: 'dag-node',
  label: 'Node',
  ports: [{ id: 'out1', group: 'out' }]
});

// ✅ Correct
graph.addNode({
  shape: 'dag-node',
  label: 'Node',
  ports: { items: [{ id: 'out1', group: 'out' }] }
});
```

### 12. Incorrect Use of addPorts Method to Add Ports

**Error Manifestation**: Calling `addPorts` to add ports after `addNode`, instead of declaring `ports.items` all at once during the `addNode` stage.  
**Correction**: Declare `ports.items` directly when calling `addNode` to avoid manually adding ports later.

```javascript
// ❌ Incorrect
const node = graph.addNode({ shape: 'dag-node', label: 'Node' });
node.addPorts([{ id: 'in1', group: 'in' }]);

// ✅ Correct
const node = graph.addNode({
  shape: 'dag-node',
  label: 'Node',
  ports: { items: [{ id: 'in1', group: 'in' }] },
});
```

### 13. Incorrect Use of Plugin Introduction Method

**Error Manifestation**: Introducing plugins via `plugins: [new Selection(...)]` results in incorrect initialization.  
**Correction**: Plugins should be introduced using `graph.use(new Plugin(...))`.

```javascript
// ❌ Incorrect
const graph = new Graph({
  plugins: [
    new Selection({ enabled: true }),
  ],
});

// ✅ Correct
import { Selection } from '@antv/x6-plugin-selection';
const graph = new Graph({ /* ... */ });
graph.use(new Selection({ enabled: true }));
```

### 14. Incorrect use of createEdge returning this.createEdge

**Error Manifestation**: Returning `this.createEdge(...)` in `createEdge` causes a recursive call stack overflow.  
**Fix**: Directly return `graph.createEdge(...)` or use `new Edge(...)`.

```javascript
// ❌ Incorrect
createEdge() {
  return this.createEdge({ ... });
}

// ✅ Correct
createEdge() {
  return graph.createEdge({ ... });
}
```