## Informação do Grupo
Linguagens Formais e Compiladores - 9º Período - Eng. Computação - PUCPR

Breno Rossi Duarte

Francisco Bley Ruthes

Rafael Olivare Piveta

Stefan Benjamim Seixas Lourenço Rodrigues

## Analisador Léxico
Desenvolvimento de um analisador léxico com Autômatos Finitos para processar expressões em notação polonesa reversa (RPN) e gerar código Assembly compatível com Arduino.

## 📌 Descrição
Este projeto implementa um **analisador léxico** e **avaliador de expressões matemáticas em Notação Polonesa Reversa (RPN)**.  
Ele permite:

- Processar arquivos contendo expressões em RPN.
- Executar operações matemáticas básicas (`+ - * / % ^`).
- Usar comandos especiais:
  - `MEM` → armazenar e recuperar valores em memória.
  - `RES` → acessar resultados anteriores.
- Gerar um arquivo **`tokens_gerados.txt`** com os tokens das últimas 10 execuções.

  # Rodar programa
  Para rodar o programa digite o seguinte comando no terminal `.\python rpn_calc.py` seguido do arquivos de teste `teste1.txt`
