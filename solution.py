from ortools.linear_solver import pywraplp
import csv
# Crée un solveur linéaire avec le backend CBC (open-source solver)
solver = pywraplp.Solver.CreateSolver('GLOP')

matrice = []
matriceprime = [
    [0, 0, 0, 1],  
    [0, 0, 0, 1],  
    [0, 0, 0, 1],  
    [1, 0, 0, 0],  
    [1, 0, 0, 0],  
    [1, 0, 0, 0],  
    [1, 0, 0, 0],  
    [1, 0, 0, 0], 
    [0, 0, 1, 0],  
    [0, 1, 0, 0],  
    [0, 1, 0, 0],  
    [0, 1, 0, 0],  
    [0, 1, 0, 0], 
    [0, 1, 0, 0],  
    [1, 0, 0, 0],  
    [0, 0, 1, 0],  
    [0, 0, 1, 0],  
    [0, 0, 1, 0],  
    [0, 0, 0, 1], 
    [0, 0, 0, 1],  
    [0, 0, 0, 1],  
    [0, 0, 0, 1],  
    [0, 0, 0, 1],  
]
distances = []
index_values = []

# Lire le fichier CSV
with open('data/bricks_index_values.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Sauter l'en-tête si le fichier en a un
    
    for row in csv_reader:
        # Ajouter la valeur float (index_value) dans la liste
        index_values.append(float(row[1]))

# Lire le fichier CSV
with open('data/brick_rp_distances.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Sauter l'en-tête si le fichier en a un
    
    for row in csv_reader:
        # Ajouter la valeur float (index_value) dans la liste
        distances.append(row[1:])


for j in range(1,23):
    ligne=[]
    for i in range(1,5):
        ligne.append(solver.NumVar(0, 1, f'b{j}a{i}'))
    matrice.append(ligne)

# Contrainte d'appartenance
for brick in matrice :
    somme = 0
    for agent in brick:
        somme += agent
    solver.Add(somme == 1) # Un seul agent par brick

# Contrainte charge de travail
somme=0
for i in range(4):

    somme += solver.Sum(matrice[j][i] for i in range(4))
    solver.Add(0.8 <= somme <= 1.2)

solver.Add(matrice[3][0]==1)
solver.Add(matrice[13][1]==1)
solver.Add(matrice[15][2]==1)
solver.Add(matrice[21][3]==1)
# Minimiser les distances agent-brick
somme=0.0
print(matrice[1][1].solution_value())
for i in range(4):
    for j in range(22):
        print(distances[j][i])
        somme += float(matrice[j][i].solution_value())*float(distances[j][i])


solver.Minimize(somme)
# somme=0
# for i in range(3):
#     for j in range(22):
#         somme += matrice[j][i].solution_value() - (2*matrice[j][i].solution_value()*matriceprime[j][i]) + (matriceprime[j][i]**2)
        
# solver.Minimize(somme)


status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    for i in matrice :
            for j in i :
                print(f'{j} =', j.solution_value())
    print('Objective value =', solver.Objective().Value())
else:
    print('Le solveur n\'a pas trouvé de solution optimale.')





