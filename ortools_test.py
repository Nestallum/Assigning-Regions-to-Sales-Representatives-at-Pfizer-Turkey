from ortools.linear_solver import pywraplp

# Crée un solveur linéaire avec le backend CBC (open-source solver)
solver = pywraplp.Solver.CreateSolver('GLOP')

# Variables
x = solver.NumVar(0, 1, 'x')
y = solver.NumVar(0, 2, 'y')

# Contrainte : x + y <= 2
solver.Add(x + y <= 2)

# Fonction objectif : Maximize x + y
solver.Maximize(x + y)

# Résoudre
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('x =', x.solution_value())
    print('y =', y.solution_value())
    print('Objective value =', solver.Objective().Value())
else:
    print('Le solveur n\'a pas trouvé de solution optimale.')
