# tokens.py
class Tipo_de_Token:
    # Números
    NUMERO_REAL = "NUMERO_REAL"

    # Operadores
    SOMA = "SOMA"
    SUBTRACAO = "SUBTRACAO"
    MULTIPLICACAO = "MULT"
    DIVISAO = "DIV"
    RESTO = "RESTO"
    POTENCIA = "POT"

    # Símbolos de Agrupamento
    ABRE_PARENTESES = "ABRE_PARENTESES"
    FECHA_PARENTESES = "FECHA_PARENTESES"

    # Comandos Especiais
    RES = "RES"
    MEM = "MEM"

    # Marcador de fim de arquivo
    FIM = "FIM"


class Token:
    def __init__(self, tipo: str, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"
