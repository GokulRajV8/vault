_DIGITS = [
    "a", "b", "c", "d", "e", "f", "g", "h",
    "i", "j", "k", "l", "m", "n", "o", "p",
    "A", "B", "C", "D", "E", "F", "G", "H",
    "I", "J", "K", "L", "M", "N", "O", "P",
]

FIRST_VAL = "aaaaaaaaaaaaaaaaaaaa"


def get_next_value(value: str) -> str:
    if value == "":
        return "a"

    last_digit_index = _DIGITS.index(value[-1])

    if last_digit_index == 31:
        return get_next_value(value[:-1]) + _DIGITS[0]
    else:
        return value[:-1] + _DIGITS[last_digit_index + 1]
