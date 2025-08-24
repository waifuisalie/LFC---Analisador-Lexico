#!/usr/bin/env python3

import math
import sys

# Função para arredondar para 2 casas decimais, simulando precisão de 16 bits
def arredondar_16bit(valor):
    return round(float(valor), 2)

def executarExpressao(tokens: list, memoria: dict, historico_resultados: list) -> float:
    """
    Executa uma expressão em notação polonesa reversa (RPN).

    Args:
        1) tokens (list): Uma lista de strings representando a expressão.
        2) memoria (dict): Um dicionário para armazenar variáveis nomeadas.
        3) historico_resultados (list): Uma lista dos resultados de expressões anteriores.

    Returns:
        float: O resultado da expressão.
    """
    pilha = []
    
    for token in tokens:
        
        # --- BLOCO DE OPERADORES E COMANDOS ESPECIAIS ---
        token_upper = token.upper()

        if token_upper in ['+', '-', '*', '/', '%', '^']:
            if len(pilha) < 2:
                print(f"-> Erro: tokens insuficientes para o operador '{token}'")
                continue
            
            v2_str, v1_str = pilha.pop(), pilha.pop()
            resultado = 0.0
            
            try:
                # Lógica para divisão
                if token_upper == '/':
                    v1, v2 = float(v1_str), float(v2_str)
                    if v2 == 0: raise ZeroDivisionError("Divisão por zero.")
                    
                    if '.' in v1_str or '.' in v2_str:
                        resultado = v1 / v2
                    else:
                        resultado = float(int(v1) // int(v2))
                # Lógica para outras operações
                else:
                    v1, v2 = float(v1_str), float(v2_str)
                    if token_upper == '+': resultado = v1 + v2
                    elif token_upper == '-': resultado = v1 - v2
                    elif token_upper == '*': resultado = v1 * v2
                    elif token_upper == '%':
                        # A operação de resto exige inteiros
                        resultado = int(v1) % int(v2)
                    elif token_upper == '^': resultado = math.pow(v1, v2)
                
                pilha.append(str(arredondar_16bit(resultado)))
            except (ZeroDivisionError, ValueError) as e:
                print(f"-> Erro de operação para '{token}': {e}")
                pilha.append('0.0')

        elif token_upper == 'RES':
            # RES sem um número na pilha
            if not pilha:
                print("-> Aviso: RES sem índice, utilizando valor da última expressão.")
                if historico_resultados:
                    pilha.append(str(historico_resultados[-1]))
                else:
                    print("-> Aviso: Histórico de resultados vazio. Retornando 0.0.")
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
                print(f"-> Erro: O valor '{n_str}' não é um índice válido para RES.")
                pilha.append('0.0') # Devolve um valor padrão para a pilha

        elif token_upper == 'MEM':
            if len(pilha) < 2:
                print("-> Erro: formato inválido para MEM. Espera-se (VALOR NOME MEM).")
                continue
            
            nome_variavel, valor_para_armazenar_str = pilha.pop(), pilha.pop()
            
            if nome_variavel.replace('.', '', 1).isdigit() or nome_variavel.upper() in ['RES', 'MEM'] + ['+', '-', '*', '/', '%', '^']:
                print(f"-> Erro: Nome de variável inválido '{nome_variavel}'.")
                pilha.append('0.0')
                continue
            
            valor_float = float(valor_para_armazenar_str)
            memoria[nome_variavel.upper()] = valor_float
            pilha.append(str(arredondar_16bit(valor_float)))

        # --- BLOCO DE DADOS (números ou variáveis) ---
        else:
            try:
                float(token)
                pilha.append(token)
            except ValueError:
                # Se não é um número, é um nome de variável
                valor = memoria.get(token_upper, 0.0)
                pilha.append(str(arredondar_16bit(valor)))

    # Lógica de retorno única e corrigida
    if len(pilha) == 1:
        return arredondar_16bit(pilha[0])
    else:
        print(f"-> Erro: A expressão finalizou com {len(pilha)} itens na pilha: {pilha}.")
        return arredondar_16bit(pilha[-1]) if pilha else 0.0

# ------------------- Funções de Teste e Execução -------------------

def rodar_testes():
    """
    Executa uma suíte de testes para a função executarExpressao.
    """
    print("--- INICIANDO SUÍTE DE TESTES PARA executarExpressao() ---")
    
    memoria = {}
    historico = []
    
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

    # Teste 12: Recuperar de MEM não inicializado
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
    nome_t_res = "Teste RES com número"
    tokens_t_res = ['1', 'RES', '2', 'RES', '-']
    esperado_t_res = 9.0
    resultado_t_res = executarExpressao(tokens_t_res, memoria, historico)
    status_t_res = "Passou" if resultado_t_res == esperado_t_res else "FALHOU"
    print(f"Teste: {nome_t_res:<30} | Esperado: {esperado_t_res:<8} | Obtido: {resultado_t_res:<8} | Status: {status_t_res}")

    # Teste RES sem número
    nome_t_res_sem_num = "Teste RES sem número"
    tokens_t_res_sem_num = ['RES', '3.0', '+']
    esperado_t_res_sem_num = 9.0
    resultado_t_res_sem_num = executarExpressao(tokens_t_res_sem_num, memoria, historico)
    status_t_res_sem_num = "Passou" if resultado_t_res_sem_num == esperado_t_res_sem_num else "FALHOU"
    print(f"Teste: {nome_t_res_sem_num:<30} | Esperado: {esperado_t_res_sem_num:<8} | Obtido: {resultado_t_res_sem_num:<8} | Status: {status_t_res_sem_num}")

    print("\n--- FIM DOS TESTES ---")

def lerArquivos(nomeArquivo: str): 
    try:
        with open(nomeArquivo, 'r', encoding="utf-8") as arquivos_teste:
            linhas = [linha.strip() for linha in arquivos_teste if linha.strip()]
        return linhas 
    except FileNotFoundError:
        print(f'-> Erro: Arquivo não encontrado: {nomeArquivo}')
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro: Especificar nome do arquivo de teste")
        sys.exit(1)

    arquivo = sys.argv[1]
    vetor_linhas = lerArquivos(arquivo) 

    # A execução principal agora pode usar a função executarExpressao
    # iterando sobre as linhas do vetor_linhas.
    print(f"\nProcessando arquivo: {arquivo}\n")
    memoria_global = {}
    historico_global = []

    for linha in vetor_linhas:
        # Aqui, o analisador léxico do Aluno 1 entraria em ação
        # Para simular, vamos dividir a linha em tokens
        tokens_simulados = linha.split()
        
        resultado = executarExpressao(tokens_simulados, memoria_global, historico_global)
        
        if resultado is not None:
            historico_global.append(resultado)
            print(f"Expressão: '{linha}' | Resultado: {resultado}")
            
    print("\n--- EXECUTANDO SUÍTE DE TESTES AUTOMÁTICOS ---")
    rodar_testes()