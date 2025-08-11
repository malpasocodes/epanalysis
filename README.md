# ROI Analytics Platform for California Associate's Degree Programs

[![Version](https://img.shields.io/badge/version-v1.0-blue.svg)](https://github.com/malpasocodes/epanalysis/releases)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/streamlit-1.48+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Live Site](https://img.shields.io/badge/live%20site-edroi.org-brightgreen.svg)](http://edroi.org)

> **🌐 Live Application**: **[http://edroi.org](http://edroi.org)**

A comprehensive research and policy analysis platform for evaluating Return on Investment (ROI) metrics and earnings premiums across California's Associate's degree-granting institutions. This tool demonstrates the impact of different baseline methodologies on institutional rankings and provides critical insights for education policy decision-making.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Demo & Screenshots](#demo--screenshots)
- [Quick Start](#quick-start)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Technology Stack](#technology-stack)
- [Data Sources & Methodology](#data-sources--methodology)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [Research Context](#research-context)
- [License](#license)
- [Citation](#citation)
- [Support](#support)

---

## Overview

The **ROI Analytics Platform** is a sophisticated research tool designed to analyze and visualize the impact of California's Earnings Premium (EP) Regulation on Associate's degree-granting institutions. By comparing statewide versus regional (county-based) baseline methodologies, this platform reveals how different calculation approaches can significantly affect institutional rankings and policy outcomes.

### Core Research Question

**How do statewide versus regional baseline methodologies impact ROI calculations and institutional rankings for California Associate's degree programs?**

This platform demonstrates that institutions in economically disadvantaged regions may be unfairly penalized when using statewide baselines, while regional baselines provide more equitable comparisons by accounting for local economic conditions.

---

## Key Features

### 📊 **Comprehensive Metrics Analysis**
- **Dual Baseline Comparison**: Side-by-side analysis of statewide vs. regional ROI calculations
- **Earnings Premium Analysis**: C-Metric vs H-Metric comparisons with interactive delta tables
- **Dynamic Rankings**: Real-time ranking changes based on methodology selection
- **Statistical Significance Testing**: Built-in statistical validation for methodology comparisons

### 🎯 **Interactive Data Exploration**
- **Quadrant Analysis Charts**: Net price vs. median earnings visualizations
- **Sector-Based Analysis**: Public vs. private institution comparisons
- **Geographic Insights**: County-level baseline impact analysis
- **Customizable Views**: User-controlled data filtering and display options

### 📈 **Advanced Analytics**
- **120 Institution Coverage**: Complete dataset of California Associate's degree institutions
- **Multi-Dimensional Ranking**: Years-to-recoup analysis with comprehensive ROI metrics
- **Data Export Capabilities**: Research-ready datasets for further analysis
- **Methodology Transparency**: Full calculation documentation and assumptions

### 🔧 **Research-Grade Infrastructure**
- **Optimized Performance**: Cached data loading with sub-second response times
- **Professional Deployment**: Production-ready Render deployment configuration
- **Version Control**: Comprehensive git workflow with documented releases
- **Extensible Architecture**: Modular design supporting additional analysis modules

---

## Demo & Screenshots

> **Live Demo**: **[http://edroi.org](http://edroi.org)**

### Main Dashboard
![Dashboard Preview](docs/images/dashboard-preview.png)
*Interactive dashboard showing earnings premium comparison and ranking analysis*

### Quadrant Analysis
![Quadrant Chart](docs/images/quadrant-analysis.png)
*Net price vs. earnings analysis with institutional positioning*

### Rankings Comparison
![Rankings Table](docs/images/rankings-comparison.png)
*Side-by-side rankings showing methodology impact*

---

## Quick Start

Get the ROI Analytics Platform running in under 5 minutes:

```bash
# Clone the repository
git clone https://github.com/malpasocodes/epanalysis.git
cd epanalysis

# Install UV package manager (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and run the application
uv sync
uv run streamlit run app.py
```

The application will be available at `http://localhost:8501`

---

## Installation & Setup

### Prerequisites

- **Python 3.13+** (recommended)
- **UV Package Manager** (preferred) or pip
- **Git** for version control

### Method 1: Using UV (Recommended)

```bash
# Clone the repository
git clone https://github.com/malpasocodes/epanalysis.git
cd epanalysis

# Create virtual environment and install dependencies
uv sync

# Run the application
uv run streamlit run app.py
```

### Method 2: Using pip

```bash
# Clone the repository
git clone https://github.com/malpasocodes/epanalysis.git
cd epanalysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### Alternative Port Configuration

If the default port (8501) is in use:

```bash
uv run streamlit run app.py --server.port 8502
```

### Development Setup

For development with additional tools:

```bash
# Install development dependencies
uv sync --dev

# Clear Streamlit cache during development
# Access via the app's "Clear Cache" option or programmatically
```

---

## Usage Guide

### Navigation Structure

The platform uses a hierarchical sidebar navigation system:

#### **🏠 Home**
- Project overview and baseline impact analysis
- Key findings summary
- Quick access to main features

#### **📊 Metrics Comparison**
- **Read First**: Essential methodology overview
- **Earnings Premium**: C-Metric vs H-Metric analysis with Delta tables
- **ROI Analysis**: Years to recoup costs analysis
- **College View**: Individual institution deep-dive

#### **📈 Rankings**
- **Earnings Premium Rankings**: Methodology-based ranking comparisons
- **ROI Rankings**: Years-to-recoup ranking analysis

#### **🔍 Data Analysis**
- **Interactive Charts**: Quadrant analysis and sector comparisons
- **Geographic Analysis**: County-level impact studies
- **Statistical Testing**: Methodology validation tools

#### **📚 Methodology & Data**
- Data sources and collection methodology
- Calculation formulas and assumptions
- Baseline methodology explanations

### Key Workflows

#### **1. Baseline Impact Analysis**
1. Navigate to **Home** → Review baseline comparison overview
2. Go to **Metrics Comparison** → **Earnings Premium**
3. Adjust the "Number of institutions to display" slider
4. Analyze the Delta column to see ranking changes

#### **2. Institution-Specific Analysis**
1. Use **Data Analysis** → **Interactive Charts**
2. Hover over points to see institution details
3. Use **College View** for detailed institutional profiles
4. Export data for further analysis

#### **3. Policy Research Workflow**
1. Start with **Methodology & Data** to understand calculations
2. Use **Rankings** to compare methodological impacts
3. Leverage **Data Analysis** for statistical validation
4. Export findings using **Tools & Export**

---

## Technology Stack

### **Core Framework**
- **[Streamlit](https://streamlit.io/)** `v1.48+` - Interactive web application framework
- **[Python](https://python.org/)** `v3.13` - Primary programming language

### **Data Processing & Analysis**
- **[Pandas](https://pandas.pydata.org/)** `v2.0+` - Data manipulation and analysis
- **[NumPy](https://numpy.org/)** `v1.24+` - Numerical computing foundation

### **Visualization**
- **[Altair](https://altair-viz.github.io/)** `v5.5+` - Statistical visualization library
- **Streamlit Native Charts** - Built-in charting components

### **Development & Deployment**
- **[UV](https://github.com/astral-sh/uv)** - Fast Python package manager
- **[Render](https://render.com/)** - Cloud deployment platform
- **Git** - Version control and collaboration

### **Architecture Benefits**
- **Performance**: Cached data loading with optimized CSV processing
- **Scalability**: Modular architecture supporting additional analysis modules
- **Maintainability**: Clear separation of concerns with dedicated modules
- **Extensibility**: Plugin-ready structure for custom analysis tools

---

## Data Sources & Methodology

### **Primary Dataset**
- **File**: `data/roi-metrics.csv`
- **Coverage**: 120 California Associate's degree-granting institutions
- **Content**: Pre-calculated ROI metrics, earnings premiums, and rankings
- **Update Frequency**: Annual (based on federal data releases)

### **Supporting Datasets**
- **Institution Characteristics**: `data/gr-institutions.csv` (sector, location, enrollment)
- **County Baselines**: `data/hs_median_county_25_34.csv` (regional high school earnings)
- **Statewide Baseline**: $24,939.44 (calculated weighted average)

### **Data Processing Pipeline**
1. **Federal Data Integration**: College Scorecard and IPEDS data merger
2. **County Baseline Calculation**: Census ACS 5-year estimates processing
3. **ROI Metric Calculation**: Net present value analysis with standardized assumptions
4. **Ranking Generation**: Methodology-specific institutional ranking
5. **Quality Assurance**: Statistical validation and outlier detection

### **Key Metrics**
- **ROI (Years to Recoup)**: Time required to recover educational investment
- **Earnings Premium**: Graduate earnings above high school baseline
- **Net Price**: Annual cost after financial aid
- **Median Earnings**: 10-year post-graduation earnings data

### **Methodology Transparency**
All calculation methodologies, data sources, and assumptions are fully documented in the **Methodology & Data** section of the application. Research-grade documentation ensures reproducibility and academic rigor.

---

## Project Structure

```
epanalysis/
├── README.md                 # This file
├── CLAUDE.md                 # AI assistant guidelines
├── pyproject.toml           # Project configuration and dependencies
├── render.yaml              # Deployment configuration
├── requirements.txt         # Pip dependencies (backup)
├── uv.lock                  # Dependency lock file
│
├── app.py                   # Main Streamlit application entry point
├── config.py                # Application configuration
│
├── lib/                     # Core application modules
│   ├── __init__.py
│   ├── data.py              # Primary data loading and processing
│   ├── ui.py                # User interface rendering functions
│   ├── charts.py            # Altair visualization components
│   ├── components.py        # Reusable UI components
│   ├── hs_baseline.py       # Baseline calculation utilities
│   ├── models.py            # Data models and schemas
│   └── utils.py             # General utility functions
│
├── data/                    # Dataset storage
│   ├── roi-metrics.csv      # Primary analysis dataset (120 institutions)
│   ├── gr-institutions.csv  # Institution characteristics
│   ├── hs_median_county_25_34.csv # County baseline earnings
│   ├── dataprep/           # Data preparation scripts and intermediate files
│   └── archive/            # Legacy datasets and processing scripts
│
├── content/                 # Application content and documentation
│   └── read_first.md       # User guidance content
│
├── documentation/          # Project documentation
│   ├── DATASETS.md         # Dataset documentation
│   ├── METRICS.md          # Metrics calculation documentation
│   └── archive/           # Historical documentation
│
└── archive/               # Legacy files and development history
    └── update_baseline.py  # Historical baseline update script
```

### **Module Descriptions**

- **`app.py`**: Main application with hierarchical navigation and page routing
- **`lib/data.py`**: Optimized data loading with caching and error handling
- **`lib/ui.py`**: Page rendering functions for all major application sections
- **`lib/charts.py`**: Interactive Altair visualizations with responsive design
- **`lib/hs_baseline.py`**: Statewide high school baseline calculations ($24,939.44)

---

## Contributing

We welcome contributions from researchers, developers, and policy analysts! Here's how to get involved:

### **Development Workflow**

```bash
# Fork the repository and clone your fork
git clone https://github.com/malpasocodes/epanalysis.git
cd epanalysis

# Create a feature branch
git checkout -b feature/your-feature-name

# Install development dependencies
uv sync --dev

# Make your changes and test
uv run streamlit run app.py

# Commit and push
git commit -m "Add: your feature description"
git push origin feature/your-feature-name

# Create a pull request
```

### **Contribution Areas**

- **📊 Data Analysis**: New metrics, statistical tests, visualization improvements
- **🎨 User Interface**: Enhanced UX, accessibility improvements, mobile optimization
- **📚 Documentation**: User guides, methodology documentation, API documentation
- **🔧 Infrastructure**: Performance optimization, deployment improvements, testing
- **🏛️ Policy Research**: Additional baseline methodologies, comparative studies

### **Code Standards**

- **Python**: Follow PEP 8 style guidelines
- **Documentation**: Include docstrings for all functions and classes
- **Testing**: Add tests for new functionality
- **Commits**: Use clear, descriptive commit messages
- **Dependencies**: Minimize new dependencies, document requirements

### **Research Contributions**

- **Methodology Improvements**: Enhanced ROI calculation methods
- **Dataset Expansion**: Additional institutional data sources
- **Comparative Analysis**: Cross-state or international comparisons
- **Policy Impact Studies**: Regulation effectiveness analysis

---

## Research Context

### **California's Earnings Premium Regulation**

The California Earnings Premium (EP) Regulation requires career education programs to demonstrate that their graduates earn more than high school graduates in the same geographic region. This platform addresses a critical policy question: **Should earnings comparisons use statewide or regional baselines?**

### **Policy Implications**

**Statewide Baseline Challenges:**
- Institutions in economically disadvantaged regions face unfair disadvantage
- Rural and urban institutions judged by different economic realities
- Potential program closure impacts on underserved communities

**Regional Baseline Benefits:**
- Accounts for local economic conditions and cost of living
- Provides more equitable comparisons across diverse regions
- Better reflects actual economic value for local students

### **Academic Research Applications**

This platform supports research in:
- **Education Policy**: Regulation impact assessment and policy optimization
- **Labor Economics**: Regional wage analysis and educational premium quantification
- **Public Policy**: Evidence-based regulatory framework development
- **Higher Education**: Institutional effectiveness measurement and improvement

### **Target Audiences**

- **Policy Researchers**: Academic and think tank researchers studying education regulation
- **Government Analysts**: State and federal education policy staff
- **Institutional Researchers**: College administrators and planning staff
- **Advocacy Organizations**: Groups representing students and institutions
- **Academic Community**: Researchers in education, economics, and public policy

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Summary**: You are free to use, modify, and distribute this software for any purpose, including commercial use, as long as you include the original copyright notice and license text.

---

## Citation

If you use this platform in your research, please cite:

```bibtex
@software{epanalysis2024,
  title = {ROI Analytics Platform for California Associate's Degree Programs},
  author = {[Your Name/Organization]},
  version = {1.0},
  year = {2024},
  url = {https://github.com/malpasocodes/epanalysis},
  note = {Research tool for analyzing earnings premium and ROI metrics}
}
```

**APA Style:**
[Your Name]. (2024). *ROI Analytics Platform for California Associate's Degree Programs* (Version 1.0) [Computer software]. https://github.com/malpasocodes/epanalysis

---

## Support

### **Getting Help**

- **📖 Documentation**: Start with the **Methodology & Data** section in the application
- **🐛 Bug Reports**: [Open an issue](https://github.com/malpasocodes/epanalysis/issues) with detailed description
- **💡 Feature Requests**: [Submit enhancement ideas](https://github.com/malpasocodes/epanalysis/issues) with use case details
- **❓ Questions**: Check [existing discussions](https://github.com/malpasocodes/epanalysis/discussions) or start a new one

### **Contact Information**

- **Project Maintainer**: [Your Name] - [your.email@domain.com]
- **Research Inquiries**: [research.contact@domain.com]
- **Technical Support**: [Open a GitHub Issue](https://github.com/malpasocodes/epanalysis/issues)

### **Acknowledgments**

- **Data Sources**: U.S. Department of Education College Scorecard, IPEDS, Census Bureau ACS
- **Policy Context**: California Community Colleges Chancellor's Office guidance
- **Technical Foundation**: Streamlit, Pandas, and Altair development communities

---

## Roadmap

### **Version 1.1 (Coming Soon)**
- Advanced statistical testing framework
- Export capabilities for research datasets
- Mobile-responsive design improvements
- Institution profile deep-dive pages

### **Version 1.2 (Planned)**
- Multi-state comparison capabilities
- Time-series analysis for regulation impact
- Custom baseline methodology builder
- API endpoint for programmatic access

### **Long-term Vision**
- Integration with additional federal datasets
- Machine learning-powered prediction models
- Interactive policy scenario modeling
- Collaborative research platform features

---

**Built with ❤️ for education policy research and data-driven decision making.**

---