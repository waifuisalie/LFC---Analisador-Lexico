; ====================================================================
; Código Assembly gerado automaticamente para Arduino Uno (ATmega328p)
; Processador RPN - 16-BIT VERSION
; Suporte para inteiros de 0 a 65535
; Compilado com PlatformIO/AVR-GCC
; ====================================================================

#include "registers.inc"
.global main

.section .text

; ====================================================================
; SEÇÃO DE DADOS - 16-BIT VERSION
; ====================================================================

.section .data
stack_ptr: .byte 1        ; Ponteiro da pilha RPN
mem_vars:  .space 52      ; 26 variáveis 16-bit (A-Z)
temp_result: .space 4     ; Resultado temporário

.section .text

; ====================================================================
; SEÇÃO DE CÓDIGO PRINCIPAL - MÚLTIPLAS OPERAÇÕES RPN - 16-BIT VERSION
; ====================================================================

main:
    ; Inicializar stack pointer
    ldi r16, 0xFF
    out SPL, r16
    ldi r16, 0x08
    out SPH, r16

    ; Inicializar UART (9600 baud) e pilha RPN
    rcall uart_init
    rcall stack_init

    ; Processar todas as operações RPN sequencialmente
    ; Operação 1
    rcall processar_rpn_op1
    rcall send_result

    ; Operação 2
    rcall processar_rpn_op2
    rcall send_result

    ; Operação 3
    rcall processar_rpn_op3
    rcall send_result

    ; Operação 4
    rcall processar_rpn_op4
    rcall send_result

    ; Operação 5
    rcall processar_rpn_op5
    rcall send_result

    ; Operação 6
    rcall processar_rpn_op6
    rcall send_result

    ; Operação 7
    rcall processar_rpn_op7
    rcall send_result

    ; Operação 8
    rcall processar_rpn_op8
    rcall send_result

    ; Operação 9
    rcall processar_rpn_op9
    rcall send_result

    ; Operação 10
    rcall processar_rpn_op10
    rcall send_result

    ; Loop infinito
    rjmp end_program

; ====================================================================
; PROCESSAMENTO OPERAÇÃO 1 - 16-BIT VERSION
; ====================================================================

processar_rpn_op1:
    ; Processando operação 1 com suporte 16-bit:
    ; Expressão: 3.0 2.0 +

    ; Cabeçalho da operação 1
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, 'P'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'C'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '1'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Mostrar expressão
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'x'
    rcall uart_transmit
    ldi r16, 'p'
    rcall uart_transmit
    ldi r16, 'r'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ldi r16, '3'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '2'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '+'
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Processando token 0: '3.0'
    ; Push 3 para a pilha
    ldi r16, 3      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 1: '2.0'
    ; Push 2 para a pilha
    ldi r16, 2      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 2: '+'
    ; Operação de soma
    rcall stack_pop_int      ; Remove segundo operando
    mov r18, r16             ; guarda segundo operando
    mov r19, r17
    rcall stack_pop_int      ; Remove primeiro operando

    ; Soma 16-bit
    add r16, r18
    adc r17, r19

    rcall stack_push_int

    ; Mostrar resultado
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'u'
    rcall uart_transmit
    ldi r16, 'l'
    rcall uart_transmit
    ldi r16, 't'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'd'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ; Fim do processamento da operação
    ret

; ====================================================================
; PROCESSAMENTO OPERAÇÃO 2 - 16-BIT VERSION
; ====================================================================

processar_rpn_op2:
    ; Processando operação 2 com suporte 16-bit:
    ; Expressão: 10.0 4.0 -

    ; Cabeçalho da operação 2
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, 'P'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'C'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '2'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Mostrar expressão
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'x'
    rcall uart_transmit
    ldi r16, 'p'
    rcall uart_transmit
    ldi r16, 'r'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ldi r16, '1'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '4'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '-'
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Processando token 0: '10.0'
    ; Push 10 para a pilha
    ldi r16, 10      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 1: '4.0'
    ; Push 4 para a pilha
    ldi r16, 4      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 2: '-'
    ; Operação de subtração
    rcall stack_pop_int      ; Remove segundo operando
    mov r18, r16             ; guarda segundo operando
    mov r19, r17
    rcall stack_pop_int      ; Remove primeiro operando

    ; Subtração 16-bit
    sub r16, r18
    sbc r17, r19

    rcall stack_push_int

    ; Mostrar resultado
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'u'
    rcall uart_transmit
    ldi r16, 'l'
    rcall uart_transmit
    ldi r16, 't'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'd'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ; Fim do processamento da operação
    ret

; ====================================================================
; PROCESSAMENTO OPERAÇÃO 3 - 16-BIT VERSION
; ====================================================================

processar_rpn_op3:
    ; Processando operação 3 com suporte 16-bit:
    ; Expressão: 2.0 3.0 *

    ; Cabeçalho da operação 3
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, 'P'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'C'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '3'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Mostrar expressão
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'x'
    rcall uart_transmit
    ldi r16, 'p'
    rcall uart_transmit
    ldi r16, 'r'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ldi r16, '2'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '3'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '*'
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Processando token 0: '2.0'
    ; Push 2 para a pilha
    ldi r16, 2      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 1: '3.0'
    ; Push 3 para a pilha
    ldi r16, 3      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 2: '*'
    ; Operação de multiplicação
    rcall stack_pop_int      ; Remove segundo operando
    mov r18, r16             ; guarda segundo operando
    mov r19, r17
    rcall stack_pop_int      ; Remove primeiro operando

    ; Multiplicação 16-bit
    rcall multiply_int

    rcall stack_push_int

    ; Mostrar resultado
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'u'
    rcall uart_transmit
    ldi r16, 'l'
    rcall uart_transmit
    ldi r16, 't'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'd'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ; Fim do processamento da operação
    ret

; ====================================================================
; PROCESSAMENTO OPERAÇÃO 4 - 16-BIT VERSION
; ====================================================================

processar_rpn_op4:
    ; Processando operação 4 com suporte 16-bit:
    ; Expressão: 9.0 2.0 /

    ; Cabeçalho da operação 4
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, 'P'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'C'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '4'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Mostrar expressão
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'x'
    rcall uart_transmit
    ldi r16, 'p'
    rcall uart_transmit
    ldi r16, 'r'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ldi r16, '9'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '2'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '/'
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Processando token 0: '9.0'
    ; Push 9 para a pilha
    ldi r16, 9      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 1: '2.0'
    ; Push 2 para a pilha
    ldi r16, 2      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 2: '/'
    ; Operação de divisão
    rcall stack_pop_int      ; Remove divisor
    mov r18, r16             ; guarda divisor
    mov r19, r17
    rcall stack_pop_int      ; Remove dividendo

    ; Divisão 16-bit
    rcall divide_int

    rcall stack_push_int

    ; Mostrar resultado
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'u'
    rcall uart_transmit
    ldi r16, 'l'
    rcall uart_transmit
    ldi r16, 't'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'd'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ; Fim do processamento da operação
    ret

; ====================================================================
; PROCESSAMENTO OPERAÇÃO 5 - 16-BIT VERSION
; ====================================================================

processar_rpn_op5:
    ; Processando operação 5 com suporte 16-bit:
    ; Expressão: 10.0 3.0 %

    ; Cabeçalho da operação 5
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, 'P'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'C'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '5'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Mostrar expressão
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'x'
    rcall uart_transmit
    ldi r16, 'p'
    rcall uart_transmit
    ldi r16, 'r'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ldi r16, '1'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '3'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '%'
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Processando token 0: '10.0'
    ; Push 10 para a pilha
    ldi r16, 10      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 1: '3.0'
    ; Push 3 para a pilha
    ldi r16, 3      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 2: '%'
    ; Operação de módulo
    rcall stack_pop_int      ; Remove divisor
    mov r18, r16             ; guarda divisor
    mov r19, r17
    rcall stack_pop_int      ; Remove dividendo

    ; Módulo 16-bit
    rcall modulo_int

    rcall stack_push_int

    ; Mostrar resultado
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'u'
    rcall uart_transmit
    ldi r16, 'l'
    rcall uart_transmit
    ldi r16, 't'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'd'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ; Fim do processamento da operação
    ret

; ====================================================================
; PROCESSAMENTO OPERAÇÃO 6 - 16-BIT VERSION
; ====================================================================

processar_rpn_op6:
    ; Processando operação 6 com suporte 16-bit:
    ; Expressão: 2.0 3.0 ^

    ; Cabeçalho da operação 6
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, 'P'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'C'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '6'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Mostrar expressão
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'x'
    rcall uart_transmit
    ldi r16, 'p'
    rcall uart_transmit
    ldi r16, 'r'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ldi r16, '2'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '3'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '^'
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Processando token 0: '2.0'
    ; Push 2 para a pilha
    ldi r16, 2      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 1: '3.0'
    ; Push 3 para a pilha
    ldi r16, 3      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 2: '^'
    ; Operação de potência
    rcall stack_pop_int      ; Remove expoente
    mov r18, r16             ; guarda expoente
    mov r19, r17
    rcall stack_pop_int      ; Remove base

    ; Potência 16-bit
    rcall power_int

    rcall stack_push_int

    ; Mostrar resultado
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'u'
    rcall uart_transmit
    ldi r16, 'l'
    rcall uart_transmit
    ldi r16, 't'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'd'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ; Fim do processamento da operação
    ret

; ====================================================================
; PROCESSAMENTO OPERAÇÃO 7 - 16-BIT VERSION
; ====================================================================

processar_rpn_op7:
    ; Processando operação 7 com suporte 16-bit:
    ; Expressão: 1.0 2.0 + 3.0 4.0 * /

    ; Cabeçalho da operação 7
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, 'P'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'C'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '7'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Mostrar expressão
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'x'
    rcall uart_transmit
    ldi r16, 'p'
    rcall uart_transmit
    ldi r16, 'r'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ldi r16, '1'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '2'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '+'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '3'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '4'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '*'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '/'
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Processando token 0: '1.0'
    ; Push 1 para a pilha
    ldi r16, 1      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 1: '2.0'
    ; Push 2 para a pilha
    ldi r16, 2      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 2: '+'
    ; Operação de soma
    rcall stack_pop_int      ; Remove segundo operando
    mov r18, r16             ; guarda segundo operando
    mov r19, r17
    rcall stack_pop_int      ; Remove primeiro operando

    ; Soma 16-bit
    add r16, r18
    adc r17, r19

    rcall stack_push_int

    ; Processando token 3: '3.0'
    ; Push 3 para a pilha
    ldi r16, 3      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 4: '4.0'
    ; Push 4 para a pilha
    ldi r16, 4      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 5: '*'
    ; Operação de multiplicação
    rcall stack_pop_int      ; Remove segundo operando
    mov r18, r16             ; guarda segundo operando
    mov r19, r17
    rcall stack_pop_int      ; Remove primeiro operando

    ; Multiplicação 16-bit
    rcall multiply_int

    rcall stack_push_int

    ; Processando token 6: '/'
    ; Operação de divisão
    rcall stack_pop_int      ; Remove divisor
    mov r18, r16             ; guarda divisor
    mov r19, r17
    rcall stack_pop_int      ; Remove dividendo

    ; Divisão 16-bit
    rcall divide_int

    rcall stack_push_int

    ; Mostrar resultado
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'u'
    rcall uart_transmit
    ldi r16, 'l'
    rcall uart_transmit
    ldi r16, 't'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'd'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ; Fim do processamento da operação
    ret

; ====================================================================
; PROCESSAMENTO OPERAÇÃO 8 - 16-BIT VERSION
; ====================================================================

processar_rpn_op8:
    ; Processando operação 8 com suporte 16-bit:
    ; Expressão: 5.0 MEM

    ; Cabeçalho da operação 8
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, 'P'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'C'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '8'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Mostrar expressão
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'x'
    rcall uart_transmit
    ldi r16, 'p'
    rcall uart_transmit
    ldi r16, 'r'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ldi r16, '5'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'M'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'M'
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Processando token 0: '5.0'
    ; Push 5 para a pilha
    ldi r16, 5      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 1: 'MEM'
    rcall comando_mem

    ; Mostrar resultado
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'u'
    rcall uart_transmit
    ldi r16, 'l'
    rcall uart_transmit
    ldi r16, 't'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'd'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ; Fim do processamento da operação
    ret

; ====================================================================
; PROCESSAMENTO OPERAÇÃO 9 - 16-BIT VERSION
; ====================================================================

processar_rpn_op9:
    ; Processando operação 9 com suporte 16-bit:
    ; Expressão: MEM

    ; Cabeçalho da operação 9
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, 'P'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'C'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '9'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Mostrar expressão
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'x'
    rcall uart_transmit
    ldi r16, 'p'
    rcall uart_transmit
    ldi r16, 'r'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ldi r16, 'M'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'M'
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Processando token 0: 'MEM'
    rcall comando_mem

    ; Mostrar resultado
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'u'
    rcall uart_transmit
    ldi r16, 'l'
    rcall uart_transmit
    ldi r16, 't'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'd'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ; Fim do processamento da operação
    ret

; ====================================================================
; PROCESSAMENTO OPERAÇÃO 10 - 16-BIT VERSION
; ====================================================================

processar_rpn_op10:
    ; Processando operação 10 com suporte 16-bit:
    ; Expressão: 5.0 RES

    ; Cabeçalho da operação 10
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, 'P'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'C'
    rcall uart_transmit
    ldi r16, 'A'
    rcall uart_transmit
    ldi r16, 'O'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '1'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, '='
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Mostrar expressão
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'x'
    rcall uart_transmit
    ldi r16, 'p'
    rcall uart_transmit
    ldi r16, 'r'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ldi r16, '5'
    rcall uart_transmit
    ldi r16, '0'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'E'
    rcall uart_transmit
    ldi r16, 'S'
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit

    ; Processando token 0: '5.0'
    ; Push 5 para a pilha
    ldi r16, 5      ; Byte baixo
    ldi r17, 0 ; Byte alto
    rcall stack_push_int

    ; Processando token 1: 'RES'
    rcall comando_res

    ; Mostrar resultado
    ldi r16, 'R'
    rcall uart_transmit
    ldi r16, 'e'
    rcall uart_transmit
    ldi r16, 's'
    rcall uart_transmit
    ldi r16, 'u'
    rcall uart_transmit
    ldi r16, 'l'
    rcall uart_transmit
    ldi r16, 't'
    rcall uart_transmit
    ldi r16, 'a'
    rcall uart_transmit
    ldi r16, 'd'
    rcall uart_transmit
    ldi r16, 'o'
    rcall uart_transmit
    ldi r16, ':'
    rcall uart_transmit
    ldi r16, ' '
    rcall uart_transmit

    ; Fim do processamento da operação
    ret

; ====================================================================
; ROTINAS AUXILIARES - TRUE 16-BIT INTEGER SUPPORT
; Suporte completo para inteiros de 0 a 65535
; ====================================================================

; Inicialização da UART
uart_init:
    ; Set baud rate to 9600
    ldi r16, 0
    sts UBRR0H, r16
    ldi r16, BAUD_9600
    sts UBRR0L, r16
    ; Enable transmitter
    ldi r16, (1 << TXEN0)
    sts UCSR0B, r16
    ; Set frame format: 8N1
    ldi r16, ((1 << UCSZ01)|(1 << UCSZ00))
    sts UCSR0C, r16
    ret

; Inicialização da pilha RPN
stack_init:
    ldi r16, 0
    sts stack_ptr, r16       ; Zera ponteiro da pilha
    ret

; EMPILHA INTEIRO DE 16 BITS (r16:r17)
; Usa endereçamento direto na SRAM para máxima confiabilidade
stack_push_int:
    push r20
    push r30
    push r31
    
    ; Get current stack pointer
    lds r20, stack_ptr
    
    ; Use direct SRAM addressing starting from 0x0200 (safe area)
    ; Each entry is 2 bytes, so address = 0x0200 + (stack_ptr * 2)
    ldi r30, 0x00          ; Base address low byte (0x0200)
    ldi r31, 0x02          ; Base address high byte
    
    ; Add offset (stack_ptr * 2)
    lsl r20                ; r20 = stack_ptr * 2
    add r30, r20           ; Add to base address
    brcc no_carry_push     ; Branch if no carry
    inc r31                ; Handle carry
no_carry_push:
    
    ; Store the 16-bit value (little endian)
    st Z+, r16             ; Store low byte and increment Z
    st Z, r17              ; Store high byte
    
    ; Increment stack pointer
    lds r20, stack_ptr
    inc r20
    sts stack_ptr, r20
    
    pop r31
    pop r30
    pop r20
    ret

; DESEMPILHA INTEIRO DE 16 BITS para r16:r17
stack_pop_int:
    push r20
    push r30
    push r31
    
    ; Decrement stack pointer first
    lds r20, stack_ptr
    dec r20
    sts stack_ptr, r20
    
    ; Use direct SRAM addressing starting from 0x0200
    ldi r30, 0x00          ; Base address low byte
    ldi r31, 0x02          ; Base address high byte
    
    ; Add offset (stack_ptr * 2)
    lsl r20                ; r20 = stack_ptr * 2
    add r30, r20           ; Add to base address
    brcc no_carry_pop      ; Branch if no carry
    inc r31                ; Handle carry
no_carry_pop:
    
    ; Load the 16-bit value (little endian)
    ld r16, Z+             ; Load low byte and increment Z
    ld r17, Z              ; Load high byte
    
    pop r31
    pop r30
    pop r20
    ret

; TRUE 16-BIT MULTIPLICATION: (r16:r17) * (r18:r19) -> (r16:r17)
; Implementa multiplicação completa 16x16 usando produtos parciais
; Resultado pode overflow - mantém apenas os 16 bits inferiores
multiply_int:
    push r0
    push r1
    push r20
    push r21
    push r22
    push r23
    
    ; 16x16 -> 32 bit multiplication using partial products
    ; (AH:AL) * (BH:BL) = AH*BH*65536 + (AH*BL + AL*BH)*256 + AL*BL
    ; r16:r17 = AL:AH (little endian)
    ; r18:r19 = BL:BH (little endian)
    
    clr r20                ; Clear result accumulator
    clr r21
    clr r22
    clr r23
    
    ; AL * BL -> r21:r20
    mul r16, r18           ; AL * BL
    mov r20, r0            ; Store low byte
    mov r21, r1            ; Store high byte
    
    ; AL * BH -> add to r22:r21
    mul r16, r19           ; AL * BH
    add r21, r0            ; Add to middle bytes
    adc r22, r1
    
    ; AH * BL -> add to r22:r21
    mul r17, r18           ; AH * BL
    add r21, r0            ; Add to middle bytes
    adc r22, r1
    
    ; AH * BH -> add to r23:r22 (but we'll ignore high overflow)
    mul r17, r19           ; AH * BH
    add r22, r0            ; Add to high bytes (ignore carry out)
    
    ; Store result in r16:r17 (keep only lower 16 bits)
    mov r16, r20           ; Low byte of result
    mov r17, r21           ; High byte of result
    
    ; Clear multiplication result registers
    clr r0
    clr r1
    
    pop r23
    pop r22
    pop r21
    pop r20
    pop r1
    pop r0
    ret

; TRUE 16-BIT DIVISION: (r16:r17) / (r18:r19) -> quotient in (r16:r17)
; Implementa divisão usando subtração repetida para simplicidade e confiabilidade
divide_int:
    push r20
    push r21
    push r22
    push r23
    
    ; Check for division by zero
    cp r18, r1             ; Compare divisor with 0
    cpc r19, r1
    breq div_by_zero       ; If divisor is 0, return maximum value
    
    ; Initialize quotient counter to 0
    clr r22                ; Quotient low byte
    clr r23                ; Quotient high byte
    
    ; Save dividend in r20:r21 for comparison
    mov r20, r16
    mov r21, r17
    
div_subtract_loop:
    ; Compare dividend (r20:r21) with divisor (r18:r19)
    cp r20, r18            ; Compare low bytes
    cpc r21, r19           ; Compare high bytes with carry
    brlo div_done          ; If dividend < divisor, we're done
    
    ; Subtract divisor from dividend
    sub r20, r18           ; Subtract low bytes
    sbc r21, r19           ; Subtract high bytes with borrow
    
    ; Increment quotient
    inc r22                ; Increment low byte
    brne div_no_carry      ; If no overflow, continue
    inc r23                ; Handle carry to high byte
    
div_no_carry:
    ; Continue loop
    rjmp div_subtract_loop
    
div_by_zero:
    ldi r16, 0xFF          ; Return maximum value on division by zero
    ldi r17, 0xFF
    rjmp div_exit
    
div_done:
    ; Store quotient in result registers
    mov r16, r22
    mov r17, r23
    
div_exit:
    pop r23
    pop r22
    pop r21
    pop r20
    ret

; TRUE 16-BIT MODULO: (r16:r17) % (r18:r19) -> remainder in (r16:r17)
; Implementa operação módulo usando subtração repetida para simplicidade e confiabilidade
modulo_int:
    push r20
    push r21
    
    ; Check for division by zero
    cp r18, r1             ; Compare divisor with 0
    cpc r19, r1
    breq mod_by_zero       ; If divisor is 0, return dividend unchanged
    
    ; Simple repeated subtraction approach
    ; Keep subtracting divisor from dividend until dividend < divisor
    ; The result is the remainder
    
mod_subtract_loop:
    ; Compare dividend (r16:r17) with divisor (r18:r19)
    cp r16, r18            ; Compare low bytes
    cpc r17, r19           ; Compare high bytes with carry
    brlo mod_done          ; If dividend < divisor, we're done
    
    ; Subtract divisor from dividend
    sub r16, r18           ; Subtract low bytes
    sbc r17, r19           ; Subtract high bytes with borrow
    
    ; Continue loop
    rjmp mod_subtract_loop
    
mod_by_zero:
    ; Return dividend unchanged on mod by zero
    ; (r16:r17 already contains dividend)
    
mod_done:
    pop r21
    pop r20
    ret

; 16-BIT POWER: (r16:r17) ^ (r18:r19) -> result in (r16:r17)
; Implementa exponenciação com verificação de overflow
power_int:
    push r20
    push r21
    push r22
    push r23
    
    ; Check for exponent = 0
    cp r18, r1             ; Compare exponent with 0
    cpc r19, r1
    brne pow_not_zero
    ldi r16, 1             ; x^0 = 1
    clr r17
    rjmp pow_done
    
pow_not_zero:
    ; Check for exponent = 1
    cpi r18, 1
    ldi r20, 0
    cpc r19, r20
    breq pow_done          ; x^1 = x (already in r16:r17)
    
    ; Save base in r20:r21
    mov r20, r16
    mov r21, r17
    
    ; Initialize result to base (first multiplication)
    ; r22:r23 = exponent counter
    mov r22, r18
    mov r23, r19
    dec r22                ; Decrement exponent (already have base)
    sbc r23, r1            ; Handle borrow
    
pow_loop:
    ; Check if exponent counter is 0
    cp r22, r1
    cpc r23, r1
    breq pow_done
    
    ; Multiply current result by base
    ; Move base to r18:r19 for multiplication
    mov r18, r20
    mov r19, r21
    rcall multiply_int     ; r16:r17 = r16:r17 * r18:r19
    
    ; Decrement exponent counter
    dec r22
    sbc r23, r1
    rjmp pow_loop
    
pow_done:
    pop r23
    pop r22
    pop r21
    pop r20
    ret

; Comando MEM - armazena resultado no topo da pilha
comando_mem:
    ; TODO: Implementação para armazenar em variáveis A-Z
    ret

; Comando RES - recupera valor da memória
comando_res:
    ; TODO: Implementação para recuperar de variáveis A-Z
    ret

; Carrega variável da memória
load_var:
    ; r17 contém o índice da variável (0-25)
    ; TODO: Implementação para carregar variável A-Z
    ret

; Envia resultado via UART
send_result:
    rcall stack_pop_int      ; Pega resultado do topo
    ; Converte para ASCII e envia
    rcall send_number_16bit
    ; Envia newlines para separar
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ldi r16, 13
    rcall uart_transmit
    ldi r16, 10
    rcall uart_transmit
    ret

; CONVERSÃO 16-BIT PARA ASCII: Converte (r16:r17) para string decimal
; Suporte completo para valores de 0 a 65535
send_number_16bit:
    push r18
    push r19
    push r20
    push r21
    push r22
    push r23
    push r30
    push r31
    
    ; Check for zero
    cp r16, r1
    cpc r17, r1
    brne not_zero_16
    ldi r16, '0'
    rcall uart_transmit
    rjmp send_16_done
    
not_zero_16:
    ; Use repeated division by 10 to extract digits
    ; Store digits in a buffer and then send in reverse order
    ldi r30, lo8(0x0500)    ; Point to digit buffer in SRAM
    ldi r31, hi8(0x0500)
    clr r22                 ; Digit counter
    
extract_digits:
    ; Divide by 10: r16:r17 / 10 -> quotient in r16:r17, remainder in r20
    ldi r18, 10
    clr r19
    rcall divide_by_10_16bit    ; Special optimized division by 10
    
    ; Convert remainder to ASCII and store
    mov r20, r18               ; Remainder is returned in r18
    ldi r21, '0'
    add r20, r21               ; Convert to ASCII
    st Z+, r20                 ; Store digit and increment pointer
    inc r22                    ; Increment digit count
    
    ; Check if quotient is zero
    cp r16, r1
    cpc r17, r1
    brne extract_digits        ; Continue if not zero
    
    ; Now send digits in reverse order
    ; Z now points one past the last digit, so decrement first
    
send_digits:
    dec r30                    ; Move to previous digit
    ld r16, Z                  ; Load digit
    rcall uart_transmit        ; Send it
    dec r22                    ; Decrement counter
    brne send_digits           ; Continue until all sent
    
send_16_done:
    pop r31
    pop r30
    pop r23
    pop r22
    pop r21
    pop r20
    pop r19
    pop r18
    ret

; DIVISÃO OTIMIZADA POR 10 para números 16-bit
; Input: r16:r17 = dividend
; Output: r16:r17 = quotient, r18 = remainder
divide_by_10_16bit:
    push r19
    push r20
    push r21
    
    ; Save original value for remainder calculation
    mov r20, r16
    mov r21, r17
    
    ; Simple approach: repeated subtraction by 10
    ; This is slower but accurate and simple for embedded systems
    clr r18                    ; Quotient counter
    clr r19
    
div10_loop:
    ; Check if we can subtract 10
    cpi r16, 10
    cpc r17, r1                ; Compare with zero register
    brlo div10_remainder       ; If < 10, we're done
    
    ; Subtract 10
    subi r16, 10
    sbci r17, 0
    
    ; Increment quotient
    inc r18
    brne div10_check_carry
    inc r19                    ; Handle 16-bit quotient overflow
    
div10_check_carry:
    rjmp div10_loop
    
div10_remainder:
    ; r18:r19 = quotient, r16 = remainder
    mov r20, r16               ; Save remainder
    mov r16, r18               ; Quotient to r16:r17
    mov r17, r19
    mov r18, r20               ; Remainder to r18
    
    pop r21
    pop r20
    pop r19
    ret

; Keep the original send_number for compatibility
send_number:
    rcall send_number_16bit
    ret

; ENVIA BYTE COMO HEXADECIMAL (r16) - para debug
; Converte um byte para dois dígitos hexadecimais
send_byte_as_hex:
    push r17
    push r18
    
    ; Salvar byte original
    mov r18, r16
    
    ; Enviar nibble alto (bits 7-4)
    swap r16                   ; Trocar nibbles
    andi r16, 0x0F            ; Manter apenas nibble baixo
    cpi r16, 10
    brlo hex_digit_0_9_high   ; Se < 10, é dígito 0-9
    subi r16, -55             ; Converter para A-F (10-15 -> 65-70)
    rjmp send_high_nibble
hex_digit_0_9_high:
    subi r16, -48             ; Converter para 0-9 (0-9 -> 48-57)
send_high_nibble:
    rcall uart_transmit
    
    ; Enviar nibble baixo (bits 3-0)
    mov r16, r18              ; Restaurar byte original
    andi r16, 0x0F            ; Manter apenas nibble baixo
    cpi r16, 10
    brlo hex_digit_0_9_low    ; Se < 10, é dígito 0-9
    subi r16, -55             ; Converter para A-F
    rjmp send_low_nibble
hex_digit_0_9_low:
    subi r16, -48             ; Converter para 0-9
send_low_nibble:
    rcall uart_transmit
    
    pop r18
    pop r17
    ret

; Transmite caractere via UART
uart_transmit:
    push r22
wait_transmit2:
    lds r22, UCSR0A
    sbrs r22, UDRE0
    rjmp wait_transmit2
    sts UDR0, r16
    pop r22
    ret

; ====================================================================
; FINALIZAÇÃO - 16-BIT VERSION
; ====================================================================

end_program:
    rjmp end_program         ; Loop infinito

; ====================================================================
; FIM DO CÓDIGO - 16-BIT RPN CALCULATOR
; Suporte completo para inteiros de 0 a 65535
; ====================================================================
