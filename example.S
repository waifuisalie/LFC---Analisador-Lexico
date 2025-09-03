#include "registers.inc"
.global main  

.section .text

main:
    // Initialize stack pointer to end of SRAM (0x08FF for ATmega328P)
    ldi r16, 0xFF
    out SPL, r16    // SPL is at I/O address 0x3D
    ldi r16, 0x08
    out SPH, r16    // SPH is at I/O address 0x3E
    
    // Initialize UART (Serial)
    // Set baud rate to 9600 (16MHz / (16 * 9600) - 1 = 103)
    ldi r16, 0
    sts UBRR0H, r16    // UBRR0H
    ldi r16, BAUD_9600
    sts UBRR0L, r16    // UBRR0L
    
    // Enable transmitter
    ldi r16, (1 << TXEN0)// TXEN0 bit
    sts UCSR0B, r16    // UCSR0B
    
    // Set frame format: 8 data bits, 1 stop bit
    ldi r16, ((1 << UCSZ01)|(1 << UCSZ00))      // UCSZ01 | UCSZ00
    sts UCSR0C, r16    // UCSR0C
    
    // Load two numbers to add
    ldi r17, 25      // First number
    ldi r18, 15      // Second number
    
    // Perform addition
    add r17, r18     // r17 = r17 + r18 = 42
    
    // Convert result to ASCII and send
    // For simplicity, we'll handle numbers 0-99
    clr r21          // Clear tens counter
    
    // Get tens digit
    mov r19, r17     // Copy result
    ldi r20, 10
    
divide_loop:
    cp r19, r20      // Compare with 10
    brlo send_tens   // If less than 10, we're done
    sub r19, r20     // Subtract 10
    inc r21          // Increment tens counter
    rjmp divide_loop
    
send_tens:
    // Send tens digit (if > 0)
    cpi r21, 0
    breq send_ones   // Skip if tens = 0
    
    mov r16, r21
    subi r16, -48    // Convert to ASCII ('0' = 48)
    rcall uart_transmit
    
send_ones:
    // Send ones digit
    mov r16, r19
    subi r16, -48    // Convert to ASCII
    rcall uart_transmit
    
    // Send newline
    ldi r16, 13      // Carriage return
    rcall uart_transmit
    ldi r16, 10      // Line feed
    rcall uart_transmit
    
    // Infinite loop to prevent program from continuing
end_loop:
    rjmp end_loop

// UART transmit function
uart_transmit:
    // Wait for transmit buffer to be empty
wait_transmit:
    lds r22, UCSR0A
    sbrs r22, UDRE0
    rjmp wait_transmit
    
    // Send character
    sts UDR0, r16
    ret
