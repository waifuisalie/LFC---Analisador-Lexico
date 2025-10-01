# rpn_calc_fixed.py - Versão corrigida do processador RPN

import math
from .tokens import Token, Tipo_de_Token
from .analisador_lexico import Analisador_Lexico

def parseExpressao(linha_operacao: str):
    analisador_lexico = Analisador_Lexico(linha_operacao)
    tokens = analisador_lexico.analise()
    return tokens

def arredondar_16bit(valor):
    """Simula a precisão de ponto flutuante de 16 bits (duas casas decimais)."""
    try:
        return round(float(valor), 2)
    except (ValueError, TypeError):
        return valor

def encontrar_blocos_controle(tokens: list[Token], inicio: int, num_blocos: int) -> tuple[list, int]:
    """
    Encontra blocos delimitados por parênteses para estruturas de controle.
    """
    blocos = []
    idx = inicio
    
    while idx < len(tokens) and len(blocos) < num_blocos:
        # Procura o próximo parêntese de abertura
        while idx < len(tokens) and tokens[idx].tipo != Tipo_de_Token.ABRE_PARENTESES:
            idx += 1
        
        if idx >= len(tokens):
            break
            
        # Encontrou um parêntese de abertura
        bloco = []
        contagem = 1
        idx += 1  # Pula o parêntese de abertura
        
        # Coleta tokens até encontrar o parêntese de fechamento correspondente
        while idx < len(tokens) and contagem > 0:
            token_atual = tokens[idx]
            
            if token_atual.tipo == Tipo_de_Token.ABRE_PARENTESES:
                bloco.append(token_atual)
                contagem += 1
            elif token_atual.tipo == Tipo_de_Token.FECHA_PARENTESES:
                contagem -= 1
                if contagem > 0:
                    bloco.append(token_atual)
            else:
                bloco.append(token_atual)
                
            idx += 1
        
        if contagem == 0:
            blocos.append(bloco)
            
    return blocos, idx

def processarEstruturaControle(tokens: list[Token], memoria: dict) -> float:
    """
    Processa estruturas de controle (IFELSE, WHILE, FOR)
    """
    # Encontra a estrutura de controle
    for i, token in enumerate(tokens):
        if token.tipo == Tipo_de_Token.IFELSE:
            return processarIFELSE(tokens, i, memoria)
        elif token.tipo == Tipo_de_Token.WHILE:
            return processarWHILE(tokens, i, memoria)
        elif token.tipo == Tipo_de_Token.FOR:
            return processarFOR(tokens, i, memoria)
    
    return 0.0

def processarIFELSE(tokens: list[Token], inicio: int, memoria: dict) -> float:
    """
    Processa estrutura IFELSE: (IFELSE (condição)(verdadeiro)(falso))
    """
    try:
        # Encontra os 3 blocos necessários
        blocos, _ = encontrar_blocos_controle(tokens, inicio + 1, 3)
        
        if len(blocos) != 3:
            print("ERRO -> IFELSE requer 3 blocos: (condição)(verdadeiro)(falso)")
            return 0.0
            
        # Processa os blocos diretamente com processarTokens
        condicao = processarTokens(blocos[0], memoria)

        
        # Executa o bloco apropriado (verdadeiro se != 0)
        if float(condicao) != 0.0:
            resultado = processarTokens(blocos[1], memoria)

            return resultado
        else:
            resultado = processarTokens(blocos[2], memoria)

            return resultado
            
    except Exception as e:
        print(f"ERRO no IFELSE: {e}")
        return 0.0

def processarWHILE(tokens: list[Token], inicio: int, memoria: dict) -> float:
    """
    Processa estrutura WHILE: (WHILE (condição)(corpo))
    Exemplo: (WHILE (X 5 <)((X X 1 +)(Y X 2 *)))
    """
    try:
        # Encontra os 2 blocos necessários
        blocos, _ = encontrar_blocos_controle(tokens, inicio + 1, 2)
        
        if len(blocos) != 2:
            print("ERRO -> WHILE requer 2 blocos: (condição)(corpo)")
            return 0.0
            
        resultado = 0.0
        iteracoes = 0
        max_iteracoes = 1000  # Limite de segurança
        
        while iteracoes < max_iteracoes:
            # Avalia a condição
            condicao = processarTokens(blocos[0], memoria)
            
            # Se a condição é falsa, sai do loop
            if float(condicao) == 0.0:
                break
                
            # Executa o corpo do loop
            # O corpo pode conter múltiplas expressões separadas por parênteses
            resultado = executarCorpoLoop(blocos[1], memoria)
            iteracoes += 1
            
        return resultado
        
    except Exception as e:
        print(f"ERRO no WHILE: {e}")
        return 0.0

def processarFOR(tokens: list[Token], inicio: int, memoria: dict) -> float:
    """
    Processa estrutura FOR: (FOR (inicial)(final)(incremento)(corpo))
    Exemplo: (FOR (1)(10)(2)((P P 1 +)(Q P 2 *)))
    """
    try:
        # Encontra os 4 blocos necessários
        blocos, _ = encontrar_blocos_controle(tokens, inicio + 1, 4)
        
        if len(blocos) != 4:
            print("ERRO -> FOR requer 4 blocos: (inicial)(final)(incremento)(corpo)")
            return 0.0
            
        # Avalia os parâmetros do FOR
        inicial = int(processarTokens(blocos[0], memoria))
        final = int(processarTokens(blocos[1], memoria))
        incremento = int(processarTokens(blocos[2], memoria)) or 1
        
        resultado = 0.0
        contador = inicial
        iteracoes = 0
        max_iteracoes = 1000  # Limite de segurança
        
        # Cria uma variável de controle implícita para o loop
        memoria['_FOR_COUNTER'] = float(contador)
        
        while contador < final and iteracoes < max_iteracoes:
            # Atualiza a variável de controle
            memoria['_FOR_COUNTER'] = float(contador)
            
            # Executa o corpo do loop
            resultado = executarCorpoLoop(blocos[3], memoria)
            
            contador += incremento
            iteracoes += 1
            
            # Debug para acompanhar execução
            # print(f"FOR iteração {iteracoes}: contador={contador-incremento}, resultado={resultado}")
            
        # Remove a variável de controle temporária
        if '_FOR_COUNTER' in memoria:
            del memoria['_FOR_COUNTER']
            
        return resultado
        
    except Exception as e:
        print(f"ERRO no FOR: {e}")
        return 0.0

def executarCorpoLoop(tokens_corpo: list[Token], memoria: dict) -> float:
    """
    Executa o corpo de um loop, que pode conter múltiplas expressões.
    Exemplo: ((X X 1 +)(Y X 2 *)) -> executa duas expressões sequenciais
    """
    if not tokens_corpo:
        return 0.0
    
    # Separa as expressões individuais
    expressoes = []
    i = 0
    
    while i < len(tokens_corpo):
        if tokens_corpo[i].tipo == Tipo_de_Token.ABRE_PARENTESES:
            # Encontra uma expressão delimitada por parênteses
            contagem = 1
            j = i + 1
            expressao = []
            
            while j < len(tokens_corpo) and contagem > 0:
                token_atual = tokens_corpo[j]
                
                if token_atual.tipo == Tipo_de_Token.ABRE_PARENTESES:
                    contagem += 1
                elif token_atual.tipo == Tipo_de_Token.FECHA_PARENTESES:
                    contagem -= 1
                    
                if contagem > 0:
                    expressao.append(token_atual)
                    
                j += 1
            
            if expressao:
                expressoes.append(expressao)
            
            i = j
        else:
            i += 1
    
    # Executa todas as expressões sequencialmente
    resultado = 0.0
    
    for expressao in expressoes:
        # Verifica se é uma atribuição de variável e inicializa se necessário (nova sintaxe: VALOR VARIAVEL)
        if len(expressao) >= 1 and expressao[-1].tipo == Tipo_de_Token.VARIAVEL:
            var_nome = expressao[-1].valor
            if var_nome not in memoria:
                memoria[var_nome] = 0.0
        
        # Adiciona parênteses de volta para processamento correto
        expressao_completa = [Token(Tipo_de_Token.ABRE_PARENTESES, '(')] + expressao + [Token(Tipo_de_Token.FECHA_PARENTESES, ')')]
        resultado = executarExpressao(expressao_completa, memoria)
    
    # Se não encontrou expressões delimitadas, processa todos os tokens como uma única expressão
    if not expressoes:
        resultado = processarTokens(tokens_corpo, memoria)
    
    return resultado

def executarExpressao(tokens: list[Token], memoria: dict) -> float:
    """
    Executa uma expressão RPN de forma recursiva, lidando corretamente com expressões aninhadas.
    """
    if not tokens:
        return 0.0
    
    # Remove tokens de parênteses e FIM para simplificar o processamento
    tokens_limpos = []
    for token in tokens:
        if token.tipo not in [Tipo_de_Token.ABRE_PARENTESES, Tipo_de_Token.FECHA_PARENTESES, Tipo_de_Token.FIM]:
            tokens_limpos.append(token)
    
    if not tokens_limpos:
        return 0.0
    
    # Verifica se é uma atribuição de variável simples (NUMERO VARIAVEL)
    if (len(tokens_limpos) == 2 and 
        tokens_limpos[0].tipo == Tipo_de_Token.NUMERO_REAL and 
        tokens_limpos[1].tipo == Tipo_de_Token.VARIAVEL):
        
        valor = float(tokens_limpos[0].valor)
        var_nome = tokens_limpos[1].valor
        memoria[var_nome] = valor
        
        return valor
    
    # Verifica se contém estruturas de controle primeiro
    for token in tokens_limpos:
        if token.tipo in [Tipo_de_Token.IFELSE, Tipo_de_Token.WHILE, Tipo_de_Token.FOR]:
            return processarEstruturaControle(tokens, memoria)
    
    # Verifica se é uma atribuição com expressão aninhada (EXPRESSAO VARIAVEL)
    if (len(tokens_limpos) >= 2 and 
        tokens_limpos[-1].tipo == Tipo_de_Token.VARIAVEL):
        
        var_nome = tokens_limpos[-1].valor
        # Processa a expressão (todos os tokens exceto o último que é a variável)
        resultado = processarTokens(tokens_limpos[:-1], memoria)
        memoria[var_nome] = resultado
                
        return resultado
    
    # Caso contrário, processa normalmente
    resultado = processarTokens(tokens_limpos, memoria)
    
    # Não adiciona ao histórico aqui, pois já foi adicionado nas atribuições
    return resultado

def processarTokens(tokens: list[Token], memoria: dict) -> float:
    """
    Processa uma lista de tokens em notação RPN.
    """
    if not tokens:
        return 0.0
    
    # Se há apenas um token
    if len(tokens) == 1:
        token = tokens[0]
        if token.tipo == Tipo_de_Token.NUMERO_REAL:
            return float(token.valor)
        elif token.tipo == Tipo_de_Token.VARIAVEL:
            return memoria.get(token.valor, 0.0)
        elif token.tipo == Tipo_de_Token.RES:
            hist = memoria.get('historico_resultados', [])
            return hist[-1] if hist else 0.0
        return 0.0
    
    # Caso especial: índice + RES (ex: 3 RES)
    if (len(tokens) == 2 and 
        tokens[0].tipo == Tipo_de_Token.NUMERO_REAL and 
        tokens[1].tipo == Tipo_de_Token.RES):
        
        idx = int(float(tokens[0].valor))
        hist = memoria.get('historico_resultados', [])
        if hist and 0 < idx <= len(hist):
            resultado = hist[-idx]

            return resultado
        else:
            print(f"ERRO -> Índice {idx} fora do intervalo do histórico (tamanho: {len(hist)})")
            return 0.0
    
    # Processa expressões aninhadas primeiro
    tokens_expandidos = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token.tipo == Tipo_de_Token.ABRE_PARENTESES:
            # Encontra o bloco correspondente
            contagem = 1
            j = i + 1
            sub_tokens = []
            
            while j < len(tokens) and contagem > 0:
                if tokens[j].tipo == Tipo_de_Token.ABRE_PARENTESES:
                    contagem += 1
                elif tokens[j].tipo == Tipo_de_Token.FECHA_PARENTESES:
                    contagem -= 1
                
                if contagem > 0:
                    sub_tokens.append(tokens[j])
                j += 1
            
            # Processa a subexpressão
            if sub_tokens:
                resultado = processarTokens(sub_tokens, memoria)
                # Cria um token com o resultado
                token_resultado = Token(Tipo_de_Token.NUMERO_REAL, resultado)
                tokens_expandidos.append(token_resultado)
            
            i = j
        else:
            tokens_expandidos.append(token)
            i += 1
    
    # Agora processa com uma pilha RPN tradicional
    pilha = []
    
    for token in tokens_expandidos:
        if token.tipo == Tipo_de_Token.NUMERO_REAL:
            pilha.append(float(token.valor))
            
        elif token.tipo == Tipo_de_Token.VARIAVEL:
            valor = memoria.get(token.valor, 0.0)
            pilha.append(valor)
            
        elif token.tipo == Tipo_de_Token.RES:
            # Verifica se há um índice na pilha
            if pilha and isinstance(pilha[-1], (int, float)):
                idx = int(pilha.pop())
                hist = memoria.get('historico_resultados', [])
                if hist and 0 < idx <= len(hist):
                    pilha.append(hist[-idx])
                else:
                    print(f"ERRO -> Índice {idx} fora do intervalo do histórico (tamanho: {len(hist)})")
                    pilha.append(0.0)
            else:
                # Sem índice, retorna o último resultado
                hist = memoria.get('historico_resultados', [])
                if hist:
                    pilha.append(hist[-1])
                else:
                    print("ERRO -> Histórico vazio")
                    pilha.append(0.0)
                
        elif str(token.valor) in ['+', '-', '*', '/', '%', '^']:
            if len(pilha) >= 2:
                b = pilha.pop()
                a = pilha.pop()
                
                try:
                    if token.valor == '+': resultado = a + b
                    elif token.valor == '-': resultado = a - b
                    elif token.valor == '*': resultado = a * b
                    elif token.valor == '/': resultado = a / b if b != 0 else 0.0
                    elif token.valor == '%': resultado = a % b if b != 0 else 0.0
                    elif token.valor == '^': resultado = math.pow(a, b)
                    
                    pilha.append(arredondar_16bit(resultado))
                except (ZeroDivisionError, ValueError, OverflowError):
                    pilha.append(0.0)
            else:
                print(f"ERRO -> Tokens insuficientes para o operador '{token.valor}'")
                pilha.append(0.0)
                
        elif str(token.valor) in ['<', '>', '==', '<=', '>=', '!=']:
            if len(pilha) >= 2:
                b = pilha.pop()
                a = pilha.pop()
                
                try:
                    # Garante que os valores sejam numéricos
                    a_num = float(a)
                    b_num = float(b)
                    
                    if token.valor == '<': resultado = 1.0 if a_num < b_num else 0.0
                    elif token.valor == '>': resultado = 1.0 if a_num > b_num else 0.0
                    elif token.valor == '==': resultado = 1.0 if abs(a_num - b_num) < 1e-10 else 0.0
                    elif token.valor == '<=': resultado = 1.0 if a_num <= b_num else 0.0
                    elif token.valor == '>=': resultado = 1.0 if a_num >= b_num else 0.0
                    elif token.valor == '!=': resultado = 1.0 if abs(a_num - b_num) >= 1e-10 else 0.0
                    else: resultado = 0.0
                    
                    pilha.append(resultado)
                except (ValueError, TypeError) as e:
                    print(f"ERRO na comparação {token.valor}: {e}")
                    pilha.append(0.0)
            else:
                print(f"ERRO -> Tokens insuficientes para o operador '{token.valor}'")
                pilha.append(0.0)
                
        elif str(token.valor) in ['&&', '||']:
            if len(pilha) >= 2:
                b = pilha.pop()
                a = pilha.pop()
                
                try:
                    # Converte para booleano: 0 = falso, qualquer outro valor = verdadeiro
                    a_bool = float(a) != 0.0
                    b_bool = float(b) != 0.0
                    
                    if token.valor == '&&': resultado = 1.0 if a_bool and b_bool else 0.0
                    elif token.valor == '||': resultado = 1.0 if a_bool or b_bool else 0.0
                    else: resultado = 0.0
                    
                    pilha.append(resultado)
                except (ValueError, TypeError) as e:
                    print(f"ERRO na operação lógica {token.valor}: {e}")
                    pilha.append(0.0)
            else:
                print(f"ERRO -> Tokens insuficientes para o operador '{token.valor}'")
                pilha.append(0.0)
                
        elif str(token.valor) == '!':
            if len(pilha) >= 1:
                a = pilha.pop()
                try:
                    # NOT lógico: 0 vira 1, qualquer outro valor vira 0
                    resultado = 1.0 if float(a) == 0.0 else 0.0
                    pilha.append(resultado)
                except (ValueError, TypeError) as e:
                    print(f"ERRO na operação NOT: {e}")
                    pilha.append(0.0)
            else:
                print("ERRO -> Token insuficiente para o operador '!'")
                pilha.append(0.0)
    
    return arredondar_16bit(pilha[-1] if pilha else 0.0)