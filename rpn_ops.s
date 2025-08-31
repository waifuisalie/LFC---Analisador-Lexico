; rpn_ops.s - VERSÃO COMPLETA
; Operações RPN 16-bit para ATmega328P (Arduino Uno)
; Suporta inteiros e decimais com 2 casas (ponto fixo)
; Formato decimal: valor * 100 (ex: 12.34 = 1234)

.include "src/registers.inc"

; -------------------------------------------------------------------
; Constantes
; -------------------------------------------------------------------
.equ SCALE_FACTOR, 100          ; Fator de escala para 2 casas decimais
.equ MAX_STACK_SIZE, 16         ; Tamanho máximo da pilha

; -------------------------------------------------------------------
; Dados: pilha de 16-bit em SRAM
; -------------------------------------------------------------------
    .section .data
stack_ptr:    .byte 1          ; número de elementos na pilha (0..MAX_STACK_SIZE)
rpn_stack:    .byte 32         ; espaço para 16 valores de 16-bit (16*2 = 32 bytes)
mode_flag:    .byte 1          ; 0 = modo inteiro, 1 = modo decimal

    .section .text
    .global stack_push_int
    .global stack_pop_int
    .global set_integer_mode
    .global set_decimal_mode
    .global rpn_add_16
    .global rpn_sub_16
    .global rpn_mul_16
    .global rpn_div_16
    .global rpn_div_int_16
    .global rpn_mod_16
    .global rpn_pow_16
    .global convert_to_fixed
    .global print_fixed_decimal

; -------------------------------------------------------------------
; Funções de modo
; -------------------------------------------------------------------
set_integer_mode:
    ldi r16, 0
    sts mode_flag, r16
    ret

set_decimal_mode:
    ldi r16, 1
    sts mode_flag, r16
    ret

; -------------------------------------------------------------------
; stack_push_int
; Entrada: r16 = low, r17 = high
; Ação : salva r16:r17 na pilha (rpn_stack), incrementa stack_ptr
; -------------------------------------------------------------------
stack_push_int:
    push r18
    push r19
    push r20
    push r21

    lds r20, stack_ptr      ; r20 = index (n)
    cpi r20, MAX_STACK_SIZE
    brsh .push_overflow     ; Se pilha cheia, não faz nada

    mov r21, r20
    lsl r21                 ; r21 = n * 2  (offset em bytes)
    clr r18                 ; r18 = 0 (para adc)

    ldi r30, lo8(rpn_stack) ; Z = base
    ldi r31, hi8(rpn_stack)
    add r30, r21
    adc r31, r18            ; Z = base + offset

    st Z, r16               ; store low byte
    adiw r30, 1
    st Z, r17               ; store high byte

    inc r20
    sts stack_ptr, r20

.push_overflow:
    pop r21
    pop r20
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; stack_pop_int
; Saída: r16 = low, r17 = high
; Ação : decrementa stack_ptr e lê topo da pilha em r16:r17
; -------------------------------------------------------------------
stack_pop_int:
    push r18
    push r19
    push r20
    push r21

    lds r20, stack_ptr
    tst r20
    breq .pop_underflow     ; Se pilha vazia, retorna 0

    dec r20
    sts stack_ptr, r20     ; atualiza novo topo

    mov r21, r20
    lsl r21                ; r21 = index * 2
    clr r18

    ldi r30, lo8(rpn_stack)
    ldi r31, hi8(rpn_stack)
    add r30, r21
    adc r31, r18           ; Z = base + offset

    ld r16, Z              ; low
    adiw r30, 1
    ld r17, Z              ; high
    rjmp .pop_done

.pop_underflow:
    clr r16
    clr r17

.pop_done:
    pop r21
    pop r20
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; rpn_add_16: soma A + B (funciona para inteiros e decimais)
; -------------------------------------------------------------------
rpn_add_16:
    push r18
    push r19

    rcall stack_pop_int    ; B -> r16:r17
    mov r18, r16
    mov r19, r17

    rcall stack_pop_int    ; A -> r16:r17
    add r16, r18
    adc r17, r19

    rcall stack_push_int
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; rpn_sub_16: subtração A - B (funciona para inteiros e decimais)
; -------------------------------------------------------------------
rpn_sub_16:
    push r18
    push r19

    rcall stack_pop_int    ; B -> r16:r17
    mov r18, r16
    mov r19, r17

    rcall stack_pop_int    ; A -> r16:r17
    sub r16, r18
    sbc r17, r19

    rcall stack_push_int
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; rpn_mul_16: multiplicação A * B
; - Para inteiros: resultado direto
; - Para decimais: divide por 100 ao final (corrige escala)
; -------------------------------------------------------------------
rpn_mul_16:
    ; Preserve temporaries
    push r18
    push r19
    push r24
    push r25
    push r26
    push r27

    ; B <- topo
    rcall stack_pop_int        ; B in r16:r17
    mov r18, r16              ; B low -> r18
    mov r19, r17              ; B high -> r19

    ; A <- next
    rcall stack_pop_int        ; A in r16:r17

    ; Multiplicação 16x16 -> 32 bits
    clr r24
    clr r25
    clr r26
    clr r27

    ; p0 = A_low * B_low
    mul r16, r18              ; r1:r0 = p0
    mov r24, r0               ; low byte
    mov r25, r1               ; next byte
    clr r1

    ; p1 = A_low * B_high  -> add to r25:r26 shifted by 8
    mul r16, r19
    add r25, r0
    adc r26, r1
    clr r1

    ; p2 = A_high * B_low  -> add to r25:r26 shifted
    mul r17, r18
    add r25, r0
    adc r26, r1
    clr r1

    ; p3 = A_high * B_high -> add to r26:r27 shifted
    mul r17, r19
    add r26, r0
    adc r27, r1
    clr r1

    ; Resultado (low 16 bits) -> r24 (low), r25 (high)
    mov r16, r24
    mov r17, r25

    ; Verificar se está em modo decimal
    lds r18, mode_flag
    tst r18
    breq .mul_push_result   ; Modo inteiro - resultado direto

    ; Modo decimal - dividir por 100
    rcall stack_push_int    ; Push resultado temporário
    
    ldi r16, 100
    clr r17
    rcall stack_push_int    ; Push 100
    
    rcall rpn_div_int_16    ; Dividir por 100
    rcall stack_pop_int     ; Obter resultado corrigido
    rjmp .mul_end

.mul_push_result:
    rcall stack_push_int

.mul_end:
    pop r27
    pop r26
    pop r25
    pop r24
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; rpn_div_16: divisão real (para decimais) A / B
; - Para modo decimal: multiplica A por 100 antes de dividir
; - Para modo inteiro: chama rpn_div_int_16
; -------------------------------------------------------------------
rpn_div_16:
    push r18
    
    ; Verificar modo
    lds r18, mode_flag
    tst r18
    breq .div_integer_mode  ; Modo inteiro
    
    ; Modo decimal - divisão real
    ; B <- topo
    rcall stack_pop_int    ; B -> r16:r17
    mov r18, r16          ; B low
    mov r19, r17          ; B high
    
    ; A <- next
    rcall stack_pop_int    ; A -> r16:r17
    
    ; Multiplicar A por 100 primeiro
    rcall stack_push_int   ; Push A
    ldi r16, 100
    clr r17
    rcall stack_push_int   ; Push 100
    
    push r18               ; Salvar B
    push r19
    rcall rpn_mul_16       ; A = A * 100 (mas sem correção de escala)
    
    ; Forçar modo inteiro temporariamente para esta multiplicação
    ldi r20, 0
    sts mode_flag, r20
    rcall stack_pop_int    ; Obter A*100
    ldi r20, 1
    sts mode_flag, r20     ; Restaurar modo decimal
    
    rcall stack_push_int   ; Push A*100
    
    pop r19                ; Restaurar B
    pop r18
    mov r16, r18
    mov r17, r19
    rcall stack_push_int   ; Push B
    
    rcall rpn_div_int_16   ; Dividir (A*100)/B
    rjmp .div_end

.div_integer_mode:
    rcall rpn_div_int_16   ; Divisão inteira normal

.div_end:
    pop r18
    ret

; -------------------------------------------------------------------
; rpn_div_int_16: divisão inteira unsigned A / B -> quociente 16-bit
; - Usado internamente e para modo inteiro
; -------------------------------------------------------------------
rpn_div_int_16:
    push r18
    push r19
    push r20
    push r21
    push r22
    push r23

    ; B <- topo
    rcall stack_pop_int    ; B -> r16:r17
    mov r18, r16          ; B low
    mov r19, r17          ; B high

    ; A <- next
    rcall stack_pop_int    ; A -> r16:r17 (dividend)
    mov r24, r16          ; remainder low <-- dividend
    mov r25, r17          ; remainder high

    ; check B == 0
    tst r18
    brne .divi_b_nonzero
    tst r19
    brne .divi_b_nonzero
    ; B == 0 -> error: push 0
    clr r16
    clr r17
    rcall stack_push_int
    rjmp .divi_end

.divi_b_nonzero:
    clr r20   ; quotient low
    clr r21   ; quotient high

.divi_loop:
    ; compare remainder >= B  (16-bit unsigned compare)
    cp r24, r18      ; compare low bytes
    cpc r25, r19     ; compare high bytes with carry
    brlo .divi_done  ; remainder < B -> done

    ; remainder -= B
    sub r24, r18
    sbc r25, r19

    ; quotient++
    inc r20
    brne .divi_loop_cont
    inc r21
.divi_loop_cont:
    rjmp .divi_loop

.divi_done:
    mov r16, r20
    mov r17, r21
    rcall stack_push_int

.divi_end:
    pop r23
    pop r22
    pop r21
    pop r20
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; rpn_mod_16: resto A % B (apenas para inteiros)
; -------------------------------------------------------------------
rpn_mod_16:
    push r18
    push r19
    push r20
    push r21

    rcall stack_pop_int    ; B
    mov r18, r16
    mov r19, r17

    rcall stack_pop_int    ; A (dividend)
    mov r20, r16          ; remainder = A
    mov r21, r17

    ; B==0 => push 0
    tst r18
    brne .mod_b_nonzero
    tst r19
    brne .mod_b_nonzero
    clr r16
    clr r17
    rcall stack_push_int
    rjmp .mod_end

.mod_b_nonzero:
.mod_loop:
    cp r20, r18
    cpc r21, r19
    brlo .mod_done
    sub r20, r18
    sbc r21, r19
    rjmp .mod_loop

.mod_done:
    mov r16, r20
    mov r17, r21
    rcall stack_push_int

.mod_end:
    pop r21
    pop r20
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; rpn_pow_16: potência A^B (B inteiro >= 0)
; - Funciona para inteiros e decimais
; - Algoritmo: multiplicação repetida otimizada
; -------------------------------------------------------------------
rpn_pow_16:
    push r18
    push r19
    push r20
    push r21
    push r22
    push r23

    rcall stack_pop_int    ; B (expoente)
    mov r18, r16          ; exp low
    mov r19, r17          ; exp high

    rcall stack_pop_int    ; A (base)
    mov r20, r16          ; base low
    mov r21, r17          ; base high

    ; Se expoente > 255, retorna 0 (overflow)
    tst r19
    brne .pow_overflow

    ; Se expoente == 0 -> retorna 1 (ou 100 se decimal)
    tst r18
    breq .pow_return_one

    ; Se base == 0 -> retorna 0
    tst r20
    brne .pow_base_nonzero
    tst r21
    brne .pow_base_nonzero
    clr r16
    clr r17
    rcall stack_push_int
    rjmp .pow_end

.pow_base_nonzero:
    ; Verificar se base == 1 (ou 100 em modo decimal)
    lds r19, mode_flag
    tst r19
    breq .pow_check_int_one   ; Modo inteiro

    ; Modo decimal - verificar se base == 100 (representa 1.00)
    cpi r20, 100
    brne .pow_compute
    tst r21
    brne .pow_compute
    rjmp .pow_return_one

.pow_check_int_one:
    ; Modo inteiro - verificar se base == 1
    cpi r20, 1
    brne .pow_compute
    tst r21
    brne .pow_compute
    rjmp .pow_return_one

.pow_compute:
    ; Inicializar resultado = base
    mov r22, r20          ; resultado = base  
    mov r23, r21
    dec r18               ; exp = exp - 1

.pow_loop:
    tst r18
    breq .pow_done
    
    ; resultado = resultado * base
    ; Push resultado atual
    mov r16, r22
    mov r17, r23
    rcall stack_push_int
    
    ; Push base
    mov r16, r20
    mov r17, r21
    rcall stack_push_int
    
    ; Multiplicar
    rcall rpn_mul_16
    
    ; Obter novo resultado
    rcall stack_pop_int
    mov r22, r16
    mov r23, r17
    
    dec r18
    rjmp .pow_loop

.pow_done:
    mov r16, r22
    mov r17, r23
    rcall stack_push_int
    rjmp .pow_end

.pow_return_one:
    ; Retorna 1 (inteiro) ou 100 (decimal = 1.00)
    lds r19, mode_flag
    tst r19
    breq .pow_one_integer
    
    ; Modo decimal - retorna 100 (1.00)
    ldi r16, 100
    clr r17
    rcall stack_push_int
    rjmp .pow_end

.pow_one_integer:
    ; Modo inteiro - retorna 1
    ldi r16, 1
    clr r17
    rcall stack_push_int
    rjmp .pow_end

.pow_overflow:
    ; Retorna 0 para indicar overflow
    clr r16
    clr r17
    rcall stack_push_int

.pow_end:
    pop r23
    pop r22
    pop r21
    pop r20
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; convert_to_fixed: Converte decimal para ponto fixo
; Entrada: r16 = parte inteira, r17 = parte decimal (0-99)
; Saída: r16:r17 = valor em ponto fixo (* 100)
; Exemplo: convert_to_fixed(12, 34) -> 1234 (representa 12.34)
; -------------------------------------------------------------------
convert_to_fixed:
    push r18
    push r19
    push r20
    
    ; Salvar parte decimal
    mov r18, r17
    
    ; Multiplicar parte inteira por 100
    clr r17           ; r16:r17 = parte inteira (high = 0)
    
    ; Multiplicação r16 * 100 usando shifts e adds
    ; 100 = 64 + 32 + 4 = 2^6 + 2^5 + 2^2
    mov r19, r16      ; Backup original
    mov r20, r16      ; Para shifts
    
    ; r16 * 64
    lsl r20
    lsl r20
    lsl r20
    lsl r20
    lsl r20
    lsl r20           ; r20 = r16 * 64
    
    mov r16, r20      ; resultado = r16 * 64
    
    ; + r16 * 32
    mov r20, r19
    lsl r20
    lsl r20
    lsl r20
    lsl r20
    lsl r20           ; r20 = r16 * 32
    add r16, r20
    
    ; + r16 * 4  
    mov r20, r19
    lsl r20
    lsl r20           ; r20 = r16 * 4
    add r16, r20
    
    ; Adicionar parte decimal
    add r16, r18      ; adicionar centavos
    adc r17, r19      ; r19 deve ser 0 se não houve overflow
    
    pop r20
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; print_fixed_decimal: Imprime número de ponto fixo como decimal
; Entrada: r16:r17 = número em ponto fixo
; Requer: uart_transmit e print_decimal definidas externamente
; -------------------------------------------------------------------
print_fixed_decimal:
    push r18
    push r19
    push r20
    push r21
    push r22
    
    mov r20, r16      ; Backup valor original
    mov r21, r17
    
    ; Verificar se é negativo (16-bit signed)
    tst r17
    brpl .fpd_positive
    
    ; É negativo - imprimir '-' e converter para positivo
    ldi r18, '-'
    mov r16, r18
    rcall uart_transmit
    
    ; Converter para positivo (complemento de 2)
    com r20
    com r21
    adiw r20, 1
    
.fpd_positive:
    ; Dividir por 100 para obter parte inteira
    mov r16, r20
    mov r17, r21
    rcall stack_push_int
    
    ldi r16, 100
    clr r17
    rcall stack_push_int
    
    rcall rpn_div_int_16
    rcall stack_pop_int      ; r16:r17 = parte inteira
    
    ; Imprimir parte inteira
    rcall print_decimal
    
    ; Imprimir ponto decimal
    ldi r18, '.'
    mov r16, r18
    rcall uart_transmit
    
    ; Calcular resto (parte decimal) = valor % 100
    mov r16, r20
    mov r17, r21
    rcall stack_push_int
    
    ldi r16, 100
    clr r17
    rcall stack_push_int
    
    rcall rpn_mod_16
    rcall stack_pop_int      ; r16:r17 = parte decimal (0-99)
    
    ; Imprimir parte decimal sempre com 2 dígitos
    cpi r16, 10
    brsh .fpd_print_decimal
    
    ; < 10: imprimir '0' primeiro
    ldi r18, '0'
    mov r22, r16          ; Backup
    mov r16, r18
    rcall uart_transmit
    mov r16, r22          ; Restaurar
    
.fpd_print_decimal:
    rcall print_decimal
    
    pop r22
    pop r21
    pop r20
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; Funções auxiliares para conversão de entrada
; -------------------------------------------------------------------

; -------------------------------------------------------------------
; parse_decimal_input: Converte string "12.34" para ponto fixo
; Entrada: Z aponta para string na SRAM
; Saída: r16:r17 = valor em ponto fixo
; -------------------------------------------------------------------
parse_decimal_input:
    push r18
    push r19
    push r20
    push r21
    
    clr r18           ; parte inteira
    clr r19           ; parte decimal
    clr r20           ; contador decimal
    
.parse_integer_part:
    ld r21, Z+
    
    ; Verificar fim da string
    tst r21
    breq .parse_done
    
    ; Verificar ponto decimal
    cpi r21, '.'
    breq .parse_decimal_part
    
    ; Verificar se é dígito
    cpi r21, '0'
    brlo .parse_error
    cpi r21, '9'+1
    brsh .parse_error
    
    ; Converter para número e acumular
    subi r21, '0'
    
    ; r18 = r18 * 10 + dígito
    mov r16, r18
    lsl r18           ; *2
    lsl r18           ; *4
    add r18, r16      ; *5
    lsl r18           ; *10
    add r18, r21      ; + dígito
    
    rjmp .parse_integer_part

.parse_decimal_part:
    ld r21, Z+
    
    ; Verificar fim
    tst r21
    breq .parse_done
    
    ; Verificar se é dígito
    cpi r21, '0'
    brlo .parse_done
    cpi r21, '9'+1
    brsh .parse_done
    
    ; Só aceita até 2 casas decimais
    cpi r20, 2
    brsh .parse_done
    
    subi r21, '0'
    
    ; Adicionar à parte decimal
    cpi r20, 0
    breq .parse_first_decimal
    
    ; Segunda casa decimal
    add r19, r21
    rjmp .parse_decimal_continue
    
.parse_first_decimal:
    ; Primeira casa decimal (dezenas)
    mov r16, r21
    lsl r21           ; *2
    lsl r21           ; *4  
    add r21, r16      ; *5
    lsl r21           ; *10
    mov r19, r21

.parse_decimal_continue:
    inc r20
    rjmp .parse_decimal_part

.parse_done:
    ; Converter para ponto fixo
    mov r16, r18      ; parte inteira
    mov r17, r19      ; parte decimal
    rcall convert_to_fixed
    rjmp .parse_end

.parse_error:
    clr r16
    clr r17

.parse_end:
    pop r21
    pop r20
    pop r19
    pop r18
    ret

; -------------------------------------------------------------------
; Usage examples:
; -------------------------------------------------------------------
; Para calcular 12.34 + 5.67 em modo decimal:
;
; rcall set_decimal_mode
;
; ; Push 12.34 (converte para 1234)
; ldi r16, 12
; ldi r17, 34
; rcall convert_to_fixed
; rcall stack_push_int
;
; ; Push 5.67 (converte para 567)  
; ldi r16, 5
; ldi r17, 67
; rcall convert_to_fixed
; rcall stack_push_int
;
; ; Somar
; rcall rpn_add_16
;
; ; Imprimir resultado
; rcall stack_pop_int
; rcall print_fixed_decimal    ; Mostra "18.01"
;
; -------------------------------------------------------------------