from enum import Enum

class Tag(Enum):
   # '''
   # Uma representacao em constante de todos os nomes 
   # de tokens para a linguagem.
   # '''

    # Fim de arquivo
    EOF = -1

    # Palavras-chave
    KW_IF = 1
    KW_ELSE = 2
    KW_THEN = 3
    KW_PRINT = 4

    # Operadores 
    OP_MENOR = 10
    OP_MENOR_IGUAL = 11
    OP_MAIOR_IGUAL = 12
    OP_MAIOR = 13
    OP_IGUAL = 14
    OP_DIFERENTE = 15
    OP_PRODUTO = 35
    OP_DIVISAO = 36
    OP_ADICAO = 37
    OP_SUBTRACAO = 38
    OP_AND = 39
    OP_OR = 40
    
    # Operador unario
    OP_UNARIO = 34

    # Identificador
    ID = 20

    # Numeros
    NUM = 30
    INTEGER = 31
    DOUBLE = 32
    

    # String
    STRING = 33


