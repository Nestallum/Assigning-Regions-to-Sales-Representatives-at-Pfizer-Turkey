from ortools.linear_solver import pywraplp
import csv
import sys
import math

distances = []  # Distances brick/agent
index_values = []  # Workloads

# Lecture des charges de travail des bricks
with open('data/bricks_index_values.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Sauter l'en-tête

    for row in csv_reader:
        index_values.append(float(row[1]))  # Ajouter la valeur float (index_value) dans la liste

# Lecture des distances brick/agent
with open('data/brick_rp_distances.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Sauter l'en-tête

    for row in csv_reader:
        distances.append(list(map(float, row[1:])))  # Convertir chaque distance en float

num_bricks = len(index_values)
num_agents = len(distances[0])

# Initial matrix brick/agent
associations = [3, 3, 3, 0, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 0, 2, 2, 2, 3, 3, 3, 3]
initial_matrix = []
for agent in associations:
    agent_list = [0] * num_agents
    agent_list[agent] = 1
    initial_matrix.append(agent_list)

def Solver():

    # Create the linear solver with the GLOP backend (MILP).
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Could not create solver GLOP")
        sys.exit()

    # New matrix to compute with solver
    matrix = []
    is_assigned = []

    # Remplissage de la matrice brick/agent avec variables continues et binaires auxiliaires
    for j in range(num_bricks):
        row = []
        row_assigned = []
        for i in range(num_agents):
            row.append(solver.NumVar(0, 1, f'b{j}a{i}'))  # Variables continues pour assignation partielle
            row_assigned.append(solver.IntVar(0, 1, f'is_assigned_{j}_{i}'))  # Variable binaire d'assignation
        matrix.append(row)
        is_assigned.append(row_assigned)

    # Contrainte des Center bricks
    solver.Add(matrix[3][0] == 1)
    solver.Add(matrix[13][1] == 1)
    solver.Add(matrix[15][2] == 1)
    solver.Add(matrix[21][3] == 1)

    # Contrainte d'appartenance modifiée pour assignation partielle
    for j in range(num_bricks):
        solver.Add(solver.Sum(matrix[j][i] for i in range(num_agents)) == 1)  # 100% de chaque brique doit être couverte

    # Contrainte de charge de travail pour chaque agent
    for i in range(num_agents):
        sum_workloads = solver.Sum(matrix[j][i] * index_values[j] for j in range(num_bricks))
        solver.Add(sum_workloads >= 0.9)  # Limite inférieure
        solver.Add(sum_workloads <= 1.1)  # Limite supérieure

    # Contrainte pour lier matrix[j][i] et is_assigned[j][i]
    M = 1  # Choisir une grande valeur pour M (ici 1 car matrix[j][i] est entre 0 et 1)
    for j in range(num_bricks):
        for i in range(num_agents):
            # if matrix[j][i] > 0 then is_assigned[j][i] must be 1
            solver.Add(matrix[j][i] <= is_assigned[j][i] * M)

    # Minimiser les distances sans réduire les distances avec l'assignation partielle
    sum_distances = solver.Sum(is_assigned[j][i] * distances[j][i] for j in range(num_bricks) for i in range(num_agents))

    # Minimiser par contrainte la disruption avec la matrice initiale
    disruption = solver.Sum(
        is_assigned[j][i] - (2 * is_assigned[j][i] * initial_matrix[j][i]) + initial_matrix[j][i]
        for j in range(num_bricks) for i in range(num_agents)
    )

    solver.Minimize(sum_distances + (disruption * 0.001))  # Minimiser avec epsilon sur la disruption

    #---------------------------------------------------------------------------
    # Resolve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # print("------------------------------------------------")
        for j in range(num_bricks):
            for i in range(num_agents):
                if matrix[j][i].solution_value() > 0:
                    print(f'Brique {j+1} attribuée à l\'agent {i+1} : {matrix[j][i].solution_value()}')
        return solver.Objective().Value() - (0.001 * disruption.solution_value()), disruption.solution_value(), True
    else:
        return 0, 0, False

def find_non_dominated_solutions():
    non_dominated_solutions = []

    sum_distances, disruption, solution_found = Solver()
    non_dominated_solutions.append([sum_distances, disruption])
    # while solution_found:  # Calcul des autres solutions non dominées avec une disruption plus faible
    #     non_dominated_solutions.append([sum_distances, disruption])
    #     sum_distances, disruption, solution_found = Solver(disruption)

    return non_dominated_solutions

# Affichage des solutions
non_dominated_solutions = find_non_dominated_solutions()
print(f"Number of non dominated solutions : {len(non_dominated_solutions)}")
print(f"Non dominated solutions [sum_distances, disruption] :")
for i, (sum_distance, disruption) in enumerate(non_dominated_solutions):
    print(f"    - Solution {i + 1}: {sum_distance}, {disruption}")
