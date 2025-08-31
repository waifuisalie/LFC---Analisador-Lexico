def gerarAssembly(lista_de_linhas_com_tokens: list) -> str:
    """
    Gera código Assembly AVR completo a partir de expressões RPN tokenizadas.
    Compatível com avr-gcc e inclui saída serial para debug.
    
    Args:
        lista_de_linhas_com_tokens: Lista de listas, onde cada sublista contém
                                   os tokens de uma linha RPN
    
    Returns:
        String contendo o código Assembly AVR completo
    """
    
    # Coletar todas as variáveis usadas
    variaveis = set()
    
    for linha in lista_de_linhas_com_tokens:
        for token in linha:
            # Identifica variáveis (não são números nem operadores)
            if (not token.isdigit() and 
                token not in ['+', '-', '*', '/', '^', 'RES'] and
                not (len(token) == 1 and token.isdigit())):  # Para tokens como '0', '1', etc.
                variaveis.add(token)
    
    # Início do código Assembly
    assembly = []
    
    # Cabeçalho compatível com avr-gcc
    assembly.extend([
        "; Código Assembly AVR para ATmega328p",
        "; Compilar com: avr-gcc -mmcu=atmega328p -nostartfiles -o prog.elf prog.s",
        "",
        "; Definições de registradores UART do ATmega328p",
        ".equ UDR0, 0xC6",
        ".equ UBRR0L, 0xC4", 
        ".equ UBRR0H, 0xC5",
        ".equ UCSR0C, 0xC2",
        ".equ UCSR0B, 0xC1",
        ".equ UCSR0A, 0xC0",
        "",
        "; Definições de constantes",
        ".equ FOSC, 16000000",
        ".equ BAUD, 9600", 
        ".equ UBRR_VAL, 103",
        "",
        "; Seção de dados",
        ".section .data",
        ""
    ])
    
    # Declaração das variáveis
    for var in sorted(variaveis):
        assembly.append(f"{var}: .space 2  ; Variável {var} (16 bits)")
    
    # Declaração do histórico de resultados
    for i in range(len(lista_de_linhas_com_tokens)):
        assembly.append(f"_result_line_{i}: .space 2  ; Resultado da linha {i}")
    
    assembly.extend([
        "",
        "; Área da pilha RPN",
        "stack_area: .space 64  ; 32 valores de 16 bits",
        "",
        "; Seção de código",
        ".section .text",
        ".global main",
        ""
    ])
    
    # Função de inicialização da UART
    assembly.extend([
        "; Inicialização da UART para comunicação serial",
        "uart_init:",
        "    ; Configura baud rate (103 para 9600 baud a 16MHz)",
        "    ldi r16, 0",
        "    sts UBRR0H, r16",
        "    ldi r16, 103", 
        "    sts UBRR0L, r16",
        "    ",
        "    ; Habilita transmissor e receptor",
        "    ldi r16, 0x18  ; (1<<RXEN0)|(1<<TXEN0)",
        "    sts UCSR0B, r16",
        "    ",
        "    ; Configura formato: 8 bits de dados, 1 stop bit",
        "    ldi r16, 0x06  ; (1<<UCSZ01)|(1<<UCSZ00)",
        "    sts UCSR0C, r16",
        "    ",
        "    ret",
        ""
    ])
    
    # Função para transmitir um caractere
    assembly.extend([
        "; Transmite um caractere via UART",
        "; Entrada: r16 = caractere a transmitir", 
        "uart_transmit:",
        "uart_wait:",
        "    lds r17, UCSR0A",
        "    sbrs r17, 5  ; UDRE0 bit",
        "    rjmp uart_wait",
        "    sts UDR0, r16",
        "    ret",
        ""
    ])
    
    # Função para transmitir string
    assembly.extend([
        "; Transmite string terminada em null",
        "; Entrada: Z pointer aponta para string",
        "uart_print_string:",
        "    lpm r16, Z+",
        "    cpi r16, 0",
        "    breq uart_string_done",
        "    call uart_transmit",
        "    rjmp uart_print_string",
        "uart_string_done:",
        "    ret",
        ""
    ])
    
    # Função para transmitir número decimal
    assembly.extend([
        "; Transmite número de 16 bits em decimal",
        "; Entrada: r25:r24 = número",
        "uart_print_number:",
        "    push r18",
        "    push r19", 
        "    push r20",
        "    push r21",
        "    push r22",
        "    push r23",
        "    ",
        "    ; Buffer para dígitos (máximo 5 dígitos + null)",
        "    ; Usa registradores como buffer temporário",
        "    ldi r18, 0  ; contador de dígitos",
        "    ldi r21, 10 ; divisor = 10",
        "    clr r22",
        "    ",
        "    ; Se número é 0, imprime '0' diretamente",
        "    cp r24, r22",
        "    cpc r25, r22", 
        "    brne num_not_zero",
        "    ldi r16, '0'",
        "    call uart_transmit",
        "    rjmp uart_num_done",
        "    ",
        "num_not_zero:",
        "    ; Extrai dígitos (do menos significativo para o mais significativo)",
        "extract_digits:",
        "    ; Divide por 10",
        "    mov r20, r24  ; backup do número",
        "    mov r23, r25",
        "    ",
        "    ; Divisão por 10 (simplificada)",
        "    clr r19",
        "    ldi r18, 16   ; contador de bits",
        "div_by_10_loop:",
        "    lsl r24",
        "    rol r25", 
        "    rol r19",
        "    cpi r19, 10",
        "    brcs div_by_10_next",
        "    subi r19, 10",
        "    ori r24, 1",
        "div_by_10_next:",
        "    dec r18",
        "    brne div_by_10_loop",
        "    ",
        "    ; r19 = resto (dígito), r25:r24 = quociente",
        "    subi r19, -'0'  ; converte para ASCII",
        "    push r19        ; empilha dígito",
        "    inc r18         ; incrementa contador",
        "    ",
        "    ; Continue se quociente não é zero",
        "    cp r24, r22",
        "    cpc r25, r22",
        "    brne extract_digits",
        "    ",
        "    ; Imprime dígitos na ordem correta",
        "print_digits:",
        "    pop r16",
        "    call uart_transmit", 
        "    dec r18",
        "    brne print_digits",
        "    ",
        "uart_num_done:",
        "    pop r23",
        "    pop r22",
        "    pop r21",
        "    pop r20",
        "    pop r19",
        "    pop r18",
        "    ret",
        ""
    ])
    
    # Sub-rotina de multiplicação 16x16 bits (simplificada)
    assembly.extend([
        "; Multiplicação 16x16 bits",
        "; Entrada: r25:r24 * r23:r22",
        "; Saída: r25:r24",
        "multiply_16:",
        "    push r0",
        "    push r1",
        "    push r18",
        "    push r19", 
        "    ",
        "    clr r18",
        "    clr r19",
        "    clr r0",
        "    ",
        "    ; Multiplicação usando mul (8x8)",
        "    mul r24, r22  ; low * low",
        "    mov r18, r0",
        "    mov r19, r1",
        "    ",
        "    mul r24, r23  ; low * high",
        "    add r19, r0",
        "    ",
        "    mul r25, r22  ; high * low", 
        "    add r19, r0",
        "    ",
        "    mov r24, r18",
        "    mov r25, r19",
        "    ",
        "    clr r1  ; restore zero register",
        "    pop r19",
        "    pop r18", 
        "    pop r1",
        "    pop r0",
        "    ret",
        ""
    ])
    
    # Sub-rotina de divisão (simplificada)
    assembly.extend([
        "; Divisão 16/16 bits",
        "; Entrada: r25:r24 / r23:r22",
        "; Saída: r25:r24",
        "divide_16:",
        "    push r18",
        "    push r19",
        "    ",
        "    ; Verifica divisão por zero",
        "    cp r22, r1",
        "    cpc r23, r1", 
        "    breq div_by_zero",
        "    ",
        "    clr r18",
        "    clr r19",
        "    ",
        "div_loop:",
        "    cp r24, r22",
        "    cpc r25, r23",
        "    brlo div_done",
        "    ",
        "    sub r24, r22",
        "    sbc r25, r23", 
        "    ",
        "    subi r18, -1",
        "    sbci r19, -1",
        "    ",
        "    rjmp div_loop",
        "    ",
        "div_done:",
        "    mov r24, r18",
        "    mov r25, r19",
        "    rjmp div_exit",
        "    ",
        "div_by_zero:",
        "    clr r24",
        "    clr r25",
        "    ",
        "div_exit:",
        "    pop r19",
        "    pop r18",
        "    ret",
        ""
    ])
    
    # Sub-rotina de potenciação  
    assembly.extend([
        "; Potenciação base^exp",
        "; Entrada: r25:r24 ^ r23:r22",
        "; Saída: r25:r24",
        "power_16:",
        "    push r18",
        "    push r19",
        "    push r20",
        "    push r21",
        "    ",
        "    ; Se expoente é 0, resultado é 1",
        "    cp r22, r1",
        "    cpc r23, r1",
        "    brne power_not_zero",
        "    ldi r24, 1",
        "    clr r25",
        "    rjmp power_exit",
        "    ",
        "power_not_zero:",
        "    mov r20, r24  ; salva base",
        "    mov r21, r25",
        "    mov r18, r22  ; salva expoente",
        "    mov r19, r23", 
        "    ldi r24, 1    ; resultado = 1",
        "    clr r25",
        "    ",
        "power_loop:",
        "    cp r18, r1",
        "    cpc r19, r1",
        "    breq power_exit",
        "    ",
        "    ; multiplica resultado pela base",
        "    mov r22, r20",
        "    mov r23, r21",
        "    call multiply_16",
        "    ",
        "    ; decrementa expoente",
        "    subi r18, 1",
        "    sbci r19, 0",
        "    ",
        "    rjmp power_loop",
        "    ",
        "power_exit:",
        "    pop r21",
        "    pop r20",
        "    pop r19",
        "    pop r18",
        "    ret",
        ""
    ])
    
    # Strings para output
    assembly.extend([
        "; Strings para output serial",
        ".section .progmem.data, \"a\", @progbits",
        "str_linha: .asciz \"Linha \"",
        "str_resultado: .asciz \": \"", 
        "str_newline: .asciz \"\\r\\n\"",
        "str_inicio: .asciz \"Calculadora RPN iniciada\\r\\n\"",
        "",
        ".section .text",
        ""
    ])
    
    # Rotina principal
    assembly.extend([
        "main:",
        "    ; Inicializa UART",
        "    call uart_init",
        "    ",
        "    ; Mensagem de início",
        "    ldi r30, lo8(str_inicio)",
        "    ldi r31, hi8(str_inicio)",
        "    call uart_print_string",
        "    ",
        "    ; Inicializa ponteiro de pilha para área reservada",
        "    ldi r28, lo8(stack_area + 64)",
        "    ldi r29, hi8(stack_area + 64)",
        "    ",
        ""
    ])
    
    # Gera código para cada linha
    for linha_idx, tokens in enumerate(lista_de_linhas_com_tokens):
        assembly.extend([
            f"; === Linha {linha_idx}: {' '.join(tokens)} ===",
            f"linha_{linha_idx}:",
            ""
        ])
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.isdigit():
                # Número - empilha na stack
                valor = int(token)
                assembly.extend([
                    f"    ; Empilha número {valor}",
                    f"    ldi r16, {valor & 0xFF}",
                    f"    ldi r17, {(valor >> 8) & 0xFF}",
                    "    st -Y, r17",
                    "    st -Y, r16",
                    ""
                ])
                
            elif token in variaveis and i == len(tokens) - 1:
                # Variável no final = operação de armazenamento
                assembly.extend([
                    f"    ; Armazena em variável {token}",
                    "    ld r16, Y+",
                    "    ld r17, Y+",
                    f"    sts {token}, r16",
                    f"    sts {token}+1, r17",
                    ""
                ])
                
            elif token in variaveis:
                # Variável no meio = carregamento
                assembly.extend([
                    f"    ; Carrega variável {token}",
                    f"    lds r16, {token}",
                    f"    lds r17, {token}+1",
                    "    st -Y, r17", 
                    "    st -Y, r16",
                    ""
                ])
                
            elif token == '+':
                # Soma
                assembly.extend([
                    "    ; Operação soma (+)",
                    "    ld r18, Y+",
                    "    ld r19, Y+",
                    "    ld r16, Y+",
                    "    ld r17, Y+",
                    "    add r16, r18",
                    "    adc r17, r19",
                    "    st -Y, r17",
                    "    st -Y, r16",
                    ""
                ])
                
            elif token == '-':
                # Subtração
                assembly.extend([
                    "    ; Operação subtração (-)",
                    "    ld r18, Y+", 
                    "    ld r19, Y+",
                    "    ld r16, Y+",
                    "    ld r17, Y+",
                    "    sub r16, r18",
                    "    sbc r17, r19",
                    "    st -Y, r17",
                    "    st -Y, r16",
                    ""
                ])
                
            elif token == '*':
                # Multiplicação
                assembly.extend([
                    "    ; Operação multiplicação (*)",
                    "    ld r22, Y+",
                    "    ld r23, Y+", 
                    "    ld r24, Y+",
                    "    ld r25, Y+",
                    "    call multiply_16",
                    "    st -Y, r25",
                    "    st -Y, r24",
                    ""
                ])
                
            elif token == '/':
                # Divisão
                assembly.extend([
                    "    ; Operação divisão (/)",
                    "    ld r22, Y+",
                    "    ld r23, Y+",
                    "    ld r24, Y+",
                    "    ld r25, Y+",
                    "    call divide_16",
                    "    st -Y, r25",
                    "    st -Y, r24",
                    ""
                ])
                
            elif token == '^':
                # Potenciação
                assembly.extend([
                    "    ; Operação potenciação (^)",
                    "    ld r22, Y+",
                    "    ld r23, Y+",
                    "    ld r24, Y+", 
                    "    ld r25, Y+",
                    "    call power_16",
                    "    st -Y, r25",
                    "    st -Y, r24",
                    ""
                ])
                
            elif token == 'RES' and i > 0 and tokens[i-1].isdigit():
                # Comando N RES - carrega resultado da linha N
                linha_num = int(tokens[i-1])
                assembly.extend([
                    f"    ; Carrega resultado da linha {linha_num}",
                    f"    lds r16, _result_line_{linha_num}",
                    f"    lds r17, _result_line_{linha_num}+1",
                    "    st -Y, r17",
                    "    st -Y, r16",
                    ""
                ])
                
            i += 1
        
        # Armazena o resultado final da linha e exibe via serial
        assembly.extend([
            f"    ; Armazena e exibe resultado da linha {linha_idx}",
            "    ld r16, Y+",
            "    ld r17, Y+",
            f"    sts _result_line_{linha_idx}, r16",
            f"    sts _result_line_{linha_idx}+1, r17",
            "    ",
            "    ; Exibe resultado via serial",
            "    ldi r30, lo8(str_linha)",
            "    ldi r31, hi8(str_linha)", 
            "    call uart_print_string",
            "    ",
            f"    ; Imprime número da linha ({linha_idx})",
            f"    ldi r24, {linha_idx}",
            "    clr r25",
            "    call uart_print_number",
            "    ",
            "    ldi r30, lo8(str_resultado)",
            "    ldi r31, hi8(str_resultado)",
            "    call uart_print_string",
            "    ",
            "    ; Imprime o resultado",
            "    mov r24, r16",
            "    mov r25, r17", 
            "    call uart_print_number",
            "    ",
            "    ldi r30, lo8(str_newline)",
            "    ldi r31, hi8(str_newline)",
            "    call uart_print_string",
            ""
        ])
    
    # Finalização do programa
    assembly.extend([
        "done:",
        "    rjmp done  ; Loop infinito",
        ""
    ])
    
    return '\n'.join(assembly)


# Exemplo de uso e teste
if __name__ == "__main__":
    # Teste com o exemplo fornecido
    exemplo_input = [['10', 'VAR'], ['VAR', '5', '+']]
    resultado = gerarAssembly(exemplo_input)
    print(resultado)
    # Save output to .s file
    with open("calculadora.s", "w") as f:
        f.write(resultado)
