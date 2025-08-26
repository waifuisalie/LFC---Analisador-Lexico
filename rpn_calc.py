#!/usr/bin/env python3

import math
import sys

def arredondar_16bit(valor):
    """Simula a precisão de ponto flutuante de 16 bits (duas casas decimais)."""
    return round(float(valor), 2)

def executarExpressao(tokens: list, memoria: dict, historico_resultados: list) -> float:
    """Executa uma expressão em notação polonesa reversa (RPN)."""
    pilha = []
    
    for token in tokens:
        token_upper = token.upper()

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

def rodar_testes():
    """Executa uma suíte de testes para a função executarExpressao."""
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
    
    nome_t10 = "Armazenar em MEM"
    tokens_t10 = ['12.5', 'MEM']
    esperado_t10 = 12.5
    resultado_t10 = executarExpressao(tokens_t10, memoria, historico)
    status_t10 = "Passou" if resultado_t10 == esperado_t10 and memoria.get('MEM') == 12.5 else "FALHOU"
    print(f"Teste: {nome_t10:<30} | Esperado: {esperado_t10:<8} | Obtido: {resultado_t10:<8} | Status: {status_t10}")
    print(f"      Estado da memória: {memoria}")

    nome_t11 = "Recuperar de MEM"
    tokens_t11 = ['MEM', '2.5', '+']
    esperado_t11 = 15.0
    resultado_t11 = executarExpressao(tokens_t11, memoria, historico)
    status_t11 = "Passou" if resultado_t11 == esperado_t11 else "FALHOU"
    print(f"Teste: {nome_t11:<30} | Esperado: {esperado_t11:<8} | Obtido: {resultado_t11:<8} | Status: {status_t11}")

    print("\n--- Cenário Multi-linha para RES ---")
    
    historico.clear()
    tokens_res1 = ['10', '5', '+']
    res1 = executarExpressao(tokens_res1, memoria, historico)
    historico.append(res1)
    print(f"Linha 1: Expressão {tokens_res1} -> Resultado: {res1} | Histórico: {historico}")

    tokens_res2 = ['3', '2', '*']
    res2 = executarExpressao(tokens_res2, memoria, historico)
    historico.append(res2)
    print(f"Linha 2: Expressão {tokens_res2} -> Resultado: {res2} | Histórico: {historico}")

    nome_t_res = "Teste RES com número"
    tokens_t_res = ['2', 'RES', '1', 'RES', '-']
    esperado_t_res = 9.0
    resultado_t_res = executarExpressao(tokens_t_res, memoria, historico)
    status_t_res = "Passou" if resultado_t_res == esperado_t_res else "FALHOU"
    print(f"Teste: {nome_t_res:<30} | Esperado: {esperado_t_res:<8} | Obtido: {resultado_t_res:<8} | Status: {status_t_res}")

    print("\n--- FIM DOS TESTES ---")

def lerArquivos(nomeArquivo: str): 
    try:
        with open(nomeArquivo, 'r', encoding="utf-8") as arquivos_teste:
            linhas = [linha.strip() for linha in arquivos_teste if linha.strip()]
        return linhas 
    except FileNotFoundError:
        print(f'-> Erro: Arquivo não encontrado: {nomeArquivo}')
        return []

def exibirResultados(vetor_linhas: list[str]) -> None: 
    memoria_global = {}
    historico_global =[]
    tokens_salvo = []

    for i ,linha in enumerate(vetor_linhas, start=1): 
            tokens_recebidos = linha.replace('(', '').replace(')', '').strip().split()
            tokens_salvo.append(tokens_recebidos)
            resultado = executarExpressao(tokens_recebidos, memoria_global, historico_global)

            if resultado is not None:
                historico_global.append(resultado)
            
            print(f"Linha {i:02d}: Expressão '{linha}' -> Resultado: {resultado}")

    try:
        with open("tokens_gerados.txt","w", encoding='utf-8') as f:
            for lista_de_tokens in tokens_salvo:
                linha_formatada = " ".join(lista_de_tokens)
                f.write(linha_formatada + "\n")
    except Exception as e:
        print(f'Erro ao escreve os tokens no arquivo {e}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro: Especificar nome do arquivo de teste")
        sys.exit(1)

    arquivo = sys.argv[1]
    vetor_linhas = lerArquivos(arquivo) 

    print(f"\nProcessando arquivo: {arquivo}\n")
    exibirResultados(vetor_linhas)
            
    print("\n--- EXECUTANDO SUÍTE DE TESTES AUTOMÁTICOS ---")
    rodar_testes()
