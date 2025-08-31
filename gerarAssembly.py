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
        "; Processador de expressões RPN (Reverse Polish Notation)",
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


def _gerar_secao_dados(codigo):
    """Gera a seção de dados (variáveis e constantes)"""
    dados = [
        "; ====================================================================", 
        "; SEÇÃO DE DADOS",
        "; ====================================================================",
        "",
        "; Stack pointer para pilha de floats (simula pilha RPN)",
        "; Usaremos registradores r16-r31 para operações",
        "; Memória SRAM para armazenar resultados e variáveis",
        "",
        ".section .data",
        "stack_ptr: .byte 1        ; Ponteiro da pilha RPN",
        "mem_vars:  .space 26      ; Espaço para 26 variáveis (A-Z)",
        "temp_result: .space 4     ; Resultado temporário (4 bytes para float)",
        "",
        ".section .text",
        ""
    ]
    codigo.extend(dados)


def _gerar_secao_codigo(codigo, tokens):
    """Gera o código principal que processa os tokens RPN"""
    codigo_principal = [
        "; ====================================================================",
        "; SEÇÃO DE CÓDIGO PRINCIPAL", 
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
            # Se é número, empilha na pilha RPN
            if _is_integer(token):
                valor = int(float(token))  # Converte para int se não tem parte decimal
                codigo.extend(_gerar_push_int(valor))
            else:
                # Para floats, vamos simplificar usando apenas inteiros por enquanto :3
                valor = int(float(token))
                codigo.extend(_gerar_push_int(valor))
                
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


def _gerar_push_int(valor):
    """Gera código para empilhar um inteiro"""
    return [
        f"    ldi r16, {valor & 0xFF}      ; Byte baixo do valor {valor}",
        f"    ldi r17, {(valor >> 8) & 0xFF} ; Byte alto do valor {valor}",
        "    rcall stack_push_int         ; Empilha valor inteiro",
        ""
    ]


def _gerar_operacao(operador):
    """Gera código para operações aritméticas"""
    operacoes = {
        '+': [
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; Salva em r18:r19", 
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "    add r16, r18             ; Soma: r16 = r16 + r18",
            "    adc r17, r19             ; Soma com carry",
            "    rcall stack_push_int     ; Empilha resultado",
            ""
        ],
        '-': [
            "    rcall stack_pop_int      ; Remove segundo operando (b)",
            "    mov r18, r16             ; Salva b em r18:r19",
            "    mov r19, r17", 
            "    rcall stack_pop_int      ; Remove primeiro operando (a)",
            "    sub r16, r18             ; Subtração: r16 = a - b",
            "    sbc r17, r19             ; Subtração com borrow",
            "    rcall stack_push_int     ; Empilha resultado",
            ""
        ],
        '*': [
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; Salva em r18",
            "    rcall stack_pop_int      ; Remove primeiro operando", 
            "    rcall multiply_int       ; Multiplicação r16 * r18",
            "    rcall stack_push_int     ; Empilha resultado",
            ""
        ],
        '/': [
            "    rcall stack_pop_int      ; Remove divisor",
            "    mov r18, r16             ; Salva divisor em r18",
            "    rcall stack_pop_int      ; Remove dividendo",
            "    rcall divide_int         ; Divisão r16 / r18",
            "    rcall stack_push_int     ; Empilha quociente",
            ""
        ],
        '%': [
            "    rcall stack_pop_int      ; Remove divisor", 
            "    mov r18, r16             ; Salva divisor em r18",
            "    rcall stack_pop_int      ; Remove dividendo",
            "    rcall modulo_int         ; Resto r16 % r18",
            "    rcall stack_push_int     ; Empilha resto",
            ""
        ],
        '^': [
            "    rcall stack_pop_int      ; Remove expoente",
            "    mov r18, r16             ; Salva expoente em r18",
            "    rcall stack_pop_int      ; Remove base",
            "    rcall power_int          ; Potência r16 ^ r18",
            "    rcall stack_push_int     ; Empilha resultado",
            ""
        ]
    }
    return operacoes.get(operador, [f"    ; Operação {operador} não implementada", ""])


def _gerar_rotinas_auxiliares(codigo):
    """Gera rotinas auxiliares para pilha e operações"""
    rotinas = [
        "; ====================================================================",
        "; ROTINAS AUXILIARES",
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
        "; Empilha inteiro de 16 bits (r16:r17)",
        "stack_push_int:",
        "    push r20",
        "    push r21",
        "    lds r20, stack_ptr       ; Carrega ponteiro atual",
        "    ; Calcula endereço na SRAM (RAMSTART + stack_ptr * 2)",
        "    ldi r21, 2",
        "    mul r20, r21             ; stack_ptr * 2",
        "    ldi r20, lo8(RAMSTART)",
        "    add r0, r20              ; Adiciona base da RAM",
        "    ldi r20, hi8(RAMSTART)",
        "    adc r1, r20",
        "    ; Salva o valor na memória",
        "    movw r30, r0             ; Z = endereço calculado",
        "    st Z+, r16               ; Salva byte baixo",
        "    st Z, r17                ; Salva byte alto",
        "    ; Incrementa ponteiro da pilha",
        "    lds r20, stack_ptr",
        "    inc r20",
        "    sts stack_ptr, r20",
        "    pop r21",
        "    pop r20",
        "    ret",
        "",
        "; Desempilha inteiro de 16 bits para r16:r17",
        "stack_pop_int:",
        "    push r20",
        "    push r21",
        "    lds r20, stack_ptr       ; Carrega ponteiro atual",
        "    dec r20                  ; Decrementa ponteiro",
        "    sts stack_ptr, r20",
        "    ; Calcula endereço na SRAM",
        "    ldi r21, 2",
        "    mul r20, r21",
        "    ldi r20, lo8(RAMSTART)",
        "    add r0, r20",
        "    ldi r20, hi8(RAMSTART)", 
        "    adc r1, r20",
        "    ; Carrega valor da memória",
        "    movw r30, r0",
        "    ld r16, Z+               ; Carrega byte baixo",
        "    ld r17, Z                ; Carrega byte alto",
        "    pop r21",
        "    pop r20",
        "    ret",
        "",
        "; Multiplicação simples de 8 bits (r16 * r18 -> r16)",
        "multiply_int:",
        "    mul r16, r18             ; Multiplica (resultado em r1:r0)",
        "    mov r16, r0              ; Move resultado para r16",
        "    mov r17, r1              ; Move parte alta para r17",
        "    clr r1                   ; Limpa r1 (usado por mul)",
        "    ret",
        "",
        "; Divisão simples de 8 bits (r16 / r18 -> r16)",
        "divide_int:",
        "    clr r17                  ; Contador do quociente",
        "    cp r16, r18              ; Compara dividendo com divisor",
        "    brlo div_done            ; Se menor, quociente = 0",
        "div_loop:",
        "    sub r16, r18             ; Subtrai divisor",
        "    inc r17                  ; Incrementa quociente",
        "    cp r16, r18              ; Ainda pode dividir?",
        "    brsh div_loop            ; Se sim, continua",
        "div_done:",
        "    mov r16, r17             ; Resultado em r16",
        "    clr r17                  ; Limpa r17",
        "    ret",
        "",
        "; Módulo simples (r16 % r18 -> r16)",  
        "modulo_int:",
        "    cp r16, r18",
        "    brlo mod_done            ; Se dividendo < divisor, resto = dividendo",
        "mod_loop:",
        "    sub r16, r18",
        "    cp r16, r18",
        "    brsh mod_loop",
        "mod_done:",
        "    ret",
        "",
        "; Potência simples (r16 ^ r18 -> r16)",
        "power_int:",
        "    cpi r18, 0               ; Expoente = 0?",
        "    brne pow_start",
        "    ldi r16, 1               ; x^0 = 1",
        "    ret",
        "pow_start:",
        "    mov r19, r16             ; Salva base",
        "    dec r18                  ; Decrementa expoente",
        "    cpi r18, 0",
        "    breq pow_done",
        "pow_loop:",
        "    mul r16, r19             ; Multiplica pela base",
        "    mov r16, r0",
        "    dec r18",
        "    brne pow_loop",
        "pow_done:",
        "    clr r1",
        "    ret",
        "",
        "; Comando MEM - armazena resultado no topo da pilha",
        "comando_mem:",
        "    ; Implementação simplificada",
        "    ret",
        "",
        "; Comando RES - recupera valor da memória",
        "comando_res:",
        "    ; Implementação simplificada",
        "    ret",
        "",
        "; Carrega variável da memória",
        "load_var:",
        "    ; r17 contém o índice da variável (0-25)",
        "    ; Implementação simplificada",
        "    ret",
        "",
        "; Envia resultado via UART",
        "send_result:",
        "    rcall stack_pop_int      ; Pega resultado do topo",
        "    ; Converte para ASCII e envia",
        "    rcall send_number",
        "    ; Envia newline",
        "    ldi r16, 13",
        "    rcall uart_transmit",
        "    ldi r16, 10", 
        "    rcall uart_transmit",
        "    ret",
        "",
        "; Envia número via UART (conversão para ASCII)",
        "send_number:",
        "    ; Implementação similar ao main.S original",
        "    clr r21                  ; Contador de dezenas",
        "    mov r19, r16             ; Copia resultado",
        "    ldi r20, 10",
        "divide_loop2:",
        "    cp r19, r20",
        "    brlo send_tens2",
        "    sub r19, r20",
        "    inc r21",
        "    rjmp divide_loop2",
        "send_tens2:",
        "    cpi r21, 0",
        "    breq send_ones2",
        "    mov r16, r21",
        "    subi r16, -48            ; Converte para ASCII",
        "    rcall uart_transmit",
        "send_ones2:",
        "    mov r16, r19",
        "    subi r16, -48",
        "    rcall uart_transmit",
        "    ret",
        "",
        "; Transmite caractere via UART",
        "uart_transmit:",
        "wait_transmit2:",
        "    lds r22, UCSR0A",
        "    sbrs r22, UDRE0",
        "    rjmp wait_transmit2",
        "    sts UDR0, r16",
        "    ret",
        ""
    ]
    codigo.extend(rotinas)


def _gerar_footer_assembly(codigo):
    """Gera código de finalização"""
    footer = [
        "; ====================================================================",
        "; FINALIZAÇÃO",
        "; ====================================================================",
        "",
        "end_program:",
        "    rjmp end_program         ; Loop infinito",
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
        print(f"Código Assembly salvo em: {nome_arquivo}")
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return False


# Função de teste
if __name__ == "__main__":
    # Teste básico com tokens simples
    tokens_teste = ["6", "2", "+"]  # 6 + 2 = 8 
    codigo_assembly = []
    
    print("Testando gerarAssembly()...")
    print(f"Expressão RPN: {' '.join(tokens_teste)} (resultado esperado: 8)")
    
    gerarAssembly(tokens_teste, codigo_assembly)
    
    # Salva o arquivo
    save_assembly(codigo_assembly, "programa.S")
    
