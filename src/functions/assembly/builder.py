# builder.py
from typing import List
from .header import gerar_header
from .data_section import gerar_secao_dados
from .code_section import gerar_secao_codigo
from .footer import gerar_footer
from .routines import gerar_rotinas_auxiliares

def gerarAssembly(tokens: list[str], codigoAssembly: List[str]) -> None:
    codigoAssembly.clear()
    gerar_header(codigoAssembly)
    gerar_secao_dados(codigoAssembly)
    gerar_secao_codigo(codigoAssembly, tokens)
    gerar_rotinas_auxiliares(codigoAssembly)
    gerar_footer(codigoAssembly)
