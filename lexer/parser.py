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
        self.TipoPrimitivo()
        self.ID()
        if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
            self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def ListaFuncao(self):
        self.ListaFuncaoLinha()
    
    def ListaFuncaoLinha(self):
        self.Funcao()

    def Funcao(self):
        if(self.eat(Tag.KW_DEF)):
            self.TipoPrimitivo()
            self.ID()
            if(self.eat(Tag.SIMB_ABRE_PARENT)):
                self.ListaArg()
                if(self.eat(Tag.SIMB_FECHA_PARENT)):
                    if(self.eat(Tag.SIMB_DOIS_PONTOS)):
                        self.RegexDeclaraId()
                        self.ListaCmd()
                    else:
                        self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\"" + self.token.getLexema() + "\"")    
                else:
                    self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\"" + self.token.getLexema() + "\"")    
            else:
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\"" + self.token.getLexema() + "\"")


    def RegexDeclaraId(self):
        if(self.token.getNome() == Tag.KW_BOOL or self.token.getNome() == Tag.KW_INTEGER or self.token.getNome()== Tag.KW_STRING or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_VOID):
            self.DeclaraID()
            self.RegexDeclaraId()
        else:
            return

    def ListaArg(self):
        self.Arg()
        self.ListaArgLinha()

    def ListaArgLinha(self):
        if(self.eat(Tag.SIMB_VIRGULA)):
            self.ListaArg()

    def Arg(self):
        self.TipoPrimitivo()
        self.ID()

    def Retorno(self):
        pass

    def Main(self):
        pass

    def TipoPrimitivo(self):
        if(self.eat(Tag.KW_BOOL) or self.eat(Tag.KW_INTEGER) or self.eat(Tag.KW_STRING) or self.eat(Tag.KW_DOUBLE) or self.eat(Tag.KW_VOID)):
            pass
        else:
            self.sinalizaErroSintatico("Esperado \"Operator\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def ListaCmd(self):
        self.ListaCmdLinha()

    def ListaCmdLinha(self):
        self.Cmd()

    def Cmd(self):
        if self.token.getNome() == Tag.KW_IF:
            self.CmdIF()
        elif self.token.getNome() == Tag.KW_WHILE:
            self.CmdWhile()
        elif self.token.getNome() == Tag.ID:
            self.CmdAtribFun
        elif self.token.getNome() == Tag.KW_WRITELN:
            self.CmdWrite()
        else:
            self.sinalizaErroSintatico("Esperado \"CMD if, while, Id, or write\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def CmdAtribFun(self):
        pass

    def CmdIF(self):
        if(self.eat(Tag.KW_IF)):
            if(self.eat(Tag.SIMB_ABRE_PARENT)):
                self.Expressao()
        else:
            self.sinalizaErroSintatico("Esperado \"if\"; encontrado " + "\"" + self.token.getLexema() + "\"")

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
        self.Exp1()
        self.ExpLinha()

    def ExpLinha(self):
        if(self.eat(Tag.OP_OR) or self.eat(Tag.OP_AND)):
            self.Exp1()
            self.ExpLinha()
        else:
            return

    def Exp1(self):
        self.Exp2()
        self.Exp1Linha()
        

    def Exp1Linha(self):
        if(self.eat(Tag.OP_MENOR) or self.eat(Tag.OP_MENOR_IGUAL) or self.eat(Tag.OP_MAIOR) or self.eat(Tag.OP_MAIOR_IGUAL) or self.eat(Tag.OP_IGUAL) or self.eat(Tag.OP_DIFERENTE)):
            self.Exp2()
            self.ExpLinha()
        else:
            return

    def Exp2(self):
        self.Exp3()
        self.Exp2Linha

    def Exp2Linha(self):
        if(self.eat(Tag.OP_ADICAO) or self.eat(Tag.OP_SUBTRACAO)):
            self.Exp3()
        else:
            return

    def Exp3(self):
        self.Exp4()
        self.Exp3Linha()

    def Exp3Linha(self):
        print('parei aqui. Seguindo fazendo Exp3Linha, lembrando que estou fazendo o CMDIf, e depois seguir em diante.')

    def Exp4(self):
        pass

    def Exp4Linha(self):
        pass

    def OpUnario(self):
        pass
