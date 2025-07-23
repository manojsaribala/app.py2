import random

def player(prev_play, opponent_history=[]):
    # Initialize histories if empty
    if not opponent_history:
        opponent_history.clear()
        player.my_history = []
    
    # Append opponent's last move to history
    opponent_history.append(prev_play)
    my_history = player.my_history

    # Define counters for rock, paper, scissors
    counters = {"R": "P", "P": "S", "S": "R"}

    # If it's the first move, choose randomly
    if not prev_play:
        move = random.choice(["R", "P", "S"])
        my_history.append(move)
        return move

    # Strategy 1: Counter Quincy's pattern
    # Quincy may follow a fixed sequence, e.g., ["R", "R", "P", "P", "S"]
    if len(opponent_history) < 100:
        quincy_pattern = ["R", "R", "P", "P", "S"]
        move_index = (len(opponent_history) - 1) % 5
        expected_move = quincy_pattern[move_index]
        move = counters[expected_move]
        my_history.append(move)
        return move

    # Strategy 2: Counter Abbey (counters player's last move)
    if len(opponent_history) < 200:
        # Assume Abbey plays the counter to our last move
        my_last_move = my_history[-1]
        # Play the move that beats what beats our last move
        move = counters[counters[my_last_move]]
        my_history.append(move)
        return move

    # Strategy 3: Counter Kris (counters what beats their last move)
    if len(opponent_history) < 300:
        # Kris plays the counter to what beats their last move
        last_opponent_move = opponent_history[-1]
        # What beats their last move
        counter_to_last = counters[last_opponent_move]
        # Play the move that beats Kris's counter
        move = counters[counter_to_last]
        my_history.append(move)
        return move

    # Strategy 4: Counter Mrugesh (plays counter to player's most frequent move)
    if len(opponent_history) >= 300:
        # Analyze last 10 moves for most frequent
        recent_moves = my_history[-10:] if len(my_history) >= 10 else my_history
        if recent_moves:
            most_common = max(set(recent_moves), key=recent_moves.count)
            # Mrugesh plays the counter to our most common move
            # Play the move that beats Mrugesh's counter
            move = counters[counters[most_common]]
            my_history.append(move)
            return move

    # Fallback: Random move
    move = random.choice(["R", "P", "S"])
    my_history.append(move)
    return move

# Ensure my_history persists between calls
player.my_history = []