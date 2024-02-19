import re


def camel_to_snake(camel_str: str) -> str:
    """
    Convert a CamelCase string to snake_case.

    The implementation of this function is taken directly from the accepted answer
    to a StackOverflow question. See the following URL for reference:

    https://shorturl.at/hABI1


    Args:
        camel_str: a string in CamelCase format.

    Returns:
        A string in snake_case format.
    """
    # Add underscore before uppercase followed by lowercase
    temp_str = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
    # Add underscore before lowercase or digit followed by uppercase
    snake_str = re.sub("([a-z0-9])([A-Z])", r"\1_\2", temp_str)

    return snake_str.lower()
