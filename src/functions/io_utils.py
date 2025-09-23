# io_utils.py

from pathlib import Path

def lerArquivo(nomeArquivo: str):
    try:
        with open(nomeArquivo, 'r', encoding="utf-8") as arquivos_teste:
            return [linha.strip() for linha in arquivos_teste if linha.strip()]
    except FileNotFoundError:
        print(f'ERRO -> Arquivo não encontrado: {nomeArquivo}')
        return []

def salvar_tokens(tokens_por_linha, nome_arquivo="tokens_gerados.txt"):
    try:
        raiz = Path(__file__).resolve().parents[2]   # .../LFC---ANALISADOR-LEXICO
        pasta_destino = raiz / "outputs" / "tokens"
        pasta_destino.mkdir(parents=True, exist_ok=True)

        destino = pasta_destino / Path(nome_arquivo).name  # garante só o nome do arquivo
        with destino.open("w", encoding='utf-8') as f:
            for lista_de_tokens in tokens_por_linha:
                f.write(" ".join(lista_de_tokens) + "\n")
        return True
    except Exception as e:
        print(f'ERRO -> Falha ao escrever os tokens no arquivo {e}')
        return False
