# ✅ Bio-Mapping Engine: Task Checklist

**Status:** 📝 Planning Phase
**Reference Plan:** `docs/plan.md`

---

## 🏗️ Milestone 1: Data Extraction & Foundation
- [ ] **M1.1: Environment Setup**
    - [ ] Create `venv`
    - [ ] Install `pypdf`, `pytest`
    - [ ] Git init & structure
- [ ] **M1.2: The Extraction Pipeline**
    - [ ] Implement `src/parser/cleaner.py`
    - [ ] Implement `src/parser/segmenter.py`
    - [ ] Implement `src/parser/mapper.py`
    - [ ] Run extraction & generate `data/processed/processed_data.json`
- [ ] **M1.3: Verification**
    - [ ] Perform "Truth Test" (Manual vs JSON)
    - [ ] Perform Schema Validation

## 🔍 Milestone 2: Search Engine Core
- [ ] **M2.1: Core Engine**
    - [ ] Implement `src/engine/search.py`
    - [ ] Implement Vector Intersection logic
    - [ ] Implement Fuzzy/Synonym matching
- [ ] **M2.2: Testing**
    - [ ] Unit tests for search logic
    - [ ] Integration tests with JSON data

## 🖥️ Milestone 3: CLI & Compliance
- [ ] **M3.1: CLI Implementation**
    - [ ] Implement `src/cli/main.py`
    - [ ] Format terminal output for readability
- [ ] **M3.2: Legal & Documentation**
    - [ ] Finalize `README.md` (AGPL-3, Citations, Disclaimer)
    - [ ] Verify Disclaimer in CLI output

---
**Notes:**
*   *Always follow the SDD commit strategy.*
*   *Do not skip verification steps.*
