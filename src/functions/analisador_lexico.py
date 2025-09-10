# analisador_lexico.py

from .tokens import Token, Tipo_de_Token

class Analisador_Lexico:
    def __init__(self, texto_fonte: str):
        self.texto_fonte = texto_fonte
        self.ponteiro = 0
        self.caractere = self.texto_fonte[self.ponteiro] if self.texto_fonte else None
        self.resultado = ""

    def avanca_ponteiro(self):
        self.ponteiro += 1
        if self.ponteiro < len(self.texto_fonte):
            self.caractere = self.texto_fonte[self.ponteiro]
        else:
            self.caractere = None

    def ignora_espaco(self):
        while self.caractere is not None and self.caractere.isspace():
            self.avanca_ponteiro()

    def analise(self):
        tokens = []
        while self.caractere is not None:
            token = self.estado_zero()
            if token:
                tokens.append(token)
        tokens.append(Token(Tipo_de_Token.FIM, None))
        return tokens

    def estado_zero(self):
        self.ignora_espaco()
        if self.caractere is None:
            return None
        if self.caractere.isalpha():
            return self.estado_comando()
        if self.caractere.isdigit():
            return self.estado_numero()
        return self.estado_operador()

    def estado_operador(self):
        token = None
        if self.caractere == '(':
            token = Token(Tipo_de_Token.ABRE_PARENTESES, '(')
        elif self.caractere == ')':
            token = Token(Tipo_de_Token.FECHA_PARENTESES, ')')
        elif self.caractere == '+':
            token = Token(Tipo_de_Token.SOMA, '+')
        elif self.caractere == '-':
            token = Token(Tipo_de_Token.SUBTRACAO, '-')
        elif self.caractere == '*':
            token = Token(Tipo_de_Token.MULTIPLICACAO, '*')
        elif self.caractere == '/':
            token = Token(Tipo_de_Token.DIVISAO, '/')
        elif self.caractere == '%':
            token = Token(Tipo_de_Token.RESTO, '%')
        elif self.caractere == '^':
            token = Token(Tipo_de_Token.POTENCIA, '^')
        if token:
            self.avanca_ponteiro()
            return token
        raise ValueError(f"Caractere inválido: '{self.caractere}'")

    def estado_numero(self):
        resultado = ""
        while self.caractere is not None and self.caractere.isdigit():
            resultado += self.caractere
            self.avanca_ponteiro()
        if self.caractere == '.':
            resultado += self.caractere
            self.avanca_ponteiro()
            if not (self.caractere and self.caractere.isdigit()):
                raise ValueError("ERRO: espera-se dígito após o ponto decimal.")
            while self.caractere is not None and self.caractere.isdigit():
                resultado += self.caractere
                self.avanca_ponteiro()
        return Token(Tipo_de_Token.NUMERO_REAL, float(resultado))

    def estado_comando(self):
        resultado = ""
        while self.caractere is not None and self.caractere.isalpha():
            resultado += self.caractere
            self.avanca_ponteiro()
        if resultado == "RES":
            return Token(Tipo_de_Token.RES, resultado)
        else:
            return Token(Tipo_de_Token.MEM, resultado)