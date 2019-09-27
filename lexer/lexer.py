import sys

from ts import TS
from tag import Tag
from token import Token

class Lexer():
   def __init__(self, input_file):
      try:
         self.input_file = open(input_file, 'rb')
         self.lookahead = 0
         self.n_line = 1
         self.n_column = 0
         self.ts = TS()
      except IOError:
         print('Erro de abertura do arquivo. Encerrando.')
         sys.exit(0)

   def closeFile(self):
      try:
         self.input_file.close()
      except IOError:
         print('Erro dao fechar arquivo. Encerrando.')
         sys.exit(0)

   def sinalizaErroLexico(self, message):
      print("[Erro Lexico]: ", message, "\n")

   def retornaPonteiro(self):
      if(self.lookahead.decode('ascii') != ''):
         self.input_file.seek(self.input_file.tell()-1)

   def printTS(self):
      self.ts.printTS()

   def proxToken(self):
      estado = 1
      lexema = ""
      c = '\u0000'

      while(True):
         self.lookahead = self.input_file.read(1)
         c = self.lookahead.decode('ascii')

         if(estado == 1):
            if(c == ''):
               return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
            elif(c == ' ' or c == '\t' or c == '\r'):
               estado = 1
            elif(c == '\n'):
               estado = 1
               self.n_line += 1
               self.n_column = 0
            elif(c.isalpha()):
               lexema += c
               estado = 2
            elif(c.isdigit()):
               lexema += c
               estado = 5
            elif(c == '"'):
               lexema += c
               estado = 11
            elif(c == '-'):
               estado = 15
            elif (c == '!'):
               estado = 16
            elif (c == "<"):
               estado = 17
            elif (c == ">"):
               estado = 20
            elif (c == "="):
               estado = 23
            elif (c == "/"):
               estado = 27
            elif (c == "*"):
               estado = 28
            elif (c == "+"):
               estado = 29
            else:
               self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " +
               str(self.n_line) + " e coluna " + str(self.n_column))
               estado = 1
         elif(estado == 2):
            if(c.isalnum()):
               lexema += c           
            else:
               self.retornaPonteiro()
               token = self.ts.getToken(lexema)
               if(token is None):
                  token = Token(Tag.ID, lexema, self.n_line, self.n_column)
                  self.ts.addToken(lexema, token)
               return token
         elif(estado == 5):
            if(c.isdigit()  or c == '.'):
               lexema += c           
            else:
               self.retornaPonteiro()
               if('.' in lexema):
                  return Token(Tag.DOUBLE, lexema, self.n_line, self.n_column)
               else: 
                  return Token(Tag.INTEGER, lexema, self.n_line, self.n_column)
         elif(estado == 11):
            if (c.isalnum() or c == '"' or c == " "):
               lexema += c         
            else:
               self.retornaPonteiro()
               token = self.ts.getToken(lexema)
               if(token is None):
                  token = Token(Tag.STRING, lexema, self.n_line, self.n_column)
               return token
         elif (estado == 15):
            # if(c == '='):
            #    return Token(Tag.OP_MAIOR_IGUAL, "!=", self.n_line, self.n_column)
            # else:
            #    self.retornaPonteiro()
            #    return Token(Tag.OP_MAIOR, "!", self.n_line, self.n_column)
            return Token(Tag.OP_MAIOR_IGUAL, "-", self.n_line, self.n_column)
         elif (estado == 16):
            if(c == '='):
               return Token(Tag.OP_DIFERENTE, "!=", self.n_line, self.n_column)
            else:
               self.retornaPonteiro()
               return Token(Tag.OP_UNARIO, "!", self.n_line, self.n_column)
         elif(estado == 17):
            if(c == '='):
               return Token(Tag.OP_MENOR_IGUAL, "<=", self.n_line, self.n_column)
            else:
               self.retornaPonteiro()
               return Token(Tag.OP_MENOR, "<", self.n_line, self.n_column)
         elif(estado == 20):
            if(c == '='):
               return Token(Tag.OP_MAIOR_IGUAL, ">=", self.n_line, self.n_column)
            else:
               self.retornaPonteiro()
               return Token(Tag.OP_MAIOR, ">", self.n_line, self.n_column)
         elif(estado == 23):
            if(c == '='):
               return Token(Tag.OP_IGUAL, "==", self.n_line, self.n_column)
            else:
               self.retornaPonteiro()
               return Token(Tag.OP_IGUAL, "=", self.n_line, self.n_column)
         elif(estado == 27):
            return Token(Tag.OP_DIVISAO, "/", self.n_line, self.n_column)
         elif(estado == 28):
            return Token(Tag.OP_PRODUTO, "*", self.n_line, self.n_column)
         elif(estado == 29):
            return Token(Tag.OP_ADICAO, "+", self.n_line, self.n_column)