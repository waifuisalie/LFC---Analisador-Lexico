#!/usr/bin/env python3
import sys
import math

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
    
    def __repr__(self):
        return f"Token({self._tipo}, {self._valor})"

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
        
        return self.estado_operador()

    def estado_operador(self):

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
        if resultado == "MEM":
            return Token(Tipo_de_Token.MEM, resultado) 
        else:
            return Token(Tipo_de_Token.RES, resultado)
        
def parseExpressao(linha: str):
    analisador_lexico = Analisador_Lexico(linha)
    tokens = analisador_lexico.analise()
    # Vamos remover os tokens de parênteses, pois não são necessários na RPN
    # Mas manteremos para validação futura, se necessário
    tokens = [t for t in tokens if t.tipo not in 
              (Tipo_de_Token.ABRE_PARENTESES, Tipo_de_Token.FECHA_PARENTESES)]
    return tokens

def arredondar_16bit(valor):
    """Simula a precisão de ponto flutuante de 16 bits (duas casas decimais)."""
    return round(float(valor), 2)

def executarExpressao(tokens: list[Token], memoria: dict, historico_resultados: list) -> float:
    """Executa uma expressão em notação polonesa reversa (RPN)."""
    pilha = []

    for token in tokens:
        # Garante que token.valor é sempre string para comparação
        token_val = token.valor
        token_upper = token_val.upper()

        # Verifica se o token é um operador.
        if token_upper in ['+', '-', '*', '/', '%', '^']:
            if len(pilha) < 2:
                print(f"-> Erro: tokens insuficientes para o operador '{token}'")
                continue
            
            # Desempilha os dois últimos operandos. A ordem é crucial.
            v2_str, v1_str = pilha.pop(), pilha.pop()
            resultado = 0.0
            
            try:
                # Lógica para tratar a divisão inteira vs. real.
                if token_upper == '/':
                    v1, v2 = float(v1_str), float(v2_str)
                    if v2 == 0: raise ZeroDivisionError("Divisão por zero.")
                    if '.' in v1_str or '.' in v2_str:
                        resultado = v1 / v2
                    else:
                        resultado = float(int(v1) // int(v2))
                # Lógica para as demais operações.
                else:
                    v1, v2 = float(v1_str), float(v2_str)
                    if token_upper == '+': resultado = v1 + v2
                    elif token_upper == '-': resultado = v1 - v2
                    elif token_upper == '*': resultado = v1 * v2
                    elif token_upper == '%': resultado = int(v1) % int(v2)
                    elif token_upper == '^': resultado = math.pow(v1, v2)
                
                pilha.append(str(arredondar_16bit(resultado)))
            except (ZeroDivisionError, ValueError) as e:
                print(f"-> Erro de operação para '{token}': {e}")
                pilha.append('0.0')

        # Lógica para o comando RES.
        elif token_upper == 'RES':
            if len(pilha) == 0:
                print("-> Erro: RES requer um índice numérico na pilha.")
                pilha.append('0.0')
                continue
            
            n_str = pilha.pop()
            
            try:
                n = int(float(n_str))
                tamanho_historico = len(historico_resultados)
                if 0 < n <= tamanho_historico:
                    pilha.append(str(historico_resultados[tamanho_historico - n]))
                else:
                    print(f"-> Erro: Índice N={n} inválido para RES.")
                    pilha.append('0.0')
            except ValueError:
                print(f"-> Erro: O valor '{n_str}' não é um índice numérico válido para RES.")
                pilha.append('0.0')

        # Lógica para o comando MEM.
        elif token_upper == 'MEM':
            # Trata a sintaxe (V MEM) e (MEM).
            if len(pilha) > 0 and pilha[-1].replace('.', '', 1).isdigit():
                # Caso (V MEM): atribui o valor da pilha à memória.
                valor_para_armazenar_str = pilha.pop()
                valor_float = float(valor_para_armazenar_str)
                memoria['MEM'] = valor_float
                pilha.append(str(arredondar_16bit(valor_float)))
            elif 'MEM' in memoria:
                # Caso (MEM): recupera o valor da memória.
                valor = memoria.get('MEM', 0.0)
                pilha.append(str(arredondar_16bit(valor)))
            else:
                print("-> Erro: Formato inválido para MEM ou memória não inicializada.")
                pilha.append('0.0')

        # Processamento de dados (números e nomes de variáveis).
        else:
            try:
                # Tenta converter o token para um número e empilha.
                float(token)
                pilha.append(token)
            except ValueError:
                # Se não é um número, é uma variável.
                if token_upper in memoria:
                    # Se a variável existe na memória, empilha o valor.
                    valor = memoria.get(token_upper, 0.0)
                    pilha.append(str(arredondar_16bit(valor)))
                else:
                    # Se não existe, empilha o nome para uso futuro (ex: com MEM).
                    pilha.append(token)

    # Retorna o resultado final. A pilha deve conter apenas um item.
    if len(pilha) == 1:
        return arredondar_16bit(pilha[0])
    else:
        print(f"-> Erro: A expressão finalizou com {len(pilha)} itens na pilha: {pilha}.")
        return arredondar_16bit(pilha[-1]) if pilha else 0.0

if __name__ == "__main__":
    memoria = {}
    historico = []

    testes = [
        "3 2 +",                 # 3 + 2 = 5
        "10 5 /",                # 10 / 5 = 2
        "3 2 + 10 5 / *",        # (3+2) * (10/5) = 10
        "12 4 / 3 5 * +",        # 12/4 + (3*5) = 18
        "9 2 %",                 # 9 % 2 = 1
        "2 3 ^",                 # 2^3 = 8

        # Testes com parênteses (só decorativos, vão ser ignorados)
        "( 3 2 + )",             
        "(( 3 2 + ) ( 10 5 / ) *)",  
        "((12 4 /) (3 5 *) +)",  
    ]

    for expr in testes:
        print(f"\nExpressão: {expr}")
        tokens = parseExpressao(expr)
        valores = [t.valor for t in tokens if t.tipo != Tipo_de_Token.FIM]
        resultado = executarExpressao(valores, memoria, historico)
        historico.append(resultado)
        print(f"Resultado = {resultado}")

