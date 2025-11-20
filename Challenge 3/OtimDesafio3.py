# Desafio 3 - Otimização
# Problema do caixeiro viajante resolvido em Python

import pyomo.environ as pyo
import cplex

# Definindo as variáveis:
cidades = ['São Paulo', 'Campinas', 'Santos', 'Cascavel', 'Francisco Beltrão']
dist = [[0, 97.4, 81.4, 928., 894.],
        [97.4, 0, 189., 868., 869.],
        [81.4, 189., 0, 925., 890.],
        [928., 868., 925., 0, 179.],
        [894., 869., 890., 179., 0]]
n = len(dist)

# Definindo os modelos:
modelo = pyo.ConcreteModel()
modelo.I = range(n)
modelo.J = range(n)
modelo.U = range(1,n)

# Definindo as variáveis de decisão:
modelo.x = pyo.Var(modelo.I, modelo.J, within = pyo.Binary)
modelo.u = pyo.Var(modelo.I, within = pyo.NonNegativeIntegers, bounds = (0, n-1))

# Definindo os parâmetros:
modelo.dist= pyo.Param(modelo.I, modelo.J, initialize = lambda modelo, i, j: dist[i][j])

# Definindo a função objetivo:
def f_obj(mod):
     return sum(sum(mod.x[i, j] * mod.dist[i, j] for i in mod.I) for j in mod.J)
modelo.objetivo = pyo.Objective(rule = f_obj, sense = pyo.minimize)

# Definindo as restrições:
def rest1(mod, i):
     return sum(mod.x[i, j] for j in mod.J if i != j) == 1
modelo.rest1 = pyo.Constraint(modelo.I, rule = rest1)

def rest2(mod, j):
     return sum(mod.x[i, j] for i in mod.I if i != j) == 1
modelo.rest2 = pyo.Constraint(modelo.J, rule = rest2)

def rest3(mod, i, j):
     if i != j:
         return mod.u[i] - mod.u[j] + mod.x[i, j] * (n) <= n - 1
     else:
         return mod.u[i] - mod.u[j] == 0
modelo.rest3 = pyo.Constraint(modelo.U, modelo.J, rule = rest3)

# Resolvendo o modelo:
opt = pyo.SolverFactory('cplex_direct')
resultado = opt.solve(modelo)

print('\n Apresentando as informações da solução:')
resultado.write()

print('\n Apresentando as informações das variáveis de decisão:')
modelo.x.pprint()

print('\n Apresentando as informações da função objetivo: \n')
modelo.objetivo.pprint()

print('\n Apresentando as informações das restrições:')
modelo.rest1.pprint()
modelo.rest1.display()
modelo.rest2.pprint()
modelo.rest2.display()
modelo.rest3.pprint()
modelo.rest3.display()

print('\nApresentando as rotas a serem feitas:\n')
l = list(modelo.x.keys())
for i in l:
    if modelo.x[i]() != 0:
        print(i,'--', modelo.x[i]())
