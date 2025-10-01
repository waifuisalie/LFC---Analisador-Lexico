#!/usr/bin/env python3
import sys
from pathlib import Path

from src.RA1.functions.python.rpn_calc import parseExpressao, executarExpressao
from src.RA1.functions.python.io_utils import lerArquivo, salvar_tokens
from src.RA1.functions.python.tokens import Tipo_de_Token
from src.RA1.functions.assembly import gerarAssemblyMultiple, save_assembly, save_registers_inc

# --- caminhos base do projeto ---
BASE_DIR    = Path(__file__).resolve().parent        # raiz do repo
INPUTS_DIR  = BASE_DIR / "inputs" / "RA1"                       # raiz/inputs
OUT_TOKENS  = BASE_DIR / "outputs" / "RA1" / "tokens" / "tokens_gerados.txt"
OUT_ASM_DIR = BASE_DIR / "outputs" / "RA1" / "assembly"          # raiz/outputs/assembly

# garante pastas de saída
OUT_ASM_DIR.mkdir(parents=True, exist_ok=True)
OUT_TOKENS.parent.mkdir(parents=True, exist_ok=True)

def exibirResultados(vetor_linhas: list[str]) -> None:
    memoria_global = {}
    historico_global = []
    tokens_salvos_txt = []

    for i, linha in enumerate(vetor_linhas, start=1):
        lista_de_tokens = parseExpressao(linha)
        # para salvar tokens completos (incluindo parênteses) para RA2
        tokens_completos = [str(token.valor) for token in lista_de_tokens if token.tipo != Tipo_de_Token.FIM]
        tokens_salvos_txt.append(tokens_completos)

        resultado = executarExpressao(lista_de_tokens, memoria_global, historico_global)
        if resultado is not None:
            historico_global.append(resultado)
        print(f"Linha {i:02d}: Expressão '{linha}' -> Resultado: {resultado}")

    # Salva em ambos os locais: RA1 e raiz
    salvar_tokens(tokens_salvos_txt, OUT_TOKENS)  # Salva em RA1
    salvar_tokens(tokens_salvos_txt, BASE_DIR / "tokens_gerados.txt")  # Salva na raiz

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ERRO -> Especificar caminho do arquivo de teste (ex.: int/teste1.txt ou float/teste2.txt)")
        sys.exit(1)

    # --- resolve caminho da entrada ---
    arg = Path(sys.argv[1])

    # Tenta encontrar o arquivo em várias localizações possíveis
    possibilidades = [
        Path.cwd() / arg,  # Relativo ao diretório atual
        BASE_DIR / arg,    # Relativo à raiz do projeto
        INPUTS_DIR / arg,  # Dentro da pasta inputs/RA1
    ]

    entrada = None
    for caminho in possibilidades:
        if caminho.exists():
            entrada = caminho.resolve()
            break

    if entrada is None and arg.is_absolute():  # Se for caminho absoluto
        entrada = Path(arg)

    if not entrada.exists():
        print(f"ERRO -> arquivo não encontrado: {entrada}")
        sys.exit(1)

    operacoes_lidas = lerArquivo(str(entrada))

    # Exibe caminho relativo à raiz se possível (evita ValueError do relative_to)
    try:
        mostrar = entrada.relative_to(BASE_DIR)
    except ValueError:
        print("AVISO -> Não foi possível exibir o caminho relativo ao diretório base. Exibindo caminho absoluto.")
        mostrar = entrada
        
    print(f"\nArquivo de teste: {mostrar}\n")

    exibirResultados(operacoes_lidas)
    print("\n--- FIM DOS TESTES ---\n")

    # --- Geração de código assembly para todas as operações em um único arquivo ---
    codigo_assembly = []

    # tokens foram salvos em raiz/outputs/tokens/tokens_gerados.txt
    linhas = lerArquivo(str(OUT_TOKENS))

    # Salvar registers.inc em ambos os locais
    save_registers_inc(str(OUT_ASM_DIR / "registers.inc"))  # Em RA1
    save_registers_inc(str(BASE_DIR / "registers.inc"))  # Na raiz

    # Preparar lista de todas as operações (filtrar parênteses para assembly)
    all_tokens = []
    for linha in linhas:
        tokens = linha.split()
        # Filtrar parênteses apenas para geração de assembly (RA1 compatibility)
        tokens_sem_parenteses = [token for token in tokens if token not in ['(', ')']]
        all_tokens.append(tokens_sem_parenteses)

    # Gerar um único arquivo com todas as operações
    gerarAssemblyMultiple(all_tokens, codigo_assembly)
    
    # Salvar programa_completo.S em ambos os locais
    nome_arquivo_ra1 = OUT_ASM_DIR / "programa_completo.S"
    nome_arquivo_root = BASE_DIR / "programa_completo.S"
    
    save_assembly(codigo_assembly, str(nome_arquivo_ra1))  # Salva em RA1
    save_assembly(codigo_assembly, str(nome_arquivo_root))  # Salva na raiz
    
    print(f"Arquivo {nome_arquivo_ra1.name} gerado com sucesso em:")
    print(f"- {OUT_ASM_DIR}")
    print(f"- {BASE_DIR}")
    print(f"Contém {len(all_tokens)} operações RPN em sequência.")

    print("\nPara testar:")
    print("- Compile e carregue programa_completo.S no Arduino Uno")
    print("- Monitore a saída serial em 9600 baud para ver os resultados!")
    print("- Todas as operações serão executadas sequencialmente")