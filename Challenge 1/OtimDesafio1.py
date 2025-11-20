# Desafio 1 - Artigo 8
# Aluno: Leonardo Aparecido Ferreira Souza - RA: 2140543

# Método apresentado no artigo:
    # Definindo o intervalo, tol e x inicial:
a = 8.
b = 9.
tol = 1e-8
x0 = 8.1

def fun1(x):
    return x ** 4 - 8.5 * x ** 3 - 31.0625 * x ** 2 - 7.5 * x + 45      # Função a ser otimizada

def dfun1(x):
    return 4*x**3 - 25.5 * x**2 - 2*31.0625 * x - 7.5

def uoa_otim(f, a, b, x0, tol = 1e-10):
    k = 0                # Iniciando o contador de iterações
    x = x0               # Definindo um x com valor inicial x0
    dx0 = abs(b - a)     # Definindo tamanho do passo

    while True:
        gamma = (f(x + dx0) - f(x)) / dx0       # Derivada da função em um ponto x0

        if abs(f(x)) <= tol:
            break

        if gamma != 0:
            hi = -f(x) / gamma

        if 0 < hi < dx0:
            xi = x + hi
        else:
            xi = x + dx0
        print(x, f(x))

        k += 1
        x = xi                  # Definindo a proxima iteração e repetindo o processo

    solution = {'x_min': x, 'f(x_min)': fun1(x), 'n_iter': k}
    return solution

result = uoa_otim(fun1, a, b, x0, tol)
print('Resultado da otimização 1:', result)         # Neste resultado é encontrado o mínimo local

# Outra maneira de encontrar o mínimo global é:
from scipy.optimize import minimize_scalar as min    # Biblioteca com função de otimizar/encontar o min de funções

def fun1(x):
    return x**4 - 8.5 * x**3 - 31.0625 * x**2 - 7.5 * x + 45

result = min(fun1, bounds=(8.0, 9.0), method='bounded')     # O termo "method='bounded'" é aplicado para selecionar
                                                            # o método a ser aplicado pela biblioteca
print("Resultado da otimização 2:", result.x)               # Neste resulatdo é encontrado o mínimo global
