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
