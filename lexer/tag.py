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
    KW_CLASS = 41
    KW_MAIN = 42
    KW_DEF = 43
    KW_ARG = 44
    KW_END = 45
    KW_VOID = 45
    KW_MAINM = 47
    KW_DEFSTATIC = 48
    KW_BOOL = 49
    KW_INTEGER = 50
    KW_STRING = 51
    KW_DOUBLE = 52
    KW_WHILE = 53
    KW_WRITELN = 54
    KW_RETURN = 63
    KW_TRUE = 64
    KW_FALSE = 65

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

    # Simbolos
    SIMB_VIRGULA = 55
    SIMB_PONTO_VIRGULA = 56
    SIMB_DOIS_PONTOS = 57
    SIMB_PONTO = 58
    SIMB_ABRE_PARENT = 59
    SIMB_FECHA_PARENT = 60
    SIMB_ABRE_CHAVE = 61
    SIMB_FECHA_CHAVE = 62

    SMB_AB_CHA = 70
    SMB_FE_CHA = 71
    OP_SOMA = 72
    OP_SUB = 73
