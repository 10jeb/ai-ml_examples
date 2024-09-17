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
