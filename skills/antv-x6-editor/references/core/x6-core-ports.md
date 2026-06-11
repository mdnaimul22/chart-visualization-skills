---
id: "x6-core-ports"
title: "X6 Ports Configuration"
description: |
  Definition, grouping, positioning, styling, and dynamic visibility of X6 ports.
  Ports are connection anchors on nodes, used in DAG/flowchart scenarios.

library: "x6"
version: "3.x"
category: "core"
subcategory: "ports"
tags:
  - "ports"
  - "port"
  - "magnet"
  - "anchor"
  - "connection"
  - "position"
  - "group"
  - "dynamic ports"
  - "DAG"

related:
  - "x6-core-node"
  - "x6-core-edge"
  - "x6-core-graph-init"

use_cases:
  - "Adding ports to nodes"
  - "Configuring port groups and positions"
  - "Creating input/output ports for DAG nodes"
  - "Dynamically adding/removing ports"
  - "Displaying ports on mouse hover"

anti_patterns:
  - "Do not omit magnet: true, otherwise ports cannot be connected"
  - "Do not duplicate attrs defined in group within items"
  - "When Graph.registerNode declares ports.items, do not pass ports.items with the same id in addNode, as it will trigger Duplicated port id"
  - "The id added by node.addPort cannot have the same name as existing ports.items in registerNode/addNode"

difficulty: "intermediate"
completeness: "full"
---

## Basic Port Configuration

```javascript
graph.addNode({
  shape: 'rect',
  x: 100, y: 60,
  width: 120, height: 50,
  label: 'DAG Node',
  ports: {
    groups: {
      in: {
        position: 'left',
        attrs: {
          circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' },
        },
      },
      out: {
        position: 'right',
        attrs: {
          circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' },
        },
      },
    },
    items: [
      { id: 'in1', group: 'in' },
      { id: 'out1', group: 'out' },
    ],
  },
});
```

## Port Position

| position | Description |
|----------|-------------|
| `'top'` | Centered at the top |
| `'bottom'` | Centered at the bottom |
| `'left'` | Centered on the left |
| `'right'` | Centered on the right |

Multiple ports in the same group will be automatically distributed evenly:

```javascript
ports: {
  groups: {
    in: { position: 'top' },
    out: { position: 'bottom' },
  },
  items: [
    { id: 'in1', group: 'in' },
    { id: 'in2', group: 'in' },   // Two top ports will be evenly distributed
    { id: 'out1', group: 'out' },
  ],
}
```

## Connect via Ports

```javascript
// Edge connects to specified ports
graph.addEdge({
  source: { cell: node1, port: 'out1' },
  target: { cell: node2, port: 'in1' },
  attrs: { line: { stroke: '#1890ff', strokeWidth: 1, targetMarker: 'classic' } },
});

// Can also use node IDs
graph.addEdge({
  source: { cell: 'node-1', port: 'out1' },
  target: { cell: 'node-2', port: 'in1' },
});
```

## DAG Node Registration (Common Pattern)

```javascript
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

// When using, only need to specify items
graph.addNode({
  shape: 'dag-node',
  x: 100, y: 60,
  label: 'ETL Task',
  ports: { items: [{ id: 'in1', group: 'in' }, { id: 'out1', group: 'out' }] },
});
```

## Dynamic Port Operations

```javascript
// Add a port
node.addPort({ id: 'new-port', group: 'out' });

// Remove a port
node.removePort('port-id');

// Get all ports
const ports = node.getPorts();

// Check if a port exists
const hasPort = node.hasPort('port-id');
```

## Display Ports on Mouse Hover

```javascript
const graph = new Graph({
  container: 'container',
});

// Ports are hidden by default
graph.addNode({
  shape: 'rect',
  x: 100, y: 60,
  width: 120, height: 50,
  ports: {
    groups: {
      in: {
        position: 'left',
        attrs: {
          circle: {
            magnet: true, r: 5, stroke: '#1890ff', fill: '#fff',
            style: { visibility: 'hidden' },
          },
        },
      },
      out: {
        position: 'right',
        attrs: {
          circle: {
            magnet: true, r: 5, stroke: '#1890ff', fill: '#fff',
            style: { visibility: 'hidden' },
          },
        },
      },
    },
    items: [{ id: 'in1', group: 'in' }, { id: 'out1', group: 'out' }],
  },
});

// Display ports on mouse enter
graph.on('node:mouseenter', ({ node }) => {
  node.getPorts().forEach((port) => {
    node.portProp(port.id, 'attrs/circle/style/visibility', 'visible');
  });
});

// Hide ports on mouse leave
graph.on('node:mouseleave', ({ node }) => {
  node.getPorts().forEach((port) => {
    node.portProp(port.id, 'attrs/circle/style/visibility', 'hidden');
  });
});
```

## Port Style Customization

```javascript
ports: {
  groups: {
    in: {
      position: 'top',
      attrs: {
        circle: {
          magnet: true,
          r: 6,
          stroke: '#52c41a',
          fill: '#f6ffed',
          strokeWidth: 2,
        },
      },
      label: {
        position: 'top',  // Label position
      },
    },
  },
  items: [
    { id: 'in1', group: 'in', attrs: { text: { text: 'input' } } },
  ],
}
```

## Connection Validation

Use the `connecting` configuration to restrict port connection rules:

```javascript
const graph = new Graph({
  container: 'container',
  connecting: {
    allowBlank: false,
    allowNode: false,        // Only allow connections to ports
    allowLoop: false,        // Prohibit self-loops
    validateConnection({ sourcePort, targetPort, sourceCell, targetCell }) {
      // Do not allow output ports to connect to output ports
      if (sourcePort && sourcePort.startsWith('out') && targetPort && targetPort.startsWith('out')) {
        return false;
      }
      // Do not allow connections to itself
      if (sourceCell === targetCell) return false;
      return true;
    },
  },
});
```

## Common Errors and Fixes

### Error 1: Ports Not Properly Grouped Resulting in Connection Failure

**Error Example:**
```javascript
// Error: Groups are not defined, directly using the group property
graph.addNode({
  shape: 'rect',
  x: 100, y: 60,
  width: 120, height: 50,
  ports: {
    items: [
      { id: 'port1', group: 'top' },  // group is not defined
      { id: 'port2', group: 'bottom' },
    ],
  },
});
```

**Correction Method:**
```javascript
// Correct: Define groups first, then reference them in items
graph.addNode({
  shape: 'rect',
  x: 100, y: 60,
  width: 120, height: 50,
  ports: {
    groups: {
      top: {
        position: 'top',
        attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
      },
      bottom: {
        position: 'bottom',
        attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
      },
    },
    items: [
      { id: 'port1', group: 'top' },
      { id: 'port2', group: 'bottom' },
    ],
  },
});
```

### Error 2: Port Not Set with Magnet, Resulting in Connection Failure

**Error Example:**
```javascript
// Error: Missing magnet: true
ports: {
  groups: {
    in: {
      position: 'left',
      attrs: { circle: { r: 5, stroke: '#1890ff', fill: '#fff' } }, // Missing magnet
    },
  },
  items: [{ id: 'in1', group: 'in' }],
}
```

**Correction Method:**
```javascript
// Correct: Set magnet: true
ports: {
  groups: {
    in: {
      position: 'left',
      attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
    },
  },
  items: [{ id: 'in1', group: 'in' }],
}
```

### Error 3: Port Style Settings Error Causing Display Anomalies

**Error Example:**
```javascript
// Error: Redundantly setting attrs in items that are already defined in the group
ports: {
  groups: {
    in: {
      position: 'left',
      attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
    },
  },
  items: [
    { id: 'in1', group: 'in', attrs: { circle: { r: 10 } } }, // Redundant setting of circle
  ],
}
```

**Correction Method:**
```javascript
// Correct: Avoid redundantly setting attrs in items that are already defined in the group
ports: {
  groups: {
    in: {
      position: 'left',
      attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
    },
  },
  items: [
    { id: 'in1', group: 'in' },
  ],
}
```

### Error 4: Connection Failure Due to Incorrect Node References When Creating Edges

**Error Example:**
```javascript
// Error: source and target should be node instances or node ID strings
const edge = graph.addEdge({
  source: 'source',
  target: 'target',
  attrs: {
    line: {
      stroke: '#5F95FF',
      strokeWidth: 2,
      targetMarker: {
        name: 'classic',
        size: 8,
      },
    },
  },
})
```

**Correction Method:**
```javascript
// Correct: Ensure source and target are valid node references
const sourceNode = graph.addNode({
  id: 'source',
  shape: 'rect',
  label: 'hello',
  x: 40,
  y: 100,
  width: 100,
  height: 40,
})

const targetNode = graph.addNode({
  id: 'target',
  shape: 'rect',
  label: 'world',
  x: 340,
  y: 100,
  width: 100,
  height: 40,
})

const edge = graph.addEdge({
  source: sourceNode, // or 'source'
  target: targetNode, // or 'target'
  attrs: {
    line: {
      stroke: '#5F95FF',
      strokeWidth: 2,
      targetMarker: {
        name: 'classic',
        size: 8,
      },
    },
  },
})
```

### Error 5: Missing Required Selector Definition in Port Configuration

**Error Example:**
```javascript
// Error: portMarkup uses an undefined selector
ports: {
  groups: {
    in: {
      position: 'left',
      attrs: { portBody: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
    },
  },
  items: [{ id: 'in1', group: 'in' }],
}
```

**Correction Method:**
```javascript
// Correct: Define selector name in portMarkup
ports: {
  groups: {
    in: {
      position: 'left',
      attrs: { portBody: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
    },
  },
  items: [{ id: 'in1', group: 'in' }],
  portMarkup: [
    {
      tagName: 'circle',
      selector: 'portBody', // Matches the key in attrs
    },
  ],
}
```

### Error 6: Ports Not Displayed Due to Use of Undeclared Group Names

**Error Example:**
```javascript
// Error: Using an undeclared group name in items that is not defined in groups
graph.addNode({
  shape: 'rect',
  x: 100,
  y: 60,
  width: 120,
  height: 50,
  ports: {
    groups: {
      in: {
        position: 'left',
        attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
      },
    },
    items: [
      { id: 'port1', group: 'top' }, // group 'top' is not defined
    ],
  },
});
```

**Correction:**
```javascript
// Correct: Ensure the group name used in items is defined in groups
graph.addNode({
  shape: 'rect',
  x: 100,
  y: 60,
  width: 120,
  height: 50,
  ports: {
    groups: {
      in: {
        position: 'left',
        attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
      },
      top: {
        position: 'top',
        attrs: { circle: { magnet: true, r: 5, stroke: '#1890ff', fill: '#fff' } },
      },
    },
    items: [
      { id: 'port1', group: 'top' },
    ],
  },
});
```

### Error 7: Rendering Failure Due to Invalid Container Reference

**Error Example:**
```javascript
// Error: container variable is undefined or null
const graph = new Graph({
  container: container, // ❌ container is not declared, should use the string 'container'
});
```

**Correction Method:**
```javascript
// Correct: Use the string 'container' (runtime environment injected, do not declare const container)
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
});
```

### Error 8: Incorrect API Usage When Dynamically Modifying Edge Attributes

**Error Example:**
```javascript
// Incorrect: Improper parameter format when using edge.attr() and edge.prop() to modify edge attributes
setTimeout(() => {
  edge.attr('line/stroke', '#ff4d4f')
  edge.attr('line/strokeWidth', 2)
  edge.prop('vertices', [{ x: 200, y: 200 }])
}, 2000)
```

**Correction Method:**
```javascript
// Correct: Using the correct API call method
edge.attr('line/stroke', '#1890ff');
edge.prop('vertices', [{ x: 200, y: 50 }]);
```

### Error 9: Improper Configuration When Creating a Canvas Supporting Drag-and-Drop Connections from Connection Points

**Error Example:**
```javascript
// Error: Incomplete or incorrect connecting configuration
const graph = new Graph({
  container: 'container',
  connecting: {
    snap: true,
    allowBlank: true,
    allowLoop: false,
    highlight: true,
    connector: 'rounded',
    connectionPoint: 'anchor',
    router: {
      name: 'manhattan',
      args: {
        padding: 1,
      },
    },
    createEdge() {
      return new Shape.Edge({
        attrs: {
          line: {
            stroke: '#5F95FF',
            strokeWidth: 2,
            targetMarker: {
              name: 'classic',
              size: 8,
            },
          },
        },
        zIndex: 0,
      })
    },
  },
})
```

**Correction Method:**
```javascript
// Correct: Using a complete connecting configuration
const graph = new Graph({
  container: 'container',
  background: { color: '#F2F7FA' },
  connecting: {
    allowBlank: true,
    allowMulti: true,
    allowLoop: true,
    allowNode: true,
    allowEdge: false,
    allowPort: true,
    createEdge() {
      return this.createEdge({
        attrs: {
          line: {
            stroke: '#8f8f8f',
            strokeWidth: 1,
          },
        },
      });
    },
  },
});
```

## ⚠️ `registerNode` + `addNode` Port Merging Behavior (Must Read)

X6 3.x executes `ObjectExt.merge({}, defaults, metadata)` when `new Cell(metadata)` is called, **recursively merging** the ports registered with `registerNode` and the ports added with `addNode`. Meanwhile, `node.addPort` / `node.addPorts` uses `[...current.items, ...new]` for **simple concatenation**. **Neither path performs ID deduplication**. If duplicate IDs are found, X6 immediately throws `Error: Duplicitied port id.`, preventing the entire canvas from rendering.

### ❌ Counterexample (Typical Duplicated Port ID)

```javascript
// Declared 'in1' during registration
Graph.registerNode('my-node', {
  inherit: 'rect',
  width: 120, height: 60,
  ports: {
    groups: { in: { position: 'left', attrs: { circle: { magnet: true, r: 4 } } } },
    items: [{ id: 'in1', group: 'in' }],
  },
});

// addNode redefines 'in1' → Array merges by index, resulting in items: [{ id: 'in1' }, { id: 'in1' }] → Error
graph.addNode({
  shape: 'my-node', x: 100, y: 100,
  ports: { items: [{ id: 'in1', group: 'in' }] },
});
// → Error: Duplicated port id.
```

### ✅ Correct Writing (Choose One of Three)

**1. Register only declares groups, all items are provided during `addNode`:**
```javascript
Graph.registerNode('my-node', {
  inherit: 'rect',
  width: 120, height: 60,
  ports: {
    groups: { in: { position: 'left', attrs: { circle: { magnet: true, r: 4 } } } },
    // items not defined, left for addNode
  },
});
graph.addNode({ shape: 'my-node', x: 100, y: 100,
  ports: { items: [{ id: 'in1', group: 'in' }] } });
```

**2. Fully declare items during registration, no ports passed in `addNode`:**
```javascript
Graph.registerNode('my-node', {
  inherit: 'rect',
  width: 120, height: 60,
  ports: {
    groups: { in: { position: 'left', attrs: { circle: { magnet: true, r: 4 } } } },
    items: [{ id: 'in1', group: 'in' }],
  },
});
graph.addNode({ shape: 'my-node', x: 100, y: 100 }); // Directly reuse ports from registry
```

**3. Partially declare ports during registration, add additional ports at runtime using `node.addPort` with unique ids:**
```javascript
const node = graph.addNode({ shape: 'my-node', x: 100, y: 100 }); // Already has in1
node.addPort({ id: 'in2', group: 'in' }); // ✅ New id
node.addPort({ id: 'in1', group: 'in' }); // ❌ Duplicated port id
```

> Troubleshooting Tip: If you see `Duplicated port id.`, always grep for the same port id first. Often, it’s already declared in the registry and passed again during `addNode`.