#!/usr/bin/env python3
import sys
import math

# Classes para a geracao de tokens
class Tipo_de_Token():
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

# Classe do Analisador Léxico
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
            if token: # Veriifica se esta vazio
                tokens.append(token)

        tokens.append(Token(Tipo_de_Token.FIM, None)) # Adiciona o marcador de fim
        return tokens
        
    # Estados da nossa Maquina de Estados Finitos (FSM)

    def estado_zero(self):

        self.ignora_espaco()

        #Verifica se chegou ao fim do arquivo
        if self.caractere is None:
            return None
        
        # Verifica se é um comando especial (alfabetico)
        if self.caractere.isalpha():
            return self.estado_comando()
        
        # Verifica se é um número
        if self.caractere.isdigit():
            return self.estado_numero()
        
        return self.estado_operador()

    def estado_operador(self):

        # Verifica qual é o caractere especial 
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

        # Ao final retorna o token criado e avança o ponteiro
        if token:
            self.avanca_ponteiro()
            return token
        
        # Caractere inválido
        raise ValueError(f"Caractere inválido: '{self.caractere}'")
    
    def estado_numero(self):
        resultado = ""

        # Lê a parte inteira do número
        while self.caractere is not None and self.caractere.isdigit():
            resultado += self.caractere
            self.avanca_ponteiro()

        # Inicia a leiturta da parte decimal
        if self.caractere == '.':
            resultado += self.caractere
            self.avanca_ponteiro()

            if not (self.caractere and self.caractere.isdigit()):
                raise ValueError("ERRO: espera-se dígito após o ponto decimal.")
            
            # Percorre todos os dígitos da parte decimal
            while self.caractere is not None and self.caractere.isdigit():
                resultado += self.caractere
                self.avanca_ponteiro()
        return Token(Tipo_de_Token.NUMERO_REAL, float(resultado)) # Crai token de número real
    
    def estado_comando(self):
        resultado = ""

        # Verifica se é um comando especial (alfabetico)
        while self.caractere is not None and self.caractere.isalpha():  
            resultado += self.caractere
            self.avanca_ponteiro()

        # Checa qual dos dois comandos (MEM ou RES) foi inserido
        if resultado == "MEM":
            return Token(Tipo_de_Token.MEM, resultado) 
        elif resultado == "RES":
            return Token(Tipo_de_Token.RES, resultado)
        else:
            raise ValueError(f"Comando inválido: '{resultado}'")
        
def parseExpressao(linha_operacao):
    analisador_lexico = Analisador_Lexico(linha_operacao)
    tokens = analisador_lexico.analise()
    # Vamos remover os tokens de parênteses, pois não são necessários na RPN
    # Mas manteremos para validação futura, se necessário
    tokens = [t for t in tokens if t.tipo not in 
            (Tipo_de_Token.ABRE_PARENTESES, Tipo_de_Token.FECHA_PARENTESES)]
    return tokens

def arredondar_16bit(valor):
    """Simula a precisão de ponto flutuante de 16 bits (duas casas decimais)."""
    return round(float(valor), 2)

def executarExpressao(tokens: list[Token], memoria: dict, historico_resultados: list) -> float:
    pilha = []

    for token in tokens:
        if token.tipo == Tipo_de_Token.FIM:
            continue
        # Transforma a string em maiuscula para poder trabalhar com os comandos MEM e RES
        valor_token = str(token.valor).upper()

        # Se for operador
        if valor_token in ['+', '-', '*', '/', '%', '^']:
            if len(pilha) < 2:
                print(f"-> Erro: tokens insuficientes para o operador '{valor_token}'")
                continue

            v2_str, v1_str = pilha.pop(), pilha.pop()
            resultado = 0.0

            try:
                v1, v2 = float(v1_str), float(v2_str)
                if valor_token == '+': resultado = v1 + v2
                elif valor_token == '-': resultado = v1 - v2
                elif valor_token == '*': resultado = v1 * v2
                elif valor_token == '/':
                    if v2 == 0: raise ZeroDivisionError("Divisão por zero.")
                    resultado = v1 / v2
                elif valor_token == '%': resultado = int(v1) % int(v2)
                elif valor_token == '^': resultado = math.pow(v1, v2)

                pilha.append(str(arredondar_16bit(resultado)))
            except (ZeroDivisionError, ValueError) as e:
                print(f"-> Erro de operação para '{valor_token}': {e}")
                pilha.append('0.0')

        # Comando RES (recupera valor do histórico)
        elif token.tipo == Tipo_de_Token.RES:
            if len(pilha) == 0:
                print("-> Erro: RES requer um índice numérico na pilha.")
                pilha.append('0.0')
                continue

            n_str = pilha.pop()
            try:
                n = int(float(n_str)) # Nos interessa apenas o inteiro para o comando RES
                if 0 < n <= len(historico_resultados):
                    pilha.append(str(historico_resultados[-n]))
                else:
                    print(f"-> Erro: Índice N={n} inválido para RES.")
                    pilha.append('0.0')
            except ValueError:
                print(f"-> Erro: O valor '{n_str}' não é válido para RES.")
                pilha.append('0.0')

        # Lógica para o comando MEM (armazenar/recuperar valor da memória)
        elif token.tipo == Tipo_de_Token.MEM:
            if len(pilha) > 0 and pilha[-1].replace('.', '', 1).isdigit():
                valor_para_armazenar_str = pilha.pop()
                valor_float = float(valor_para_armazenar_str)
                memoria['MEM'] = valor_float
                pilha.append(str(arredondar_16bit(valor_float)))
            elif 'MEM' in memoria:
                valor = memoria.get('MEM', 0.0)
                pilha.append(str(arredondar_16bit(valor)))
            else:
                print("-> Erro: MEM não inicializado.")
                pilha.append('0.0')

        # Só converte para número tokens do tipo NUMERO_REAL
        elif token.tipo == Tipo_de_Token.NUMERO_REAL:
            pilha.append(str(token.valor))

        # Caso variável desconhecida. Em algumas das etapas irá dar erro caso haja texto inválido.
        else:
            pilha.append(valor_token)

    # Retorna o resultado final. A pilha deve conter apenas um item.
    if len(pilha) == 1:
        return arredondar_16bit(pilha[0])
    else:
        print(f"-> Erro: {len(pilha)} itens na pilha: {pilha}")
        return arredondar_16bit(pilha[-1]) if pilha else 0.0

def lerArquivos(nomeArquivo: str): 
    try:
        with open(nomeArquivo, 'r', encoding="utf-8") as arquivos_teste:
            linhas = [linha.strip() for linha in arquivos_teste if linha.strip()]
        return linhas 
    except FileNotFoundError:
        print(f'-> Erro: Arquivo não encontrado: {nomeArquivo}')
        return []
    
def exibirResultados(vetor_linhas: list[str]) -> None: 
    memoria_global = {}
    historico_global =[]
    tokens_salvo = []

    for i ,linha in enumerate(vetor_linhas, start=1): 
            lista_de_tokens = parseExpressao(linha)
            # Limpa a linha dos parênteses para salvar os tokens
            linhas_tokens_recebidos = linha.replace('(', '').replace(')', '').strip().split()
            tokens_salvo.append(linhas_tokens_recebidos)
            resultado = executarExpressao(lista_de_tokens, memoria_global, historico_global)

            if resultado is not None:
                historico_global.append(resultado)
            
            print(f"Linha {i:02d}: Expressão '{linha}' -> Resultado: {resultado}")
            
    try:
        # Cria o arquivo tokens_gerados.txt e escreve os tokens nele
        with open("tokens_gerados.txt","w", encoding='utf-8') as f:
            for lista_de_tokens in tokens_salvo:
                linha_formatada = " ".join(lista_de_tokens)
                f.write(linha_formatada + "\n")
    except Exception as e:
        print(f'Erro ao escreve os tokens no arquivo {e}')

if __name__ == "__main__":
    # Não aceita argumentos suficientes
    if len(sys.argv) < 2:
        print("Erro: Especificar nome do arquivo de teste")
        sys.exit(1)
    # Pega o nome do arquivo a partir dos argumentos da linha de comando
    arquivo = sys.argv[1]
    # Inicia-se a leitura do arquivo e o processamento das operações
    operacoes_lidas = lerArquivos(arquivo)
    # Exibe os resultados
    print("\nArquivo de teste:", f"{arquivo}\n")
    exibirResultados(operacoes_lidas)
    print("\n--- FIM DOS TESTES ---\n")

