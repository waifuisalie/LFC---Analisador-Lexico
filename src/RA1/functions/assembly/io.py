from pathlib import Path

def save_assembly(codigo_assembly: list[str], nome_arquivo: str | Path = "programa.s") -> bool:
    try:
        caminho_arquivo = Path(nome_arquivo)
        caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

        with caminho_arquivo.open('w', encoding='utf-8') as arquivo:
            for linha in codigo_assembly:
                arquivo.write(linha + '\n')

        print(f"Código Assembly salvo em: {caminho_arquivo} (16-bit version)")
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo Assembly: {e}")
        return False
