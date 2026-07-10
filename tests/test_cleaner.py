from src.parser.cleaner import CleanText


def test_cleaning_basic():
    cleaner = CleanText()
    result = cleaner.clean("  Texto con espacios  ")
    assert result == "Texto con espacios"


def test_cleaning_special_chars():
    cleaner = CleanText()
    result = cleaner.clean("¡Hola! ¿Cómo estás?")
    assert result == "¡Hola! ¿Cómo estás?"


def test_cleaning_page_markers():
    cleaner = CleanText()
    text = "Contenido\n--- PAGE 26 ---\nMás contenido"
    result = cleaner.clean(text)
    assert "--- PAGE 26 ---" not in result
    assert "Contenido" in result
    assert "Más contenido" in result


def test_cleaning_standalone_page_numbers():
    cleaner = CleanText()
    text = "Texto\n  15  \nMás texto"
    result = cleaner.clean(text)
    assert result == "Texto\n\nMás texto"


def test_cleaning_multiple_spaces_tabs():
    cleaner = CleanText()
    text = "Texto   con\t\tmuchos   espacios"
    result = cleaner.clean(text)
    assert result == "Texto con muchos espacios"


def test_cleaning_multiple_newlines():
    cleaner = CleanText()
    text = "Línea 1\n\n\n\nLínea 2"
    result = cleaner.clean(text)
    assert result == "Línea 1\n\nLínea 2"


def test_cleaning_empty_string():
    cleaner = CleanText()
    result = cleaner.clean("")
    assert result == ""


def test_cleaning_none_input():
    cleaner = CleanText()
    result = cleaner.clean("")
    assert result == ""
