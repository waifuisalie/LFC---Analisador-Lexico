# LFC — Analisador Léxico

> **Informação do Grupo**  
> Linguagens Formais e Compiladores — 9º Período — Engenharia da Computação — PUCPR  
> Alunos: Breno Rossi Duarte — Francisco Bley Ruthes — Rafael Olivare Piveta — Stefan Benjamim Seixas Lourenço Rodrigues

## Visão Geral

Este projeto implementa:

- Um analisador léxico baseado em Autômatos Finitos para tokenizar expressões matemáticas em notação polonesa reversa (RPN).
- Um avaliador de expressões RPN com suporte a operações aritméticas, memória e histórico.
- Um gerador de código Assembly AVR (ATmega328P / Arduino Uno), produzindo um arquivo `.S` por linha de expressão.


> **Fluxo resumido**
>
> 1. Forneça um arquivo de entrada com uma expressão RPN por linha.  
> 2. O sistema tokeniza e avalia cada linha, mostrando os resultados no terminal.  
> 3. Os tokens “limpos” de todas as linhas são salvos em `outputs/tokens/tokens_gerados.txt`.  
> 4. Para cada linha, é gerado um arquivo Assembly em `outputs/assembly/op_X.S`.



## Estrutura de Pastas

```text
LFC---Analisador-Lexico/
├─ docs/
│  └─ flowcharts/                 # Diagramas dos fluxogramas em assembly
├─ inputs/
│  ├─ int/                        # Arquivos de teste com inteiros
│  └─ float/                      # Arquivos de teste com reais
├─ outputs/
│  ├─ assembly/                   # Saída: op_1.S, op_2.S, ..., registers.inc
│  └─ tokens/
│     └─ tokens_gerados.txt       # Saída: tokens gerados a partir do último input
└─ src/
   ├─ functions/
   │  ├─ __init__.py
   │  ├─ analisador_lexico.py     
   │  ├─ gerar_assembly.py       
   │  ├─ io_utils.py            
   │  ├─ rpn_calc.py              
   │  └─ tokens.py                
  └─ main.py                     

```



## Como rodar:

```powershell
# Raiz do código (LFC---ANALISADOR-LEXICO)
python .\src\main.py .\inputs\int\teste1_assembly.txt
```

  

## Sintaxe e Semântica de RPN Suportadas
```
-> Operadores

  - `+` soma
  - `_` subtração
  - `*` multiplicação
  - `/` divisão (com detecção de divisão por zero)
  - `%` resto da divisão inteira
  - `^` exponenciação



-> Comandos Especiais

  *MEM*
      - Se a pilha contiver um número no topo, armazena esse valor em memória interna e retorna-o ao topo.
      - Se a pilha não contiver número, retorna o último valor armazenado em MEM.
      - Se MEM ainda não tiver sido inicializado, registra erro e empilha 0.0.

  *RES*
      - Espera um índice N no topo da pilha e empilha o resultado obtido há N avaliações atrás.
      - Exemplo: `5 RES` pega o quinto resultado mais recente.
      - Índices fora do alcance resultam em erro e 0.0.



-> Números

  - Números reais são aceitos no léxico e arredondados para simular precisão de 16 bits (duas casas decimais) na avaliação.
```
  

## Arquitetura dos Módulos

  - **functions/tokens.py:** Define os tipos de token (`NUMERO_REAL`, `SOMA`, `SUBTRACAO`, `MULT`, `DIV`, `RESTO`, `POT`, `ABRE_PARENTESES`, `FECHA_PARENTESES`, `RES`, `MEM`, `FIM`) e a classe Token.
  - **functions/analisador_lexico.py:** Implementa o analisador léxico (DFA): ignora espaços, reconhece números, comandos (MEM, RES) e operadores; lança erro para caracteres inválidos.
  - **functions/rpn_calc.py:** `parseExpressao(linha)` chama o léxico e filtra parênteses. `executarExpressao(tokens, memoria, historico)` executa a expressão em pilha, trata erros, atualiza memória e histórico.
  - **functions/io_utils.py:** `lerArquivo(caminho)` lê linhas não vazias. `salvar_tokens(tokens, nome)` sempre salva em `outputs/tokens/<nome>` (criando as pastas).
  - **functions/gerar_assembly.py:** Gera o código Assembly completo para ATmega328P, incluindo cabeçalho, seção de dados, rotinas de pilha de 16 bits, aritmética e UART. Fornece `save_registers_inc()` e `save_assembly()` para gravar os arquivos.
  - **src/main.py:** Ponto de entrada. Resolve caminhos de entrada de forma robusta, executa o pipeline, salva tokens e gera `.S` para cada linha.

  

## Exemplo de Saída no Console

  Arquivo de teste: `inputs\int\teste1_assembly.txt`
  ```
  Linha 01: Expressão '(3 2 +)' -> Resultado: 5.0
  Linha 02: Expressão '(10 4 -)' -> Resultado: 6.0
  Linha 03: Expressão '(2 3 *)' -> Resultado: 6.0
  Linha 04: Expressão '(9 2 /)' -> Resultado: 4.5
  Linha 05: Expressão '(10 3 %)' -> Resultado: 1.0
  Linha 06: Expressão '(2 3 ^)' -> Resultado: 8.0
  Linha 07: Expressão '((1 2 +) (3 4 *) /)' -> Resultado: 0.25
  Linha 08: Expressão '(5 MEM)' -> Resultado: 5.0
  Linha 09: Expressão '(MEM)' -> Resultado: 5.0
  Linha 10: Expressão '(5 RES)' -> Resultado: 1.0

  --- FIM DOS TESTES ---

  Arquivo outputs/assembly/registers.inc criado com sucesso (16-bit version).
  Código Assembly salvo em: outputs/assembly/op_1.S (16-bit version)
  ```

  
## Compilação e Teste do Assembly

  1. Abra um projeto configurado para AVR-GCC ou PlatformIO com alvo ATmega328P (Arduino Uno).
  2. Copie de `outputs/assembly/` os arquivos `registers.inc` e algum `op_X.S`.
  3. Compile e carregue no Arduino Uno.
  4. Monitore a saída serial configurada em 9600 baud para depuração e resultado.

  

## Materiais de Apoio

  - Fluxogramas em `docs/flowcharts/`.
  - Exemplos de entradas em `inputs/int/` e `inputs/float/`.
  - Saídas geradas automaticamente em `outputs/`.

