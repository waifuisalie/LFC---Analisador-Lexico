; ATmega328P Register Definitions
; Custom header for assembly programming

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

; Useful Constants
.equ BAUD_9600, 103     ; Baud rate divisor for 9600 bps at 16MHz
