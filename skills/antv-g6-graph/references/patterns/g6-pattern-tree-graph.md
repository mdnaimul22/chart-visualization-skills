---
id: "g6-pattern-tree-graph"
title: "G6 Tree Graph Pattern"
description: |
  A complete example of creating tree visualizations using G6, including common tree graph patterns such as mind maps, organizational charts,
  and file trees, with support for collapsing/expanding.

library: "g6"
version: "5.x"
category: "patterns"
subcategory: "tree"
tags:
  - "pattern"
  - "tree graph"
  - "mindmap"
  - "organizational structure"
  - "tree"
  - "mindmap"
  - "hierarchy"
  - "pattern"

related:
  - "g6-layout-mindmap"
  - "g6-layout-dagre"
  - "g6-core-data-structure"
  - "g6-node-rect"

use_cases:
  - "Organizational Chart"
  - "Mind Map"
  - "File Directory Tree"
  - "Hierarchical Classification Display"

difficulty: "intermediate"
completeness: "full"
created: "2026-04-15"
updated: "2026-04-15"
author: "antv-team"
---

## Mind Map (Horizontal Expansion)

```javascript
import { Graph, treeToGraphData } from '@antv/g6';

const treeData = {
  id: 'root',
  data: { label: 'Core Theme', level: 0 },
  children: [
    {
      id: 'branch-a',
      data: { label: 'Branch A', level: 1 },
      children: [
        { id: 'leaf-a1', data: { label: 'Subitem A1', level: 2 } },
        { id: 'leaf-a2', data: { label: 'Subitem A2', level: 2 } },
        { id: 'leaf-a3', data: { label: 'Subitem A3', level: 2 } },
      ],
    },
    {
      id: 'branch-b',
      data: { label: 'Branch B', level: 1 },
      children: [
        { id: 'leaf-b1', data: { label: 'Subitem B1', level: 2 } },
        { id: 'leaf-b2', data: { label: 'Subitem B2', level: 2 } },
      ],
    },
    {
      id: 'branch-c',
      data: { label: 'Branch C', level: 1 },
      children: [
        { id: 'leaf-c1', data: { label: 'Subitem C1', level: 2 } },
      ],
    },
  ],
};

const COLORS = {
  0: { fill: '#1783FF', text: '#fff', stroke: '#1783FF' },
  1: { fill: '#e6f4ff', text: '#1783FF', stroke: '#91caff' },
  2: { fill: '#f5f5f5', text: '#333', stroke: '#d9d9d9' },
};

const graph = new Graph({
  container: 'container',
  width: 1000,
  height: 600,
  autoFit: 'view',
  data: treeToGraphData(treeData),
  node: {
    type: 'rect',
    style: {
      size: (d) => {
        const sizes = { 0: [120, 44], 1: [100, 36], 2: [90, 30] };
        return sizes[d.data.level] || [90, 30];
      },
      radius: (d) => d.data.level === 0 ? 22 : 15,
      fill: (d) => COLORS[d.data.level]?.fill || '#f5f5f5',
      stroke: (d) => COLORS[d.data.level]?.stroke || '#d9d9d9',
      lineWidth: 1,
      labelText: (d) => d.data.label,
      labelPlacement: 'center',
      labelFill: (d) => COLORS[d.data.level]?.text || '#333',
      labelFontSize: (d) => ({ 0: 16, 1: 14, 2: 12 }[d.data.level] || 12),
      labelFontWeight: (d) => d.data.level === 0 ? 'bold' : 'normal',
      cursor: 'pointer',
    },
  },
  edge: {
    type: 'cubic-horizontal',
    style: {
      stroke: '#c0d8f0',
      lineWidth: 1.5,
    },
  },
  layout: {
    type: 'mindmap',
    direction: 'H',
    getWidth: (d) => ({ 0: 120, 1: 100, 2: 90 }[d.data?.level] || 90),
    getHeight: (d) => ({ 0: 44, 1: 36, 2: 30 }[d.data?.level] || 30),
    getHGap: () => 50,
    getVGap: () => 8,
  },
  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    {
      type: 'collapse-expand',
      trigger: 'click',
      animation: true,
    },
  ],
});

graph.render();
```

## Organizational Structure Chart (Top to Bottom)

```javascript
import { Graph, treeToGraphData } from '@antv/g6';

const orgData = {
  id: 'ceo',
  data: { name: 'Li Zong', title: 'CEO', dept: 'Board of Directors' },
  children: [
    {
      id: 'cto',
      data: { name: 'Zhang Zong', title: 'CTO', dept: 'Technology Department' },
      children: [
        { id: 'fe-lead', data: { name: 'Wang Gong', title: 'Front-end Lead', dept: 'Front-end Team' } },
        { id: 'be-lead', data: { name: 'Chen Gong', title: 'Back-end Lead', dept: 'Back-end Team' } },
      ],
    },
    {
      id: 'cmo',
      data: { name: 'Liu Zong', title: 'CMO', dept: 'Marketing Department' },
      children: [
        { id: 'marketing1', data: { name: 'Zhao Ce Hua', title: 'Marketing Specialist', dept: 'Marketing Department' } },
      ],
    },
    {
      id: 'cfo',
      data: { name: 'Qian Zong', title: 'CFO', dept: 'Finance Department' },
    },
  ],
};

const graph = new Graph({
  container: 'container',
  width: 900,
  height: 600,
  autoFit: 'view',
  data: treeToGraphData(orgData),
  node: {
    type: 'rect',
    style: {
      size: [150, 56],
      radius: 6,
      fill: '#f0f5ff',
      stroke: '#adc6ff',
      lineWidth: 1,
      // Main title: name
      labelText: (d) => `${d.data.name}\n${d.data.title}`,
      labelPlacement: 'center',
      labelFontSize: 13,
      labelFill: '#1d39c4',
      labelWordWrap: true,
      cursor: 'pointer',
    },
    state: {
      selected: {
        fill: '#1783FF',
        stroke: '#1783FF',
        labelFill: '#fff',
      },
    },
  },
  edge: {
    type: 'cubic-vertical',
    style: {
      stroke: '#adc6ff',
      lineWidth: 1.5,
    },
  },
  layout: {
    type: 'compact-box',
    direction: 'TB',
    getHeight: () => 56,
    getWidth: () => 150,
    getVGap: () => 50,
    getHGap: () => 20,
  },
  behaviors: [
    'drag-canvas',
    'zoom-canvas',
    'click-select',
    {
      type: 'collapse-expand',
      trigger: 'dblclick',      // Double-click to collapse/expand
    },
  ],
});

graph.render();
```

## Key Notes

| Scenario       | Recommended Layout | Recommended Edge Type | Features               |
|----------------|--------------------|-----------------------|------------------------|
| Mind Map       | `mindmap`          | `cubic-horizontal`    | Bidirectional expansion, H direction |
| Organizational Chart | `compact-box`    | `cubic-vertical`      | Top-to-bottom, TB direction |
| File Tree      | `indented`         | `line`                | Indented display       |
| Knowledge Tree | `dendrogram`       | `cubic-vertical`      | Leaf nodes aligned     |

## Collapse and Expand

```javascript
// Programmatically control collapse
graph.collapse('branch-a');    // Collapse node (hide subtree)
graph.expand('branch-a');      // Expand node

// Listen for collapse events
graph.on('node:collapse', (event) => {
  console.log('Collapsed:', event.target.id);
});
graph.on('node:expand', (event) => {
  console.log('Expanded:', event.target.id);
});
```