from src.engine.search import SearchEngine


def test_search_by_symptom():
    # Create a mock engine with minimal data
    engine = SearchEngine.__new__(SearchEngine)
    engine.data = [
        {
            "sintoma_canonico": "ACNÉ",
            "zonas_detectadas": ["piel"],
            "interpretaciones": [],
        },
        {
            "sintoma_canonico": "GASTRITIS",
            "zonas_detectadas": ["estómago"],
            "interpretaciones": [],
        },
    ]

    results = engine.search_by_symptom("acné")
    assert len(results) == 1
    assert results[0]["sintoma_canonico"] == "ACNÉ"


def test_search_by_zone():
    engine = SearchEngine.__new__(SearchEngine)
    engine.data = [
        {
            "sintoma_canonico": "ACNÉ",
            "zonas_detectadas": ["piel", "cara"],
            "interpretaciones": [],
        },
        {
            "sintoma_canonico": "GASTRITIS",
            "zonas_detectadas": ["estómago"],
            "interpretaciones": [],
        },
    ]

    results = engine.search_by_zone("piel")
    assert len(results) == 1
    assert results[0]["sintoma_canonico"] == "ACNÉ"


def test_multi_vector_search():
    engine = SearchEngine.__new__(SearchEngine)
    engine.data = [
        {
            "sintoma_canonico": "ACNÉ",
            "zonas_detectadas": ["piel", "cara"],
            "interpretaciones": [],
        },
        {
            "sintoma_canonico": "ACNÉ",
            "zonas_detectadas": ["piel", "cuello"],
            "interpretaciones": [],
        },
        {
            "sintoma_canonico": "GASTRITIS",
            "zonas_detectadas": ["estómago"],
            "interpretaciones": [],
        },
    ]

    # Intersection of Symptom: ACNÉ and Zone: piel should return 2 results
    results = engine.multi_vector_search(symptom="acné", zone="piel")
    assert len(results) == 2

    # Intersection of Symptom: ACNÉ and Zone: cara should return 1 result
    results = engine.multi_vector_search(symptom="acné", zone="cara")
    assert len(results) == 1


def test_empty_search():
    engine = SearchEngine.__new__(SearchEngine)
    engine.data = []
    assert engine.search_by_symptom("anything") == []
    assert engine.search_by_zone("anything") == []
    assert engine.search_by_description("anything") == []
