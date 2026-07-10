import json
import pytest
import os
from src.engine.search import SearchEngine

@pytest.fixture
def mock_engine(tmp_path):
    data_file = tmp_path / "test_data.json"
    data = [
        {
            "sintoma_canonico": "ACNÉ",
            "zonas_detectadas": ["piel", "cara"],
            "interpretaciones": [
                {"conflicto_emocional": "ira contenida", "modelo_mental": "biológico"},
                {"conflicto_emocional": "necesidad de ser visto", "modelo_mental": "psicológico"}
            ]
        },
        {
            "sintoma_canonico": "GASTRITIS",
            "zonas_detectadas": ["estómago"],
            "interpretaciones": [
                {"conflicto_emocional": "dificultad para digerir situaciones", "modelo_mental": "emocional"}
            ]
        }
    ]
    data_file.write_text(json.dumps(data))
    return SearchEngine(str(data_file))

def test_load_data_error(tmp_path):
    # Test error loading data (file not found)
    engine = SearchEngine(str(tmp_path / "non_existent.json"))
    assert engine.data == []

def test_normalize(mock_engine):
    # Test internal _normalize (via search)
    # Using a trick to access protected method for testing if needed, 
    # but let's just use the search methods.
    assert mock_engine.search_by_symptom("ACNÉ!") == mock_engine.search_by_symptom("acne")

def test_search_by_symptom_variants(mock_engine):
    assert len(mock_engine.search_by_symptom("acne")) == 1
    assert len(mock_engine.search_by_symptom("GASTRITIS")) == 1
    assert len(mock_engine.search_by_symptom("unknown")) == 0

def test_search_by_zone_variants(mock_engine):
    assert len(mock_engine.search_by_zone("cara")) == 1
    assert len(mock_engine.search_by_zone("estómago")) == 1
    assert len(mock_engine.search_by_zone("unknown")) == 0

def test_search_by_description_variants(mock_engine):
    # Test description search (conflicto_emocional and modelo_mental)
    assert len(mock_engine.search_by_description("ira")) == 1
    assert len(mock_engine.search_by_description("biológico")) == 1
    assert len(mock_engine.search_by_description("digerir")) == 1
    assert len(mock_engine.search_by_description("unknown")) == 0

def test_search_by_description_empty_query(mock_engine):
    assert mock_engine.search_by_description("") == []

def test_multi_vector_search_full(mock_engine):
    # Symptom: ACNÉ AND Zone: cara
    results = mock_engine.multi_vector_search(symptom="acné", zone="cara")
    assert len(results) == 1
    assert results[0]["sintoma_canonico"] == "ACNÉ"

def test_multi_vector_search_partial(mock_engine):
    # Only symptom
    results = mock_engine.multi_vector_search(symptom="acné")
    assert len(results) == 1
    
    # Only zone
    results = mock_engine.multi_vector_search(zone="cara")
    assert len(results) == 1

def test_multi_vector_search_no_results(mock_engine):
    # Symptom: ACNÉ AND Zone: estómago (no intersection)
    results = mock_engine.multi_vector_search(symptom="acné", zone="estómago")
    assert len(results) == 0

def test_multi_vector_search_empty_inputs(mock_engine):
    assert mock_engine.multi_vector_search() == []

def test_multi_vector_search_description_match(mock_engine):
    # Symptom: ACNÉ AND Description: ira
    results = mock_engine.multi_vector_search(symptom="acné", description="ira")
    assert len(results) == 1
