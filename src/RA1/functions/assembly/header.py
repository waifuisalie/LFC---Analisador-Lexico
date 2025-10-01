def gerar_header(codigo: list[str]) -> None:
    header = [
        "; ====================================================================",
        "; Código Assembly gerado automaticamente para Arduino Uno (ATmega328p)",
        "; Processador RPN - 16-BIT VERSION",
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
