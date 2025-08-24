# Classes para a geracao de tokens
class Tipo_de_Token():
    # Números
    NUMERO_REAL = "NUMERO_REAL"

    # Operadores
    SOMA = "SOMA"
    SUBTRACAO = "SUBTRACAO"
    MULTIPLICACAO = "MULT"  
    DIVISAO = "DIV"
    RESTO = "RESTO"
    POTENCIA = "POT"

    # Símbolos de Agrupamento
    ABRE_PARENTESES = "ABRE_PARENTESES"
    FECHA_PARENTESES = "FECHA_PARENTESES"

    # Comandos Especiais
    RES = "RES"
    MEM = "MEM"

    # Marcador de fim de arquivo
    FIM = "FIM"

class Token:
    def __init__(self, tipo: str, valor):
        self.tipo = tipo
        self.valor = valor

    # Retorno dos atributos do token
    def tipo(self):
        return self.tipo
    
    def valor(self):
        return self.valor
    
    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"

# Classe do Analisador Léxico
class Analisador_Lexico:
    def __init__(self, texto_fonte: str):
        self.texto_fonte = texto_fonte
        self.ponteiro = 0
        self.caractere = self.texto_fonte[self.ponteiro] if self.texto_fonte else None
        self.resultado = ""

    def avanca_ponteiro(self):
        self.ponteiro += 1
        if self.ponteiro < len(self.texto_fonte):
            self.caractere = self.texto_fonte[self.ponteiro]
        else:
            self.caractere = None

    def ignora_espaco(self):
        while self.caractere is not None and self.caractere.isspace():
            self.avanca_ponteiro()

    def analise(self):
        tokens = []
        while self.caractere is not None:
            token = self.estado_zero()
            if token: # Veriifica se esta vazio
                tokens.append(token)

        tokens.append(Token(Tipo_de_Token.FIM, None)) # Adiciona o marcador de fim
        return tokens
        
    # Estados da nossa Maquina de Estados Finitos (FSM)

    def estado_zero(self):

        self.ignora_espaco()

        #Verifica se chegou ao fim do arquivo
        if self.caractere is None:
            return None
        
        # Verifica se é um comando especial (alfabetico)
        if self.caractere.isalpha():
            return self.estado_comando()
        
        # Verifica se é um número
        if self.caractere.isdigit():
            return self.estado_numero()
        
        # Verifica qual é o caractere especial 
        token = None
        if self.caractere == '(':
            token = Token(Tipo_de_Token.ABRE_PARENTESES, '(')
        elif self.caractere == ')':
            token = Token(Tipo_de_Token.FECHA_PARENTESES, ')')
        elif self.caractere == '+':
            token = Token(Tipo_de_Token.SOMA, '+')
        elif self.caractere == '-':
            token = Token(Tipo_de_Token.SUBTRACAO, '-')
        elif self.caractere == '*':
            token = Token(Tipo_de_Token.MULTIPLICACAO, '*')
        elif self.caractere == '/':
            token = Token(Tipo_de_Token.DIVISAO, '/')
        elif self.caractere == '%':
            token = Token(Tipo_de_Token.RESTO, '%')
        elif self.caractere == '^':
            token = Token(Tipo_de_Token.POTENCIA, '^')

        # Ao final retorna o token criado e avança o ponteiro
        if token:
            self.avanca_ponteiro()
            return token
        
        # Caractere inválido
        raise ValueError(f"Caractere inválido: '{self.caractere}'")
    
    def estado_numero(self):
        resultado = ""

        # Lê a parte inteira do número
        while self.caractere is not None and self.caractere.isdigit():
            resultado += self.caractere
            self.avanca_ponteiro()

        # Inicia a leiturta da parte decimal
        if self.caractere == '.':
            resultado += self.caractere
            self.avanca_ponteiro()

            if not (self.caractere and self.caractere.isdigit()):
                raise ValueError("ERRO: espera-se dígito após o ponto decimal.")
            
            # Percorre todos os dígitos da parte decimal
            while self.caractere is not None and self.caractere.isdigit():
                resultado += self.caractere
                self.avanca_ponteiro()
        return Token(Tipo_de_Token.NUMERO_REAL, float(resultado)) # Crai token de número real
    
    def estado_comando(self):
        resultado = ""

        # Verifica se é um comando especial (alfabetico)
        while self.caractere is not None and self.caractere.isalpha():  
            resultado += self.caractere
            self.avanca_ponteiro()

        # Checa qual dos dois comandos (MEM ou RES) foi inserido
        if self.resultado == "MEM":
            return Token(Tipo_de_Token.MEM, resultado) 
        else:
            return Token(Tipo_de_Token.RES, resultado)
        
def parseExpressao(linha: str):
    analisador_lexico = Analisador_Lexico(linha)
    return analisador_lexico.analise()

# Testes unitários da funcao parseExpressao()
# Adicionar etapa ler para ler arquivos!
"""
if __name__ == "__main__":
    expressoes_teste = [
        "(3.0 2.0 +)",
        "(10.0 4.0 -)",
        "((1.0 2.0 +) (3.0 4.0 *) /)",
        "(5.0 MEM)",
        "(MEM)",
        "(1 RES)",
        "(2 3 ^)" # Teste com inteiro
    ]

    for expr in expressoes_teste:
        try:
            tokens_gerados = parseExpressao(expr)
            print(f"Expressão: '{expr}'")
            print(f"Tokens: {tokens_gerados}\n")
        except ValueError as e:
            print(f"Erro ao analisar '{expr}': {e}\n")

    # Teste de erro
    expressao_invalida = "(3.14.5 & 2.0)"
    try:
        parseExpressao(expressao_invalida)
    except ValueError as e:
        print(f"Teste de erro (esperado):")
        print(f"Expressão: '{expressao_invalida}'")
        print(f"Erro: {e}\n")
"""

# Obtendo o vetor de tokens, podemos partir para a etapa de calculo