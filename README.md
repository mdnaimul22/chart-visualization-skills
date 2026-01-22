# Chart Visualization Skills

<div align="center">

**A comprehensive chart generation toolkit powered by AntV**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7+-green.svg)](https://www.python.org/)

[Features](#features) • [Quick Start](#quick-start) • [Chart Types](#chart-types) • [Usage](#usage) • [Documentation](#documentation)

</div>

---

## Overview

Chart Visualization Skills is an intelligent data visualization toolkit that automatically selects the most appropriate chart type from 26 available options, extracts parameters based on detailed specifications, and generates high-quality chart images. Built on the powerful AntV visualization library, it provides a seamless workflow from data to visual insights.

## Features

✨ **Intelligent Chart Selection** - Automatically determines the best chart type based on data characteristics

📊 **26+ Chart Types** - Comprehensive coverage including statistical, geographic, hierarchical, and specialized visualizations

🎨 **Customizable Themes** - Multiple built-in themes (default, academy, dark) and extensive styling options

🚀 **Simple API** - Easy-to-use Python script with JSON configuration

📖 **Detailed Documentation** - Comprehensive specifications for each chart type in the `references/` directory

🔄 **Flexible Data Input** - Supports various data formats and structures

## Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection (for API access)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/antvis/chart-visualization-skills.git
cd chart-visualization-skills
```

2. Set up environment variables (optional):
```bash
export VIS_REQUEST_SERVER="https://antv-studio.alipay.com/api/gpt-vis"
export SERVICE_ID="your-service-id"
```

### Basic Usage

Generate a chart using the Python script:

```bash
python ./scripts/generate.py '{
  "tool": "generate_line_chart",
  "args": {
    "data": [
      {"time": "2025-01", "value": 100},
      {"time": "2025-02", "value": 120},
      {"time": "2025-03", "value": 150}
    ],
    "title": "Monthly Growth Trend",
    "theme": "default"
  }
}'
```

The script outputs the URL of the generated chart image.

## Chart Types

### 📈 Time Series & Trends
- **Line Chart** (`generate_line_chart`) - Display trends over time
- **Area Chart** (`generate_area_chart`) - Show accumulated trends
- **Dual Axes Chart** (`generate_dual_axes_chart`) - Compare two metrics with different scales

### 📊 Comparisons
- **Bar Chart** (`generate_bar_chart`) - Horizontal categorical comparisons
- **Column Chart** (`generate_column_chart`) - Vertical categorical comparisons
- **Histogram** (`generate_histogram_chart`) - Frequency distributions

### 🥧 Part-to-Whole
- **Pie Chart** (`generate_pie_chart`) - Show proportions of a whole
- **Treemap** (`generate_treemap_chart`) - Hierarchical proportions

### 🔗 Relationships & Flow
- **Scatter Chart** (`generate_scatter_chart`) - Reveal correlations
- **Sankey Diagram** (`generate_sankey_chart`) - Visualize flow between nodes
- **Venn Diagram** (`generate_venn_chart`) - Show set overlaps
- **Network Graph** (`generate_network_graph`) - Complex node-edge relationships

### 🗺️ Geographic
- **District Map** (`generate_district_map`) - Regional data visualization
- **Pin Map** (`generate_pin_map`) - Location markers
- **Path Map** (`generate_path_map`) - Routes and trajectories

### 🌳 Hierarchies & Structures
- **Organization Chart** (`generate_organization_chart`) - Organizational structures
- **Mind Map** (`generate_mind_map`) - Concept relationships and hierarchies

### 📊 Statistical
- **Box Plot** (`generate_boxplot_chart`) - Statistical distribution summary
- **Violin Chart** (`generate_violin_chart`) - Distribution density visualization

### 🎯 Specialized
- **Radar Chart** (`generate_radar_chart`) - Multi-dimensional comparisons
- **Funnel Chart** (`generate_funnel_chart`) - Process stages and conversion rates
- **Liquid Chart** (`generate_liquid_chart`) - Percentage or progress visualization
- **Word Cloud** (`generate_word_cloud_chart`) - Text frequency visualization
- **Fishbone Diagram** (`generate_fishbone_diagram`) - Cause-and-effect analysis
- **Flow Diagram** (`generate_flow_diagram`) - Process flows
- **Spreadsheet** (`generate_spreadsheet`) - Tabular data and pivot tables

## Usage

### Workflow

The visualization process follows these steps:

#### 1. **Chart Selection**

Analyze your data characteristics and select the appropriate chart type:

```python
# For time-based trends
"tool": "generate_line_chart"

# For categorical comparisons
"tool": "generate_bar_chart"

# For part-to-whole relationships
"tool": "generate_pie_chart"
```

#### 2. **Parameter Configuration**

Consult the corresponding specification file in `references/` to understand required and optional parameters:

```json
{
  "tool": "generate_scatter_chart",
  "args": {
    "data": [
      {"x": 10, "y": 20},
      {"x": 15, "y": 25}
    ],
    "title": "Correlation Analysis",
    "theme": "academy",
    "style": {
      "backgroundColor": "#f5f5f5",
      "palette": ["#5B8FF9", "#5AD8A6"]
    }
  }
}
```

#### 3. **Chart Generation**

Execute the generation script:

```bash
python ./scripts/generate.py '<your-json-payload>'
```

#### 4. **Result**

The script returns:
- URL of the generated chart image
- Complete specification used for generation

### Configuration Options

Most chart types support the following common options:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | `""` | Chart title |
| `theme` | string | `"default"` | Visual theme: `default`, `academy`, `dark` |
| `width` | number | `600` | Chart width in pixels |
| `height` | number | `400` | Chart height in pixels |
| `style.backgroundColor` | string | - | Custom background color |
| `style.palette` | string[] | - | Custom color palette |
| `style.texture` | string | `"default"` | Texture style: `default`, `rough` |

For specific parameters, refer to the documentation in the `references/` directory.

## Documentation

Detailed specifications for each chart type are available in the [`references/`](references/) directory:

- Each file contains complete field definitions
- Usage recommendations and best practices
- Data format requirements
- Styling options

### Example Reference Files

- [`generate_line_chart.md`](references/generate_line_chart.md) - Line chart specifications
- [`generate_scatter_chart.md`](references/generate_scatter_chart.md) - Scatter plot specifications
- [`generate_sankey_chart.md`](references/generate_sankey_chart.md) - Sankey diagram specifications

## Examples

### Line Chart with Multiple Series

```bash
python ./scripts/generate.py '{
  "tool": "generate_line_chart",
  "args": {
    "data": [
      {"time": "2025-01", "value": 100, "group": "Product A"},
      {"time": "2025-02", "value": 120, "group": "Product A"},
      {"time": "2025-01", "value": 90, "group": "Product B"},
      {"time": "2025-02", "value": 110, "group": "Product B"}
    ],
    "title": "Product Comparison",
    "axisXTitle": "Month",
    "axisYTitle": "Sales"
  }
}'
```

### Pie Chart

```bash
python ./scripts/generate.py '{
  "tool": "generate_pie_chart",
  "args": {
    "data": [
      {"category": "Desktop", "value": 45},
      {"category": "Mobile", "value": 35},
      {"category": "Tablet", "value": 20}
    ],
    "title": "Traffic Distribution"
  }
}'
```

### Scatter Plot

```bash
python ./scripts/generate.py '{
  "tool": "generate_scatter_chart",
  "args": {
    "data": [
      {"x": 160, "y": 50},
      {"x": 170, "y": 65},
      {"x": 180, "y": 70}
    ],
    "title": "Height vs Weight Correlation",
    "axisXTitle": "Height (cm)",
    "axisYTitle": "Weight (kg)"
  }
}'
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VIS_REQUEST_SERVER` | Chart generation API endpoint | `https://antv-studio.alipay.com/api/gpt-vis` |
| `SERVICE_ID` | Optional service identifier | - |

## Project Structure

```
chart-visualization-skills/
├── LICENSE              # MIT License
├── README.md           # This file
├── SKILL.md            # Skill workflow documentation
├── scripts/
│   └── generate.py     # Chart generation script
└── references/         # Chart type specifications (26 files)
    ├── generate_line_chart.md
    ├── generate_bar_chart.md
    ├── generate_scatter_chart.md
    └── ...
```

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Developed by the [AntV Visualization Team](https://github.com/antvis)

Powered by [AntV](https://antv.antgroup.com/) - A professional data visualization solution

---

<div align="center">

**Made with ❤️ by the AntV Team**

[GitHub](https://github.com/antvis) • [AntV Website](https://antv.antgroup.com/)

</div>