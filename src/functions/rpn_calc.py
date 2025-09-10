# rpn_calc.py

import math
from .tokens import Token, Tipo_de_Token
from .analisador_lexico import Analisador_Lexico

def parseExpressao(linha_operacao: str):
    analisador_lexico = Analisador_Lexico(linha_operacao)
    tokens = analisador_lexico.analise()
    # Mantém tokens com parênteses
    return tokens

def arredondar_16bit(valor):
    """Simula a precisão de ponto flutuante de 16 bits (duas casas decimais)."""
    return round(float(valor), 2)

def executarExpressao(tokens: list[Token], memoria: dict, historico_resultados: list) -> float:
    pilha = []
    for token in tokens:
        if token.tipo == Tipo_de_Token.FIM:
            continue
        valor_token = str(token.valor).upper()

        if token.tipo == Tipo_de_Token.ABRE_PARENTESES or token.tipo == Tipo_de_Token.FECHA_PARENTESES:
            continue

        if valor_token in ['+', '-', '*', '/', '%', '^']:
            if len(pilha) < 2:
                print(f"-> Erro: tokens insuficientes para o operador '{valor_token}'")
                continue
            v2_str, v1_str = pilha.pop(), pilha.pop()
            resultado = 0.0
            try:
                v1, v2 = float(v1_str), float(v2_str)
                if valor_token == '+': resultado = v1 + v2
                elif valor_token == '-': resultado = v1 - v2
                elif valor_token == '*': resultado = v1 * v2
                elif valor_token == '/':
                    if v2 == 0: raise ZeroDivisionError("Divisão por zero.")
                    resultado = v1 / v2
                elif valor_token == '%': resultado = v1 % v2
                elif valor_token == '^': resultado = math.pow(v1, v2)
                pilha.append(str(arredondar_16bit(resultado)))
            except (ZeroDivisionError, ValueError) as e:
                print(f"-> Erro de operação para '{valor_token}': {e}")
                pilha.append('0.0')

        elif token.tipo == Tipo_de_Token.RES:
            if len(pilha) == 0:
                print("-> Erro: RES requer um índice numérico na pilha.")
                pilha.append('0.0'); continue
            n_str = pilha.pop()
            try:
                n = int(float(n_str))
                if 0 < n <= len(historico_resultados):
                    pilha.append(str(historico_resultados[-n]))
                else:
                    print(f"-> Erro: Índice N={n} fora de alcance.")
                    pilha.append('0.0')
            except ValueError:
                print(f"-> Erro: O valor '{n_str}' não é válido para RES.")
                pilha.append('0.0')

        elif token.tipo == Tipo_de_Token.MEM:
            if len(pilha) > 0 and pilha[-1].replace('.', '', 1).isdigit():
                valor_para_armazenar_str = pilha.pop()
                valor_float = float(valor_para_armazenar_str)
                memoria[token.valor] = valor_float
                pilha.append(str(arredondar_16bit(valor_float)))
            elif token.valor in memoria:
                valor = memoria.get(token.valor, 0.0)
                pilha.append(str(arredondar_16bit(valor)))
            else:
                print("-> Erro: Variável do tipo MEM não inicializada.")
                pilha.append('0.0')

        elif token.tipo == Tipo_de_Token.NUMERO_REAL:
            pilha.append(str(token.valor))
        else:
            pilha.append(valor_token)

    if len(pilha) == 1:
        return arredondar_16bit(pilha[0])
    else:
        print(f"-> Erro: {len(pilha)} itens na pilha: {pilha}")
        return arredondar_16bit(pilha[-1]) if pilha else 0.0
