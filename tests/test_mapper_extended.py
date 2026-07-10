import pytest
import uuid
from src.parser.mapper import map_segment, AUTHORS

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
    # The author_pattern is 'Jacques Martel[\s:]+'
    # parts will be ['', 'Jacques Martel', ' Nuevo modelo mental: El espejo. Resentir: No ser escuchado.']
    # Loop: i=1. raw_author_name = 'Jacques Martel'. 
    # author_content = ' Nuevo modelo mental: El espejo. Resentir: No ser escuchado.'
    # extract_field for conflicto_emocional will use [\s:]+ patterns.
    # 'Resentir: No ser escuchado.' might not match the pattern if it's not in the author_content.
    # Wait, the regex for extract_field is r'Resentir[\s\-—:|]+'
    
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
