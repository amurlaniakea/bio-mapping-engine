# Bio-Mapping Engine Architecture

This document describes the architectural design and data flow of the **Bio-Mapping Engine**.

## 🏗️ System Overview

The Bio-Mapping Engine is designed to convert unstructured PDF literature into a structured, topological knowledge graph. It operates through a linear pipeline of specialized processing stages.

## 🔄 Data Pipeline

The pipeline consists of four primary stages:

### 1. Text Cleaning
* **Input:** Raw text extracted from PDF files.
* **Process:** Removal of page numbers, headers/footers, and non-textual noise.
* **Output:** A clean, continuous stream of text.

### 2. Semantic Segmentation
* **Input:** Cleaned text stream.
* **Process:** Identification of "Symptom Blocks" using a topological segmentation algorithm. 
    * The engine identifies **Headers** (symptom names in uppercase).
    * It intelligently ignores **Index Entries** (lines with trailing numbers) to prevent noise.
    * It aggregates content under the most recent valid header.
* **Output:** A list of raw symptom segments (Header + Content).

### 3. Semantic Mapping
* **Input:** Raw symptom segments.
* **Process:** 
    * **Author Attribution:** Splits segments based on identified authors (e.g., Louise L. Hay, Jacques Martel).
    * **Field Extraction:** Uses regex-based pattern matching to extract `conflicto_emocional`, `modelo_mental`, and `etapa_biologica`.
    * **Fallback Engine:** For authors or segments without explicit markers, a secondary heuristic extracts the most relevant descriptive text.
    * **Anatomical Mapping:** Maps keywords in the content and header to a hierarchical anatomical ontology (System $\rightarrow$ Region $\rightarrow$ Organ).
* **Output:** Structured interpretation objects.

### 4. Data Serialization
* **Input:** Structured interpretation objects.
* **Process:** Aggregation into a master JSON dataset.
* **Output:** `data/processed/processed_data.json`.

## 📊 Data Schema

The final dataset is a JSON array of objects with the following structure:

```json
{
  "id": "uuid-string",
  "sintoma_canonico": "ACNÉ",
  "zonas_detectadas": ["piel", "cara"],
  "sistema_padre": "Desconocido",
  "interpretaciones": [
    {
      "autor": "Louise L. Hay",
      "conflicto_emocional": "Causa probable: No aceptación de uno mismo.",
      "modelo_mental": "Soy divina.",
      "etapa_biologica": "Etapa 1"
    }
  ],
  "keywords": ["acné", "piel"]
}
```

## 🛠️ Technology Stack

* **Language:** Python 3.12+
* **Core Libraries:** `re` (Regex), `json` (Data serialization), `uuid` (Unique identifiers).
* **Methodology:** Spec-Driven Development (SDD).
