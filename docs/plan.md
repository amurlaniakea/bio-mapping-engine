# 🗺️ Implementation Plan: Bio-Mapping Engine

**Status:** 🚀 Planning Phase
**Reference Spec:** `docs/spec.md`

## 🎯 Overview
This plan decomposes the `spec.md` into actionable, atomic milestones to guide the implementation of the Bio-Mapping Engine.

---

## 🏁 Milestone 1: Data Extraction & Foundation (The Parser)
*Goal: Transform `Biodescodificacion.pdf` into a structured `processed_data.json`.*

### 1.1 Environment Setup
- [ ] Create `venv`.
- [ ] Install dependencies (`pypdf`, `pytest`).
- [ ] Initialize Git repository with professional structure.

### 1.2 The Extraction Pipeline
- [ ] **Module: `src/parser/cleaner.py`**: Implement text sanitization (remove page numbers, noise).
- [ ] **Module: `src/parser/segmenter.py`**: Implement regex-based chunking to identify symptom blocks and author names.
- [ ] **Module: `src/parser/mapper.py`**: Implement the initial mapping of symptoms to the Canonical Ontology (Zone/System).
- [ ] **Output Generation**: Script to save the final structured JSON.

### 1.3 Verification (Milestone 1)
- [ ] **Truth Test**: Compare JSON content against manual PDF reading.
- [ ] **Schema Validation**: Ensure JSON strictly adheres to `spec.md` schema.

---

## 🔍 Milestone 2: Search Engine Core (The Mapping Engine)
*Goal: Implement the multivector search logic.*

### 2.1 Core Engine Development
- [ ] **Module: `src/engine/search.py`**: Implement the search algorithm.
- [ ] **Feature: Vector Intersections**: Implement logic to combine (Symptom AND Zone) or (Zone only).
- [ ] **Feature: Fuzzy Matching**: Implement basic synonym/typo handling for user input.

### 2.2 Testing
- [ ] Unit tests for the search logic.
- [ ] Integration tests with the `processed_data.json`.

---

## 🖥️ Milestone 3: CLI & Compliance (The Interface)
*Goal: Finalize the user experience and legal integrity.*

### 3.1 CLI Implementation
- [ ] **Module: `src/cli/main.py`**: Implement the command-line interface.
- [ ] **User UX**: Clear input prompts and formatted, readable outputs.

### 3.2 Legal & Documentation
- [ ] **README.md**: Finalize with AGPL-3.0, citations, and the mandatory Medical Disclaimer.
- [ ] **Disclaimer Integration**: Ensure every CLI output includes the required legal warning.

---

## 🛠️ Commit Strategy
Each task in the `tasks.md` should correspond to a single, atomic Git commit.
`feat: implement regex-based segmenter`
`fix: resolve pagination noise in parser`
`docs: update readme with disclaimer`
