from ortools.linear_solver import pywraplp
import csv
import sys

distances = [] # Distances brick/agent
index_values = [] # Workloads

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
        
def Solver(index_values,distances,contraint_disruption,initial_matrix) :
    # Create the linear solver with the CBC backend (MILP).
    solver = pywraplp.Solver.CreateSolver('CBC')
    if not solver:
        print("Could not create solver CBC")
        sys.exit()


    # New matrix to compute with solver
    matrix = []

    # Remplissage de la matrice brick/agent
    for j in range(num_bricks):
        row = []
        for i in range(num_agents):
            row.append(solver.IntVar(0, 1, f'b{j}a{i}'))  # Ajouter brick_j_agent_i
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
        solver.Add(sum_workloads >= 0.8)  # Limite inférieure
        solver.Add(sum_workloads <= 1.2)  # Limite supérieure
        
    # Minimiser la disruption avec la matrice initiale
    sum_disruption = solver.Sum(
        matrix[j][i] - (2*matrix[j][i]*initial_matrix[j][i]) + initial_matrix[j][i] for j in range(num_bricks) for i in range(num_agents)
    )
    solver.Add(sum_disruption<=contraint_disruption-0.001)
    
    # Minimiser les distances
    sum_distances = solver.Sum(matrix[j][i] * distances[j][i] for j in range(num_bricks) for i in range(num_agents))
    solver.Minimize(sum_distances)

    
    #---------------------------------------------------------------------------
    # Resolve
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        # print('Solution optimale trouvée:')
        # for j in range(num_bricks):
        #     for i in range(num_agents):
        #         if matrix[j][i].solution_value() == 1:
        #             print(f'Brique {j+1} attribuée à l\'agent {i+1}')
        # for i in range(num_agents):
        #     print(f"Workloads agent {i+1} : {sum(matrix[j][i].solution_value() * index_values[j] for j in range(num_bricks)) * 100:.2f}%")
        # print('Valeur objective =', solver.Objective().Value())
        sum_disruption = solver.Sum(
        matrix[j][i] - (2*matrix[j][i].solution_value()*initial_matrix[j][i]) + initial_matrix[j][i] for j in range(num_bricks) for i in range(num_agents)
        )
        
        return solver.Objective().Value(),sum_disruption.solution_value(),True
    else:
        print('Le solveur n\'a pas trouvé de solution optimale.')
        return 0,0,False
        

def Algorithm_alpha(index_values,distances,initial_matrix) : 
    print("ok")
    perfect_point=[]
    distance,disruption,boolean = Solver(index_values,distances,15,initial_matrix) 
    perfect_point.append([distance,disruption])
    
    
    while(boolean):
        distance,disruption,boolean = Solver(index_values,distances,disruption,initial_matrix)
        perfect_point.append([distance,disruption])
        
    
    return perfect_point[:-1]

print(Algorithm_alpha(index_values,distances,initial_matrix))
print(len(Algorithm_alpha(index_values,distances,initial_matrix)))
    
    



