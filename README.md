# 🧬 Bio-Mapping Engine

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agp3.0.html)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)

**Bio-Mapping Engine** is a high-fidelity semantic extraction and topological mapping framework designed to transform unstructured esoteric literature—specifically from the field of **Biodescodificación**—into a structured, multidimensional, and navigable knowledge base.

Utilizing advanced semantic segmentation and topological mapping, the engine extracts and formalizes complex relational archetypes between biological symptoms, anatomical locations, and emotional conflict models.

---

## 🔍 Key Features

* **Advanced Semantic Segmentation:** Topological parsing that intelligently distinguishes between symptom headers, emotional content, and structural noise (indices/navigation).
* **Multidimensional Relational Mapping:** High-fidelity extraction of complex relationships across three primary vectors:
    * **Canonical Symptoms:** Standardized nomenclature for symptoms and conditions.
    * **Anatomical Hierarchy:** Intelligent mapping from biological Systems $\\rightarrow$ Regions $\\rightarrow$ Organs.
    * **Emotional Archetypes:** Structured extraction of emotional conflicts and mental models (e.g., "Causa probable", "Bloqueo emocional").
* **Multi-Axis Querying:** A powerful CLI designed for cross-referencing symptoms, physical zones, and emotional archetypes.
* **Robust Fallback Intelligence:** Heuristic text-scraping for authors (e.g., Jacques Martel) who lack explicit structural prefixes.

---

## 🚀 Installation

### Prerequisites
* Python 3.12 or higher.

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/amurlaniakea/bio-mapping-engine.git
   cd bio-mapping-engine
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Data Ingestion:**
   Place your source PDF in `data/raw/Biodescodificacion.pdf`.

---

## 🛠️ Usage

### 1. Build the Knowledge Base
Run the ingestion pipeline to process the raw PDF and generate the structured dataset:
```bash
python main.py
```
The engine will clean the text, segment it into symptom blocks, and map each block into a structured JSON format stored in `data/processed/`.

### 2. Query the Engine
Get real-time insights using the CLI to explore the extracted knowledge base.

**Search by Symptom:**
```bash
python src/cli/main.py --symptom "acné"
```

**Search by Physical Zone:**
```bash
python src/cli/main.py --zone "estómago"
```

**Multi-Vector Intersection Search:**
Find symptoms related to a specific condition within a specific body part:
```bash
python src/cli/main.py --symptom "acné" --zone "cara"
```

---

## 🏛️ Architecture & Methodology

Engineered under the **Spec-Driven Development (SDD)** lifecycle to ensure maximum technical rigor, traceability, and structural integrity.

### Data Pipeline Flow
`Raw PDF` $\\rightarrow$ `Text Cleaning` $\\rightarrow$ `Semantic Segmentation` $\\rightarrow$ `Semantic Mapping` $\\rightarrow$ `Structured JSON`

### Data Schema
The output is a high-fidelity JSON dataset. Each entry represents a canonical symptom and includes:
| Field | Description |
| :--- | :--- |
| **Anatomical Zones** | A hierarchy of detected physical locations. |
| **Interpretations** | A list of mappings, including the author, emotional conflict, mental model, and biological stage. |
| **Keywords** | Extracted semantic tags for rapid indexing. |

---

## ⚠️ Medical Disclaimer

**IMPORTANT:** This software is a research and educational tool designed for the analysis of alternative medicine literature.

**IT IS NOT A MEDICAL DEVICE.** This tool does not provide medical diagnoses, treatments, or clinical advice. Always consult a qualified healthcare professional for any medical concerns. The developers and authors of the source literature are not responsible for any decisions made based on the output of this software.

---

## 📜 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. See the [LICENSE](LICENSE) file for details.

## 👤 Author

**Pedro Sordo Martínez** — [amurlaniakea@gmail.com](mailto:amurlaniakea@gmail.com)
