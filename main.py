#-*- coding: utf-8 -*-
# Alunos: Eduardo de Abreu Neves, Laure Hundzinski da Rocha, Vinicius Salles Zaia

import sys
from validator import validate_file

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo_de_entrada>")
        sys.exit(1)

    filename = sys.argv[1]
    resultados = validate_file(filename)

    for resultado in resultados:
        print(resultado)

if __name__ == "__main__":
    main()
