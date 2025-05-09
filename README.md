# 🏛️ Pattern-Scale – Architecture Pattern Evaluation Platform

**Pattern-Scale** is a Streamlit-based web application for analyzing and comparing software architecture patterns. The platform allows users to explore various patterns, run custom tests, and visualize results through an intuitive interface backed by modular, well-structured Python logic.

## 📌 Table of Contents

- [Overview](#-overview)
- [Architecture](#%EF%B8%8F-architecture)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Contributing](#-contributing)
- [License](#-license)
- [Useful Links](#-useful-links)

---

## 🧭 Overview

Pattern-Scale provides insights into architecture patterns by:
- Allowing users to compare multiple patterns
- Enabling custom test runs
- Displaying metrics and visualizations
- Supporting extensibility through modular components

---

## 🏗️ Architecture

```mermaid
graph TB
    %% UI Layer
    Browser["Client Browser"]:::ui

    %% Backend Server
    subgraph "Streamlit Server" 
        direction TB
        App["app.py"]:::backend
        Config[".streamlit/config.toml"]:::config
    end

    %% Page Routing
    subgraph "Page Routing" 
        direction TB
        About["about.py"]:::backend
        Comparison["comparison.py"]:::backend
        CustomTest["custom_test.py"]:::backend
        Dashboard["dashboard.py"]:::backend
    end

    %% Business Logic
    subgraph "Core Logic (utils)" 
        direction TB
        DataManager["data_manager.py"]:::logic
        TestRunner["test_runner.py"]:::logic
        MetricsAnalyzer["metrics_analyzer.py"]:::logic
        Visualization["visualization.py"]:::logic
    end

    %% Data & Assets
    DataStore["architecture_patterns.json"]:::data
    Assets["Updated Clarify.docx"]:::assets

    %% Configuration & Docs
    Dependencies["pyproject.toml"]:::config
    Lockfile["package-lock.json"]:::config
    Docs["README.md"]:::external

    %% Relationships
    Browser -->|"HTTP Request"| App
    App -->|"routes to"| About
    App -->|"routes to"| Comparison
    App -->|"routes to"| CustomTest
    App -->|"routes to"| Dashboard

    About -->|"calls"| DataManager
    Comparison -->|"calls"| DataManager
    Comparison -->|"calls"| TestRunner
    CustomTest -->|"calls"| TestRunner
    Dashboard -->|"calls"| DataManager

    DataManager -->|"loads data from"| DataStore
    TestRunner -->|"produces results"| MetricsAnalyzer
    MetricsAnalyzer -->|"computes metrics for"| Visualization
    Visualization -->|"returns UI components to"| About
    Visualization -->|"returns UI components to"| Comparison
    Visualization -->|"returns UI components to"| CustomTest
    Visualization -->|"returns UI components to"| Dashboard

    App -->|"uses config"| Config
    App -->|"uses deps"| Dependencies
    App -->|"uses lockfile"| Lockfile
    App -->|"project docs"| Docs

    About -->|"may embed assets"| Assets
    Comparison -->|"may embed assets"| Assets
    CustomTest -->|"may embed assets"| Assets
    Dashboard -->|"may embed assets"| Assets

    %% Click Events
    click App "https://github.com/jashwanth-kumar/pattern-scale/blob/main/app.py"
    click Config "https://github.com/jashwanth-kumar/pattern-scale/blob/main/.streamlit/config.toml"
    click About "https://github.com/jashwanth-kumar/pattern-scale/blob/main/pages/about.py"
    click Comparison "https://github.com/jashwanth-kumar/pattern-scale/blob/main/pages/comparison.py"
    click CustomTest "https://github.com/jashwanth-kumar/pattern-scale/blob/main/pages/custom_test.py"
    click Dashboard "https://github.com/jashwanth-kumar/pattern-scale/blob/main/pages/dashboard.py"
    click DataManager "https://github.com/jashwanth-kumar/pattern-scale/blob/main/utils/data_manager.py"
    click TestRunner "https://github.com/jashwanth-kumar/pattern-scale/blob/main/utils/test_runner.py"
    click MetricsAnalyzer "https://github.com/jashwanth-kumar/pattern-scale/blob/main/utils/metrics_analyzer.py"
    click Visualization "https://github.com/jashwanth-kumar/pattern-scale/blob/main/utils/visualization.py"
    click DataStore "https://github.com/jashwanth-kumar/pattern-scale/blob/main/data/architecture_patterns.json"
    click Assets "https://github.com/jashwanth-kumar/pattern-scale/blob/main/attached_assets/Updated Clarify.docx"
    click Dependencies "https://github.com/jashwanth-kumar/pattern-scale/blob/main/pyproject.toml"
    click Lockfile "https://github.com/jashwanth-kumar/pattern-scale/blob/main/package-lock.json"
    click Docs "https://github.com/jashwanth-kumar/pattern-scale/blob/main/README.md"

    %% Styling
    classDef ui fill:#D0E6FF,stroke:#0366d6,color:#0366d6;
    classDef backend fill:#E8F5E9,stroke:#2E7D32,color:#2E7D32;
    classDef logic fill:#FFF3E0,stroke:#FB8C00,color:#e65100;
    classDef data fill:#FFFDE7,stroke:#F9A825,color:#F57F17;
    classDef assets fill:#ECEFF1,stroke:#607D8B,color:#455A64;
    classDef config fill:#F3E5F5,stroke:#8E24AA,color:#6A1B9A;
    classDef external fill:#F5F5F5,stroke:#9E9E9E,color:#616161;
```

### Key Components:

- **UI Layer**: Client interacts through a browser via Streamlit.
- **Backend Routing**: Main app file (`app.py`) routes to specific pages.
- **Page Modules**: Each major section like Comparison or Dashboard has its own module.
- **Core Logic**: Business logic is encapsulated in utilities under the `utils/` directory.
- **Data & Assets**: Stores static JSON data and embeddable documents.
- **Configuration**: Project and server settings managed via TOML and lockfiles.

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.8+
- `pip` or `poetry`
- Git

### 📦 Installation

```bash
git clone https://github.com/jashwanth-kumar/pattern-scale.git
cd pattern-scale
pip install -r requirements.txt
```

Or with `poetry`:

```bash
poetry install
```

### ▶️ Running the App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
pattern-scale/
│
├── app.py                         # Main Streamlit entry point
├── .streamlit/config.toml        # Streamlit configuration
│
├── pages/                         # Routed Streamlit pages
│   ├── about.py
│   ├── comparison.py
│   ├── custom_test.py
│   └── dashboard.py
│
├── utils/                         # Core logic modules
│   ├── data_manager.py
│   ├── test_runner.py
│   ├── metrics_analyzer.py
│   └── visualization.py
│
├── data/
│   └── architecture_patterns.json
│
├── attached_assets/
│   └── Updated Clarify.docx
│
├── pyproject.toml                 # Project dependencies
├── package-lock.json             # Lock file
└── README.md                      # Documentation
```

---

## 🧰 Tech Stack

- **Frontend/UI**: Streamlit
- **Backend**: Python
- **Data Format**: JSON
- **Visualization**: Custom Streamlit components
- **Dependency Management**: Poetry / pip

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request 🚀

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🔗 Useful Links

- [Live Demo (if hosted)](https://share.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [GitHub Repository](https://github.com/jashwanth-kumar/pattern-scale)
