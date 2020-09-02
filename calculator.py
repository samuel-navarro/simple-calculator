# Expression:
#     SumExpression
# 
# SumExpression:
#     ProductExpression + SumExpression
#     ProductExpression - SumExpression
#     ProductExpression
# 
# ProductExpression:
#     ExponentExpression * ProductExpression
#     ExponentExpression / ProductExpression
#     ExponentExpression
#
# ExponentExpression:
#     ValueExpression ^ ExponentExpression
#     ValueExpression    
# 
# ValueExpression:
#     NumericValue
#     (Expression)
#
# NumericExpression: [+-]?[0-9]+\.?[0-9]*

from typing import Optional, Union, Tuple
import re

class ValueExpression:
    def __init__(self, value):
        self.value = value
    
    def eval(self):
        if isinstance(self.value, SumExpression):
            return self.value.eval()
        else:
            return self.value


class ExponentExpression:
    def __init__(self, lhs: ValueExpression, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def eval(self):
        if self.rhs is not None:
            return self.lhs.eval() ** self.rhs.eval()
        else:
            return self.lhs.eval()
 

class ProductExpression:
    def __init__(self, lhs: ExponentExpression, sign: Optional[str], rhs):
        self.lhs = lhs
        self.sign = sign
        self.rhs = rhs
    
    def eval(self):
        if self.sign is not None:
            if self.sign == '*':
                return self.lhs.eval() * self.rhs.eval()
            else:
                return self.lhs.eval() / self.rhs.eval()
        
        else:
            return self.lhs.eval()

class SumExpression:
    def __init__(self, lhs: ProductExpression, sign: Optional[str], rhs):
        self.lhs = lhs
        self.sign = sign
        self.rhs = rhs
    
    def eval(self):
        if self.sign is not None:
            if self.sign == '+':
                return self.lhs.eval() + self.rhs.eval()
            else:
                return self.lhs.eval() - self.rhs.eval()
        
        else:
            return self.lhs.eval()


class ParseError(Exception):
    pass


def parse_value_expression(user_str: str) -> Tuple[ValueExpression, str]:
    user_str = user_str.strip()
    if len(user_str) == 0:
        raise ParseError('Empty expression')

    if user_str[0] == '(':
        expr, unparsed_str = parse_expression(user_str[1:])
        unparsed_str = unparsed_str.lstrip()
        if (len(unparsed_str) == 0) or (unparsed_str[0] != ')'):
            raise ParseError('Unmatched parenthesis')
        else:
            return ValueExpression(expr), unparsed_str[1:]

    else:
        match = re.match('[+-]?[0-9]+\.?[0-9]*', user_str)
        if not match:
            raise ParseError(f'Expected a numeric value in "{user_str}"')
        else:
            match_str = match.group(0)
            value = float(match_str)
            
            return ValueExpression(value), user_str[len(match_str):]


def parse_exponent_expression(user_str: str) -> Tuple[ExponentExpression, str]:
    lhs, unparsed_str = parse_value_expression(user_str)
    
    unparsed_str = unparsed_str.lstrip()
    if len(unparsed_str) == 0:
        return ExponentExpression(lhs, None), ''

    sign = unparsed_str[0]
    if sign != '^':
        return ExponentExpression(lhs, None), unparsed_str
    
    rhs, rest = parse_exponent_expression(unparsed_str[1:])
    return ExponentExpression(lhs, rhs), rest


def parse_prod_expression(user_str: str) -> Tuple[ProductExpression, str]:
    lhs, unparsed_str = parse_exponent_expression(user_str)
    
    unparsed_str = unparsed_str.lstrip()
    if len(unparsed_str) == 0:
        return ProductExpression(lhs, None, None), ''

    sign = unparsed_str[0]
    if sign not in '*/':
        return ProductExpression(lhs, None, None), unparsed_str
    
    rhs, rest = parse_prod_expression(unparsed_str[1:])
    return ProductExpression(lhs, sign, rhs), rest


def parse_sum_expression(user_str: str) -> Tuple[SumExpression, str]:
    lhs, unparsed_str = parse_prod_expression(user_str)
    
    unparsed_str = unparsed_str.lstrip()
    if len(unparsed_str) == 0:
        return SumExpression(lhs, None, None), ''

    sign = unparsed_str[0]
    if sign not in '+-':
        return SumExpression(lhs, None, None), unparsed_str
    
    rhs, rest = parse_expression(unparsed_str[1:])
    return SumExpression(lhs, sign, rhs), rest


def parse_expression(user_str: str) -> Tuple[SumExpression, str]:
    return parse_sum_expression(user_str)


def _main():
    while True:
        user_str = input('Calculator>> ')
        try:
            expression, unparsed_str = parse_expression(user_str)
            if len(unparsed_str) > 0:
                print(f'Unrecognized input: {unparsed_str}')
            else:
                print(expression.eval())

        except ParseError as ex:
            print(f'Invalid input: {ex}')
        
        print()


if __name__ == "__main__":
    _main()
