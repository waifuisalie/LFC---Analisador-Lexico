def gerar_footer(codigo: list[str]) -> None:
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
