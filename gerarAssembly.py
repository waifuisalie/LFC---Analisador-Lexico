def gerarAssembly(tokens, codigoAssembly):
    """
    Gera código Assembly AVR para Arduino Uno a partir de tokens RPN
    
    Args:
        tokens (list): Lista de strings contendo os tokens da expressão RPN
        codigoAssembly (list): Lista para armazenar as linhas do código Assembly gerado
        
    Returns:
        None (modifica codigoAssembly in-place)
    """
    
    # Limpa o código assembly anterior
    codigoAssembly.clear() # this might be dumb lol, study if this is necessary!
    
    # Header do arquivo Assembly
    _gerar_header_assembly(codigoAssembly)
    
    # Seção de dados (variáveis, constantes)
    _gerar_secao_dados(codigoAssembly)  # this might be dumb lol, study if this is necessary
    
    # Seção de código principal
    _gerar_secao_codigo(codigoAssembly, tokens)  # this is where the magic happens
    
    # Footer (loop infinito, rotinas auxiliares)
    _gerar_footer_assembly(codigoAssembly) # this might necessary, study what this really does.


def _gerar_header_assembly(codigo):
    """Gera o cabeçalho padrão do arquivo Assembly"""
    header = [
        "; ====================================================================",
        "; Código Assembly gerado automaticamente para Arduino Uno (ATmega328p)",
        "; Processador de expressões RPN (Reverse Polish Notation)",
        "; ====================================================================",
        "" 
        ]
    codigo.extend(header)


def _gerar_secao_dados(codigo):
    """Gera a seção de dados (variáveis e constantes)"""
    dados = [
        "; ====================================================================", 
        "; SEÇÃO DE DADOS",
        "; ====================================================================",
        "",
    ]
    codigo.extend(dados)


def _gerar_secao_codigo(codigo, tokens):
    """Gera o código principal que processa os tokens RPN"""
    codigo_principal = [
        "; ====================================================================",
        "; SEÇÃO DE CÓDIGO PRINCIPAL", 
        "; ====================================================================",
        "",
    ]
    codigo.extend(codigo_principal)
    
    # Aqui será onde processaremos os tokens individualmente
    _gerar_processamento_tokens(codigo, tokens)


def _gerar_processamento_tokens(codigo, tokens):
    """Gera código específico para processar cada token"""
    codigo.extend([
        "; ====================================================================",
        "; PROCESSAMENTO DOS TOKENS RPN",
        "; ====================================================================",
        "",
        "processar_rpn:",
        "    ; Processando expressão RPN:",
    ])
    
    # Para debug: lista os tokens como comentários
    token_str = " ".join(tokens)
    codigo.append(f"    ; Expressão: {token_str}")
    codigo.append("")
    
    # Processa cada token individualmente
    for i, token in enumerate(tokens):
        codigo.append(f"    ; Processando token {i}: '{token}'")
        
        # Verifica o tipo do token
        if _is_number(token):
            codigo.append(f"    call push_float      ; Empilha {token}")
        elif token in ['+', '-', '*', '/', '%', '^']:
            codigo.append(f"    call operacao_{_name_operation(token)}  ; Executa {token}")
        elif token == 'MEM':
            codigo.append("    call comando_mem     ; Comando MEM")
        elif token == 'RES':
            codigo.append("    call comando_res     ; Comando RES")
        elif _is_variable_mem(token):
            codigo.append(f"    call load_var        ; Carrega variável {token}")
        else:
            codigo.append(f"    ; Token desconhecido: {token}")
        
        codigo.append("")
    
    codigo.extend([
        "    ; Fim do processamento",
        "    ret",
        "",
    ])


def _gerar_footer_assembly(codigo):
    """Gera rotinas auxiliares e código de finalização"""
    footer = [
        "; ====================================================================",
        "; ROTINAS AUXILIARES",
        "; ====================================================================",
        "",
        "; ====================================================================",
        "; FIM DO CÓDIGO",
        "; ====================================================================",
    ]
    codigo.extend(footer)


# ====================================================================
# FUNÇÕES AUXILIARES PARA ANÁLISE DE TOKENS
# ====================================================================

def _is_number(token):
    """Verifica se o token é um número (int ou float)"""
    try:
        float(token)
        return True
    except ValueError:
        return False


def _is_variable_mem(token):
    """Verifica se o token é uma variável de memória (letras maiúsculas)"""
    return token.isalpha() and token.isupper() and token != 'MEM' and token != 'RES'


def _name_operation(operador):
    """Converte operador para nome de função"""
    mapeamento = {
        '+': 'soma',
        '-': 'subtracao', 
        '*': 'multiplicacao',
        '/': 'divisao',
        '%': 'modulo',
        '^': 'potencia'
    }
    return mapeamento.get(operador, 'desconhecida')


def save_assembly(codigo_assembly, nome_arquivo="programa.s"):
    """Salva o código assembly em um arquivo"""
    try:
        with open(nome_arquivo, 'w') as arquivo:
            for linha in codigo_assembly:
                arquivo.write(linha + '\n')
        print(f"Código Assembly salvo em: {nome_arquivo}")
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return False


# Função de teste
if __name__ == "__main__":
    # Teste básico com tokens simples (formato correto)
    tokens_teste = ["6.0", "2.0", "*"]  # 6.0 * 2.0 = 12.0
    codigo_assembly = []
    
    print("Testando gerarAssembly()...")
    print(f"Expressão RPN: {' '.join(tokens_teste)} (resultado esperado: 12.0)")
    
    gerarAssembly(tokens_teste, codigo_assembly)
    
    print(f"Código gerado ({len(codigo_assembly)} linhas):")
    print("Primeiras 20 linhas:")
    for i, linha in enumerate(codigo_assembly[:20]):
        print(f"{i+1:3}: {linha}")
    
    if len(codigo_assembly) > 20:
        print(f"... (mais {len(codigo_assembly) - 20} linhas)")
        print("Últimas 10 linhas:")
        for i, linha in enumerate(codigo_assembly[-10:], len(codigo_assembly)-9):
            print(f"{i:3}: {linha}")
    
    # Salva o arquivo
    save_assembly(codigo_assembly, "src/programa.s")
    
    print("\nTeste com expressão complexa:")
    tokens_complexo = ["2.0", "2.0", "+", "5.0", "1.0", "-", "*"] 
    print(f"Expressão: {' '.join(tokens_complexo)}")
    print("Passos: 2.0+2.0=4.0, 5.0-1.0=4.0, 4.0*4.0=16.0")
