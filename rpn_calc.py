import math

# Constantes
TAM = 10
FIM = TAM - 1
INICIO = 0

OVERFLOW = 1
UNDERFLOW = 2
OK = 3

def push(pilha, topo, valor):
    if topo[0] == FIM:
        print(f"-> Erro: ao tentar empilhar {valor}, pilha cheia!")
        return OVERFLOW
    else:
        topo[0] += 1
        print(f"Push: topo [{topo[0]}] recebe {valor:.2f}")
        pilha[topo[0]] = round(valor, 2)
        return OK

def pop(pilha, topo):
    if topo[0] == INICIO - 1:
        print("-> Erro ao tentar desempilhar, pilha vazia!")
        return None, UNDERFLOW
    else:
        valor = pilha[topo[0]]
        print(f"Pop: devolve {valor:.2f}")
        topo[0] -= 1
        return valor, OK

def is_empty(topo):
    return topo[0] == INICIO - 1

def show(pilha, topo):
    if is_empty(topo):
        print("Pilha está vazia.")
    else:
        print(f"Pilha está com {topo[0] + 1} elemento(s):")
        for i in range(topo[0], INICIO - 1, -1):
            print(f"   Pilha ({i}) = {pilha[i]:.2f}")
    print()

def main():
    pilha = [0.0] * TAM
    topo = [-1]  # Usando lista para simular ponteiro
    print("Digite números reais e operações (+, -, *, /, //, %, ^) posfixados, para terminar <f>:")
    print("Divisão '/' é inteira (truncada), '//' é real (2 casas decimais).")

    while True:
        entrada = input("\n? ").strip()

        if entrada.lower() == 'f':
            break

        try:
            valor = float(entrada)
            r = push(pilha, topo, valor)
            show(pilha, topo)
        except ValueError:
            # Não é número, assume operador
            v2, r2 = pop(pilha, topo)
            v1, r1 = pop(pilha, topo)
            if r1 == OK and r2 == OK:
                try:
                    if entrada == '+':
                        v = v1 + v2
                    elif entrada == '-':
                        v = v1 - v2
                    elif entrada == '*':
                        v = v1 * v2
                    elif entrada == '/':
                        v = float(int(v1) // int(v2))  # divisão inteira truncada
                    elif entrada == '//':
                        v = round(v1 / v2, 2)  # divisão real com 2 casas decimais
                    elif entrada == '%':
                        v = v1 % v2
                    elif entrada == '^':
                        v = math.pow(v1, v2)
                    else:
                        print("-> Erro: operador inválido!")
                        continue
                    r = push(pilha, topo, v)
                except ZeroDivisionError:
                    print("-> Erro: divisão por zero!")
            else:
                print("-> Erro: operação não é possível")
            show(pilha, topo)

if __name__ == "__main__":
    main()