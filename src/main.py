#!/usr/bin/env python3
import sys
from pathlib import Path

from functions.rpn_calc import parseExpressao, executarExpressao
from functions.io_utils import lerArquivo, salvar_tokens
from functions.assembly import gerarAssembly, gerarAssemblyMultiple, save_assembly, save_registers_inc

# --- caminhos base do projeto ---
BASE_DIR    = Path(__file__).resolve().parents[1]        # raiz do repo
INPUTS_DIR  = BASE_DIR / "inputs"                        # raiz/inputs
OUT_TOKENS  = BASE_DIR / "outputs" / "tokens" / "tokens_gerados.txt"
OUT_ASM_DIR = BASE_DIR / "outputs" / "assembly"          # raiz/outputs/assembly

# garante pastas de saída
OUT_ASM_DIR.mkdir(parents=True, exist_ok=True)
OUT_TOKENS.parent.mkdir(parents=True, exist_ok=True)

def exibirResultados(vetor_linhas: list[str]) -> None:
    memoria_global = {}
    historico_global = []
    tokens_salvos_txt = []

    for i, linha in enumerate(vetor_linhas, start=1):
        lista_de_tokens = parseExpressao(linha)
        # para salvar tokens “limpos”
        linhas_tokens_recebidos = linha.replace('(', '').replace(')', '').strip().split()
        tokens_salvos_txt.append(linhas_tokens_recebidos)

        resultado = executarExpressao(lista_de_tokens, memoria_global, historico_global)
        if resultado is not None:
            historico_global.append(resultado)
        print(f"Linha {i:02d}: Expressão '{linha}' -> Resultado: {resultado}")

    # salva SEMPRE em raiz/outputs/tokens/tokens_gerados.txt (o io_utils já força a pasta)
    salvar_tokens(tokens_salvos_txt, "tokens_gerados.txt")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro: Especificar caminho do arquivo de teste (ex.: int/teste1.txt ou float/teste2.txt)")
        sys.exit(1)

    # --- resolve caminho da entrada ---
    arg = Path(sys.argv[1])

    # Se o caminho passado (relativo ao diretório atual) existe, usa-o;
    # caso contrário, procura dentro de raiz/inputs/<arg>.
    if (Path.cwd() / arg).exists() or arg.is_absolute():
        entrada = (Path.cwd() / arg).resolve()
    else:
        entrada = (INPUTS_DIR / arg).resolve()

    if not entrada.exists():
        print(f"Erro: arquivo não encontrado: {entrada}")
        sys.exit(1)

    operacoes_lidas = lerArquivo(str(entrada))

    # Exibe caminho relativo à raiz se possível (evita ValueError do relative_to)
    try:
        mostrar = entrada.relative_to(BASE_DIR)
    except ValueError:
        mostrar = entrada
    print(f"\nArquivo de teste: {mostrar}\n")

    exibirResultados(operacoes_lidas)
    print("\n--- FIM DOS TESTES ---\n")

    # --- Geração de código assembly para todas as operações em um único arquivo ---
    codigo_assembly = []

    # tokens foram salvos em raiz/outputs/tokens/tokens_gerados.txt
    linhas = lerArquivo(str(OUT_TOKENS))

    # registers.inc e arquivo único .S em raiz/outputs/assembly
    save_registers_inc(str(OUT_ASM_DIR / "registers.inc"))

    # Preparar lista de todas as operações
    all_tokens = []
    for linha in linhas:
        tokens = linha.split()
        all_tokens.append(tokens)

    # Gerar um único arquivo com todas as operações
    gerarAssemblyMultiple(all_tokens, codigo_assembly)
    nome_arquivo = OUT_ASM_DIR / "programa_completo.S"
    save_assembly(codigo_assembly, str(nome_arquivo))
    print(f"Arquivo {nome_arquivo.name} gerado com sucesso!")
    print(f"Contém {len(all_tokens)} operações RPN em sequência.")

    # Manter compatibilidade: gerar também os arquivos individuais
    print("\nGerando também arquivos individuais para compatibilidade...")
    for i, tokens in enumerate(all_tokens, start=1):
        codigo_individual = []
        gerarAssembly(tokens, codigo_individual)
        nome_arquivo_individual = OUT_ASM_DIR / f"op_{i}.S"
        save_assembly(codigo_individual, str(nome_arquivo_individual))
        print(f"Arquivo {nome_arquivo_individual.name} gerado com sucesso!")

    print("\nPara testar:")
    print("- Flash único: compile e carregue programa_completo.S")
    print("- Flash individual: compile e carregue qualquer arquivo op_X.S")
    print("Monitore a saída serial em 9600 baud para ver os resultados!")
