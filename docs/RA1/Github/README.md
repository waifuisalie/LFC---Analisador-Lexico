# LFC — Analisador Léxico Completo

> **Informação do Grupo**  
> Linguagens Formais e Compiladores — 9º Período — Engenharia da Computação — PUCPR  
> Alunos: Breno Rossi Duarte — Francisco Bley Ruthes — Rafael Olivare Piveta — Stefan Benjamim Seixas Lourenço Rodrigues

## Visão Geral

Este projeto implementa um **sistema completo de processamento RPN** com:

- **Analisador léxico** baseado em Autômatos Finitos para tokenização completa
- **Processador RPN avançado** com operações aritméticas, lógicas e de comparação
- **Estruturas de controle** completas (IFELSE, WHILE, FOR)
- **Sistema de variáveis** com memória persistente
- **Comando RES** para acesso ao histórico de resultados
- **Gerador de código Assembly** AVR (ATmega328P / Arduino Uno)
- **Suporte completo** a números inteiros e de ponto flutuante


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
│  └─ RA1/
├─ flowcharts/
│  └─ RA1/                        # Diagramas dos fluxogramas em assembly
├─ inputs/
│  └─ RA1/
│     ├─ int/                     # Arquivos de teste com inteiros
│     └─ float/                   # Arquivos de teste com reais
├─ outputs/
│  └─ RA1/
│     ├─ assembly/                # Saída: programa_completo.S, registers.inc
│     └─ tokens/
│        └─ tokens_gerados.txt    # Saída: tokens gerados a partir do último input
├─ src/
│  └─ RA1/
│     └─ functions/
│        ├─ assembly/             # Módulos de geração de Assembly
│        └─ python/
│           ├─ __init__.py
│           ├─ analisador_lexico.py     
│           ├─ io_utils.py            
│           ├─ rpn_calc.py        # Processador RPN completo
│           └─ tokens.py                
├─ AnalisadorLexico.py            # Ponto de entrada principal
├─ teste1.txt, teste2.txt, teste3.txt  # Arquivos de teste na raiz
└─ README.md
```



## Como Executar

### Sintaxe Básica
```bash
# Na raiz do projeto
python3 AnalisadorLexico.py <arquivo_de_teste>
```

### Exemplos de Uso
```bash
# Testes básicos
python3 AnalisadorLexico.py teste1.txt
python3 AnalisadorLexico.py teste2.txt
python3 AnalisadorLexico.py teste3.txt

# Testes em subpastas
python3 AnalisadorLexico.py inputs/RA1/int/teste1_assembly.txt
python3 AnalisadorLexico.py inputs/RA1/float/teste1.txt
```

### Sistema de Busca Inteligente
O sistema procura automaticamente o arquivo em:
- Diretório atual
- Raiz do projeto
- Pasta `inputs/RA1/`

  

## Funcionalidades Implementadas

### 🔢 **Operações Aritméticas**
- `+` Soma
- `-` Subtração  
- `*` Multiplicação
- `/` Divisão (com detecção de divisão por zero)
- `%` Módulo (resto da divisão)
- `^` Potenciação

### 🔍 **Operadores de Comparação**
- `<` Menor que
- `>` Maior que
- `==` Igual a
- `<=` Menor ou igual
- `>=` Maior ou igual
- `!=` Diferente de

### 🧠 **Operadores Lógicos**
- `&&` E lógico (AND)
- `||` Ou lógico (OR)
- `!` Não lógico (NOT)

### 🔄 **Estruturas de Controle**

#### IFELSE - Estrutura Condicional
```
Sintaxe: (IFELSE (condição) (verdadeiro) (falso))
Exemplo: (IFELSE (A B >) (1) (0))
```

#### WHILE - Loop Condicional
```
Sintaxe: (WHILE (condição) (corpo))
Exemplo: (WHILE (X 5 <) ((X X 1 +)(Y X 2 *)))
```

#### FOR - Loop com Contador
```
Sintaxe: (FOR (inicial) (final) (incremento) (corpo))
Exemplo: (FOR (1) (10) (2) ((P P 1 +)(Q P 2 *)))
```

### 💾 **Sistema de Variáveis**
- **Declaração:** `(VARIAVEL valor)`
- **Atribuição:** `(VARIAVEL expressão)`
- **Uso:** Variáveis podem ser referenciadas em qualquer expressão
- **Escopo:** Global - variáveis persistem entre expressões

### 📊 **Comando RES - Histórico**
```
Sintaxe: (N RES) ou (RES) para último resultado
Exemplos:
  (1 RES)  # Último resultado
  (3 RES)  # Terceiro resultado mais recente
```

### 🔢 **Suporte a Números**
- **Inteiros:** `1`, `42`, `100`
- **Decimais:** `3.14`, `2.5`, `0.001`
- **Precisão:** Arredondamento para 2 casas decimais (simulação 16-bit)
  

## Arquitetura dos Módulos

### 🏗️ **Módulos Principais**

- **`tokens.py`**: Define todos os tipos de token suportados (números, operadores, estruturas de controle, variáveis, parênteses) e a classe Token
- **`analisador_lexico.py`**: Implementa o analisador léxico (DFA) que reconhece números, operadores, palavras-chave (WHILE, FOR, IFELSE, RES) e variáveis
- **`rpn_calc.py`**: Processador RPN completo com:
  - `parseExpressao()`: Tokenização de expressões
  - `executarExpressao()`: Executor principal com detecção de estruturas de controle
  - `processarIFELSE()`, `processarWHILE()`, `processarFOR()`: Processadores específicos
  - `processarTokens()`: Avaliador RPN tradicional com pilha
- **`io_utils.py`**: Utilitários de entrada/saída para leitura de arquivos e salvamento de tokens
- **`assembly/`**: Módulos de geração de código Assembly AVR completo

### 🔄 **Fluxo de Execução**

1. **Tokenização**: Análise léxica converte texto em tokens
2. **Detecção**: Sistema identifica estruturas de controle vs. expressões simples  
3. **Processamento**: 
   - Estruturas de controle → Processadores específicos
   - Expressões simples → Avaliador RPN tradicional
4. **Execução**: Avaliação com pilha, memória de variáveis e histórico
5. **Assembly**: Geração de código ATmega328P para todas as operações

  

## Exemplos de Execução

### 🧮 **Teste Básico (teste1.txt)**
```
Linha 01: Expressão '(4 2 +)' -> Resultado: 6.0
Linha 02: Expressão '(6 3 /)' -> Resultado: 2.0
Linha 03: Expressão '(5 2 ^)' -> Resultado: 25.0
Linha 04: Expressão '(7 2 %)' -> Resultado: 1.0
```

### 🔄 **Teste com Estruturas de Controle (teste2.txt)**
```
Linha 01: Expressão '(A 5)' -> Resultado: 5.0
Linha 02: Expressão '(B 3)' -> Resultado: 3.0
Linha 09: Expressão '(IFELSE ((A B >) (C D <=) &&)(1)(0))' -> Resultado: 1.0
Linha 12: Expressão '(WHILE (X 5 <)((X X 1 +)(Y X 2 *)))' -> Resultado: 10.0
Linha 17: Expressão '(FOR (1)(10)(2)((P P 1 +)(Q P 2 *)))' -> Resultado: 10.0
```

### 🔢 **Teste com Float (teste3_float.txt)**
```
Linha 01: Expressão '(A 5.5)' -> Resultado: 5.5
Linha 07: Expressão '(G (A 2.5 ^))' -> Resultado: 70.94
Linha 12: Expressão '(WHILE (X 5.5 <)((X X 1.2 +)(Y X 2.3 *)))' -> Resultado: 14.95
Linha 25: Expressão '(NEGACAO ((A B ==) !))' -> Resultado: 1.0
```

### 📤 **Saída Típica**
```
--- FIM DOS TESTES ---

Arquivo outputs/RA1/assembly/registers.inc criado com sucesso (16-bit version).
Código Assembly salvo em: outputs/RA1/assembly/programa_completo.S (16-bit version)
Contém 22 operações RPN em sequência.

Para testar:
- Compile e carregue programa_completo.S no Arduino Uno
- Monitore a saída serial em 9600 baud para ver os resultados!
```

  
## Sintaxe RPN Detalhada

### 📝 **Regras Gerais**
- **Notação Pós-fixa**: Operadores vêm após os operandos
- **Parênteses**: Usados para agrupamento `(expressão)`
- **Espaços**: Ignorados pelo analisador léxico

### 🔧 **Exemplos de Sintaxe**

#### Operações Aritméticas
```
(3 2 +)           # 3 + 2 = 5
(10 3 -)          # 10 - 3 = 7
(4 5 *)           # 4 * 5 = 20
(15 3 /)          # 15 / 3 = 5
(17 5 %)          # 17 % 5 = 2
(2 8 ^)           # 2^8 = 256
```

#### Comparações e Lógica
```
(5 3 >)           # 5 > 3 = 1.0 (true)
(A B ==)          # A == B = 0.0 ou 1.0
((A B >) (C D <) &&)  # (A>B) AND (C<D)
((X 0 !=) !)      # NOT(X != 0)
```

#### Estruturas de Controle
```
# IF-ELSE
(IFELSE (X 0 >) (X) (X -))

# WHILE com múltiplas expressões no corpo
(WHILE (i 10 <) ((i i 1 +)(soma soma i +)))

# FOR com contador e múltiplas operações
(FOR (1) (5) (1) ((produto produto i *)(contador contador 1 +)))
```

#### Variáveis e Histórico
```
(resultado (A B +))    # Atribui A+B à variável 'resultado'  
(ultimo (1 RES))       # último resultado
(anterior (3 RES))     # terceiro resultado mais recente
```

## Compilação e Teste do Assembly

### 🔨 **Preparação**
1. Instale **AVR-GCC** ou use **PlatformIO** com Arduino Uno
2. Copie os arquivos gerados:
   - `outputs/RA1/assembly/registers.inc`
   - `outputs/RA1/assembly/programa_completo.S`

### ⚡ **Compilação**
```bash
# Com AVR-GCC
avr-gcc -mmcu=atmega328p programa_completo.S -o programa.elf
avr-objcopy -O ihex programa.elf programa.hex
avrdude -p atmega328p -c arduino -P /dev/ttyUSB0 -b 115200 -U flash:w:programa.hex
```

### 📊 **Monitoramento**
- **Baud Rate**: 9600
- **Saída**: Resultados das operações RPN em sequência
- **Debug**: Informações de pilha e registradores

## Recursos Avançados

### 🎯 **Detecção Inteligente**
- **Estruturas vs Expressões**: Sistema detecta automaticamente o tipo de processamento necessário
- **Aninhamento**: Suporte completo a expressões aninhadas complexas
- **Validação**: Verificação sintática e semântica em tempo de execução

### 🔄 **Controle de Fluxo**
- **Loops Seguros**: Limite de 1000 iterações para prevenir loops infinitos
- **Condições Robustas**: Avaliação correta de expressões booleanas
- **Múltiplas Expressões**: Corpo de loops pode conter várias operações

### 💾 **Gestão de Memória**
- **Variáveis Globais**: Escopo compartilhado entre todas as expressões
- **Histórico Persistente**: Acesso a resultados anteriores via RES
- **Inicialização Automática**: Variáveis inicializadas com 0.0 se necessário

## Materiais de Apoio

- **Fluxogramas**: `flowcharts/RA1/` - Diagramas de fluxo das operações Assembly
- **Testes Exemplo**: `inputs/RA1/int/` e `inputs/RA1/float/` - Casos de teste abrangentes  
- **Saídas**: `outputs/RA1/` - Assembly e tokens gerados automaticamente
- **Documentação**: Este README com exemplos completos e sintaxe detalhada

---

## 🎉 **Status do Projeto**

✅ **Analisador Léxico** - Completo  
✅ **Processador RPN** - Completo  
✅ **Operações Aritméticas** - Completo  
✅ **Operadores Lógicos** - Completo  
✅ **Estruturas de Controle** - Completo  
✅ **Sistema de Variáveis** - Completo  
✅ **Comando RES** - Completo  
✅ **Geração Assembly** - Completo  
✅ **Suporte Float** - Completo  

**Sistema 100% funcional e testado!** 🚀

