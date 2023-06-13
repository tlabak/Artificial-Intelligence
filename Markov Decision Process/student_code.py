import common


def drone_flight_planner(map, policies, values, delivery_fee, battery_drop_cost, dronerepair_cost, discount):
    # Set the initial values of the map
    # values = common.init_values()

    # # Iterate over the map to update values for customer and rivals and find starting point
    pizza_x, pizza_y = None, None
    for y in range(6):
        for x in range(6):
            if map[y][x] == common.constants.PIZZA:
                pizza_x, pizza_y = x, y
            elif map[y][x] == common.constants.CUSTOMER:
                values[y][x] = delivery_fee
            elif map[y][x] == common.constants.RIVAL:
                values[y][x] = -dronerepair_cost

    # Perform value iteration until convergence
    MAX_SIZE = 6
    convergence_threshold = 0.001
    delta = float('inf')
    iteration = 0

    while delta >= convergence_threshold:
        delta = 0
        for y in range(MAX_SIZE):
            for x in range(MAX_SIZE):
                if map[y][x] == common.constants.EMPTY or map[y][x] == common.constants.PIZZA:
                    # Initialize an empty list to store the Q-states for each action
                    q_states = []

                    # Calculate the Q-state for each action
                    for action in range(1, 9):
                        q_state = 0

                        # Calculate the resulting states and their probabilities
                        next_state, side_state1, side_state2 = get_resulting_states(map, values, x, y, action)

                        # Calculate the Q-state based on wind conditions
                        if action in [common.constants.SOFF, common.constants.WOFF, common.constants.NOFF, common.constants.EOFF]:
                            q_state += 0.7 * (-battery_drop_cost + discount * values[next_state[0]][next_state[1]])
                            q_state += 0.15 * (-battery_drop_cost + discount * values[side_state1[0]][side_state1[1]])
                            q_state += 0.15 * (-battery_drop_cost + discount * values[side_state2[0]][side_state2[1]])
                        elif action in [common.constants.SON, common.constants.WON, common.constants.NON, common.constants.EON]:
                            q_state += 0.8 * (-2 * battery_drop_cost + discount * values[next_state[0]][next_state[1]])
                            q_state += 0.1 * (-2 * battery_drop_cost + discount * values[side_state1[0]][side_state1[1]])
                            q_state += 0.1 * (-2 * battery_drop_cost + discount * values[side_state2[0]][side_state2[1]])

                        # Append the Q-state to the list
                        q_states.append(q_state)

                    # Find the action with the maximum Q-state value
                    max_q_state = max(q_states)
                    max_action = q_states.index(max_q_state) + 1

                    # Update the value and policy for the current block
                    old_value = values[y][x]
                    values[y][x] = max_q_state
                    policies[y][x] = max_action

                    # Update delta
                    delta = max(delta, abs(old_value - max_q_state))

        # Increment the iteration counter
        iteration += 1

    # print simulated results
    print_simulated_results(delta, convergence_threshold, iteration, values, policies, pizza_y, pizza_x)

    # Return the value of the starting position
    return values[pizza_y][pizza_x]
def get_resulting_states(map, values, x, y, action):
    rows = len(map)
    cols = len(map[0])

    # Calculate the next state based on the chosen action
    if action == common.constants.SOFF or action == common.constants.SON:
        next_state = (y + 1, x)
        side_state1 = (y, x - 1)  # West
        side_state2 = (y, x + 1)  # East
    elif action == common.constants.WOFF or action == common.constants.WON:
        next_state = (y, x - 1)
        side_state1 = (y - 1, x)  # North
        side_state2 = (y + 1, x)  # South
    elif action == common.constants.NOFF or action == common.constants.NON:
        next_state = (y - 1, x)
        side_state1 = (y, x - 1)  # West
        side_state2 = (y, x + 1)  # East
    elif action == common.constants.EOFF or action == common.constants.EON:
        next_state = (y, x + 1)
        side_state1 = (y - 1, x)  # North
        side_state2 = (y + 1, x)  # South

    # Check if the next state is outside the boundaries of the map
    if next_state[0] < 0 or next_state[0] >= rows or next_state[1] < 0 or next_state[1] >= cols:
        next_state = (y, x)  # Bounce off the edges by staying at the current position
    if side_state1[0] < 0 or side_state1[0] >= rows or side_state1[1] < 0 or side_state1[1] >= cols:
        side_state1 = (y, x)  # Bounce off the edges by staying at the current position
    if side_state2[0] < 0 or side_state2[0] >= rows or side_state2[1] < 0 or side_state2[1] >= cols:
        side_state2 = (y, x)  # Bounce off the edges by staying at the current position


    return next_state, side_state1, side_state2


def print_simulated_results(delta, convergence_threshold, iteration, values, policies, start_y, start_x):
    # Check if the iteration converged
    if delta < convergence_threshold:
        print("Values converged after", iteration, "iterations.")
    else:
        print("Values did not converge.")

    # Print the updated values and policies
    print("Values:")
    for row in values:
        for value in row:
            print("{:.2f}".format(value), end="\t")
        print()

    print("Policies:")
    for row in policies:
        for policy in row:
            print(policy, end="\t")
        print()

    # Calculate the delivery job value for the starting position
    delivery_job_value = values[start_y][start_x]
    print("Delivery job value:", delivery_job_value)
