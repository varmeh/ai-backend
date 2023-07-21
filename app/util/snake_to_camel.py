import re


# def snake_to_camel(snake: str) -> str:
#     """
#     Converts a snake_case string to camelCase.

#     The `start_lower` argument determines whether the first letter in the generated camelcase should
#     be lowercase (if `start_lower` is True), or capitalized (if `start_lower` is False).
#     """
#     camel = snake.title()
#     camel = re.sub("([0-9A-Za-z])_(?=[0-9A-Z])", lambda m: m.group(1), camel)
#     camel = re.sub("(^_*[A-Z])", lambda m: m.group(1).lower(), camel)
#     return camel


def to_camel_case(string: str) -> str:
    # Remove any leading/trailing whitespace
    string = string.strip()

    # If the string is already in PascalCase, insert a space between each word
    string = re.sub("([a-z])([A-Z])", r"\1 \2", string)

    # Split the string into words
    words = re.split("[ _-]", string)

    # The first word is made lowercase. Subsequent words are capitalized.
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


__all__ = ["to_camel_case"]
