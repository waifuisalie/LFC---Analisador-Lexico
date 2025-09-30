def gerar_secao_dados(codigo: list[str]) -> None:
    dados = [
        "; ====================================================================",
        "; SEÇÃO DE DADOS - 16-BIT VERSION",
        "; ====================================================================",
        "",
        ".section .data",
        "stack_ptr: .byte 1        ; Ponteiro da pilha RPN",
        "mem_vars:  .space 52      ; 26 variáveis 16-bit (A-Z)",
        "temp_result: .space 4     ; Resultado temporário",
        "",
        ".section .text",
        ""
    ]
    codigo.extend(dados)