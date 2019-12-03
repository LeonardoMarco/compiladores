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
            # self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            return False
        else:
            return True

    def Classe(self):
        if(self.eat(Tag.KW_CLASS)):
            self.ID()
            if(self.eat(Tag.SIMB_DOIS_PONTOS)):
                self.ListaFuncao()
                self.Main()
                if(self.eat(Tag.KW_END)):
                    if(not self.eat(Tag.SIMB_PONTO)):
                        self.sinalizaErroSintatico("Esperado \".\"; encontrado " + "\"" + self.token.getLexema() + "\"")        
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
                        self.Retorno()
                        if(self.eat(Tag.KW_END)):
                            if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"") 
                        else:
                            self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\"" + self.token.getLexema() + "\"")           
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
        if(self.eat(Tag.KW_RETURN)):
            self.Expressao()
            if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")   
        else:
            return


    def Main(self):
        if(self.eat(Tag.KW_DEFSTATIC)):
            if(self.eat(Tag.KW_VOID)):
                if(self.eat(Tag.KW_MAINM)):
                    if(self.eat(Tag.SIMB_ABRE_PARENT)):
                        if(self.token.getLexema() == "String" and self.eat(Tag.KW_STRING)):
                            if(self.eat(Tag.SIMB_ABRE_CHAVE)):
                                if(self.eat(Tag.SIMB_FECHA_CHAVE)):
                                    if(self.ID()):
                                        if(self.eat(Tag.SIMB_FECHA_PARENT)):
                                            if(self.eat(Tag.SIMB_DOIS_PONTOS)):
                                                print('parei p resolver isso daqui')
                                                self.RegexDeclaraId()
                                                self.ListaCmd()
                                            else:
                                                self.sinalizaErroSintatico('Esperado \"")"\"; encontrado ' + '\"' + self.token.getLexema() + '\"')
                                        else:
                                            self.sinalizaErroSintatico('Esperado \"")"\"; encontrado ' + '\"' + self.token.getLexema() + '\"')    
                                    else:
                                        self.sinalizaErroSintatico('Esperado \""ID"\"; encontrado ' + '\"' + self.token.getLexema() + '\"')
                                else:
                                    self.sinalizaErroSintatico('Esperado \""]"\"; encontrado ' + '\"' + self.token.getLexema() + '\"')
                            else:
                                self.sinalizaErroSintatico('Esperado \""["\"; encontrado ' + '\"' + self.token.getLexema() + '\"')
                        else:
                            self.sinalizaErroSintatico('Esperado \""String"\"; encontrado ' + '\"' + self.token.getLexema() + '\"')
                    else:
                        self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                else:
                    self.sinalizaErroSintatico("Esperado \"main\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            else:
                self.sinalizaErroSintatico("Esperado \"void\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"defstatic\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def TipoPrimitivo(self):
        if(self.eat(Tag.KW_BOOL) or self.eat(Tag.KW_INTEGER) or self.eat(Tag.KW_STRING) or self.eat(Tag.KW_DOUBLE) or self.eat(Tag.KW_VOID)):
            pass
        else:
            self.sinalizaErroSintatico("Esperado \"Operator\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def ListaCmd(self):
        self.ListaCmdLinha()

    def ListaCmdLinha(self):
        if(self.token.getLexema() != "" or self.token.getLexema() != " "):
            self.Cmd()
            self.eat(Tag.KW_RETURN)
            # self.ListaCmdLinha()
            

    def Cmd(self):
        if self.eat(Tag.KW_IF):
            self.CmdIF()
        elif self.eat(Tag.KW_WHILE):
            self.CmdWhile()
        elif self.eat(Tag.KW_WRITELN):
            self.CmdWrite()
        else:
            self.token = self.lexer.proxToken()
            self.CmdAtribFun()

    def CmdAtribFun(self):
        if self.token.getNome() == Tag.SIMB_ABRE_PARENT:
            self.CmdFuncao()

    def CmdIF(self):
        if(self.eat(Tag.KW_IF)):
            if(self.eat(Tag.SIMB_ABRE_PARENT)):
                self.Expressao()
                if(self.eat(Tag.SIMB_FECHA_PARENT)):
                    if(self.eat(Tag.SIMB_DOIS_PONTOS)):
                        self.ListaCmd()
                        self.CmdIFLinha()
                else:
                    self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\"" + self.token.getLexema() + "\"")        

        else:
            self.sinalizaErroSintatico("Esperado \"if\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def CmdIFLinha(self):
        if(self.eat(Tag.KW_END)):
            if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        elif(self.eat(Tag.KW_ELSE)):
            if(self.eat(Tag.SIMB_DOIS_PONTOS)):
                self.ListaCmd()
                if(self.eat(Tag.KW_END)):
                    if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                        self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                else: 
                    self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            else:
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"end, else\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                

    def CmdWhile(self):
        if(self.eat(Tag.KW_WHILE)):
            if(self.eat(Tag.SIMB_ABRE_CHAVE)):
                self.Expressao()
                if(self.eat(Tag.SIMB_FECHA_PARENT)):
                    if(self.eat(Tag.SIMB_DOIS_PONTOS)):
                        self.ListaCmd()
                        if(self.eat(Tag.KW_END)):
                            if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                                self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                        else:
                            self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                    else:
                        self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                else:
                    self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            else: 
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"while\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def CmdWrite(self):
        if(self.eat(Tag.KW_WRITELN)):
            if(self.eat(Tag.SIMB_ABRE_CHAVE)):
                self.Expressao()
                if(self.eat(Tag.SIMB_FECHA_PARENT)):
                    if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                        self.sinalizaErroSintatico("Esperado \"while\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                else:
                    self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            else:
                self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"write\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def CmdAtribui(self):
        if(self.eat(Tag.OP_IGUAL)):
            self.Expressao()
            if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                    self.sinalizaErroSintatico("Esperado \"while\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def CmdFuncao(self):
        if(self.eat(Tag.SIMB_ABRE_PARENT)):
            self.RegexExp()
            if(self.eat(Tag.SIMB_FECHA_PARENT)):
                if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                        self.sinalizaErroSintatico("Esperado \"while\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            else:
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def RegexExp(self):
        if(self.token.getLexema() != "" or self.token.getLexema() != " "):
            self.Expressao()
            self.RegexExpLinha()
        else:
            return

    def RegexExpLinha(self):
        if(self.token.getLexema() != "" or self.token.getLexema() != " "):
            if(self.eat(Tag.SIMB_VIRGULA)):
                self.Expressao()
                self.RegexExpLinha()
        else:
            return

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
        self.Exp2Linha()

    def Exp2Linha(self):
        if(self.eat(Tag.OP_ADICAO) or self.eat(Tag.OP_SUBTRACAO)):
            self.Exp3()
        else:
            return

    def Exp3(self):
        self.Exp4()
        self.Exp3Linha()

    def Exp3Linha(self):
        if(self.eat(Tag.OP_PRODUTO) or self.eat(Tag.OP_DIVISAO)):
            self.Exp4()
            self.Exp3Linha()
        else:
            return

    def Exp4(self):
        if(self.ID()):
            self.Exp4Linha()
        elif(self.token.getNome() == Tag.KW_INTEGER or self.token.getNome() == Tag.KW_DOUBLE or self.token.getNome() == Tag.KW_STRING or self.token.getNome() == Tag.KW_TRUE or self.token.getNome() == Tag.KW_FALSE or self.token.getNome() == Tag.OP_UNARIO):
            self.token = self.lexer.proxToken()
            return
        elif(self.token.getNome() == Tag.SIMB_ABRE_PARENT):
            self.Expressao()
            if(not self.eat(Tag.SIMB_FECHA_PARENT)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"if\"; encontrado " + "\"" + self.token.getLexema() + "\"")


    def Exp4Linha(self):
        if(self.token.getNome() == Tag.SIMB_ABRE_PARENT):
            self.RegexExp()
            if(not self.eat(Tag.SIMB_FECHA_PARENT)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            return

    def OpUnario(self):
        pass
