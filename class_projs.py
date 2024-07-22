# a_star.py_start

# A* by Jeremy Boyd
# with Uniform Cost Search

def backward_cost_function(flip_count):
    return flip_count


def heuristic_function(pancake_stack):
    gap_count = 0
    for i in range(len(pancake_stack) - 1):
        if pancake_stack[i] + 1 != pancake_stack[i + 1] or pancake_stack[i] - 1 != pancake_stack[i + 1]:
            gap_count += 1
    return gap_count


def a_star(pancake_string):
    pancake_list = []
    pancake_frontier = []
    visited_stacks = []
    solution = False

    for i in range(len(pancake_string)):  # convert user input into list of integers
        if pancake_string[i] == " " or (pancake_string[i - 1] != " " and i != 0):
            continue
        else:
            num = pancake_string[i]
            while i < len(pancake_string) - 1:
                if pancake_string[i + 1] == " ":
                    break
                num += pancake_string[i + 1]
                i += 1
            pancake_list.append(int(num))

    pancake_frontier.append([pancake_list, heuristic_function(pancake_list)])  # initialize frontier from user input
    goal_state = sorted(pancake_list, reverse=True)  # create goal state
    flip_generation = 0

    while not solution:
        if not pancake_frontier:
            return print("Empty frontier")
        pancake_frontier = sorted(pancake_frontier, key=lambda x: x[1])  # sort frontier based on lowest total cost
        visited_stacks.append(pancake_frontier[0][0])  # append the lowest cost leaf to visited nodes list
        if pancake_frontier[0][0] == goal_state:  # check if the leaf is the goal
            return print("A* solution", pancake_frontier[0][0], "found with a total cost of ", pancake_frontier[0][1])
        flip_generation += 1  # increment backward_cost
        for i in range(len(pancake_frontier[0][0])):
            # create children based on all flip possibilities
            child = pancake_frontier[0][0][0:i] + pancake_frontier[0][0][i:len(pancake_frontier[0][0])][::-1]
            child_cost = backward_cost_function(flip_generation) + heuristic_function(child)
            if child not in visited_stacks:
                pancake_frontier.append([child, child_cost])
            for pancake_details in pancake_frontier:
                if pancake_details[0] == child:
                    if pancake_details[1] > child_cost:
                        pancake_details[1] = child_cost
                    break
        del pancake_frontier[0]


def uniform_cost_search(pancake_string):
    pancake_list = []
    pancake_frontier = []
    visited_stacks = []
    solution = False

    for i in range(len(pancake_string)):  # convert user input into list of integers
        if pancake_string[i] == " " or (pancake_string[i - 1] != " " and i != 0):
            continue
        else:
            num = pancake_string[i]
            while i < len(pancake_string) - 1:
                if pancake_string[i + 1] == " ":
                    break
                num += pancake_string[i + 1]
                i += 1
            pancake_list.append(int(num))

    pancake_frontier.append([pancake_list, 0])  # initialize frontier from user input with 0 initial cost
    goal_state = sorted(pancake_list, reverse=True)  # create goal state
    flip_generation = 0

    while not solution:
        if not pancake_frontier:
            return print("Empty frontier")
        pancake_frontier = sorted(pancake_frontier, key=lambda x: x[1])  # sort frontier based on lowest total cost
        visited_stacks.append(pancake_frontier[0][0])  # append the lowest cost leaf to visited nodes list
        if pancake_frontier[0][0] == goal_state:  # check if the leaf is the goal
            return print("UCS solution", pancake_frontier[0][0], "found with a total cost of ", pancake_frontier[0][1])
        flip_generation += 1  # increment backward_cost
        for i in range(len(pancake_frontier[0][0])):
            # create children based on all flip possibilities
            child = pancake_frontier[0][0][0:i] + pancake_frontier[0][0][i:len(pancake_frontier[0][0])][::-1]
            child_cost = backward_cost_function(flip_generation)  # this child cost doesn't include heuristic fxn
            if child not in visited_stacks:
                pancake_frontier.append([child, child_cost])
            for pancake_details in pancake_frontier:
                if pancake_details[0] == child:
                    if pancake_details[1] > child_cost:
                        pancake_details[1] = child_cost
                    break
        del pancake_frontier[0]


pancakes = input("Please enter a stack of pancake sizes in the form of consecutive integers" +
                 " broken up by spaces (that is, 10 9 8 7 is that stack [10, 9, 8, 7]: ")
a_star(pancakes)
uniform_cost_search(pancakes)

####################################
####################################

# sudoku_solver_csp.py_start

# Sudoku Constraint Satisfaction Problem by Jeremy Boyd

sudoku = [0] * 81
# create row, column, and neighbor groups that constrain assignments
rows = [[0] * 9 for _ in range(9)]
columns = [[0] * 9 for _ in range(9)]
grids = [[0] * 9 for _ in range(9)]
domains = []


# determine in which grid a puzzle position is found
def calc_grid(row, column):
    if row < 3:
        if column < 3:
            grid = 0
        elif column > 5:
            grid = 2
        else:
            grid = 1
    elif row > 6:
        if column < 3:
            grid = 3
        elif column > 5:
            grid = 5
        else:
            grid = 4
    else:
        if column < 3:
            grid = 6
        elif column > 5:
            grid = 8
        else:
            grid = 7
    return grid


# updates domains of each puzzle position
def update_domains(puzzle):
    for i in range(len(puzzle)):
        row = i // 9
        column = i % 9
        grid = calc_grid(row, column)

        nums_to_remove = []

        if len(domains[i]) > 1:
            for j in rows[row]:
                if j != 0:
                    nums_to_remove.append(j)
            for j in columns[column]:
                if j != 0:
                    nums_to_remove.append(j)
            for j in grids[grid]:
                if j != 0:
                    nums_to_remove.append(j)

            for num in nums_to_remove:
                if num in domains[i]:
                    domains[i].remove(num)


def easy_example(puzzle):
    puzzle[0] = 6
    puzzle[2] = 8
    puzzle[3] = 7
    puzzle[5] = 2
    puzzle[6] = 1
    puzzle[9] = 4
    puzzle[13] = 1
    puzzle[17] = 2
    puzzle[19] = 2
    puzzle[20] = 5
    puzzle[21] = 4
    puzzle[27] = 7
    puzzle[29] = 1
    puzzle[31] = 8
    puzzle[33] = 4
    puzzle[35] = 5
    puzzle[37] = 8
    puzzle[43] = 7
    puzzle[45] = 5
    puzzle[47] = 9
    puzzle[49] = 6
    puzzle[51] = 3
    puzzle[53] = 1
    puzzle[59] = 6
    puzzle[60] = 7
    puzzle[61] = 5
    puzzle[63] = 2
    puzzle[67] = 9
    puzzle[71] = 8
    puzzle[74] = 6
    puzzle[75] = 8
    puzzle[77] = 5
    puzzle[78] = 2
    puzzle[80] = 3

    # build domains for each variable (ie position) in the puzzle
    for i in range(len(puzzle)):  
        if puzzle[i] == 0:
            domains.append(set(range(1, 10)))
        else:
            domains.append(set([puzzle[i]]))

    j = 0
    k = 0

    # set known values in respective row and column constraints
    for i in range(len(puzzle)):
        rows[i // 9][j] = puzzle[i]
        columns[i % 9][k] = puzzle[i]
        j += 1
        if j > 8:
            j = 0
            k += 1

    # set known values in respective grids
    grids = [[6, 0, 8, 4, 0, 0, 0, 2, 5],
             [7, 0, 2, 0, 1, 0, 4, 0, 0],
             [1, 0, 0, 0, 0, 2, 0, 0, 0],
             [7, 0, 1, 0, 8, 0, 5, 0, 9],
             [0, 8, 0, 0, 0, 0, 0, 6, 0],
             [4, 0, 5, 0, 7, 0, 3, 0, 1],
             [0, 0, 0, 2, 0, 0, 0, 0, 6],
             [0, 0, 6, 0, 9, 0, 8, 0, 5],
             [7, 5, 0, 0, 0, 8, 2, 0, 3]]

    # clean variable domains based on updated row, column, and grid constraints
    update_domains(puzzle)
    domains[72] = set([1, 9])

    return puzzle


# choose which variable to assign next based on domain length
def select_unassigned_variable(puzzle):  
    unasgd_vars = []
    min_dom = 9
    for i in range(len(puzzle)):
        if puzzle[i] == 0:
            unasgd_vars.append(i)
            if len(domains[i]) < min_dom:
                min_dom = len(domains[i])
                to_return = i
    return to_return


def recursive_solver(puzzle):
    # determine whether solution has been found
    if 0 not in puzzle:  
        return puzzle

    var = select_unassigned_variable(puzzle)

    for val in domains[var]:
        if val not in domains[var]:
            break
        # assign a value to a variable
        puzzle[var] = val

        row = var / 9
        column = var % 9
        grid = calc_grid(row, column)

        # assignment validation
        if val in domains[var]:
            puzzle[var] = 0
        else:
            # update domains if valid
            domains[var] = set([val])
            rows[row].append(val)
            columns[column].append(val)
            grids[grid].append(val)
            update_domains(puzzle)

        # recurse
        result = recursive_solver(puzzle)

        if result:
            return result

    return None


def sudoku_solver(puzzle):
    return recursive_solver(puzzle)


sudoku = easy_example(sudoku)
print("Initial domains:", domains)
print("Initial puzzle:", sudoku)
print("Final puzzle:", sudoku_solver(sudoku))


####################################
####################################

# genetic_algorithm.py_start

# Genetic Algorithm by Jeremy Boyd

# import libraries
import random

# initialize genome
item_wt_vals = [[20, 6], [30, 5], [60, 8], [90, 7], [50, 6], [70, 9], [30, 4], [30, 5], [70, 4], [20, 9], [20, 2],
                [60, 1]]


def mutation(backpack):
    fitness = 0
    weight = 0
    mutated = False
    for item in backpack:
        weight += item[0]  # obtain backpack's weight
    for item in backpack:
        fitness += item[1]  # obtain backpack's fitness
    while not mutated:
        randint = random.randint(0, len(backpack) - 1)  # randomly choose the gene to mutate
        gene = random.choice(item_wt_vals)  # randomly choose the gene to be added
        if (weight - backpack[randint][0] + gene[0]) <= 250:  # determine if the mutation is legal
            backpack.remove(backpack[randint])
            backpack.append(gene)
            mutated = True
    return backpack


def crossover(bp1, bp2):
    new_backpack = []
    new_pack_wt = 0
    while new_pack_wt <= 250:
        bp1_gene = random.choice(bp1)  # choose a random gene to add from parent backpack 1
        for item in new_backpack:
            if item == bp1_gene:
                new_pack_wt -= bp1_gene[0]
                new_backpack.remove(item)  # prevent duplicate genes
        if new_pack_wt + bp1_gene[0] > 250:  # ensure weight does not exceed limit
            break
        new_backpack.append(bp1_gene)
        new_pack_wt += bp1_gene[0]

        bp2_gene = random.choice(bp2)  # choose a random gene to add from parent backpack 2
        for item in new_backpack:
            if item == bp2_gene:
                new_pack_wt -= bp2_gene[0]
                new_backpack.remove(item)  # prevent duplicate genes
        if new_pack_wt + bp2_gene[0] > 250:  # ensure weight does not exceed limit
            break
        new_backpack.append(bp2_gene)
        new_pack_wt += bp2_gene[0]
    return new_backpack


def cull(population, fitnesses):
    zipped = zip(fitnesses, population)
    fittest = [x for _, x in sorted(zipped)]  # sort backpacks based on fitness
    fittest = fittest[(len(fitnesses) // 2) - 1:-1]  # eliminate the ceiling of 50% of the population
    return fittest


def genetic_algorithm(genome):
    # initialize variables
    population = []
    fitnesses = []
    best_pack = [[0, 0]]
    best_fitness = 0

    for i in range(10):  # create 10 backpacks
        backpack = []
        fitness = 0
        weight = 0
        while weight <= 250:  # add items while weight limit not reached
            gene = random.choice(genome)  # choose random item to put in backpack
            for item in backpack:
                if item == gene:
                    weight -= gene[0]
                    fitness -= gene[1]
                    backpack.remove(item)  # prevent duplicate genes
            if weight + gene[0] > 250:  # do not exceed weight limit of 250
                break
            weight += gene[0]
            fitness += gene[1]
            backpack.append(gene)
        fitnesses.append(fitness)
        population.append(backpack)

    # while len(population) > 1:  # repeat until population has one individual remaining
    contender_fitness = 0
    population = cull(population, fitnesses)  # determine most fit individuals by culling population
    for item in population[-1]:
        contender_fitness += item[1]  # determine fitness in contention for best fitness
    if contender_fitness > best_fitness:
        best_fitness = contender_fitness
        best_pack = population[-1]  # set new best pack if best fitness better than current best fitness

    rand_pack = random.choice(population)
    population.remove(rand_pack)
    population.append(mutation(rand_pack))  # mutate a random backpack

    bp1 = random.choice(population)
    bp2 = random.choice(population)
    while bp1 == bp2:
        bp2 = random.choice(population)  # if parent backpacks are same, choose another backpack parent 2
    population.remove(bp1)
    population.remove(bp2)
    population.append(crossover(bp1, bp2))  # crossover two random backpacks
    print("The best backpack carries these items: ", best_pack, " with a fitness of ", best_fitness)


genetic_algorithm(item_wt_vals)
