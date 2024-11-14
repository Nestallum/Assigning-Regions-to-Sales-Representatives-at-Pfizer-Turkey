from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import csv
import sys
import math

distances = []  # Distances brick/agent
index_values = []  # Workloads

# Lecture des charges de travail des bricks
with open('data/bricks_index_values.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        index_values.append(float(row[1]))

# Lecture des distances brick/agent
with open('data/brick_rp_distances.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        distances.append(list(map(float, row[1:])))

num_bricks = len(index_values)
num_agents = len(distances[0])

# Initial matrix brick/agent
associations = [3, 3, 3, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 0, 2, 2, 2, 3, 3, 3, 3]
initial_matrix = []
for agent in associations:
    agent_list = [0] * num_agents
    agent_list[agent] = 1
    initial_matrix.append(agent_list)

def Solver(upper_bound_disruption):

    # CBC backend solver (MILP).
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Could not create solver CBC")
        sys.exit()

    matrix = [] # Matrice de variables continues pour allocation partielle
    x = []  # Variables binaires x[j][i] vaut 1 si un agent i est affecté à une brique j
    steps = []  # Variables entières pour les steps (de 0 à 5)

    for j in range(num_bricks):
        row = []
        row_x = []
        row_steps = []
        for i in range(num_agents):
            row.append(solver.NumVar(0, 1, f'b{j}a{i}'))  # Variable continue
            row_x.append(solver.BoolVar(f'x{j}a{i}'))  # Variable binaire
            row_steps.append(solver.IntVar(0, 5, f'steps_{j}_{i}'))  # Nombre de paliers d'allocation (0 à 5)
        matrix.append(row)
        x.append(row_x)
        steps.append(row_steps)

    # Contrainte des bricks centrales
    solver.Add(matrix[3][0] == 1)
    solver.Add(matrix[13][1] == 1)
    solver.Add(matrix[15][2] == 1)
    solver.Add(matrix[21][3] == 1)

    # Contrainte d'appartenance partielle (somme des fractions = 1 pour chaque brique)
    for j in range(num_bricks):
        solver.Add(solver.Sum(matrix[j][i] for i in range(num_agents)) == 1)

    # Contrainte de charge de travail pour chaque agent
    for i in range(num_agents):
        sum_workloads = solver.Sum(matrix[j][i] * index_values[j] for j in range(num_bricks))
        solver.Add(sum_workloads >= 0.8)
        solver.Add(sum_workloads <= 1.2)

    # Contrainte qui lie les steps à la matrice d'allocation
    for j in range(num_bricks):
        for i in range(num_agents):
            solver.Add(matrix[j][i] == 0.2 * steps[j][i])  # Lier matrix[j][i] aux steps
            solver.Add(matrix[j][i] >= 0.2 * x[j][i])  # Si x[j][i] est 1, matrix[j][i] doit être au moins 0.2
            solver.Add(matrix[j][i] <= x[j][i])  # Si matrix[j][i] > 0, x[j][i] doit être 1

    # Calcul des distances en fonction de l'affectation
    sum_distances = solver.Sum(distances[j][i] * x[j][i] for j in range(num_bricks) for i in range(num_agents))

    # Calcul de la disruption avec la valeur absolue
    disruption_vars = []
    for j in range(num_bricks):
        for i in range(num_agents):
            abs_diff = solver.NumVar(0, solver.infinity(), f'abs_diff_{j}_{i}')
            solver.Add(abs_diff >= matrix[j][i] - initial_matrix[j][i])
            solver.Add(abs_diff >= -(matrix[j][i] - initial_matrix[j][i]))
            disruption_vars.append(abs_diff)

    # Somme des disruptions absolues
    disruption = solver.Sum(disruption_vars)
    solver.Add(disruption <= upper_bound_disruption - 0.001)

    # Fonction objective
    solver.Minimize(sum_distances + (disruption * 0.001))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print('Solution optimale trouvée:')
        for j in range(num_bricks):
            for i in range(num_agents):
                if matrix[j][i].solution_value() > 0:
                    print(f'Brique {j+1} attribuée à l\'agent {i+1} : {matrix[j][i].solution_value()}')
        print('Valeur objective =', solver.Objective().Value())
        return solver.Objective().Value() - (0.001 * disruption.solution_value()), disruption.solution_value(), True
    else:
        return 0, 0, False

def find_non_dominated_solutions(): 
    non_dominated_solutions = []

    sum_distances, disruption, solution_found = Solver(math.inf)
    
    while solution_found:
        non_dominated_solutions.append([sum_distances, disruption])
        sum_distances, disruption, solution_found = Solver(disruption)
        
    return non_dominated_solutions

def plot_graph_distance_disruption(non_dominated_solutions):
    distances = [point[0] for point in non_dominated_solutions]
    disruptions = [point[1] for point in non_dominated_solutions]

    plt.figure(figsize=(8, 6))
    colors = cm.rainbow(np.linspace(0, 1, len(non_dominated_solutions)))

    for i, (x, y) in enumerate(zip(distances, disruptions)):
        plt.scatter(x, y, color=colors[i], marker='o', label=f'Solution {i + 1}')
        plt.text(x, y, f'S{i + 1}', fontsize=9, ha='right', va='bottom')

    plt.xlabel('Distance')
    plt.ylabel('Disruption')
    plt.title('Graphique Distance vs Disruption (Allocation par paliers de 0.2)')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()

def main():
    print("Recherche de solutions avec allocation partielle par palier...")
    non_dominated_solutions = find_non_dominated_solutions()

    print(f"Nombre de solutions non dominées: {len(non_dominated_solutions)}")

    # Affichage des solutions
    # print("Solutions non dominées [distance, disruption]:")
    # for i, (sum_distance, disruption) in enumerate(non_dominated_solutions):
    #     print(f"    - Solution {i + 1}: {sum_distance}, {disruption}")

    plot_graph_distance_disruption(non_dominated_solutions)

if __name__ == "__main__":
    main()
