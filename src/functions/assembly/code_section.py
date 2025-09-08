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
