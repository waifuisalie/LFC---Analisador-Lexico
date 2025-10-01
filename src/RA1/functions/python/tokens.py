# tokens.py
class Tipo_de_Token:
    # Números
    NUMERO_REAL = "NUMERO_REAL"

    # Operadores Aritméticos
    SOMA = "SOMA"              # +
    SUBTRACAO = "SUBTRACAO"    # -
    MULTIPLICACAO = "MULT"     # *
    DIVISAO = "DIV"            # /
    RESTO = "RESTO"            # %
    POTENCIA = "POT"           # ^

    # Operadores de Comparação
    MENOR = "MENOR"            # <
    MAIOR = "MAIOR"           # >
    IGUAL = "IGUAL"           # ==
    MENOR_IGUAL = "MENOR_IGUAL" # <=
    MAIOR_IGUAL = "MAIOR_IGUAL" # >=
    DIFERENTE = "DIFERENTE"    # !=

    # Operadores Lógicos
    NOT = "NOT"               # !
    OR = "OR"                 # ||
    AND = "AND"              # &&

    # Estruturas de Controle
    WHILE = "WHILE"           # Estrutura de repetição WHILE
    FOR = "FOR"               # Estrutura de repetição FOR
    IFELSE = "IFELSE"         # Estrutura condicional IF-ELSE

    # Símbolos de Agrupamento
    ABRE_PARENTESES = "ABRE_PARENTESES"    # (
    FECHA_PARENTESES = "FECHA_PARENTESES"   # )

    # Comandos Especiais
    RES = "RES"               # Comando especial RES

    # Variáveis
    VARIAVEL = "VARIAVEL"       # Identificador de variável

    # Marcador de fim de arquivo
    FIM = "FIM"


class Token:
    def __init__(self, tipo: str, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor})"
