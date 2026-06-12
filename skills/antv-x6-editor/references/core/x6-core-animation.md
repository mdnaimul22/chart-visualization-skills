---
id: "x6-core-animation"
title: "X6 Animation and Transition"
description: |
  Comprehensive guide to the animation system for X6 nodes and edges.
  Includes animate API, configuration-based animations, registering animated Shapes, animation control (pause/resume/cancel), and animation events.

library: "x6"
version: "3.x"
category: "core"
subcategory: "animation"
tags:
  - "animation"
  - "animate"
  - "transition"
  - "pause"
  - "play"
  - "cancel"
  - "finish"
  - "reverse"
  - "Web Animations API"
  - "keyframes"
  - "duration"
  - "iterations"

related:
  - "x6-core-node"
  - "x6-core-edge"
  - "x6-core-events"

use_cases:
  - "Add position movement animation to nodes"
  - "Add size change animation to nodes"
  - "Add animation to custom properties (e.g., data)"
  - "Declare animations through configuration"
  - "Register custom Shapes with animations"
  - "Control animation pause, resume, and cancel"
  - "Listen for animation completion events"

anti_patterns:
  - "Use / to separate animation property paths (e.g., position/x), do not write x directly"
  - "Do not confuse CSS animation property names with X6 animation configurations"
---
# X6 Animation and Transition

X6's `animate` API is implemented based on the [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API) standard, providing powerful animation capabilities.

## Basic Usage

```javascript
import { Graph } from '@antv/x6';

const graph = new Graph({
  container: 'container',
  width: 800,
  height: 400,
  background: { color: '#F2F7FA' },
});

const node = graph.addNode({
  shape: 'rect',
  x: 100,
  y: 140,
  width: 100,
  height: 50,
  label: 'Hello X6',
  attrs: { body: { strokeWidth: 1, rx: 6, ry: 6 } },
});

// Add position animation: Node moves from current position to x=300
node.animate(
  { 'position/x': 300 },
  { duration: 1000, direction: 'alternate', iterations: Infinity },
);
```

## animate API Parameters

```javascript
cell.animate(keyframes, options);
```

### keyframes — Keyframes

Specifies the animation properties and their target values. The property path is separated by `/`, implemented based on `cell.setPropByPath()`.

```javascript
// Single target value (animate from current value to target value)
node.animate({ 'position/x': 300 }, { duration: 1000 });

// Array format (specify start and target values)
node.animate({ 'position/x': [100, 300] }, { duration: 1000 });

// Multiple properties animated simultaneously
node.animate(
  { 'position/x': 300, 'position/y': 200 },
  { duration: 1000 },
);
```

### Common Attribute Paths

| Path | Description |
|------|------|
| `position/x` | Node X coordinate |
| `position/y` | Node Y coordinate |
| `size/width` | Node width |
| `size/height` | Node height |
| `attrs/body/fill` | Node fill color |
| `attrs/body/opacity` | Node opacity |
| `data/xxx` | Custom data attribute (for HTML nodes) |

### options — Animation Configuration

| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `duration` | number | - | Animation duration (milliseconds) |
| `delay` | number | 0 | Delay before starting (milliseconds) |
| `direction` | string | `'normal'` | `'normal'`/`'reverse'`/`'alternate'`/`'alternate-reverse'` |
| `iterations` | number | 1 | Number of repetitions, `Infinity` means infinite |
| `easing` | string | `'linear'` | Easing function, e.g., `'ease'`、`'ease-in-out'` |
| `fill` | string | `'none'` | State after animation ends: `'forwards'`/`'backwards'`/`'both'`/`'none'` |

## Declarative Animation

Directly declare animations in the node configuration, and the animation will automatically play once the node is added to the canvas:

```javascript
graph.addNode({
  shape: 'rect',
  x: 100,
  y: 140,
  width: 100,
  height: 50,
  label: 'Hello X6',
  attrs: { body: { strokeWidth: 1, rx: 6, ry: 6 } },
  // Declarative animation: each item in the array corresponds to an animate call
  animation: [
    [
      { 'position/x': 300 },
      { duration: 1000, direction: 'alternate', iterations: Infinity },
    ],
  ],
});
```

`animation` is an array where each item is a `[keyframes, options]` tuple. The animation automatically starts playing once the node is added to the canvas.

## Register Animation Shape

Reusing the same animation effect for a batch of nodes:

```javascript
import { Graph } from '@antv/x6';

Graph.registerNode(
  'animated-rect',
  {
    inherit: 'rect',
    width: 150,
    height: 60,
    attrs: {
      body: { strokeWidth: 1, rx: 6, ry: 6 },
    },
    animation: [
      [
        { 'position/x': 300 },
        { duration: 1000, direction: 'alternate', iterations: Infinity },
      ],
    ],
  },
  true,
);

// All nodes using animated-rect automatically have the animation
graph.addNode({ shape: 'animated-rect', x: 100, y: 50, label: 'Node 1' });
graph.addNode({ shape: 'animated-rect', x: 100, y: 150, label: 'Node 2' });
```

## Custom Attribute Animation (HTML Node)

Add animations to custom attributes in the data, combined with HTML nodes to achieve complex effects:

```javascript
import { Graph, Shape, Dom } from '@antv/x6';

Shape.HTML.register({
  shape: 'progress-node',
  width: 160,
  height: 40,
  effect: ['data'],
  html(cell) {
    const { progress } = cell.getData() ?? { progress: 0 };
    const div = document.createElement('div');
    Dom.css(div, {
      width: '100%',
      height: '100%',
      background: `linear-gradient(to right, #1890ff ${progress * 100}%, #f0f0f0 ${progress * 100}%)`,
      borderRadius: '4px',
      border: '1px solid #d9d9d9',
    });
    return div;
  },
});

const node = graph.addNode({
  shape: 'progress-node',
  x: 100,
  y: 100,
  data: { progress: 0 },
});

// Add animation to data/progress
node.animate(
  { 'data/progress': 1 },
  { duration: 2000, fill: 'forwards' },
);
```

## Animation Control

`animate` returns an animation object, supporting control operations:

```javascript
const animation = node.animate(
  { 'position/x': [100, 300] },
  { duration: 2000, iterations: Infinity },
);

// Pause
animation.pause();

// Resume playback
animation.play();

// Cancel animation (revert to initial state)
animation.cancel();

// Finish animation immediately (jump to final state)
animation.finish();

// Play in reverse
animation.reverse();

// Update playback speed (2x speed)
animation.updatePlaybackRate(2);
```

### Get All Animations on a Node

```javascript
const animations = node.getAnimations(); // Animation[]
animations.forEach((anim) => anim.pause());
```

## Animation Events

### Method One: Web Animations API Style

```javascript
const animation = node.animate(
  { 'position/x': [100, 300] },
  { duration: 1000, iterations: 1 },
);

animation.onfinish = () => {
  console.log('Animation finished');
};

animation.oncancel = () => {
  console.log('Animation canceled');
};
```

### Method Two: X6 Event System

```javascript
// Listen for all node animations to finish
graph.on('node:animation:finish', ({ node }) => {
  console.log('Node animation finished:', node.id);
});

// Listen for all cell animations to be canceled
graph.on('cell:animation:cancel', ({ cell }) => {
  console.log('Animation cancelled:', cell.id);
});
```

Supported events:
- `cell:animation:finish` — Animation finished
- `cell:animation:cancel` — Animation canceled
- `node:animation:finish` — Node animation finished
- `node:animation:cancel` — Node animation canceled
- `edge:animation:finish` — Edge animation finished
- `edge:animation:cancel` — Edge animation canceled

## `translate` / `rotate` Built-in Transition Options

> ⚠️ X6 3.x **does not have** the `cell.transition(path, target, options)` method. The often misattributed "transition method" is actually a **boolean/object options field** on position transformation methods like `node.translate()` / `node.rotate()`, which still rely on `animate` under the hood.

### Real API (Verified from `model/node.ts`)

```typescript
node.translate(tx: number, ty: number, options?: {
  transition?: boolean | KeyframeEffectOptions  // ← This is where transition is defined
  restrict?: RectangleLike | null
  exclude?: Cell[]
  // ...
})
```

When `options.transition` is `true` or an object, X6 internally **automatically calls `node.animate({'position/x', 'position/y'}, animateOptions)` once**, with the default `{ duration: 100, fill: 'forwards' }`.

### Usage Examples

```javascript
// Form 1: transition: true, use default animation parameters (duration 100ms, fill forwards)
node.translate(200, 100, { transition: true });

// Form 2: transition: KeyframeEffectOptions, custom animation parameters
node.translate(200, 100, {
  transition: { duration: 800, easing: 'ease-in-out', fill: 'forwards' },
});
```

### Relationship with `node.animate`

| Method | Applicable Scenario |
|--------|---------------------|
| `node.translate(tx, ty, { transition })` | Only for position translation, and the translation itself requires a transition animation |
| `node.animate({ 'position/x', 'position/y' }, options)` | Any property, any keyframe, requires obtaining the `animation` handle for pause/play/cancel |
| Configurable `animation: [[keyframes, options]]` | Persistent animation that automatically starts after the node is added to the canvas |

`translate({ transition })` is just a syntactic sugar for `animate`, **any more complex animation must use `animate`**.

## Common Errors and Fixes

### ❌ Incorrect Property Path Syntax

```javascript
// Incorrect: Using x directly as the property name
node.animate({ x: 300 }, { duration: 1000 });

// Correct: Using the property path position/x
node.animate({ 'position/x': 300 }, { duration: 1000 });
```

### ❌ Node Returns to Original Position After Animation

```javascript
// Incorrect: Default fill='none', properties revert after animation
node.animate({ 'position/x': 300 }, { duration: 1000 });

// Correct: Set fill='forwards' to maintain final state
node.animate({ 'position/x': 300 }, { duration: 1000, fill: 'forwards' });
```

### ❌ Misuse of Non-existent `node.transition(path, target, options)` Method

```javascript
// Error: cell.transition(path, target, options) does not exist in X6 3.x
// Runtime error: node.transition is not a function
node.transition('position', { x: 300, y: 200 }, { duration: 1000 });

// Correct (Position Transition): Use translate + transition option
node.translate(300 - node.position().x, 200 - node.position().y, {
  transition: { duration: 1000, easing: 'ease-in-out', fill: 'forwards' },
});

// Correct (General Transition): Use animate
node.animate(
  { 'position/x': 300, 'position/y': 200 },
  { duration: 1000, easing: 'ease-in-out', fill: 'forwards' },
);
```

### ❌ Container Selector Error

```javascript
// Error: Directly passing DOM element variable (in evaluation/Playground environment, container is injected by the runtime environment)
const container = document.getElementById('container');
const graph = new Graph({ container });

// Correct: Directly using string literal 'container'
const graph = new Graph({ container: 'container' });
```

### ❌ Using `complete` Callback to Listen for Animation End

```javascript
// Incorrect: Neither X6 nor Web Animations API has a complete callback
node.animate({ 'position/x': 300 }, {
  duration: 1000,
  complete: () => console.log('done'),
});

// Correct: Listen to the onfinish event of the returned Animation object
const animation = node.animate(
  { 'position/x': 300 },
  { duration: 1000, fill: 'forwards' },
);
animation.onfinish = () => console.log('done');

// Alternatively, listen to the graph event (suitable for multi-node scenarios)
graph.on('node:animation:finish', ({ node }) => {
  console.log('Node animation finished:', node.id);
});
```