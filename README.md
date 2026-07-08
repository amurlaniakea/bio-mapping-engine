# 🧬 Bio-Mapping Engine

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agp3.0.html)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/)

**Bio-Mapping Engine** is a professional-grade tool designed to transform unstructured literature from the field of **Biodescodificación** into a structured, searchable, and navigable knowledge base. 

By applying a topological mapping approach, the engine extracts complex relationships between biological symptoms, physical locations, and emotional conflicts, making esoteric knowledge accessible through modern data science techniques.

---

## 🔍 Key Features

* **Multivector Search:** Query the database using three independent axes:
    * **Symptom/Disease:** Exact or fuzzy matches.
    * **Physical Zone:** Navigate through an anatomical hierarchy (System $\rightarrow$ Region $\rightarrow$ Organ).
    * **Emotional Description:** Keyword-based search within emotional conflict descriptions.
* **Automated Extraction Pipeline:** Converts raw PDF data into a structured JSON format using a semantic segmentation engine.
* **Canonical Mapping:** Automatically translates colloquial terms into a standardized anatomical ontology.
* **Professional CLI:** A clean, intuitive command-line interface for rapid data exploration.

---

## 🚀 Installation

### Prerequisites
* Python 3.12 or higher.

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/amurlaniakea/bio-mapping-engine.git
   cd bio-mapping-engine
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your data:**
   Place your source PDF in `data/raw/Biodescodificacion.pdf`.

---

## 🛠️ Usage

### 1. Build the Dataset
First, run the ingestion pipeline to process the raw PDF:
```bash
python main.py
```

### 2. Query the Engine
Use the CLI to search for symptoms, zones, or descriptions.

**Search by Symptom:**
```bash
python src/cli/main.py --symptom "acné"
```

**Search by Physical Zone:**
```bash
python src/cli/main.py --zone "estómago"
```

**Multivector Search (Intersection):**
```bash
python src/cli/main.py --symptom "acné" --zone "cara"
```

---

## 🏛️ Architecture & Methodology

This project follows the **Spec-Driven Development (SDD)** methodology, ensuring that every line of code is a direct implementation of a technical requirement.

### Data Pipeline
`Raw PDF` $\rightarrow$ `Text Cleaning` $\rightarrow$ `Semantic Segmentation` $\rightarrow$ `Semantic Mapping` $\rightarrow$ `Structured JSON`

### Data Schema
The engine produces a high-fidelity JSON dataset where each entry maps symptoms to their emotional roots, authors, and canonical anatomical locations.

---

## ⚠️ Medical Disclaimer

**IMPORTANT:** This software is a research and educational tool. It is intended for the analysis of alternative medicine literature. 

**IT IS NOT A MEDICAL DEVICE.** This tool does not provide medical diagnoses, treatments, or clinical advice. Always consult a qualified healthcare professional for any medical concerns. The developers and authors of the source literature are not responsible for any decisions made based on the output of this software.

---

## 📜 License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. See the [LICENSE](LICENSE) file for details.

## 👤 Author

**Pedro Sordo Martínez** — [amurlaniakea@gmail.com](mailto:amurlaniakea@gmail.com)
