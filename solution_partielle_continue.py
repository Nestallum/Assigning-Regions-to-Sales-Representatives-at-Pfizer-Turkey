from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import csv
import sys
import math

distances = [] # Distances brick/agent
index_values = [] # Workloads

# Lecture des charges de travail des bricks
with open('data/bricks_index_values.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
        
    for row in csv_reader:
            index_values.append(float(row[1]))  # Ajouter la valeur float (index_value) dans la liste

# Lecture des distances brick/agent
with open('data/brick_rp_distances.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
        
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
        
def Solver(upper_bound_disruption) :

    # CBC backend solver (MILP).
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Could not create solver CBC")
        sys.exit()

    # Matrice de variables continues pour allocation partielle et steps
    matrix = []

    # Remplissage de la matrice brick/agent
    for j in range(num_bricks):
        row = []
        for i in range(num_agents):
            row.append(solver.NumVar(0, 1, f'b{j}a{i}'))  # Ajouter brick_j_agent_i
        matrix.append(row)

    # Contrainte des Center bricks
    solver.Add(matrix[3][0] == 1)
    solver.Add(matrix[13][1] == 1)
    solver.Add(matrix[15][2] == 1)
    solver.Add(matrix[21][3] == 1)

    # Contrainte d'appartenance
    for j in range(num_bricks):
        solver.Add(solver.Sum(matrix[j][i] for i in range(num_agents)) == 1) # Un seul agent par brick

    # Contrainte charge de travail
    for i in range(num_agents):
        sum_workloads = solver.Sum(matrix[j][i] * index_values[j] for j in range(num_bricks))
        solver.Add(sum_workloads >= 0.8)
        solver.Add(sum_workloads <= 1.2)
        
    # Minimiser les distances
    sum_distances = solver.Sum(matrix[j][i] * distances[j][i] for j in range(num_bricks) for i in range(num_agents))
    
   # Variables pour la valeur absolue
    disruption_vars = []
    for j in range(num_bricks):
        for i in range(num_agents):
            # Variable pour la valeur absolue de la différence
            abs_diff = solver.NumVar(0, solver.infinity(), f'abs_diff_{j}_{i}')
            
            # Ajout de contraintes linéaires pour modéliser la valeur absolue
            solver.Add(abs_diff >= matrix[j][i] - initial_matrix[j][i])   # ax + b - yi
            solver.Add(abs_diff >= -(matrix[j][i] - initial_matrix[j][i]))  # -(ax + b - yi)
            
            disruption_vars.append(abs_diff)

    # Fonction objectif avec somme des disruptions absolues
    disruption = solver.Sum(disruption_vars)
    solver.Add(disruption <= upper_bound_disruption - 0.001) # Trouver la nouvelle meilleure disruption

    solver.Minimize(sum_distances+(disruption*0.001)) # Ajout d'un petit epsilon sur la disruption pour choisir la valeur non dominée en cas d'égalité
    #---------------------------------------------------------------------------

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # Affichage d'une solution avec association brick-agent et valeur objective
        # print('Solution optimale trouvée:')
        # for j in range(num_bricks):
        #     for i in range(num_agents):
        #         if matrix[j][i].solution_value() == 1:
        #             print(f'Brique {j+1} attribuée à l\'agent {i+1}')
        # print('Valeur objective =', solver.Objective().Value())
        return solver.Objective().Value()-(0.001*disruption.solution_value()), disruption.solution_value(), True
    else:
        # print('Le solveur n\'a pas trouvé de solution optimale.')
        return 0, 0, False
        
def find_non_dominated_solutions(): 
    non_dominated_solutions = []

    sum_distances, disruption, solution_found = Solver(math.inf) 
    
    while(solution_found): # Calcul des autres solutions non dominées avec une disruption plus faible
        non_dominated_solutions.append([sum_distances, disruption])
        sum_distances, disruption, solution_found = Solver(disruption)
        
    return non_dominated_solutions

def plot_graph_distance_disruption(non_dominated_solutions):
    # Séparation des distances et disruptions
    solutions_to_plot = non_dominated_solutions[0::1000] # 1 solution par pas de 1000
    distances = [point[0] for point in solutions_to_plot]
    disruptions = [point[1] for point in solutions_to_plot]

    plt.figure(figsize=(8, 6))

    colors = cm.rainbow(np.linspace(0, 1, len(solutions_to_plot)))

    for i, (x, y) in enumerate(zip(distances, disruptions)):
        plt.scatter(x, y, color=colors[i], marker='o', label=f'Solution {i + 1}')
        plt.text(x, y, f'S{i + 1}', fontsize=9, ha='right', va='bottom')

    plt.xlabel('Distance')
    plt.ylabel('Disruption')
    plt.title(f'Graphique Distance vs Disruption (Une solution tous les 1000 pas, sur {len(non_dominated_solutions)} solutions)')
    plt.legend(loc='upper right')

    plt.grid(True)
    plt.show()
   
def main():
    # Recherche et affichage des solutions non dominées
    print("Recherche de solutions avec allocation partielle continue...") # laisser tourner l'algorithme, un peu long...
    non_dominated_solutions = find_non_dominated_solutions()
    
    print(f"Number of non-dominated solutions: {len(non_dominated_solutions)}")

    # Affichage des solutions
    # print(f"Non-dominated solutions [sum_distances, disruption]:")
    # for i, (sum_distance, disruption) in enumerate(non_dominated_solutions):
    #     print(f"    - Solution {i + 1}: {sum_distance}, {disruption}")
    
    plot_graph_distance_disruption(non_dominated_solutions)

if __name__ == "__main__":
    main()

    


