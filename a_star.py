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
