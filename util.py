def index_to_letter(index: int) -> str:
    """Convert a list index to an ASCII character a-z"""
    # Only accept from 0-25 (so the 26 letters of the alphabet)
    if index > 25:
        raise ValueError(f"Index must be between 0-25 (got {index})")
    return chr(97 + index)

def letter_to_index(letter: str) -> int:
    """Convert ASCII character a-z or A-Z to a list index"""
    if len(letter) != 1:
        raise ValueError("Letter must be a single character")
    asc = ord(letter)
    # Handle lowercase letters
    if 97 <= asc <= 122:
        return asc - 97
    # Handle uppercase letters
    if 65 <= asc <= 90:
        return asc - 65
    raise ValueError(f"Invalid answer {letter}")