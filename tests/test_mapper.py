from src.parser.mapper import map_segment

def test_map_segment_basic():
    segment = {
        "header": "ACNÉ",
        "content": "Louise L. Hay: Causa probable: No aceptación de uno mismo. Nuevo modelo mental: Soy divina."
    }
    result = map_segment(segment)
    assert result["sintoma_canonico"] == "ACNÉ"
    assert len(result["interpretaciones"]) == 1
    assert result["interpretaciones"][0]["autor"] == "Louise L. Hay"
    assert "No aceptación" in result["interpretaciones"][0]["conflicto_emocional"]

def test_map_segment_multi_author():
    segment = {
        "header": "ACNÉ",
        "content": "Louise L. Hay: Causa probable: No aceptación. \nLisa Bourbeau: Bloqueo Emocional: Deseo de no acercarse."
    }
    result = map_segment(segment)
    assert len(result["interpretaciones"]) == 2
    assert result["interpretaciones"][0]["autor"] == "Louise L. Hay"
    assert result["interpretaciones"][1]["autor"] == "Lisa Bourbeau"

def test_map_segment_zones():
    segment = {
        "header": "ACNÉ",
        "content": "Problema en la piel y el rostro."
    }
    result = map_segment(segment)
    assert "piel" in result["zonas_detectadas"]
    assert "cara" in result["zonas_detectadas"]

def test_map_segment_unknown_author():
    segment = {
        "header": "DOLOR",
        "content": "Conflicto: Dolor intenso."
    }
    result = map_segment(segment)
    assert result["interpretaciones"][0]["autor"] == "General/No especificado"
    assert "Dolor intenso" in result["interpretaciones"][0]["conflicto_emocional"]
