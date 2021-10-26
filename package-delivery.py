import pygad
import numpy as np
import pandas as pd
import math
import random
from datetime import datetime


def e_dist(A, B):
    return math.sqrt((A['y'] - B['y'])**2 + (A['x']-B['x'])**2)


tsp = pd.read_csv('tsp1.csv', index_col=0)
N = len(tsp)
print(tsp)
sol = []
for i in range(N):
    sol.append(1 + i)
random.shuffle(sol)
print(sol)
total_dist = 0
for i in range(0, N-1):
    print('city 1: ', sol[i], 'x: ', tsp.loc[sol[i], 'x'],
          'y:', tsp.loc[sol[i], 'y'])
    print('city 2: ', sol[i+1], 'x: ', tsp.loc[sol[i+1], 'x'],
          'y:', tsp.loc[sol[i+1], 'y'])
    total_dist += e_dist(tsp.loc[sol[i]], tsp.loc[sol[i+1]])
    print(total_dist)


def maxcap(n):
    return math.factorial(n - 1) / 2


def e_dist(A, B):
    return math.sqrt((A['y'] - B['y'])**2 + (A['x']-B['x'])**2)

# Generate a random solution
# returns a list that has N elements that represent the order cities are visited


def solution():
    sol = []
    for i in range(N):
        sol.append(1 + i)
    random.shuffle(sol)
    print(sol)
    return sol

# the fitness function.
# captures() returns the number of possible captures
# for the queens arrangement given in solution.
# PyGAD requires the solution_idx, but I will not use it.


def captures(solution, solution_idx):
    coll = 0
    for i in range(Q):
        for j in range(i + 1, Q):
            if (solution[i] == solution[j]) or (solution[j] == (solution[i] + (j - i))) or (solution[j] == (solution[i] - (j - i))):
                coll += 1
    return maxcap(Q) - coll


def distance(solution, solution_idx):
    total_dist = 0
    for i in range(0, N-1):
        total_dist += e_dist(tsp.loc[sol[i]], tsp.loc[sol[i+1]])
        print(total_dist)

# print the solution.
# produces a rough ascii diagram and includes the number of
# possible captures for the arrangement of queens.


def printsol(s):
    for i in range(Q, 0, -1):
        print("     ", "----" * Q)
        print("{:>6}".format(i), end='')
        for j in range(1, Q + 1):
            if s[j - 1] == i:
                print("| Q ", end='')
            else:
                print("|   ", end='')
        print("|")
    print("     ", "----" * Q)
    c = captures(s, Q)
    print("Fitness = {} Captures = {}".format(c, maxcap(Q) - c))

# The on_generation is a function that will be called at the end of each generation.
# In this case we will print out the gen number.


def on_generation(g):
    s, fit, s_i = g.best_solution()
    print(datetime.now(), "Gen", g.generations_completed, "Fittest", fit, "S: ", s)
    # print("Best Solution", captures(ga_instance.best_solution(),1))
    # for p in ga.population:
    # print(p, captures(p,1))

# run the ga.


def ga():
    print(Q, maxcap(Q))
    # set up the parameters

    # assign the fitness function
    fitness_function = captures

    # how many generations to run for?
    num_generations = 50

    # what is the population size?
    sol_per_pop = 20

    # Set up the genes. How many genes make up an individual and what are the values that
    # each gene can take on.
    # In this example there are 8 genes, each representing a column on the chessboard, and
    # that possible values are 1-8 for which row the queen is placed.

    num_genes = Q
    gene_space = range(1, Q + 1)
    #init_range_low = 1
    #init_range_high = 8

    # Then we need to control how the various genetic operators are applied.
    num_parents_mating = 2
    parent_selection_type = "sss"
    keep_parents = 1

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 1

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           # init_range_low=init_range_low,
                           # init_range_high=init_range_high,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes,
                           gene_space=gene_space,
                           on_generation=on_generation)
    ga_instance.run()

    ga_instance.plot_fitness()

    s, fit, s_i = ga_instance.best_solution()
    print(s)
    return s


Q = int(input("Enter the size of the problem: "))
T = input("Enter H for hillclimb, G for GA: ")

print("{} Queens problem with maximum captures = {}".format(Q, maxcap(Q)))
sol = []

if T == "H":
    sol = hillclimb()
elif T == "G":
    sol = ga()

print("\n")
printsol(sol)
print("\n")
