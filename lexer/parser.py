import sys
import copy

from ts import TS
from tag import Tag
from token import Token
from lexer import Lexer
from no import No

class Parser():

    def __init__(self, lexer):
      self.lexer = lexer
      self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo

    def sinalizaErroSemantico(self, message):
      print("[Erro Semantico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

    def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

    def advance(self):
    #   print("[DEBUG] token: ", self.token.toString())
      self.token = self.lexer.proxToken()

      if self.token is None: # erro no Lexer
        sys.exit(0)
   
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
        tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da segunda regra)
        if(self.eat(Tag.KW_CLASS)):
            self.ID()
            self.lexer.ts.removeToken(tempToken.getLexema())
            tempToken.setTipo(Tag.TIPO_VAZIO)
            self.lexer.ts.addToken(tempToken.getLexema(), tempToken)
            if(self.eat(Tag.SIMB_DOIS_PONTOS)):
                self.ListaFuncao()
                self.Main()
                if(self.eat(Tag.KW_END)):
                    if(not self.eat(Tag.SIMB_PONTO)):
                        self.sinalizaErroSintatico("Esperado \".\"; encontrado " + "\"" + self.token.getLexema() + "\"") 
                else:
                    self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\"" + self.token.getLexema() + "\"") 
            else:
                self.sinalizaErroSintatico("Esperado \":\"; encontrado " + "\"" + self.token.getLexema() + "\"")
    def DeclaraID(self):
        noTipoPrimitivo = self.TipoPrimitivo()
        self.TipoPrimitivo()
        tempToken = copy.copy(self.token)
        self.ID()
        tempToken.setTipo(noTipoPrimitivo.tipo)
        self.lexer.ts.addToken(tempToken.getLexema(), tempToken)
        if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
            self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def ListaFuncao(self):
        self.ListaFuncaoLinha()
    
    def ListaFuncaoLinha(self):
        self.Funcao()
        if self.token.getNome() == Tag.KW_DEF:
            self.ListaFuncaoLinha()


    def Funcao(self):
        if(self.eat(Tag.KW_DEF)):
            tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da segunda regra)
            noTipoPrimitivo = self.TipoPrimitivo()
            self.TipoPrimitivo()
            tempToken = copy.copy(self.token)
            self.ID()
            tempToken.setTipo(noTipoPrimitivo.tipo)
            self.lexer.ts.addToken(tempToken.getLexema(), tempToken)
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
                                                self.RegexDeclaraId()
                                                self.ListaCmd()
                                                if(self.eat(Tag.KW_END)):
                                                    if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                                                        self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"") 
                                                else:
                                                    self.sinalizaErroSintatico("Esperado \"end\"; encontrado " + "\"" +   self.token.getLexema() + "\"") 
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
        noTipoPrimitivo = No()
        if self.eat(Tag.KW_BOOL):
            noTipoPrimitivo.tipo = Tag.TIPO_LOGICO
            return noTipoPrimitivo
            pass
        elif self.eat(Tag.KW_INTEGER):
            noTipoPrimitivo.tipo = Tag.TIPO_INT
            return noTipoPrimitivo
            pass
        elif self.eat(Tag.KW_STRING): 
            noTipoPrimitivo.tipo = Tag.TIPO_STRING
            return noTipoPrimitivo
            pass
        elif self.eat(Tag.KW_DOUBLE): 
            noTipoPrimitivo.tipo = Tag.TIPO_DOUBLE
            return noTipoPrimitivo
            pass
        elif self.eat(Tag.KW_VOID):
            noTipoPrimitivo.tipo = Tag.TIPO_VAZIO
            return noTipoPrimitivo
            pass
        # else:
        #     self.sinalizaErroSintatico("Esperado \"Operator\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def ListaCmd(self):
        self.ListaCmdLinha()

    def ListaCmdLinha(self):
        self.Cmd()
        if self.token.getNome() == Tag.KW_WRITELN or self.token.getNome() == Tag.KW_IF or self.token.getNome() == Tag.KW_WHILE:
            self.ListaCmdLinha()

    def Cmd(self):
        if self.token.getNome() == Tag.KW_IF:
            self.CmdIF()
        elif self.eat(Tag.KW_WHILE):
            self.CmdWhile()
        elif self.token.getNome() == Tag.KW_WRITELN:
            self.CmdWrite()
        elif(self.eat(Tag.ID)):
            # self.token = self.lexer.proxToken()
            self.CmdAtribFunc()

    def CmdAtribFunc(self):
        if self.token.getNome() == Tag.SIMB_ABRE_PARENT:
            self.CmdFuncao()
        elif self.token.getNome() == Tag.OP_IGUAL:
            self.CmdAtribui()

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
        if(self.eat(Tag.SIMB_ABRE_PARENT)):
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

    def CmdWrite(self):
        if(self.eat(Tag.KW_WRITELN)):
            if(self.eat(Tag.SIMB_ABRE_PARENT)):
                self.Expressao()
                if(self.eat(Tag.SIMB_FECHA_PARENT)):
                    if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                        self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")
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
                    self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def CmdFuncao(self):
        if(self.eat(Tag.SIMB_ABRE_PARENT)):
            self.RegexExp()
            if(self.eat(Tag.SIMB_FECHA_PARENT)):
                if(not self.eat(Tag.SIMB_PONTO_VIRGULA)):
                        self.sinalizaErroSintatico("Esperado \";\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            else:
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            self.sinalizaErroSintatico("Esperado \"(\"; encontrado " + "\"" + self.token.getLexema() + "\"")

    def RegexExp(self):
        self.Expressao()
        self.RegexExpLinha()
        
    def RegexExpLinha(self):
        if(self.eat(Tag.SIMB_VIRGULA)):
            self.Expressao()
            self.RegexExpLinha()


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
        noExp4 = No()
        tempToken = copy.copy(self.token) # armazena token corrente (necessario para id da primeira regra)
        if(self.ID()):
            self.Exp4Linha()
            if tempToken.getTipo() == Tag.TIPO_VAZIO:
                self.sinalizaErroSemantico("Variavel " + "\"" + tempToken.getLexema() + "\"" + " nao definida.")
                noExp4.tipo = Tag.TIPO_ERRO
        elif self.token.getNome() == Tag.KW_INTEGER:
             self.advance()
             noExp4.tipo = Tag.TIPO_INTER
             pass
        elif self.token.getNome() == Tag.KW_DOUBLE:
            self.advance()
            noExp4.tipo = Tag.TIPO_DOUBLE
            pass
        elif self.token.getNome() == Tag.STRING: 
            self.advance()
            noExp4.tipo = Tag.TIPO_STRING
            pass
        elif self.token.getNome() == Tag.KW_TRUE: 
            self.advance()
            noExp4.tipo = Tag.TIPO_LOGICO
            pass
        elif self.token.getNome() == Tag.KW_FALSE: 
            self.advance()
            noExp4.tipo = Tag.TIPO_LOGICO
            pass
        elif self.token.getNome() == Tag.OP_UNARIO:
            self.advance()
            noExp4.tipo = Tag.TIPO_LOGICO
            pass
        elif(self.eat(Tag.SIMB_ABRE_PARENT)):
            self.Expressao()
            if(not self.eat(Tag.SIMB_FECHA_PARENT)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        # else:
        #     self.sinalizaErroSintatico("Esperado \"if\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        return noExp4


    def Exp4Linha(self):
        if(self.token.getNome() == Tag.SIMB_ABRE_PARENT):
            self.RegexExp()
            if(not self.eat(Tag.SIMB_FECHA_PARENT)):
                self.sinalizaErroSintatico("Esperado \")\"; encontrado " + "\"" + self.token.getLexema() + "\"")
        else:
            return

    def OpUnario(self):
        pass
