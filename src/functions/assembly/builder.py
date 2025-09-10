# builder.py
from typing import List
from .header import gerar_header
from .data_section import gerar_secao_dados
from .code_section import gerar_secao_codigo_multiplo
from .footer import gerar_footer
from .routines import gerar_rotinas_auxiliares

def gerarAssemblyMultiple(all_tokens: List[List[str]], codigoAssembly: List[str]) -> None:
    """Gera código assembly para múltiplas operações em um único arquivo."""
    codigoAssembly.clear()
    gerar_header(codigoAssembly)
    gerar_secao_dados(codigoAssembly)
    gerar_secao_codigo_multiplo(codigoAssembly, all_tokens)
    gerar_rotinas_auxiliares(codigoAssembly)
    gerar_footer(codigoAssembly)
