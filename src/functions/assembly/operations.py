# operations.py
from typing import List

# -----------------------------
# Helpers de análise de tokens
# -----------------------------

def is_number(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False

def is_integer(token: str) -> bool:
    try:
        val = float(token)
        return val == int(val)
    except ValueError:
        return False

def is_variable_mem(token: str) -> bool:
    return token.isalpha() and token.isupper() and token not in ("MEM", "RES")

# ---------------------------------
# Geração de PUSH (público + interno)
# ---------------------------------

def _gerar_push_int_com_debug(valor: int) -> List[str]:
    return [
        f"    ; Push {valor} para a pilha",
        f"    ldi r16, {valor & 0xFF}      ; Byte baixo",
        f"    ldi r17, {(valor >> 8) & 0xFF} ; Byte alto",
        "    rcall stack_push_int",
        ""
    ]

def gerar_push_int(valor: int) -> List[str]:
    """Wrapper público (não recursivo)."""
    return _gerar_push_int_com_debug(valor)

# ---------------------------------
# Geração de operações aritméticas
# ---------------------------------

def _operacao_map() -> dict[str, List[str]]:
    return {
        '+': [
            "    ; Operação de soma",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Soma 16-bit",
            "    add r16, r18",
            "    adc r17, r19",
            "",
            "    rcall stack_push_int",
            ""
        ],
        '-': [
            "    ; Operação de subtração",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Subtração 16-bit",
            "    sub r16, r18",
            "    sbc r17, r19",
            "",
            "    rcall stack_push_int",
            ""
        ],
        '*': [
            "    ; Operação de multiplicação",
            "    rcall stack_pop_int      ; Remove segundo operando",
            "    mov r18, r16             ; guarda segundo operando",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove primeiro operando",
            "",
            "    ; Multiplicação 16-bit",
            "    rcall multiply_int",
            "",
            "    rcall stack_push_int",
            ""
        ],
        '/': [
            "    ; Operação de divisão",
            "    rcall stack_pop_int      ; Remove divisor",
            "    mov r18, r16             ; guarda divisor",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove dividendo",
            "",
            "    ; Divisão 16-bit",
            "    rcall divide_int",
            "",
            "    rcall stack_push_int",
            ""
        ],
        '%': [
            "    ; Operação de módulo",
            "    rcall stack_pop_int      ; Remove divisor",
            "    mov r18, r16             ; guarda divisor",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove dividendo",
            "",
            "    ; Módulo 16-bit",
            "    rcall modulo_int",
            "",
            "    rcall stack_push_int",
            ""
        ],
        '^': [
            "    ; Operação de potência",
            "    rcall stack_pop_int      ; Remove expoente",
            "    mov r18, r16             ; guarda expoente",
            "    mov r19, r17",
            "    rcall stack_pop_int      ; Remove base",
            "",
            "    ; Potência 16-bit",
            "    rcall power_int",
            "",
            "    rcall stack_push_int",
            ""
        ],
    }

def gerar_operacao(operador: str) -> List[str]:
    """Retorna as linhas Assembly para o operador informado."""
    mapa = _operacao_map()
    return mapa.get(operador, [f"    ; Operação {operador} não implementada", ""])

__all__ = [
    "is_number", "is_integer", "is_variable_mem",
    "gerar_push_int", "gerar_operacao",
]
