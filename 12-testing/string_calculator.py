import re


def sum_numbers_in(expression: str) -> int:
    if expression is None or expression == "":
        return 0
    beginning_of_config = "//"
    contains_custom_separator = expression.startswith(beginning_of_config)
    if contains_custom_separator:
        end_of_config = "/"
        separator = get_separator(beginning_of_config, end_of_config, expression)
        expression = clean_expression(beginning_of_config, end_of_config, expression)
    else:
        separator = ","
    tokens = expression.split(separator)
    return sum_total(tokens)


def sum_total(tokens):
    total = 0
    for token in tokens:



def parse_int(token):
    if re.match("^[0-9]+$", token):
        return int(token)
    return 0
