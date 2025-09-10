# rpn_calc.py

import math
from .tokens import Token, Tipo_de_Token
from .analisador_lexico import Analisador_Lexico

def parseExpressao(linha_operacao: str):
    analisador_lexico = Analisador_Lexico(linha_operacao)
    tokens = analisador_lexico.analise()
    # remove parênteses (mantém-se se quiser validar no futuro)
    tokens = [t for t in tokens if t.tipo not in (Tipo_de_Token.ABRE_PARENTESES, Tipo_de_Token.FECHA_PARENTESES)]
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

        if valor_token in ['+', '-', '*', '/', '%', '^']:
            if len(pilha) < 2:
                print(f"ERRO -> Tokens insuficientes para o operador '{valor_token}'")
                continue
            v2_str, v1_str = pilha.pop(), pilha.pop()
            resultado = 0.0
            try:
                v1, v2 = float(v1_str), float(v2_str)
                if valor_token == '+': resultado = v1 + v2
                elif valor_token == '-': resultado = v1 - v2
                elif valor_token == '*': resultado = v1 * v2
                elif valor_token == '/':
                    if v2 == 0:
                        raise ZeroDivisionError("ERRO -> Operação de divisão por zero não é permitida.")
                    resultado = v1 / v2
                elif valor_token == '%': resultado = v1 % v2
                elif valor_token == '^': resultado = math.pow(v1, v2)
                pilha.append(str(arredondar_16bit(resultado)))
            except (ZeroDivisionError, ValueError) as e:
                print(f"ERRO -> Operação de divisão para '{valor_token}': {e}")
                pilha.append('0.0')

        elif token.tipo == Tipo_de_Token.RES:
            if len(pilha) == 0:
                print("ERRO -> RES requer um índice numérico na pilha.")
                pilha.append('0.0'); continue
            n_str = pilha.pop()
            try:
                n = int(float(n_str))
                if 0 < n <= len(historico_resultados):
                    pilha.append(str(historico_resultados[-n]))
                else:
                    print(f"ERRO -> Índice N={n} fora de alcance.")
                    pilha.append('0.0')
            except ValueError:
                print(f"-ERRO -> O valor '{n_str}' não é válido para RES.")
                pilha.append('0.0')

        elif token.tipo == Tipo_de_Token.MEM:
            if len(pilha) > 0 and pilha[-1].replace('.', '', 1).isdigit():
                valor_para_armazenar_str = pilha.pop()
                valor_float = float(valor_para_armazenar_str)
                memoria['MEM'] = valor_float
                pilha.append(str(arredondar_16bit(valor_float)))
            elif 'MEM' in memoria:
                valor = memoria.get('MEM', 0.0)
                pilha.append(str(arredondar_16bit(valor)))
            else:
                print("ERRO -> MEM não inicializado.")
                pilha.append('0.0')

        elif token.tipo == Tipo_de_Token.NUMERO_REAL:
            pilha.append(str(token.valor))
        else:
            pilha.append(valor_token)

    if len(pilha) == 1:
        return arredondar_16bit(pilha[0])
    else:
        print(f"ERRO -> {len(pilha)} itens na pilha: {pilha}")
        return arredondar_16bit(pilha[-1]) if pilha else 0.0
