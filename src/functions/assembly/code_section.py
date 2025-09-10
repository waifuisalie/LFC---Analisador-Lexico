from .operations import (
    is_number, is_integer, is_variable_mem,
    gerar_push_int, gerar_operacao,
)

def gerar_secao_codigo(codigo: list[str], tokens: list[str]) -> None:
    """Gera o corpo principal e o processamento dos tokens RPN."""
    codigo_principal = [
        "; ====================================================================",
        "; SEÇÃO DE CÓDIGO PRINCIPAL - 16-BIT VERSION",
        "; ====================================================================",
        "",
        "main:",
        "    ; Inicializar stack pointer",
        "    ldi r16, 0xFF",
        "    out SPL, r16",
        "    ldi r16, 0x08",
        "    out SPH, r16",
        "",
        "    ; Inicializar UART (9600 baud) e pilha RPN",
        "    rcall uart_init",
        "    rcall stack_init",
        "",
        "    ; Processar expressão RPN",
        "    rcall processar_rpn",
        "",
        "    ; Enviar resultado via UART",
        "    rcall send_result",
        "",
        "    ; Loop infinito",
        "    rjmp end_program",
        ""
    ]
    codigo.extend(codigo_principal)
    _gerar_processamento_tokens(codigo, tokens)

def _gerar_processamento_tokens(codigo: list[str], tokens: list[str]) -> None:
    codigo.extend([
        "; ====================================================================",
        "; PROCESSAMENTO DOS TOKENS RPN - 16-BIT VERSION",
        "; ====================================================================",
        "",
        "processar_rpn:",
        "    ; Processando expressão RPN com suporte 16-bit:",
    ])

    token_str = " ".join(tokens)
    codigo.append(f"    ; Expressão: {token_str}")
    codigo.append("")

    # Mensagem inicial de debug
    codigo.extend([
        "    ; Debug: Enviar mensagem inicial",
        "    ldi r16, 'S'",
        "    rcall uart_transmit",
        "    ldi r16, 't'",
        "    rcall uart_transmit",
        "    ldi r16, 'a'",
        "    rcall uart_transmit",
        "    ldi r16, 'r'",
        "    rcall uart_transmit",
        "    ldi r16, 't'",
        "    rcall uart_transmit",
        "    ldi r16, 13",
        "    rcall uart_transmit",
        "    ldi r16, 10",
        "    rcall uart_transmit",
        ""
    ])

    # Loop nos tokens
    for i, token in enumerate(tokens):
        codigo.append(f"    ; Processando token {i}: '{token}'")

        if is_number(token):
            valor = int(float(token)) if not is_integer(token) else int(float(token))
            if valor > 65535:
                valor = valor & 0xFFFF
            codigo.extend(gerar_push_int(valor))

        elif token in ['+', '-', '*', '/', '%', '^']:
            codigo.extend(gerar_operacao(token))

        elif token == 'MEM':
            codigo.extend(["    rcall comando_mem", ""])

        elif token == 'RES':
            codigo.extend(["    rcall comando_res", ""])

        elif is_variable_mem(token):
            var_index = ord(token) - ord('A')
            codigo.extend([
                f"    ldi r17, {var_index}  ; Índice da variável {token}",
                "    rcall load_var",
                ""
            ])
        else:
            codigo.extend([f"    ; Token desconhecido: {token}", ""])

    codigo.extend([
        "    ; Fim do processamento",
        "    ret",
        "",
    ])

def gerar_secao_codigo_multiplo(codigo: list[str], all_tokens: list[list[str]]) -> None:
    """Gera o código principal para múltiplas operações RPN."""
    codigo_principal = [
        "; ====================================================================",
        "; SEÇÃO DE CÓDIGO PRINCIPAL - MÚLTIPLAS OPERAÇÕES RPN - 16-BIT VERSION",
        "; ====================================================================",
        "",
        "main:",
        "    ; Inicializar stack pointer",
        "    ldi r16, 0xFF",
        "    out SPL, r16",
        "    ldi r16, 0x08",
        "    out SPH, r16",
        "",
        "    ; Inicializar UART (9600 baud) e pilha RPN",
        "    rcall uart_init",
        "    rcall stack_init",
        "",
        "    ; Processar todas as operações RPN sequencialmente",
    ]
    codigo.extend(codigo_principal)
    
    # Gerar chamadas para cada operação
    for i in range(len(all_tokens)):
        codigo.extend([
            f"    ; Operação {i+1}",
            f"    rcall processar_rpn_op{i+1}",
            "    rcall send_result",
            ""
        ])
    
    codigo.extend([
        "    ; Loop infinito",
        "    rjmp end_program",
        ""
    ])
    
    # Gerar função para cada operação
    for i, tokens in enumerate(all_tokens, 1):
        _gerar_processamento_operacao(codigo, tokens, i)

def _gerar_processamento_operacao(codigo: list[str], tokens: list[str], op_number: int) -> None:
    """Gera o processamento de uma operação RPN específica."""
    codigo.extend([
        "; ====================================================================",
        f"; PROCESSAMENTO OPERAÇÃO {op_number} - 16-BIT VERSION",
        "; ====================================================================",
        "",
        f"processar_rpn_op{op_number}:",
        f"    ; Processando operação {op_number} com suporte 16-bit:",
    ])

    token_str = " ".join(tokens)
    codigo.append(f"    ; Expressão: {token_str}")
    codigo.append("")

    # Cabeçalho estético da operação
    codigo.extend([
        f"    ; Cabeçalho da operação {op_number}",
        "    ldi r16, 13",
        "    rcall uart_transmit",
        "    ldi r16, 10",
        "    rcall uart_transmit",
        "    ldi r16, '='",
        "    rcall uart_transmit",
        "    ldi r16, '='",
        "    rcall uart_transmit",
        "    ldi r16, '='",
        "    rcall uart_transmit",
        "    ldi r16, '='",
        "    rcall uart_transmit",
        "    ldi r16, ' '",
        "    rcall uart_transmit",
        "    ldi r16, 'O'",
        "    rcall uart_transmit",
        "    ldi r16, 'P'",
        "    rcall uart_transmit",
        "    ldi r16, 'E'",
        "    rcall uart_transmit",
        "    ldi r16, 'R'",
        "    rcall uart_transmit",
        "    ldi r16, 'A'",
        "    rcall uart_transmit",
        "    ldi r16, 'C'",
        "    rcall uart_transmit",
        "    ldi r16, 'A'",
        "    rcall uart_transmit",
        "    ldi r16, 'O'",
        "    rcall uart_transmit",
        "    ldi r16, ' '",
        "    rcall uart_transmit",
    ])
    
    # Enviar número da operação
    if op_number < 10:
        codigo.extend([
            f"    ldi r16, '{op_number}'",
            "    rcall uart_transmit",
        ])
    else:
        codigo.extend([
            f"    ldi r16, '1'",
            "    rcall uart_transmit",
            f"    ldi r16, '0'",
            "    rcall uart_transmit",
        ])
    
    codigo.extend([
        "    ldi r16, ' '",
        "    rcall uart_transmit",
        "    ldi r16, '='",
        "    rcall uart_transmit",
        "    ldi r16, '='",
        "    rcall uart_transmit",
        "    ldi r16, '='",
        "    rcall uart_transmit",
        "    ldi r16, '='",
        "    rcall uart_transmit",
        "    ldi r16, 13",
        "    rcall uart_transmit",
        "    ldi r16, 10",
        "    rcall uart_transmit",
        "",
        "    ; Mostrar expressão",
        "    ldi r16, 'E'",
        "    rcall uart_transmit",
        "    ldi r16, 'x'",
        "    rcall uart_transmit",
        "    ldi r16, 'p'",
        "    rcall uart_transmit",
        "    ldi r16, 'r'",
        "    rcall uart_transmit",
        "    ldi r16, 'e'",
        "    rcall uart_transmit",
        "    ldi r16, 's'",
        "    rcall uart_transmit",
        "    ldi r16, 's'",
        "    rcall uart_transmit",
        "    ldi r16, 'a'",
        "    rcall uart_transmit",
        "    ldi r16, 'o'",
        "    rcall uart_transmit",
        "    ldi r16, ':'",
        "    rcall uart_transmit",
        "    ldi r16, ' '",
        "    rcall uart_transmit",
        ""
    ])
    
    # Enviar a expressão caractere por caractere
    for char in token_str:
        if char == ' ':
            codigo.extend([
                "    ldi r16, ' '",
                "    rcall uart_transmit",
            ])
        elif char.isalnum() or char in "+-*/%^()":
            codigo.extend([
                f"    ldi r16, '{char}'",
                "    rcall uart_transmit",
            ])
    
    codigo.extend([
        "    ldi r16, 13",
        "    rcall uart_transmit",
        "    ldi r16, 10",
        "    rcall uart_transmit",
        ""
    ])

    # Processar tokens (reutilizando a lógica existente)
    for i, token in enumerate(tokens):
        codigo.append(f"    ; Processando token {i}: '{token}'")

        if is_number(token):
            valor = int(float(token)) if not is_integer(token) else int(float(token))
            if valor > 65535:
                valor = valor & 0xFFFF
            codigo.extend(gerar_push_int(valor))

        elif token in ['+', '-', '*', '/', '%', '^']:
            codigo.extend(gerar_operacao(token))

        elif token == 'MEM':
            codigo.extend(["    rcall comando_mem", ""])

        elif token == 'RES':
            codigo.extend(["    rcall comando_res", ""])

        elif is_variable_mem(token):
            var_index = ord(token) - ord('A')
            codigo.extend([
                f"    ldi r17, {var_index}  ; Índice da variável {token}",
                "    rcall load_var",
                ""
            ])
        else:
            codigo.extend([f"    ; Token desconhecido: {token}", ""])

    # Cabeçalho do resultado
    codigo.extend([
        "    ; Mostrar resultado",
        "    ldi r16, 'R'",
        "    rcall uart_transmit",
        "    ldi r16, 'e'",
        "    rcall uart_transmit",
        "    ldi r16, 's'",
        "    rcall uart_transmit",
        "    ldi r16, 'u'",
        "    rcall uart_transmit",
        "    ldi r16, 'l'",
        "    rcall uart_transmit",
        "    ldi r16, 't'",
        "    rcall uart_transmit",
        "    ldi r16, 'a'",
        "    rcall uart_transmit",
        "    ldi r16, 'd'",
        "    rcall uart_transmit",
        "    ldi r16, 'o'",
        "    rcall uart_transmit",
        "    ldi r16, ':'",
        "    rcall uart_transmit",
        "    ldi r16, ' '",
        "    rcall uart_transmit",
        "",
        "    ; Fim do processamento da operação",
        "    ret",
        "",
    ])
