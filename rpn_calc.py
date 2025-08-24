#!/usr/bin/env python3

import math

def executarExpressao(tokens: list, memoria: dict, historico_resultados: list) -> float:
    pilha = []
    
    KEYWORDS = ['RES', 'MEM']
    OPERADORES = ['+', '-', '*', '/', '%', '^']

    for i, token in enumerate(tokens):
        
        if token in OPERADORES:
            if len(pilha) < 2: print(f"-> Erro: tokens insuficientes para o operador '{token}'"); continue
            v2_str, v1_str = pilha.pop(), pilha.pop()
            resultado = 0.0
            try:
                if token == '/':
                    # Lógica especial para divisão inteira vs real 
                    if '.' in v1_str or '.' in v2_str:
                        v1, v2 = float(v1_str), float(v2_str)
                        if v2 == 0: raise ZeroDivisionError
                        resultado = v1 / v2
                    else:
                        v1, v2 = int(v1_str), int(v2_str)
                        if v2 == 0: raise ZeroDivisionError
                        resultado = float(v1 // v2)
                else:
                    v1, v2 = float(v1_str), float(v2_str)
                    if token == '+': resultado = v1 + v2
                    elif token == '-': resultado = v1 - v2
                    elif token == '*': resultado = v1 * v2
                    elif token == '%': resultado = v1 % v2
                    elif token == '^': resultado = math.pow(v1, v2)
                pilha.append(str(resultado))
            except (ZeroDivisionError, ValueError) as e:
                print(f"-> Erro de operação para '{token}': {e}"); pilha.append('0.0')

        elif token.upper() == 'RES':
            if not pilha: print("-> Erro: Pilha vazia para o comando RES."); return 0.0
            n_str = pilha.pop()
            n = int(float(n_str))
            tamanho_historico = len(historico_resultados)
            if 0 < n <= tamanho_historico:
                pilha.append(str(historico_resultados[tamanho_historico - n]))
            else:
                print(f"-> Erro: Índice N={n} inválido para RES."); pilha.append('0.0')

        elif token.upper() == 'MEM':
            if len(pilha) < 2: print("-> Erro: formato inválido para MEM."); continue
            nome_variavel, valor_para_armazenar_str = pilha.pop(), pilha.pop()
            if nome_variavel.replace('.','',1).isdigit():
                print(f"-> Erro: Nome de variável inválido '{nome_variavel}'."); continue
            valor_float = float(valor_para_armazenar_str)
            memoria[nome_variavel.upper()] = valor_float
            pilha.append(str(valor_float))

        # --- BLOCO DE DADOS ---
        else:
            # Se não é uma ação (operador/keyword), é um dado.
            # Pode ser um número, ou um nome de variável.
            # Primeiro, verificamos se o token é um identificador para RECUPERAÇÃO.
            # Um identificador é para recuperação se NÃO for seguido por MEM.
            # Para simplificar, vamos assumir que um identificador sozinho é para recuperação.
            is_number = False
            try:
                float(token)
                is_number = True
            except ValueError:
                pass

            if is_number:
                pilha.append(token)
            else: # É um identificador (uma palavra)
                # Se o próximo token for 'MEM', então este identificador é um NOME para atribuição
                # e deve ser empilhado como está.
                is_assignment_name = False
                if (i + 1) < len(tokens):
                    if tokens[i+1].upper() == 'MEM':
                        is_assignment_name = True
                
                if is_assignment_name:
                    pilha.append(token) # Empilha 'VALOR' como string
                else:
                    # Se não, é para recuperação de valor.
                    valor = memoria.get(token.upper(), 0.0)
                    pilha.append(str(valor)) # Empilha o valor '0.0' para 'DADO_NOVO'

    if len(pilha) == 1:
        return round(float(pilha[0]), 2)
    else:
        print(f"-> Erro: A expressão finalizou com {len(pilha)} itens na pilha: {pilha}.")
        return 0.0 if not pilha else round(float(pilha[-1]), 2)

    if len(pilha) == 1:
        return round(float(pilha[0]), 2)
    else:
        print(f"-> Erro: A expressão finalizou com {len(pilha)} itens na pilha: {pilha}.")
        return round(float(pilha[-1]), 2) if pilha else 0.0

def rodar_testes():
    """
    Executa uma suíte de testes para a função executarExpressao.
    """
    print("--- INICIANDO SUÍTE DE TESTES PARA executarExpressao() ---")
    
    # Estruturas de dados para os testes
    memoria = {}
    historico = []
    
    # Lista de testes no formato: (nome, tokens, resultado_esperado)
    testes_simples = [
        ("Soma Simples", ['3.14', '2.0', '+'], 5.14),
        ("Subtração", ['10.5', '0.5', '-'], 10.0),
        ("Multiplicação", ['7.0', '0.5', '*'], 3.5),
        ("Divisão Real", ['10.0', '4.0', '/'], 2.5),
        ("Divisão Inteira", ['10', '3', '/'], 3.0),
        ("Resto da Divisão", ['10', '3', '%'], 1.0),
        ("Potenciação", ['3', '4', '^'], 81.0),
        ("Soma com Multiplicação Aninhada", ['10', '2', '3', '*', '+'], 16.0),
        ("Divisão de Produtos", ['10', '5', '*', '5', '2', '*', '/'], 5.0),
    ]

    for nome, tokens, esperado in testes_simples:
        resultado = executarExpressao(list(tokens), memoria, list(historico))
        status = "Passou" if resultado == esperado else "FALHOU"
        print(f"Teste: {nome:<30} | Esperado: {esperado:<8} | Obtido: {resultado:<8} | Status: {status}")

    print("\n--- TESTANDO COMANDOS MEM E RES ---")
    
    # Teste 10: Armazenar em MEM
    # Para o teste, simplificamos a tokenização de (12.5 VALOR MEM)
    nome_t10 = "Armazenar em MEM"
    tokens_t10 = ['12.5', 'VALOR', 'MEM']
    esperado_t10 = 12.5
    resultado_t10 = executarExpressao(tokens_t10, memoria, historico)
    status_t10 = "Passou" if resultado_t10 == esperado_t10 and memoria.get('VALOR') == 12.5 else "FALHOU"
    print(f"Teste: {nome_t10:<30} | Esperado: {esperado_t10:<8} | Obtido: {resultado_t10:<8} | Status: {status_t10}")
    print(f"      Estado da memória: {memoria}")

    # Teste 11: Recuperar de MEM
    nome_t11 = "Recuperar de MEM"
    tokens_t11 = ['VALOR', '2.5', '+']
    esperado_t11 = 15.0
    resultado_t11 = executarExpressao(tokens_t11, memoria, historico)
    status_t11 = "Passou" if resultado_t11 == esperado_t11 else "FALHOU"
    print(f"Teste: {nome_t11:<30} | Esperado: {esperado_t11:<8} | Obtido: {resultado_t11:<8} | Status: {status_t11}")

    # Teste 12: Recuperar de MEM sem Inicializar
    nome_t12 = "Recuperar MEM não inicializado"
    tokens_t12 = ['DADO_NOVO', '1', '+']
    esperado_t12 = 1.0
    resultado_t12 = executarExpressao(tokens_t12, memoria, historico)
    status_t12 = "Passou" if resultado_t12 == esperado_t12 else "FALHOU"
    print(f"Teste: {nome_t12:<30} | Esperado: {esperado_t12:<8} | Obtido: {resultado_t12:<8} | Status: {status_t12}")

    # Cenário Multi-linha para RES
    print("\n--- Cenário Multi-linha para RES ---")
    
    # Linha 1
    tokens_res1 = ['10', '5', '+']
    res1 = executarExpressao(tokens_res1, memoria, historico)
    historico.append(res1)
    print(f"Linha 1: Expressão {tokens_res1} -> Resultado: {res1} | Histórico: {historico}")

    # Linha 2
    tokens_res2 = ['3', '2', '*']
    res2 = executarExpressao(tokens_res2, memoria, historico)
    historico.append(res2)
    print(f"Linha 2: Expressão {tokens_res2} -> Resultado: {res2} | Histórico: {historico}")

    # Linha 3 (Teste RES)
    nome_t_res = "Teste RES"
    tokens_t_res = ['1', 'RES', '2', 'RES', '-']
    esperado_t_res = -9.0
    resultado_t_res = executarExpressao(tokens_t_res, memoria, historico)
    status_t_res = "Passou" if resultado_t_res == esperado_t_res else "FALHOU"
    print(f"Teste: {nome_t_res:<30} | Esperado: {esperado_t_res:<8} | Obtido: {resultado_t_res:<8} | Status: {status_t_res}")

    print("\n--- TESTANDO CASOS DE ERRO ---")

    # Teste 13: Divisão por Zero
    nome_t13 = "Divisão por Zero"
    tokens_t13 = ['10', '0', '/']
    esperado_t13 = 0.0
    resultado_t13 = executarExpressao(tokens_t13, memoria, historico)
    status_t13 = "Passou" if resultado_t13 == esperado_t13 else "FALHOU"
    print(f"Teste: {nome_t13:<30} | Esperado: {esperado_t13:<8} | Obtido: {resultado_t13:<8} | Status: {status_t13}")

    # Teste 14: Índice Inválido para RES
    nome_t14 = "Índice RES Inválido"
    tokens_t14 = ['3', 'RES']
    esperado_t14 = 0.0 # Valor padrão de falha
    # O histórico atual é [15.0, 6.0]
    resultado_t14 = executarExpressao(tokens_t14, memoria, historico)
    status_t14 = "Passou" if resultado_t14 == esperado_t14 else "FALHOU"
    print(f"Teste: {nome_t14:<30} | Esperado: {esperado_t14:<8} | Obtido: {resultado_t14:<8} | Status: {status_t14}")
    
    print("\n--- FIM DOS TESTES ---")

if __name__ == "__main__":
    rodar_testes()
