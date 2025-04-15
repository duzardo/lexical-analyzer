#-*- coding: utf-8 -*-
# Alunos: Eduardo de Abreu Neves, Laura Hundzinski da Rocha, Vinicius Salles Zaia

import re
from typing import List

TOKEN_REGEX = [
    ("ABREPAREN", re.compile(r"\(")),
    ("FECHAPAREN", re.compile(r"\)")),
    ("OPERATORUNARIO", re.compile(r"\\neg")),
    ("OPERATORBINARIO", re.compile(r"\\wedge|\\vee|\\rightarrow|\\leftrightarrow")),
    ("CONSTANTE", re.compile(r"(true|false)")),
    ("PROPOSICAO", re.compile(r"[0-9][0-9a-z]*")),
    ("WHITESPACE", re.compile(r"\s+")),
]

def tokenize(expression: str):
    position = 0
    tokens = []
    while position < len(expression):
        match = None
        for token_type, pattern in TOKEN_REGEX:
            match = pattern.match(expression, position)
            if match:
                if token_type != "WHITESPACE": # <- ignora espaços
                    tokens.append((token_type, match.group(0)))
                position = match.end()
                break
        if not match:
            return None 
    return tokens

class Parser:
    def __init__(self, tokens: List[tuple]):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position][0]
        return None

    def consume(self, expected_type):
        if self.current_token() == expected_type:
            self.position += 1
        else:
            raise Exception("Token inesperado")

    def parse(self):
        try:
            self.formula()
            return self.position == len(self.tokens)
        except:
            return False

    def formula(self):
        token = self.current_token()
        if token in ("CONSTANTE", "PROPOSICAO"):
            self.consume(token)
        elif token == "ABREPAREN":
            self.consume("ABREPAREN")
            next_token = self.current_token()
            if next_token == "OPERATORUNARIO":
                self.consume("OPERATORUNARIO")
                self.formula()
                self.consume("FECHAPAREN")
            elif next_token == "OPERATORBINARIO":
                self.consume("OPERATORBINARIO")
                self.formula()
                self.formula()
                self.consume("FECHAPAREN")
            else:
                raise Exception("Expressão inválida")
        else:
            raise Exception("Expressão inválida ")
        
def validate_file(filename):
    results = []
    with open(filename, "r") as f:
        lines = f.read().strip().splitlines()
        num_expressions = int(lines[0])
        expressions = lines[1:num_expressions + 1]

        for expr in expressions:
            tokens = tokenize(expr)
            if tokens is None:
                results.append("invalida")
            else:
                parser = Parser(tokens)
                valid = parser.parse()
                results.append("valida" if valid else "invalida")
    return results
