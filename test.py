from ortools.linear_solver import pywraplp
import csv

# Créer un solveur linéaire avec le backend GLOP
solver = pywraplp.Solver.CreateSolver('GLOP')

# Variables et matrices
matrice = []
index_values = []
distances = []

# Lire le fichier CSV pour les index de valeurs
with open('data/bricks_index_values.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Sauter l'en-tête si le fichier en a un
    
    for row in csv_reader:
        index_values.append(float(row[1]))

# Lire le fichier CSV pour les distances
with open('data/brick_rp_distances.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Sauter l'en-tête si le fichier en a un
    
    for row in csv_reader:
        distances.append(list(map(float, row[1:])))  # Convertir chaque distance en float

# Créer des variables de décision
num_bricks = len(index_values)
num_agents = 4  # Nombre d'agents

for j in range(num_bricks):
    ligne = []
    for i in range(num_agents):
        ligne.append(solver.NumVar(0, 1, f'b{j}a{i}'))
    matrice.append(ligne)

# Contrainte d'appartenance
for j in range(num_bricks):
    somme = solver.Sum(matrice[j][i] for i in range(num_agents))
    solver.Add(somme == 1)  # Un seul agent par brique

# Contrainte de charge de travail
for i in range(num_agents):
    somme = solver.Sum(matrice[j][i] * index_values[j] for j in range(num_bricks))
    solver.Add(0.8 <= somme <= 1.2)

# Contraintes spécifiques
solver.Add(matrice[3][0] == 1)  # Brique 4 à agent 1
solver.Add(matrice[13][1] == 1)  # Brique 14 à agent 2
solver.Add(matrice[15][2] == 1)  # Brique 16 à agent 3
solver.Add(matrice[21][3] == 1)  # Brique 22 à agent 4

# Minimiser les distances agent-brique
somme_distance = solver.Sum(matrice[j][i] * distances[j][i] for j in range(num_bricks) for i in range(num_agents))
solver.Minimize(somme_distance)

# Résoudre le problème
status = solver.Solve()

# Vérifier le statut de la solution
if status == pywraplp.Solver.OPTIMAL:
    print('Solution optimale trouvée:')
    for j in range(num_bricks):
        for i in range(num_agents):
            if matrice[j][i].solution_value() == 1:
                print(f'Brique {j+1} attribuée à l\'agent {i+1}')
    print('Valeur objective =', solver.Objective().Value())
else:
    print('Le solveur n\'a pas trouvé de solution optimale.')