def gerarAssembly(tokens, codigoAssembly):
    """
    Gera código Assembly AVR para Arduino Uno a partir de tokens RPN - 16-BIT VERSION
    
    Args:
        tokens (list): Lista de strings contendo os tokens da expressão RPN
        codigoAssembly (list): Lista para armazenar as linhas do código Assembly gerado
        
    Returns:
        None (modifica codigoAssembly in-place)
    """
    
    # Limpa o código assembly anterior
    codigoAssembly.clear()
    
    # Header do arquivo Assembly
    _gerar_header_assembly(codigoAssembly)
    
    # Seção de dados (variáveis, constantes)
    _gerar_secao_dados(codigoAssembly)
    
    # Seção de código principal
    _gerar_secao_codigo(codigoAssembly, tokens)
    
    # Rotinas auxiliares (stack operations, arithmetic, etc.)
    _gerar_rotinas_auxiliares(codigoAssembly)
    
    # Footer (loop infinito)
    _gerar_footer_assembly(codigoAssembly)


def _gerar_header_assembly(codigo):
    """Gera o cabeçalho padrão do arquivo Assembly"""
    header = [
        "; ====================================================================",
        "; Código Assembly gerado automaticamente para Arduino Uno (ATmega328p)",
        "; Processador de expressões RPN (Reverse Polish Notation) - 16-BIT VERSION",
        "; Suporte para inteiros de 0 a 65535",
        "; Compilado com PlatformIO/AVR-GCC",
        "; ====================================================================",
        "",
        '#include "registers.inc"',
        ".global main",
        "",
        ".section .text",
        ""
    ]
    codigo.extend(header)


def _gerar_footer_assembly(codigo):
    """Gera código de finalização"""
    footer = [
        "; ====================================================================",
        "; FINALIZAÇÃO - 16-BIT VERSION",
        "; ====================================================================",
        "",
        "end_program:",
        "    rjmp end_program         ; Loop infinito",
        "",
        "; ====================================================================",
        "; FIM DO CÓDIGO - 16-BIT RPN CALCULATOR",
        "; Suporte completo para inteiros de 0 a 65535",
        "; ====================================================================",
    ]
    codigo.extend(footer)


# ====================================================================
# GERANDO CÓDIGO REGISTERS.INC - 16-BIT VERSION
# ====================================================================

def save_registers_inc(nome_arquivo="registers.inc"):
    """Cria o arquivo registers.inc com as definições do ATmega328P - 16-BIT VERSION"""
    conteudo = """; ATmega328P Register Definitions
; Custom header for assembly programming
; Updated for RPN Calculator Project - TRUE 16-BIT VERSION
; Supports integers from 0 to 65535

; Stack Pointer Registers
.equ SPL,     0x3D    ; Stack Pointer Low
.equ SPH,     0x3E    ; Stack Pointer High

; SRAM Memory Layout
.equ RAMSTART, 0x0100  ; Start of SRAM
.equ RAMEND,   0x08FF  ; End of SRAM (2KB)

; UART0 Registers
.equ UDR0,    0xC6    ; UART Data Register
.equ UBRR0L,  0xC4    ; UART Baud Rate Register Low
.equ UBRR0H,  0xC5    ; UART Baud Rate Register High
.equ UCSR0A,  0xC0    ; UART Control and Status Register A
.equ UCSR0B,  0xC1    ; UART Control and Status Register B
.equ UCSR0C,  0xC2    ; UART Control and Status Register C

; UART0 Control Bits
.equ RXC0,    7       ; Receive Complete
.equ TXC0,    6       ; Transmit Complete
.equ UDRE0,   5       ; Data Register Empty
.equ FE0,     4       ; Frame Error
.equ DOR0,    3       ; Data OverRun
.equ UPE0,    2       ; Parity Error
.equ U2X0,    1       ; Double Transmission Speed
.equ MPCM0,   0       ; Multi-processor Communication Mode

.equ RXCIE0,  7       ; RX Complete Interrupt Enable
.equ TXCIE0,  6       ; TX Complete Interrupt Enable
.equ UDRIE0,  5       ; Data Register Empty Interrupt Enable
.equ RXEN0,   4       ; Receiver Enable
.equ TXEN0,   3       ; Transmitter Enable
.equ UCSZ02,  2       ; Character Size bit 2
.equ RXB80,   1       ; Receive Data Bit 8
.equ TXB80,   0       ; Transmit Data Bit 8

.equ UMSEL01, 7       ; UART Mode Select bit 1
.equ UMSEL00, 6       ; UART Mode Select bit 0
.equ UPM01,   5       ; Parity Mode bit 1
.equ UPM00,   4       ; Parity Mode bit 0
.equ USBS0,   3       ; Stop Bit Select
.equ UCSZ01,  2       ; Character Size bit 1
.equ UCSZ00,  1       ; Character Size bit 0
.equ UCPOL0,  0       ; Clock Polarity

; GPIO Ports (commonly used)
.equ PORTB,   0x05    ; Port B Data Register
.equ DDRB,    0x04    ; Port B Data Direction Register
.equ PINB,    0x03    ; Port B Input Pins Register

.equ PORTC,   0x08    ; Port C Data Register
.equ DDRC,    0x07    ; Port C Data Direction Register
.equ PINC,    0x06    ; Port C Input Pins Register

.equ PORTD,   0x0B    ; Port D Data Register
.equ DDRD,    0x0A    ; Port D Data Direction Register
.equ PIND,    0x09    ; Port D Input Pins Register

; Timer/Counter0 Registers
.equ TCNT0,   0x46    ; Timer/Counter0 Register
.equ TCCR0A,  0x44    ; Timer/Counter0 Control Register A
.equ TCCR0B,  0x45    ; Timer/Counter0 Control Register B
.equ TIMSK0,  0x6E    ; Timer/Counter0 Interrupt Mask Register
.equ TIFR0,   0x15    ; Timer/Counter0 Interrupt Flag Register

; Interrupt Vectors (word addresses)
.equ RESET_VECTOR,    0x0000
.equ INT0_VECTOR,     0x0001
.equ INT1_VECTOR,     0x0002
.equ TIMER0_OVF_VECTOR, 0x0010

; Useful Constants for 16-bit Calculator
.equ BAUD_9600, 103     ; Baud rate divisor for 9600 bps at 16MHz
.equ BAUD_19200, 51     ; Baud rate divisor for 19200 bps at 16MHz
.equ BAUD_38400, 25     ; Baud rate divisor for 38400 bps at 16MHz

; ASCII Constants
.equ ASCII_0,     48    ; ASCII code for '0'
.equ ASCII_9,     57    ; ASCII code for '9'
.equ ASCII_CR,    13    ; Carriage Return
.equ ASCII_LF,    10    ; Line Feed
.equ ASCII_SPACE, 32    ; Space character

; 16-bit Math Constants for RPN calculator
.equ MAX_STACK_SIZE, 16 ; Maximum stack depth for RPN
.equ MAX_VARIABLES, 26  ; Number of variables (A-Z)
.equ MAX_INT16, 65535   ; Maximum 16-bit unsigned integer
.equ MIN_INT16, 0       ; Minimum 16-bit unsigned integer

; Memory Layout for 16-bit RPN Calculator
.equ RPN_STACK_START, 0x0200   ; Start of RPN stack in SRAM (16-bit entries)
.equ RPN_VARS_START,  0x0300   ; Start of variable storage (16-bit each)
.equ RPN_TEMP_START,  0x0400   ; Temporary calculation area
.equ DIGIT_BUFFER,    0x0500   ; Buffer for number to string conversion

; Status Flags for RPN Calculator
.equ FLAG_OVERFLOW,   0    ; Arithmetic overflow (bit position)
.equ FLAG_UNDERFLOW,  1    ; Stack underflow  
.equ FLAG_DIVZERO,    2    ; Division by zero
.equ FLAG_INVALID,    3    ; Invalid operation

; Register Usage Convention for 16-bit RPN Calculator
; r16-r17: Primary 16-bit operand (little endian: r16=low, r17=high)
; r18-r19: Secondary 16-bit operand (little endian: r18=low, r19=high)
; r20-r23: Temporary storage for 16-bit operations
; r24-r27: Variable operations, memory access, loop counters
; r28-r31: Pointer registers (X=r27:r26, Y=r29:r28, Z=r31:r30)
; 
; IMPORTANT NOTES:
; - r0, r1 used by mul instruction - always clear r1 after mul!
; - All 16-bit values stored in little endian format (low byte first)
; - Stack grows from 0x0200 upward, each entry is 2 bytes
; - Maximum safe operations depend on available SRAM (2KB total)
"""
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        print(f"Arquivo {nome_arquivo} criado com sucesso (16-bit version).")
        return True
    except Exception as e:
        print(f"Erro ao criar {nome_arquivo}: {e}")
        return False


# ====================================================================
# FUNÇÕES AUXILIARES PARA ANÁLISE DE TOKENS - 16-BIT VERSION
# ====================================================================

def _is_number(token):
    """Verifica se o token é um número (int ou float)"""
    try:
        float(token)
        return True
    except ValueError:
        return False


def _is_integer(token):
    """Verifica se o token é um número inteiro"""
    try:
        val = float(token)
        return val == int(val)
    except ValueError:
        return False


def _is_variable_mem(token):
    """Verifica se o token é uma variável de memória (letras maiúsculas)"""
    return token.isalpha() and token.isupper() and token != 'MEM' and token != 'RES'


def save_assembly(codigo_assembly, nome_arquivo="programa.s"):
    """Salva o código assembly em um arquivo"""
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            for linha in codigo_assembly:
                arquivo.write(linha + '\n')
        print(f"Código Assembly salvo em: {nome_arquivo} (16-bit version)")
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return False


def _gerar_secao_dados(codigo):
    """Gera a seção de dados (variáveis e constantes)"""
    dados = [
        "; ====================================================================", 
        "; SEÇÃO DE DADOS - 16-BIT VERSION",
        "; ====================================================================",
        "",
        "; Stack pointer para pilha de inteiros 16-bit (simula pilha RPN)",
        "; Cada entrada da pilha ocupa 2 bytes (16 bits)",
        "; Memória SRAM para armazenar resultados e variáveis",
        "",
        ".section .data",
        "stack_ptr: .byte 1        ; Ponteiro da pilha RPN",
        "mem_vars:  .space 52      ; Espaço para 26 variáveis de 16-bit (A-Z)",
        "temp_result: .space 4     ; Resultado temporário",
        "",
        ".section .text",
        ""
    ]
    codigo.extend(dados)


def _gerar_secao_codigo(codigo, tokens):
    """Gera o código principal que processa os tokens RPN"""
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
        "    ; Inicializar UART para debug (9600 baud)",
        "    rcall uart_init",
        "",
        "    ; Inicializar pilha RPN",
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
    
    # Aqui será onde processaremos os tokens individualmente
    _gerar_processamento_tokens(codigo, tokens)


def _gerar_processamento_tokens(codigo, tokens):
    """Gera código específico para processar cada token"""
    codigo.extend([
        "; ====================================================================",
        "; PROCESSAMENTO DOS TOKENS RPN - 16-BIT VERSION",
        "; ====================================================================",
        "",
        "processar_rpn:",
        "    ; Processando expressão RPN com suporte 16-bit:",
    ])
    
    # Para debug: lista os tokens como comentários
    token_str = " ".join(tokens)
    codigo.append(f"    ; Expressão: {token_str}")
    codigo.append("")
    
    # Debug: Enviar mensagem inicial
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
    
    # Processa cada token individualmente
    for i, token in enumerate(tokens):
        codigo.append(f"    ; Processando token {i}: '{token}'")
        
        # Verifica o tipo do token
        if _is_number(token):
            # Se é número, empilha na pilha RPN
            if _is_integer(token):
                valor = int(float(token))  # Converte para int se não tem parte decimal
                # Verifica se está dentro do range 16-bit
                if valor > 65535:
                    print(f"Aviso: Valor {valor} excede 16-bit, truncando para {valor & 0xFFFF}")
                    valor = valor & 0xFFFF
                codigo.extend(_gerar_push_int_com_debug(valor))
            else:
                # Para floats, vamos simplificar usando apenas inteiros por enquanto
                valor = int(float(token))
                if valor > 65535:
                    print(f"Aviso: Valor {valor} excede 16-bit, truncando para {valor & 0xFFFF}")
                    valor = valor & 0xFFFF
                codigo.extend(_gerar_push_int_com_debug(valor))
                
        elif token in ['+', '-', '*', '/', '%', '^']:
            # Operações aritméticas
            codigo.extend(_gerar_operacao(token))
            
        elif token == 'MEM':
            # Comando MEM - armazena resultado em variável
            codigo.extend([
                "    rcall comando_mem     ; Comando MEM",
                ""
            ])
            
        elif token == 'RES':
            # Comando RES - recupera variável
            codigo.extend([
                "    rcall comando_res     ; Comando RES", 
                ""
            ])
            
        elif _is_variable_mem(token):
            # Carrega variável de memória
            var_index = ord(token) - ord('A')  # A=0, B=1, etc.
            codigo.extend([
                f"    ldi r17, {var_index}  ; Índice da variável {token}",
                "    rcall load_var        ; Carrega variável",
                ""
            ])
        else:
            codigo.append(f"    ; Token desconhecido: {token}")
            codigo.append("")
    
    codigo.extend([
        "    ; Fim do processamento",
        "    ret",
        "",
    ])


def _gerar_push_int_com_debug(valor):
    """Gera código para empilhar um inteiro com debug - 16-BIT VERSION"""
    # Handle values larger than single digits for debug display
    if valor < 10:
        digit_char = str(valor)
    else:
        digit_char = 'X'  # Use 'X' for multi-digit numbers in debug
    
    return [
        f"    ; Debug: Enviar \"P{valor}\"",
        "    ldi r16, 'P'",
        "    rcall uart_transmit",
        f"    ldi r16, '{digit_char}'",
        "    rcall uart_transmit",
        "    ldi r16, ' '",
        "    rcall uart_transmit",
        "",
        f"    ldi r16, {valor & 0xFF}      ; Byte baixo do valor {valor}",
        f"    ldi r17, {(valor >> 8) & 0xFF} ; Byte alto do valor {valor}",
        "    rcall stack_push_int         ; Empilha valor inteiro 16-bit",
        ""
    ]


def _gerar_push_int(valor):
    """Gera código para empilhar um inteiro (versão sem debug para compatibilidade)"""
    return [
        f"    ldi r16, {valor & 0xFF}      ; Byte baixo do valor {valor}",
        f"    ldi r17, {(valor >> 8) & 0xFF} ; Byte alto do valor {valor}",
        "    rcall stack_push_int         ; Empilha valor inteiro 16-bit",
        ""
    ]


def _gerar_operacao(operador):
    """Gera código para operações aritméticas - 16-BIT VERSION"""
    operacoes = {
        '+': [
            "    ; Debug: Enviar \"ADD\"",
            "    ldi r16, 'A'",
            "    rcall uart_transmit",
            "    ldi r16, 'D'",
            "    rcall uart_transmit",
            "    ldi r16, 'D'",
            "    rcall uart_transmit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "",
            "    ; Debug: Mostrar segundo operando (bytes individuais)",
            "    push r16                 ; Salvar r16",
            "    push r17                 ; Salvar r17",
            "    ldi r16, 'B'             ; Debug: mostrar bytes",
            "    rcall uart_transmit",
            "    ldi r16, ':'",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    push r16                 ; Salvar novamente para debug",
            "    push r17",
            "    mov r16, r17             ; Move high byte para r16", 
            "    rcall send_byte_as_hex   ; Enviar byte alto como hex",
            "    pop r17                  ; Restaurar",
            "    pop r16                  ; Restaurar low byte",
            "    push r16                 ; Salvar novamente",
            "    push r17",
            "    rcall send_byte_as_hex   ; Enviar byte baixo como hex",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar",
            "    pop r16",
            "    push r16                 ; Salvar para debug decimal",
            "    push r17",
            "    rcall send_number_16bit  ; Também mostrar como decimal",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "",
            "    mov r18, r16             ; Salva segundo operando em r18:r19",
            "    mov r19, r17",
            "",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Debug: Mostrar primeiro operando (bytes individuais)",
            "    push r16                 ; Salvar r16",
            "    push r17                 ; Salvar r17",
            "    ldi r16, 'A'             ; Debug: mostrar bytes",
            "    rcall uart_transmit",
            "    ldi r16, ':'",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    push r16                 ; Salvar novamente para debug",
            "    push r17",
            "    mov r16, r17             ; Move high byte para r16", 
            "    rcall send_byte_as_hex   ; Enviar byte alto como hex",
            "    pop r17                  ; Restaurar",
            "    pop r16                  ; Restaurar low byte",
            "    push r16                 ; Salvar novamente",
            "    push r17",
            "    rcall send_byte_as_hex   ; Enviar byte baixo como hex",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar",
            "    pop r16",
            "    push r16                 ; Salvar para debug decimal",
            "    push r17",
            "    rcall send_number_16bit  ; Também mostrar como decimal",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "",
            "    ; TRUE 16-BIT ADDITION",
            "    add r16, r18             ; Add low bytes",
            "    adc r17, r19             ; Add high bytes with carry",
            "",
            "    ; Debug: Mostrar resultado (bytes individuais)",
            "    push r16                 ; Salvar resultado",
            "    push r17",
            "    ldi r16, 'R'             ; Debug: resultado bytes",
            "    rcall uart_transmit",
            "    ldi r16, ':'",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar resultado",
            "    pop r16",
            "    push r16                 ; Salvar novamente",
            "    push r17",
            "    rcall send_byte_as_hex   ; Enviar byte alto como hex",
            "    mov r16, r17             ; Move high byte para r16", 
            "    rcall send_byte_as_hex   ; Enviar byte baixo como hex",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar",
            "    pop r16",
            "    push r16                 ; Salvar para debug decimal",
            "    push r17",
            "    rcall send_number_16bit  ; Mostrar como decimal",
            "    ldi r16, 13",
            "    rcall uart_transmit",
            "    ldi r16, 10",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar resultado",
            "    pop r16",
            "",
            "    rcall stack_push_int     ; Empilha resultado",
            ""
        ],
        '-': [
            "    ; Debug: Enviar \"SUB\"",
            "    ldi r16, 'S'",
            "    rcall uart_transmit",
            "    ldi r16, 'U'",
            "    rcall uart_transmit",
            "    ldi r16, 'B'",
            "    rcall uart_transmit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "",
            "    rcall stack_pop_int      ; Remove segundo operando (b)",
            "    push r16                 ; Salvar r16 antes do debug",
            "    push r17                 ; Salvar r17 antes do debug", 
            "    rcall send_number_16bit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    mov r18, r16             ; Salva b em r18:r19",
            "    mov r19, r17", 
            "    rcall stack_pop_int      ; Remove primeiro operando (a)",
            "    push r16                 ; Salvar r16 antes do debug",
            "    push r17                 ; Salvar r17 antes do debug",
            "    rcall send_number_16bit",
            "    ldi r16, ' '",
            "    rcall uart_transmit", 
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "",
            "    ; TRUE 16-BIT SUBTRACTION", 
            "    sub r16, r18             ; Subtract low bytes",
            "    sbc r17, r19             ; Subtract high bytes with borrow",
            "",
            "    ; Debug: Mostrar resultado da subtração",
            "    push r16                 ; Salvar resultado",
            "    push r17",
            "    rcall send_number_16bit",
            "    ldi r16, 13",
            "    rcall uart_transmit",
            "    ldi r16, 10",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar resultado", 
            "    pop r16",
            "    rcall stack_push_int     ; Empilha resultado",
            ""
        ],
        '*': [
            "    ; Debug: Enviar \"MUL\"",
            "    ldi r16, 'M'",
            "    rcall uart_transmit",
            "    ldi r16, 'U'",
            "    rcall uart_transmit",
            "    ldi r16, 'L'",
            "    rcall uart_transmit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    push r16                 ; Salvar r16 antes do debug",
            "    push r17                 ; Salvar r17 antes do debug",
            "    rcall send_number_16bit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    mov r18, r16             ; Move para r18:r19",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "    push r16                 ; Salvar r16 antes do debug",
            "    push r17                 ; Salvar r17 antes do debug", 
            "    rcall send_number_16bit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    rcall multiply_int       ; TRUE 16-bit multiplication",
            "    push r16                 ; Salvar resultado",
            "    push r17",
            "    rcall send_number_16bit",
            "    ldi r16, 13",
            "    rcall uart_transmit",
            "    ldi r16, 10",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar resultado",
            "    pop r16",
            "    rcall stack_push_int     ; Empilha resultado",
            ""
        ],
        '/': [
            "    ; Debug: Enviar \"DIV\"",
            "    ldi r16, 'D'",
            "    rcall uart_transmit",
            "    ldi r16, 'I'",
            "    rcall uart_transmit",
            "    ldi r16, 'V'",
            "    rcall uart_transmit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "",
            "    rcall stack_pop_int      ; Remove divisor",
            "    push r16                 ; Salvar r16 antes do debug",
            "    push r17                 ; Salvar r17 antes do debug",
            "    rcall send_number_16bit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    mov r18, r16             ; Move divisor para r18:r19",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove dividendo",
            "    push r16                 ; Salvar r16 antes do debug",
            "    push r17                 ; Salvar r17 antes do debug",
            "    rcall send_number_16bit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    rcall divide_int         ; TRUE 16-bit division",
            "    push r16                 ; Salvar resultado",
            "    push r17",
            "    rcall send_number_16bit",
            "    ldi r16, 13",
            "    rcall uart_transmit",
            "    ldi r16, 10",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar resultado",
            "    pop r16",
            "    rcall stack_push_int     ; Empilha quociente",
            ""
        ],
        '%': [
            "    ; Debug: Enviar \"MOD\"",
            "    ldi r16, 'M'",
            "    rcall uart_transmit",
            "    ldi r16, 'O'",
            "    rcall uart_transmit",
            "    ldi r16, 'D'",
            "    rcall uart_transmit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "",
            "    rcall stack_pop_int      ; Remove segundo operando (divisor)",
            "    push r16                 ; Salvar r16 antes do debug",
            "    push r17                 ; Salvar r17 antes do debug", 
            "    rcall send_number_16bit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    mov r18, r16             ; Move divisor para r18:r19",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando (dividendo)",
            "    push r16                 ; Salvar r16 antes do debug",
            "    push r17                 ; Salvar r17 antes do debug",
            "    rcall send_number_16bit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    ; Now r16:r17 = dividendo, r18:r19 = divisor",
            "    ; For RPN \"10 4 %\" we want 10 % 4, so this is correct",
            "    rcall modulo_int         ; TRUE 16-bit modulo",
            "    push r16                 ; Salvar resultado",
            "    push r17",
            "    rcall send_number_16bit",
            "    ldi r16, 13",
            "    rcall uart_transmit",
            "    ldi r16, 10",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar resultado",
            "    pop r16",
            "    rcall stack_push_int     ; Empilha resto",
            ""
        ],
        '^': [
            "    ; Debug: Enviar \"POW\"",
            "    ldi r16, 'P'",
            "    rcall uart_transmit",
            "    ldi r16, 'O'",
            "    rcall uart_transmit",
            "    ldi r16, 'W'",
            "    rcall uart_transmit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "",
            "    rcall stack_pop_int      ; Remove expoente",
            "    push r16                 ; Salvar r16 antes do debug",
            "    push r17                 ; Salvar r17 antes do debug",
            "    rcall send_number_16bit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    mov r18, r16             ; Move expoente para r18:r19",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove base",
            "    push r16                 ; Salvar r16 antes do debug",
            "    push r17                 ; Salvar r17 antes do debug",
            "    rcall send_number_16bit",
            "    ldi r16, ' '",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar r17",
            "    pop r16                  ; Restaurar r16",
            "    rcall power_int          ; TRUE 16-bit power",
            "    push r16                 ; Salvar resultado",
            "    push r17",
            "    rcall send_number_16bit",
            "    ldi r16, 13",
            "    rcall uart_transmit",
            "    ldi r16, 10",
            "    rcall uart_transmit",
            "    pop r17                  ; Restaurar resultado",
            "    pop r16",
            "    rcall stack_push_int     ; Empilha resultado",
            ""
        ]
    }
    return operacoes.get(operador, [f"    ; Operação {operador} não implementada", ""])


def _gerar_rotinas_auxiliares(codigo):
    """Gera rotinas auxiliares para pilha e operações - 16-BIT VERSION"""
    rotinas = [
        "; ====================================================================",
        "; ROTINAS AUXILIARES - TRUE 16-BIT INTEGER SUPPORT",
        "; Suporte completo para inteiros de 0 a 65535",
        "; ====================================================================",
        "",
        "; Inicialização da UART",
        "uart_init:",
        "    ; Set baud rate to 9600",
        "    ldi r16, 0",
        "    sts UBRR0H, r16",
        "    ldi r16, BAUD_9600",
        "    sts UBRR0L, r16",
        "    ; Enable transmitter",
        "    ldi r16, (1 << TXEN0)",
        "    sts UCSR0B, r16",
        "    ; Set frame format: 8N1",
        "    ldi r16, ((1 << UCSZ01)|(1 << UCSZ00))",
        "    sts UCSR0C, r16",
        "    ret",
        "",
        "; Inicialização da pilha RPN",
        "stack_init:",
        "    ldi r16, 0",
        "    sts stack_ptr, r16       ; Zera ponteiro da pilha",
        "    ret",
        "",
        "; EMPILHA INTEIRO DE 16 BITS (r16:r17)",
        "; Usa endereçamento direto na SRAM para máxima confiabilidade",
        "stack_push_int:",
        "    push r20",
        "    push r30",
        "    push r31",
        "    ",
        "    ; Get current stack pointer",
        "    lds r20, stack_ptr",
        "    ",
        "    ; Use direct SRAM addressing starting from 0x0200 (safe area)",
        "    ; Each entry is 2 bytes, so address = 0x0200 + (stack_ptr * 2)",
        "    ldi r30, 0x00          ; Base address low byte (0x0200)",
        "    ldi r31, 0x02          ; Base address high byte",
        "    ",
        "    ; Add offset (stack_ptr * 2)",
        "    lsl r20                ; r20 = stack_ptr * 2",
        "    add r30, r20           ; Add to base address",
        "    brcc no_carry_push     ; Branch if no carry",
        "    inc r31                ; Handle carry",
        "no_carry_push:",
        "    ",
        "    ; Store the 16-bit value (little endian)",
        "    st Z+, r16             ; Store low byte and increment Z",
        "    st Z, r17              ; Store high byte",
        "    ",
        "    ; Increment stack pointer",
        "    lds r20, stack_ptr",
        "    inc r20",
        "    sts stack_ptr, r20",
        "    ",
        "    pop r31",
        "    pop r30",
        "    pop r20",
        "    ret",
        "",
        "; DESEMPILHA INTEIRO DE 16 BITS para r16:r17",
        "stack_pop_int:",
        "    push r20",
        "    push r30",
        "    push r31",
        "    ",
        "    ; Decrement stack pointer first",
        "    lds r20, stack_ptr",
        "    dec r20",
        "    sts stack_ptr, r20",
        "    ",
        "    ; Use direct SRAM addressing starting from 0x0200",
        "    ldi r30, 0x00          ; Base address low byte",
        "    ldi r31, 0x02          ; Base address high byte",
        "    ",
        "    ; Add offset (stack_ptr * 2)",
        "    lsl r20                ; r20 = stack_ptr * 2",
        "    add r30, r20           ; Add to base address",
        "    brcc no_carry_pop      ; Branch if no carry",
        "    inc r31                ; Handle carry",
        "no_carry_pop:",
        "    ",
        "    ; Load the 16-bit value (little endian)",
        "    ld r16, Z+             ; Load low byte and increment Z",
        "    ld r17, Z              ; Load high byte",
        "    ",
        "    pop r31",
        "    pop r30",
        "    pop r20",
        "    ret",
        "",
        "; TRUE 16-BIT MULTIPLICATION: (r16:r17) * (r18:r19) -> (r16:r17)",
        "; Implementa multiplicação completa 16x16 usando produtos parciais",
        "; Resultado pode overflow - mantém apenas os 16 bits inferiores",
        "multiply_int:",
        "    push r0",
        "    push r1",
        "    push r20",
        "    push r21",
        "    push r22",
        "    push r23",
        "    ",
        "    ; 16x16 -> 32 bit multiplication using partial products",
        "    ; (AH:AL) * (BH:BL) = AH*BH*65536 + (AH*BL + AL*BH)*256 + AL*BL",
        "    ; r16:r17 = AL:AH (little endian)",
        "    ; r18:r19 = BL:BH (little endian)",
        "    ",
        "    clr r20                ; Clear result accumulator",
        "    clr r21",
        "    clr r22", 
        "    clr r23",
        "    ",
        "    ; AL * BL -> r21:r20",
        "    mul r16, r18           ; AL * BL",
        "    mov r20, r0            ; Store low byte",
        "    mov r21, r1            ; Store high byte",
        "    ",
        "    ; AL * BH -> add to r22:r21",
        "    mul r16, r19           ; AL * BH", 
        "    add r21, r0            ; Add to middle bytes",
        "    adc r22, r1",
        "    ",
        "    ; AH * BL -> add to r22:r21",
        "    mul r17, r18           ; AH * BL",
        "    add r21, r0            ; Add to middle bytes",
        "    adc r22, r1",
        "    ",
        "    ; AH * BH -> add to r23:r22 (but we'll ignore high overflow)",
        "    mul r17, r19           ; AH * BH",
        "    add r22, r0            ; Add to high bytes (ignore carry out)",
        "    ",
        "    ; Store result in r16:r17 (keep only lower 16 bits)",
        "    mov r16, r20           ; Low byte of result",
        "    mov r17, r21           ; High byte of result",
        "    ",
        "    ; Clear multiplication result registers",
        "    clr r0",
        "    clr r1",
        "    ",
        "    pop r23",
        "    pop r22",
        "    pop r21", 
        "    pop r20",
        "    pop r1",
        "    pop r0",
        "    ret",
        "",
        "; TRUE 16-BIT DIVISION: (r16:r17) / (r18:r19) -> quotient in (r16:r17)",
        "; Implementa divisão usando subtração repetida para simplicidade e confiabilidade",
        "divide_int:",
        "    push r20",
        "    push r21",
        "    push r22",
        "    push r23",
        "    ",
        "    ; Check for division by zero",
        "    cp r18, r1             ; Compare divisor with 0",
        "    cpc r19, r1",
        "    breq div_by_zero       ; If divisor is 0, return maximum value",
        "    ",
        "    ; Initialize quotient counter to 0",
        "    clr r22                ; Quotient low byte",
        "    clr r23                ; Quotient high byte", 
        "    ",
        "    ; Save dividend in r20:r21 for comparison",
        "    mov r20, r16",
        "    mov r21, r17",
        "    ",
        "div_subtract_loop:",
        "    ; Compare dividend (r20:r21) with divisor (r18:r19)",
        "    cp r20, r18            ; Compare low bytes",
        "    cpc r21, r19           ; Compare high bytes with carry",
        "    brlo div_done          ; If dividend < divisor, we're done",
        "    ",
        "    ; Subtract divisor from dividend",
        "    sub r20, r18           ; Subtract low bytes",
        "    sbc r21, r19           ; Subtract high bytes with borrow",
        "    ",
        "    ; Increment quotient",
        "    inc r22                ; Increment low byte",
        "    brne div_no_carry      ; If no overflow, continue",
        "    inc r23                ; Handle carry to high byte",
        "    ",
        "div_no_carry:",
        "    ; Continue loop",
        "    rjmp div_subtract_loop",
        "    ",
        "div_by_zero:",
        "    ldi r16, 0xFF          ; Return maximum value on division by zero",
        "    ldi r17, 0xFF",
        "    rjmp div_exit",
        "    ",
        "div_done:",
        "    ; Store quotient in result registers",
        "    mov r16, r22",
        "    mov r17, r23",
        "    ",
        "div_exit:",
        "    pop r23",
        "    pop r22",
        "    pop r21",
        "    pop r20",
        "    ret",
        "",
        "; TRUE 16-BIT MODULO: (r16:r17) % (r18:r19) -> remainder in (r16:r17)",
        "; Implementa operação módulo usando subtração repetida para simplicidade e confiabilidade",
        "modulo_int:",
        "    push r20",
        "    push r21",
        "    ",
        "    ; Check for division by zero",
        "    cp r18, r1             ; Compare divisor with 0",
        "    cpc r19, r1",
        "    breq mod_by_zero       ; If divisor is 0, return dividend unchanged",
        "    ",
        "    ; Simple repeated subtraction approach",
        "    ; Keep subtracting divisor from dividend until dividend < divisor",
        "    ; The result is the remainder",
        "    ",
        "mod_subtract_loop:",
        "    ; Compare dividend (r16:r17) with divisor (r18:r19)",
        "    cp r16, r18            ; Compare low bytes",
        "    cpc r17, r19           ; Compare high bytes with carry",
        "    brlo mod_done          ; If dividend < divisor, we're done",
        "    ",
        "    ; Subtract divisor from dividend",
        "    sub r16, r18           ; Subtract low bytes",
        "    sbc r17, r19           ; Subtract high bytes with borrow",
        "    ",
        "    ; Continue loop",
        "    rjmp mod_subtract_loop",
        "    ",
        "mod_by_zero:",
        "    ; Return dividend unchanged on mod by zero",
        "    ; (r16:r17 already contains dividend)",
        "    ",
        "mod_done:",
        "    pop r21",
        "    pop r20",
        "    ret",
        "",
        "; 16-BIT POWER: (r16:r17) ^ (r18:r19) -> result in (r16:r17)",
        "; Implementa exponenciação com verificação de overflow",
        "power_int:",
        "    push r20",
        "    push r21",
        "    push r22",
        "    push r23",
        "    ",
        "    ; Check for exponent = 0",
        "    cp r18, r1             ; Compare exponent with 0",
        "    cpc r19, r1",
        "    brne pow_not_zero",
        "    ldi r16, 1             ; x^0 = 1",
        "    clr r17",
        "    rjmp pow_done",
        "    ",
        "pow_not_zero:",
        "    ; Check for exponent = 1",
        "    cpi r18, 1",
        "    ldi r20, 0",
        "    cpc r19, r20",
        "    breq pow_done          ; x^1 = x (already in r16:r17)",
        "    ",
        "    ; Save base in r20:r21",
        "    mov r20, r16",
        "    mov r21, r17",
        "    ",
        "    ; Initialize result to base (first multiplication)",
        "    ; r22:r23 = exponent counter",
        "    mov r22, r18",
        "    mov r23, r19", 
        "    dec r22                ; Decrement exponent (already have base)",
        "    sbc r23, r1            ; Handle borrow",
        "    ",
        "pow_loop:",
        "    ; Check if exponent counter is 0",
        "    cp r22, r1",
        "    cpc r23, r1",
        "    breq pow_done",
        "    ",
        "    ; Multiply current result by base",
        "    ; Move base to r18:r19 for multiplication",
        "    mov r18, r20",
        "    mov r19, r21",
        "    rcall multiply_int     ; r16:r17 = r16:r17 * r18:r19",
        "    ",
        "    ; Decrement exponent counter",
        "    dec r22",
        "    sbc r23, r1",
        "    rjmp pow_loop",
        "    ",
        "pow_done:",
        "    pop r23",
        "    pop r22",
        "    pop r21",
        "    pop r20", 
        "    ret",
        "",
        "; Comando MEM - armazena resultado no topo da pilha",
        "comando_mem:",
        "    ; TODO: Implementação para armazenar em variáveis A-Z",
        "    ret",
        "",
        "; Comando RES - recupera valor da memória",
        "comando_res:",
        "    ; TODO: Implementação para recuperar de variáveis A-Z",
        "    ret",
        "",
        "; Carrega variável da memória",
        "load_var:",
        "    ; r17 contém o índice da variável (0-25)",
        "    ; TODO: Implementação para carregar variável A-Z",
        "    ret",
        "",
        "; Envia resultado via UART",
        "send_result:",
        "    ; Debug message",
        "    ldi r16, 'R'",
        "    rcall uart_transmit",
        "    ldi r16, ':'",
        "    rcall uart_transmit",
        "    ldi r16, ' '",
        "    rcall uart_transmit",
        "    ",
        "    rcall stack_pop_int      ; Pega resultado do topo",
        "    ; Converte para ASCII e envia",
        "    rcall send_number_16bit",
        "    ; Envia newline",
        "    ldi r16, 13",
        "    rcall uart_transmit",
        "    ldi r16, 10", 
        "    rcall uart_transmit",
        "    ret",
        "",
        "; CONVERSÃO 16-BIT PARA ASCII: Converte (r16:r17) para string decimal",
        "; Suporte completo para valores de 0 a 65535",
        "send_number_16bit:",
        "    push r18",
        "    push r19",
        "    push r20",
        "    push r21",
        "    push r22",
        "    push r23",
        "    push r30",
        "    push r31",
        "    ",
        "    ; Check for zero",
        "    cp r16, r1",
        "    cpc r17, r1",
        "    brne not_zero_16",
        "    ldi r16, '0'",
        "    rcall uart_transmit",
        "    rjmp send_16_done",
        "    ",
        "not_zero_16:",
        "    ; Use repeated division by 10 to extract digits",
        "    ; Store digits in a buffer and then send in reverse order",
        "    ldi r30, lo8(0x0500)    ; Point to digit buffer in SRAM",
        "    ldi r31, hi8(0x0500)",
        "    clr r22                 ; Digit counter",
        "    ",
        "extract_digits:",
        "    ; Divide by 10: r16:r17 / 10 -> quotient in r16:r17, remainder in r20",
        "    ldi r18, 10",
        "    clr r19",
        "    rcall divide_by_10_16bit    ; Special optimized division by 10",
        "    ",
        "    ; Convert remainder to ASCII and store",
        "    mov r20, r18               ; Remainder is returned in r18",
        "    ldi r21, '0'",
        "    add r20, r21               ; Convert to ASCII",
        "    st Z+, r20                 ; Store digit and increment pointer",
        "    inc r22                    ; Increment digit count",
        "    ",
        "    ; Check if quotient is zero",
        "    cp r16, r1",
        "    cpc r17, r1",
        "    brne extract_digits        ; Continue if not zero",
        "    ",
        "    ; Now send digits in reverse order",
        "    ; Z now points one past the last digit, so decrement first",
        "    ",
        "send_digits:",
        "    dec r30                    ; Move to previous digit",
        "    ld r16, Z                  ; Load digit",
        "    rcall uart_transmit        ; Send it",
        "    dec r22                    ; Decrement counter",
        "    brne send_digits           ; Continue until all sent",
        "    ",
        "send_16_done:",
        "    pop r31",
        "    pop r30",
        "    pop r23",
        "    pop r22",
        "    pop r21",
        "    pop r20",
        "    pop r19",
        "    pop r18",
        "    ret",
        "",
        "; DIVISÃO OTIMIZADA POR 10 para números 16-bit",
        "; Input: r16:r17 = dividend",
        "; Output: r16:r17 = quotient, r18 = remainder",
        "divide_by_10_16bit:",
        "    push r19",
        "    push r20",
        "    push r21",
        "    ",
        "    ; Save original value for remainder calculation",
        "    mov r20, r16",
        "    mov r21, r17",
        "    ",
        "    ; Simple approach: repeated subtraction by 10",
        "    ; This is slower but accurate and simple for embedded systems",
        "    clr r18                    ; Quotient counter",
        "    clr r19",
        "    ",
        "div10_loop:",
        "    ; Check if we can subtract 10",
        "    cpi r16, 10",
        "    cpc r17, r1                ; Compare with zero register",
        "    brlo div10_remainder       ; If < 10, we're done",
        "    ",
        "    ; Subtract 10",
        "    subi r16, 10",
        "    sbci r17, 0",
        "    ",
        "    ; Increment quotient",
        "    inc r18",
        "    brne div10_check_carry",
        "    inc r19                    ; Handle 16-bit quotient overflow",
        "    ",
        "div10_check_carry:",
        "    rjmp div10_loop",
        "    ",
        "div10_remainder:",
        "    ; r18:r19 = quotient, r16 = remainder",
        "    mov r20, r16               ; Save remainder",
        "    mov r16, r18               ; Quotient to r16:r17",
        "    mov r17, r19",
        "    mov r18, r20               ; Remainder to r18",
        "    ",
        "    pop r21",
        "    pop r20",
        "    pop r19",
        "    ret",
        "",
        "; Keep the original send_number for compatibility",
        "send_number:",
        "    rcall send_number_16bit",
        "    ret",
        "",
        "; ENVIA BYTE COMO HEXADECIMAL (r16) - para debug",
        "; Converte um byte para dois dígitos hexadecimais",
        "send_byte_as_hex:",
        "    push r17",
        "    push r18",
        "    ",
        "    ; Salvar byte original",
        "    mov r18, r16",
        "    ",
        "    ; Enviar nibble alto (bits 7-4)",
        "    swap r16                   ; Trocar nibbles",
        "    andi r16, 0x0F            ; Manter apenas nibble baixo",
        "    cpi r16, 10",
        "    brlo hex_digit_0_9_high   ; Se < 10, é dígito 0-9",
        "    subi r16, -55             ; Converter para A-F (10-15 -> 65-70)",
        "    rjmp send_high_nibble",
        "hex_digit_0_9_high:",
        "    subi r16, -48             ; Converter para 0-9 (0-9 -> 48-57)",
        "send_high_nibble:",
        "    rcall uart_transmit",
        "    ",
        "    ; Enviar nibble baixo (bits 3-0)",  
        "    mov r16, r18              ; Restaurar byte original",
        "    andi r16, 0x0F            ; Manter apenas nibble baixo",
        "    cpi r16, 10",
        "    brlo hex_digit_0_9_low    ; Se < 10, é dígito 0-9",
        "    subi r16, -55             ; Converter para A-F",
        "    rjmp send_low_nibble",
        "hex_digit_0_9_low:",
        "    subi r16, -48             ; Converter para 0-9",
        "send_low_nibble:",
        "    rcall uart_transmit",
        "    ",
        "    pop r18",
        "    pop r17",
        "    ret",
        "",
        "; Transmite caractere via UART",
        "uart_transmit:",
        "    push r22",
        "wait_transmit2:",
        "    lds r22, UCSR0A",
        "    sbrs r22, UDRE0",
        "    rjmp wait_transmit2",
        "    sts UDR0, r16",
        "    pop r22",
        "    ret",
        ""
    ]
    codigo.extend(rotinas)


# ====================================================================
# FUNÇÃO DE TESTE - 16-BIT VERSION
# ====================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TESTANDO gerarAssembly() - TRUE 16-BIT VERSION")
    print("Suporte completo para inteiros de 0 a 65535")
    print("=" * 70)
    print()
    
    # Teste com números maiores para demonstrar capacidade 16-bit
    test_cases = [
        (["1000", "2000", "+"], "1000 + 2000 = 3000"),
        (["300", "200", "*"], "300 * 200 = 60000"),  
        (["65000", "100", "/"], "65000 / 100 = 650"),
        (["12345", "678", "+"], "12345 + 678 = 13023"),
        (["255", "256", "*"], "255 * 256 = 65280"),
        (["1000", "7", "^"], "1000 ^ 7 = overflow (mas teste interessante)")
    ]
    
    #for i, (tokens, description) in enumerate(test_cases):
    #    print(f"Teste {i+1}: {description}")
    #    print(f"Expressão RPN: {' '.join(tokens)}")
    #    
    #    codigo_assembly = []
    #    gerarAssembly(tokens, codigo_assembly)
        
        # Salva o arquivo para este teste específico
    #    filename = f"programa_test_{i+1}.S"
    #    save_assembly(codigo_assembly, filename)
    #    print(f"Arquivo gerado: {filename}")
    #    print()
    
    # Gerar o arquivo principal com um teste padrão
    tokens_padrao = ["12", "4", "/", "3", "5", "*", "+"]
    codigo_assembly = []
    gerarAssembly(tokens_padrao, codigo_assembly)
    save_assembly(codigo_assembly, "src/programa.S")
    save_registers_inc("registers.inc")
    
    
    
    
    print("Para testar, compile e carregue qualquer arquivo programa_test_X.S")
    print("Monitore a saída serial em 9600 baud para ver os resultados!")
