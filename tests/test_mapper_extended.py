import pytest
import uuid
from src.parser.mapper import map_segment, AUTHORS, _get_interpretations, _apply_global_fallback


def test_map_segment_basic():
    segment = {
        "header": "ACNÉ",
        "content": "Conflicto: Identidad"
    }
    result = map_segment(segment)
    assert result["sintoma_canonico"] == "ACNÉ"
    assert len(result["interpretaciones"]) == 1
    assert result["interpretaciones"][0]["autor"] == "General/No especificado"


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


def test_map_segment_blacklist():
    segment = {
        "header": "EL",
        "content": "Some content"
    }
    result = map_segment(segment)
    assert "error" in result


def test_map_segment_short_header():
    segment = {
        "header": "A",
        "content": "Some content"
    }
    result = map_segment(segment)
    assert "error" in result


def test_map_segment_normalization():
    segment = {
        "header": "LA GASTRITIS",
        "content": "Conflicto: Hambre"
    }
    result = map_segment(segment)
    assert result["sintoma_canonico"] == "GASTRITIS"


def test_map_segment_complex_interpretation():
    # Test extract_field logic within _get_interpretations
    segment = {
        "header": "ACNÉ",
        "content": (
            "Jacques Martel: Nuevo modelo mental: El espejo. "
            "Resentir: No ser escuchado."
        )
    }
    result = map_segment(segment)
    # Since Jacques Martel is an author, it should create an interpretation
    # However, the current implementation might split things differently.
    # Let's check how many interpretations we get.
    # The author_pattern is 'Jacques Martel[\\s:]+'
    # parts will be ['', 'Jacques Martel', ' Nuevo modelo mental: El espejo. Resentir: No ser escuchado.']
    # Loop: i=1. raw_author_name = 'Jacques Martel'. 
    # author_content = ' Nuevo modelo mental: El espejo. Resentir: No ser escuchado.'
    # extract_field for conflicto_emocional will use [\\s:]+ patterns.
    # 'Resentir: No ser escuchado.' might not match the pattern if it's not in the author_content.
    # Actually, it's called on author_content.
    # We need to verify if the current implementation handles multiple fields for one author.
    # In the current code, extract_field is called for each field.
    # It doesn't look like it supports multiple fields in one block easily if they are separated by newlines but not markers.
    # Actually, it's called on author_content.
    assert any(interp["autor"] == "Jacques Martel" for interp in result["interpretaciones"])


def test_map_segment_fallback_logic():
    # Test _apply_global_fallback
    segment = {
        "header": "ACNÉ",
        "content": "Conflicto: Identidad. No hay autor."
    }
    result = map_segment(segment)
    # It should create a 'General/No especificado' interpretation.
    assert result["interpretaciones"][0]["autor"] == "General/No especificado"
    assert "Identidad" in result["interpretaciones"][0]["conflicto_emocional"]


def test_map_segment_empty_content():
    segment = {
        "header": "ACNÉ",
        "content": ""
    }
    result = map_segment(segment)
    assert result["interpretaciones"][0]["autor"] == "General/No especificado"
    assert result["interpretaciones"][0]["conflicto_emocional"] == ""


def test_map_segment_etapa_biologica():
    segment = {
        "header": "ACNÉ",
        "content": "Louise L. Hay: 1ª Etapa: Causa"
    }
    result = map_segment(segment)
    assert result["interpretaciones"][0]["etapa_biologica"] == "1ª Etapa: Causa"


def test_get_interpretations_general_fallback():
    """Test _get_interpretations with no author markers."""
    content = "Conflicto: Dolor generalizado. Nuevo modelo mental: Estrés."
    header = "DOLOR"
    interpretations = _get_interpretations(content, header)
    assert len(interpretations) == 1
    assert interpretations[0]["autor"] == "General/No especificado"
    assert "Dolor generalizado" in interpretations[0]["conflicto_emocional"]
    assert "Estrés" in interpretations[0]["modelo_mental"]


def test_get_interpretations_with_author():
    """Test _get_interpretations with author markers."""
    content = "Louise L. Hay: Conflicto: Identidad. Nuevo modelo mental: Aceptación."
    header = "ACNÉ"
    interpretations = _get_interpretations(content, header)
    assert len(interpretations) == 1
    assert interpretations[0]["autor"] == "Louise L. Hay"
    assert "Identidad" in interpretations[0]["conflicto_emocional"]
    assert "Aceptación" in interpretations[0]["modelo_mental"]


def test_apply_global_fallback_with_author():
    """Test _apply_global_fallback when author section exists but no interpretation."""
    mapped_item = {
        "interpretaciones": [
            {"autor": "Louise L. Hay", "conflicto_emocional": "", "modelo_mental": ""}
        ]
    }
    content = "Louise L. Hay: Solo texto sin marcadores."
    header = "ACNÉ"
    _apply_global_fallback(mapped_item, content, header)
    assert "Solo texto" in mapped_item["interpretaciones"][0]["conflicto_emocional"]


def test_apply_global_fallback_general():
    """Test _apply_global_fallback for General/No especificado author."""
    mapped_item = {
        "interpretaciones": [
            {"autor": "General/No especificado", "conflicto_emocional": "", "modelo_mental": ""}
        ]
    }
    content = "Conflicto: Dolor general. Sin autor específico."
    header = "DOLOR"
    _apply_global_fallback(mapped_item, content, header)
    assert "Dolor general" in mapped_item["interpretaciones"][0]["conflicto_emocional"]


def test_apply_global_fallback_multiple_authors():
    """Test _apply_global_fallback with multiple author interpretations."""
    mapped_item = {
        "interpretaciones": [
            {"autor": "Louise L. Hay", "conflicto_emocional": "", "modelo_mental": ""},
            {"autor": "General/No especificado", "conflicto_emocional": "", "modelo_mental": ""}
        ]
    }
    content = (
        "Louise L. Hay: Texto de Louise. "
        "Jacques Martel: Texto de Jacques. "
        "Contenido general."
    )
    header = "ACNÉ"
    _apply_global_fallback(mapped_item, content, header)
    assert "Texto de Louise" in mapped_item["interpretaciones"][0]["conflicto_emocional"]
    assert "Contenido general" in mapped_item["interpretaciones"][1]["conflicto_emocional"]


def test_normalize_symptom_various():
    """Test normalize_symptom with various inputs."""
    from src.parser.mapper import normalize_symptom
    assert normalize_symptom("LA GASTRITIS") == "GASTRITIS"
    assert normalize_symptom("EL DOLOR") == "DOLOR"
    assert normalize_symptom("LOS SÍNTOMAS") == "SÍNTOMAS"
    assert normalize_symptom("LAS ENFERMEDADES") == "ENFERMEDADES"
    assert normalize_symptom("ACNÉ") == "ACNÉ"
    assert normalize_symptom("  ACNÉ  ") == "ACNÉ"


def test_extract_field_edge_cases():
    """Test extract_field with various edge cases."""
    from src.parser.mapper import extract_field
    assert extract_field("", ["pattern"]) == ""
    assert extract_field("text", []) == ""
    assert extract_field("Conflicto: Valor", [r"Conflicto:\s+(.*)"]) == "Valor"
    assert extract_field("No match", [r"Pattern:\s+(.*)"]) == ""
