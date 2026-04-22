---
id: "g6-node-react"
title: "G6 Custom Nodes with React/Vue (react-node / vue-node)"
description: |
  Use @antv/g6-extension-react to define node content with React components.
  Supports UI libraries like Ant Design, suitable for complex node scenarios involving interaction logic, form inputs, etc.
  Node data is passed through the component callback, supporting state responses and two-way communication with the graph instance.

library: "g6"
version: "5.x"
category: "elements"
subcategory: "nodes"
tags:
  - "react-node"
  - "vue-node"
  - "React Node"
  - "Custom Node"
  - "Rich Text Node"
  - "g6-extension-react"

related:
  - "g6-node-html"
  - "g6-core-custom-element"

difficulty: "advanced"
completeness: "full"
created: "2026-04-16"
updated: "2026-04-16"
---

## Solution Selection

| Solution | Recommended Scenario |
|------|---------|
| Built-in Nodes (circle/rect, etc.) | Simple geometric shapes, requiring high performance (>2000 nodes) |
| HTML Nodes (html) | Lightweight rich text, not dependent on React/Vue |
| React Nodes (react-node) | Integration with UI libraries like Ant Design, including interaction logic |
| Vue Nodes (vue-node) | Vue projects, integration with libraries like Element Plus |

---

## React Nodes

### Install Dependencies

```bash
npm install @antv/g6-extension-react
```

# Vue Project: npm install @antv/g6-extension-vue
```

### Basic Example

```jsx
import { ExtensionCategory, Graph, register } from '@antv/g6';
import { ReactNode } from '@antv/g6-extension-react';

// 1. Register React node type
register(ExtensionCategory.NODE, 'react-node', ReactNode);

// 2. Define React component
const MyNode = ({ data }) => (
  <div style={{
    width: '100%',
    height: '100%',
    background: '#fff',
    border: '1px solid #1783FF',
    borderRadius: 6,
    padding: 8,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  }}>
    {data.data.label}
  </div>
);

// 3. Use in Graph
const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
      { id: 'n1', style: { x: 100, y: 200 }, data: { label: 'Service A' } },
      { id: 'n2', style: { x: 400, y: 200 }, data: { label: 'Service B' } },
    ],
    edges: [{ source: 'n1', target: 'n2' }],
  },
  node: {
    type: 'react-node',
    style: {
      size: [120, 50],              // Must specify dimensions
      component: (data) => <MyNode data={data} />,
    },
  },
  behaviors: ['drag-element', 'zoom-canvas', 'drag-canvas'],
});

graph.render();
```

> **Important:** React nodes must specify width and height via `style.size` (`[width, height]` or a single value), otherwise the node size will be 0.

### Responding to Built-in Interaction States

The `states` field of node data reflects the current built-in states (from behaviors like `hover-activate`, `click-select`, etc.):

```jsx
register(ExtensionCategory.NODE, 'react-node', ReactNode);

const StatefulNode = ({ data }) => {
  const isActive = data.states?.includes('active');
  const isSelected = data.states?.includes('selected');

  return (
    <div style={{
      width: '100%',
      height: '100%',
      background: isSelected ? '#fff7e6' : '#fff',
      border: `2px solid ${isActive ? '#1783FF' : '#ddd'}`,
      borderRadius: 6,
      padding: 8,
      boxShadow: isActive ? '0 0 8px rgba(24,144,255,0.6)' : 'none',
      transform: `scale(${isActive ? 1.05 : 1})`,
      transition: 'all 0.2s',
    }}>
      {data.data.label}
    </div>
  );
};

const graph = new Graph({
  node: {
    type: 'react-node',
    style: {
      size: [140, 60],
      component: (data) => <StatefulNode data={data} />,
    },
  },
  behaviors: ['hover-activate', 'click-select', 'drag-element'],
});
```

### Bidirectional Communication Between Nodes and Graph Instances

Inject the `graph` instance into the node component to enable internal node operations to trigger graph updates:

```jsx
register(ExtensionCategory.NODE, 'react-node', ReactNode);

const ActionNode = ({ data, graph }) => {
  const handleToggle = () => {
    graph.updateNodeData([{
      id: data.id,
      data: { expanded: !data.data.expanded },
    }]);
    graph.draw();
  };

  return (
    <div style={{ width: '100%', height: '100%', padding: 10, background: '#fff', border: '1px solid #d9d9d9', borderRadius: 8 }}>
      <div style={{ fontWeight: 600, marginBottom: 4 }}>{data.data.name}</div>
      {data.data.expanded && (
        <div style={{ fontSize: 12, color: '#666' }}>{data.data.detail}</div>
      )}
      <button onClick={handleToggle} style={{ marginTop: 6, fontSize: 12 }}>
        {data.data.expanded ? 'Collapse' : 'Expand'}
      </button>
    </div>
  );
};

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 600,
  data: {
    nodes: [
      {
        id: 'n1',
        style: { x: 100, y: 100 },
        data: { name: 'Server', detail: 'IP: 192.168.1.1 / Status: Running', expanded: false },
      },
    ],
    edges: [],
  },
  node: {
    type: 'react-node',
    style: {
      size: (datum) => datum.data.expanded ? [200, 120] : [200, 60],
      component: (data) => <ActionNode data={data} graph={graph} />,
    },
  },
  behaviors: ['drag-element', 'zoom-canvas', 'drag-canvas'],
});

graph.render();
```

### Integrating Ant Design Components

```jsx
import { Badge, Card, Tag } from 'antd';
import { DatabaseFilled } from '@ant-design/icons';
import { ExtensionCategory, Graph, register } from '@antv/g6';
import { ReactNode } from '@antv/g6-extension-react';

register(ExtensionCategory.NODE, 'react-node', ReactNode);

const ServerNode = ({ data }) => {
  const { status, type } = data.data;
  return (
    <Card
      size="small"
      style={{ width: '100%', height: '100%', borderRadius: 8 }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span><DatabaseFilled /> {data.id}</span>
        <Badge status={status} />
      </div>
      <Tag color={type === 'primary' ? 'blue' : 'default'}>{type}</Tag>
    </Card>
  );
};

const graph = new Graph({
  node: {
    type: 'react-node',
    style: {
      size: [200, 80],
      component: (data) => <ServerNode data={data} />,
    },
  },
});
```

---

## Vue Node

```javascript
// Installation: npm install @antv/g6-extension-vue
import { ExtensionCategory, Graph, register } from '@antv/g6';
import { VueNode } from '@antv/g6-extension-vue';
import { defineComponent } from 'vue';

register(ExtensionCategory.NODE, 'vue-node', VueNode);

const MyVueNode = defineComponent({
  props: ['data'],
  template: `
    <div style="width:100%;height:100%;background:#fff;border:1px solid #1783FF;border-radius:6px;padding:8px;text-align:center">
      {{ data.data.label }}
    </div>
  `,
});

const graph = new Graph({
  node: {
    type: 'vue-node',
    style: {
      size: [120, 50],
      component: (data) => h(MyVueNode, { data }),
    },
  },
});
```

---

## Notes

1. **Must specify size**: React/Vue nodes must explicitly set `style.size`, which can be a static value or a callback function.
2. **Update size when node expands/collapses**: If the node size changes after expansion, use a callback for size: `size: (datum) => datum.data.expanded ? [w2, h2] : [w1, h1]`.
3. **Performance limit**: React node rendering has a higher cost and is not suitable for scenarios with more than 500 nodes. Use built-in nodes instead when exceeding this limit.
4. **Event bubbling prevention**: To prevent click events within React components from triggering G6 events, use `e.stopPropagation()`.
5. **Cleanup on destruction**: Call `graph.destroy()` when the component is unmounted to prevent memory leaks.