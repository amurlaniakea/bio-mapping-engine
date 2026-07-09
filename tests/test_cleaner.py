from src.parser.cleaner import CleanText


def test_cleaning_basic():
    cleaner = CleanText()
    result = cleaner.clean("  Texto con espacios  ")
    assert result == "Texto con espacios"


def test_cleaning_special_chars():
    cleaner = CleanText()
    result = cleaner.clean("¡Hola! ¿Cómo estás?")
    assert result == "¡Hola! ¿Cómo estás?"
