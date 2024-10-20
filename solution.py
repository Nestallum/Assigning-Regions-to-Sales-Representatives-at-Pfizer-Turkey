from ortools.linear_solver import pywraplp
import csv
# Crée un solveur linéaire avec le backend CBC (open-source solver)
solver = pywraplp.Solver.CreateSolver('GLOP')

matrice =[]
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

print(distances)
for j in range(1,23):
    ligne=[]
    for i in range(1,4):
        ligne.append(solver.NumVar(0, 1, f'b{j}a{i}'))
    matrice.append(ligne)


for i in matrice :
    somme=0
    for j in i :
        somme=somme+j
    solver.Add(somme == 1)

# contrainte charge de travail
for i in range(3):
    somme=0
    for j in range(22):
        somme+=matrice[j][i]
    solver.Add(0.8 <= somme <= 1.2)
    
    





