---
id: "x6-core-model-query"
title: "X6 Graph Model Query and Traversal API"
description: |
  Graph Model's graph structure query API: Retrieve neighboring nodes, connected edges, predecessors/successors, root/leaf nodes, graph traversal search, etc.
library: x6
version: 3.x
category: "core"
tags:
  - model
  - query
  - neighbors
  - traverse
  - graph-algorithm
  - getConnectedEdges
  - getNeighbors
  - getSuccessors
  - getPredecessors
---

# Graph Model Query and Traversal API

## Overview

X6's Graph Model provides rich graph structure query capabilities to retrieve topological relationships between nodes (neighbors, predecessors, successors), connected edges, root/leaf nodes, etc. These APIs can be accessed via `graph.model` or directly through the `graph` proxy.

## Get Elements

### getCells / getNodes / getEdges

```javascript
// Get all elements
const cells = graph.getCells();

// Get only nodes
const nodes = graph.getNodes();

// Get only edges
const edges = graph.getEdges();
```

### getCellById

```javascript
const cell = graph.getCellById('node-1');
```

## Edge Query

(Note: The original content provided only contained a header in Chinese. The translation above adheres to the strict instructions provided, maintaining the Markdown syntax and structure while translating the header to English.)

### getConnectedEdges — Get all edges connected to a node

```javascript
// Get all connected edges (incoming + outgoing)
const edges = graph.getConnectedEdges(node);

// Get only outgoing edges
const outEdges = graph.getConnectedEdges(node, { outgoing: true });

// Get only incoming edges
const inEdges = graph.getConnectedEdges(node, { incoming: true });

// Include indirect connections (edges connected through edges)
const allEdges = graph.getConnectedEdges(node, { indirect: true });

// Deep search (include edges connected to embedded child nodes)
const deepEdges = graph.getConnectedEdges(node, { deep: true });
```

**options parameter:**

| Parameter | Type | Description |
|------|------|------|
| `incoming` | boolean | Include incoming edges |
| `outgoing` | boolean | Include outgoing edges |
| `indirect` | boolean | Include indirect connections |
| `deep` | boolean | Include edges connected to embedded child nodes |
| `enclosed` | boolean | Whether to include internal edges in deep mode |

> Note: If neither `incoming` nor `outgoing` is provided, both default to `true`.

### getOutgoingEdges — Get Outgoing Edges

```javascript
const outEdges = graph.getOutgoingEdges(node);
// Returns Edge[] | null
```

### getIncomingEdges — Get Incoming Edges

```javascript
const inEdges = graph.getIncomingEdges(node);
// Returns Edge[] | null
```

## Neighbor Node Query

### getNeighbors — Get Neighbor Nodes

```javascript
// Get all neighbors (incoming + outgoing)
const neighbors = graph.getNeighbors(node);

// Get only downstream neighbors
const downstream = graph.getNeighbors(node, { outgoing: true });

// Get only upstream neighbors
const upstream = graph.getNeighbors(node, { incoming: true });
```

### isNeighbor — Determine if Two Nodes Are Neighbors

```javascript
const isNear = graph.isNeighbor(node1, node2);
const isDownstream = graph.isNeighbor(node1, node2, { outgoing: true });
```

## Predecessor and Successor

### getSuccessors — Get All Successor Nodes

Retrieves all nodes reachable from the current node along the outgoing edges (recursive traversal):

```javascript
const successors = graph.getSuccessors(node);

// Limit distance
const near = graph.getSuccessors(node, { distance: 1 });  // Only get direct successors
const farther = graph.getSuccessors(node, { distance: [2, 3] });  // Successors at distance 2~3
```

### isSuccessor — Determine if it is a successor

```javascript
const isAfter = graph.isSuccessor(node1, node2);  // Whether node2 is a successor of node1
```

### getPredecessors — Get All Predecessor Nodes

All nodes reachable from the current node along the incoming edges (recursive traversal):

```javascript
const predecessors = graph.getPredecessors(node);
```

### isPredecessor — Determine if it is a Predecessor

```javascript
const isBefore = graph.isPredecessor(node1, node2);  // Whether node2 is a predecessor of node1
```

## Root Node and Leaf Node

### getRoots — Get Root Nodes (Nodes with No Incoming Edges)

```javascript
const roots = graph.getRootNodes();
```

### getLeafs — Get Leaf Nodes (Nodes with No Outgoing Edges)

```javascript
const leafs = graph.getLeafNodes();
```

### isRoot / isLeaf — Determine if a node is a root or leaf

```javascript
graph.isRootNode(node);  // true if no incoming edges
graph.isLeafNode(node);  // true if no outgoing edges
```

## Graph Traversal Search

### searchCell — Graph Search (BFS/DFS)

```javascript
// Perform a breadth-first search starting from the node
graph.searchCell(node, (cell, distance) => {
  console.log(`${cell.id} distance from start: ${distance}`);
}, { breadthFirst: true });

// Depth-first search (default)
graph.searchCell(node, (cell, distance) => {
  if (cell.id === 'target') {
    return false;  // Return false to stop the search
  }
});
```

### getShortestPath — Shortest Path

```javascript
const path = graph.getShortestPath(sourceNode, targetNode);
// Returns an array of node IDs
```

## Complete Example: DAG Topology Analysis

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({ container: 'container', width: 800, height: 600 });

const a = graph.addNode({ shape: 'rect', x: 50, y: 200, width: 80, height: 40, label: 'A' });
const b = graph.addNode({ shape: 'rect', x: 200, y: 100, width: 80, height: 40, label: 'B' });
const c = graph.addNode({ shape: 'rect', x: 200, y: 300, width: 80, height: 40, label: 'C' });
const d = graph.addNode({ shape: 'rect', x: 400, y: 200, width: 80, height: 40, label: 'D' });

graph.addEdge({ source: a, target: b });
graph.addEdge({ source: a, target: c });
graph.addEdge({ source: b, target: d });
graph.addEdge({ source: c, target: d });

// Query successors of A
const successors = graph.getSuccessors(a);
console.log('Successors of A:', successors.map(n => n.id));  // [B, C, D]

// Query predecessors of D
const predecessors = graph.getPredecessors(d);
console.log('Predecessors of D:', predecessors.map(n => n.id));  // [B, C, A]

// Get root nodes
const roots = graph.getRootNodes();
console.log('Root nodes:', roots.map(n => n.id));  // [A]

// Get leaf nodes
const leafs = graph.getLeafNodes();
console.log('Leaf nodes:', leafs.map(n => n.id));  // [D]

// Get neighbors of B
const neighbors = graph.getNeighbors(b);
console.log('Neighbors of B:', neighbors.map(n => n.id));  // [A, D]
```

## Common Errors

```javascript
// ❌ Error: getConnectedEdges returns a possibly empty array, while getOutgoingEdges returns null
const edges = graph.getOutgoingEdges(node);
edges.forEach(e => ...);  // TypeError: null.forEach

// ✅ Correct: Check for null first
const edges = graph.getOutgoingEdges(node);
if (edges) {
  edges.forEach(e => ...);
}

// Or use getConnectedEdges (always returns an array)
const edges = graph.getConnectedEdges(node, { outgoing: true });
edges.forEach(e => ...);  // Safe, empty array
```