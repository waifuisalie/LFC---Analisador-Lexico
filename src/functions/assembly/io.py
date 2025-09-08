def save_assembly(codigo_assembly: list[str], nome_arquivo="programa.s") -> bool:
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            for linha in codigo_assembly:
                arquivo.write(linha + '\n')
        print(f"Código Assembly salvo em: {nome_arquivo} (16-bit version)")
        return True
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")
        return False