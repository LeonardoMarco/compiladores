import sys

from ts import TS
from tag import Tag
from token import Token
from lexer import Lexer

class Parser():

    def __init__(self, lexer):
      self.lexer = lexer
      self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo

    def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

    def advance(self):
      print("[DEBUG] token: ", self.token.toString())
      self.token = self.lexer.proxToken()
   
    def skip(self, message):
      self.sinalizaErroSintatico(message)
      self.advance()

   # verifica token esperado t 
    def eat(self, t):
      if(self.token.getNome() == t):
         self.advance()
         return True
      else:
         return False
   # Programa -> CMD EOF
    def Programa(self):
      self.Classe()
      if(self.token.getNome() != Tag.EOF):
         self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def ID(self):
        if not self.eat(Tag.ID):
            self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def Classe(self):
        if(self.eat(Tag.KW_CLASS)):
            self.ID()
            if(self.eat(Tag.SIMB_DOIS_PONTOS)):
                self.ListaFuncao()
            else:
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\"" + self.token.getLexema() + "\"")
    def DeclaraID(self):
        pass

    def ListaFuncao(self):
        self.ListaFuncaoLinha()
    
    def ListaFuncaoLinha(self):
        self.Funcao()

    def Funcao(self):
        if(self.eat(Tag.KW_DEF)):
            self.ID()
            if(self.eat(Tag.SIMB_ABRE_PARENT)):
                self.ListaArg()

    def regexDeclaraId(self):
        pass

    def ListaArg(self):
        print('parei aqui')

    def ListaArgLinha(self):
        pass

    def Arg(self):
        pass

    def Retorno(self):
        pass

    def Main(self):
        pass

    def TipoPrimitivo(self):
        pass

    def ListaCmd(self):
        pass

    def ListaCmdLinha(self):
        pass

    def Cmd(self):
        pass

    def CmdAtribFun(self):
        pass

    def CmdIF(self):
        pass

    def CmdIFLinha(self):
        pass

    def CmdWhile(self):
        pass

    def CmdWrite(self):
        pass

    def CmdAtribui(self):
        pass

    def CmdFuncao(self):
        pass

    def RegexExp(self):
        pass

    def RegexExpLinha(self):
        pass

    def Expressao(self):
        pass

    def ExpLinha(self):
        pass

    def Exp1(self):
        pass

    def Exp1Linha(self):
        pass

    def Exp2(self):
        pass

    def Exp2Linha(self):
        pass

    def Exp3(self):
        pass

    def Exp3Linha(self):
        pass

    def Exp4(self):
        pass

    def Exp4Linha(self):
        pass

    def OpUnario(self):
        pass
