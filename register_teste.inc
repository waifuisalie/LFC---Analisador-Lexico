; ATmega328P Register Definitions
; Custom header for assembly programming
; Updated for RPN Calculator Project

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
.equ RXEN0,   4       ; Receiver Enable
.equ TXEN0,   3       ; Transmitter Enable

; GPIO Ports (commonly used) - AGORA COM ENDEREÇOS DE I/O CORRETOS
.equ PORTB,   0x05    ; Port B Data Register (Endereço de I/O)
.equ DDRB,    0x04    ; Port B Data Direction Register (Endereço de I/O)
.equ PINB,    0x03    ; Port B Input Pins Register (Endereço de I/O)

; Constants for our test
.equ LED_PIN, 5       ; O LED embutido do Arduino Uno é o PINO 13, que corresponde ao PB5 (Port B, bit 5)

; Math Constants (for RPN calculator)
.equ MAX_STACK_SIZE, 16 ; Maximum stack depth for RPN