import json
import keyboard
import time
from collections import deque


def main():
    moves_data = load_moves()

    game = select_game(moves_data)
    character = select_character(moves_data, game)
    move = select_move(moves_data, game, character)
    difficulty = select_difficulty()
    inputs = moves_data[game][character][move]

    show_summary(game, character, move, difficulty, inputs)
    track_user_inputs(inputs)
    training_loop(inputs)


def load_moves():
    with open("moves.json", "r") as f:
        return json.load(f)

def select_game(moves_data):
    print("\nSelect a game:")
    games = list(moves_data.keys())
    for idx, game in enumerate(games):
        print(f"{idx + 1}. {game}")
    choice = int(input("Enter your choice: ")) - 1
    return games[choice]

def select_character(moves_data, game):
    print(f"\nSelect a character in {game}:")
    characters = list(moves_data[game].keys())
    for idx, char in enumerate(characters):
        print(f"{idx + 1}. {char}")
    choice = int(input("Enter your choice: ")) - 1
    return characters[choice]

def select_move(moves_data, game, character):
    print(f"\nMoves for {character}:")
    move_list = list(moves_data[game][character].keys())
    for idx, move in enumerate(move_list):
        print(f"{idx + 1}. {move}")
    choice = int(input("Choose a move to practice: ")) - 1
    return move_list[choice]

def select_difficulty():
    print("\nChoose difficulty level:")
    difficulties = ["Beginner", "Advanced", "Expert"]
    for idx, level in enumerate(difficulties):
        print(f"{idx + 1}. {level}")
    choice = int(input("Enter your choice: ")) - 1
    return difficulties[choice]

def show_summary(game, character, move, difficulty, inputs):
    print("\n Training Setup:")
    print(f"Game: {game}")
    print(f"Character: {character}")
    print(f"Move: {move}")
    print(f"Difficulty: {difficulty}")
    print(f"Input Sequence: {inputs}")

keyboard_inputs ={
    'w': 'up',
    's': 'down',
    'a': 'left',
    'd': 'right',
    'w+a': 'up-left',
    'w+d': 'up-right',
    's+a':'down-left',
    's+d': 'down-right',
    'j': 'punch',
    'k': 'kick',
    'l': 'slash'
}

def track_user_inputs(expected_sequence, time_limit=8):
    print('\n Your Training Begins Now!. Match the inputs')
    print("press ESC to quit.\n")

    user_inputs = deque()
    start_time = time.time()

    while time.time() - start_time <time_limit:
        for key in keyboard_inputs:
            if keyboard.is_pressed(key):
                translated = keyboard_inputs[key]
                if not user_inputs or translated != user_inputs[-1]:
                    user_inputs.append(translated)
                    print(f'Input: {translated}')
                    time.sleep(0.1)

        if keyboard.is_pressed('esc'):
            print("Trainings Over Come Back Again!")
            return False

    if list(user_inputs)[-len(expected_sequence):] == expected_sequence:
        print('\n Great!! But you cant stop here Again!')
        return True
    else:
        print('\n Wrong!! Do it Again! ')
        print(f'Your input: {list(user_inputs)[-len(expected_sequence):]}')
        print(f'It should be this   {expected_sequence}')
        return False


def training_loop(expected_sequence):
    attempts = 0
    successes = 0

    while True:
        print(f"\nAttempt #{attempts + 1}")
        success = track_user_inputs(expected_sequence)

        attempts += 1
        if success:
            successes += 1

        accuracy = (successes / attempts) * 100
        print(f" Accuracy: {accuracy:.2f}% ({successes}/{attempts})")

        again = input("\nTry again? (y/n): ").strip().lower()
        if again != 'y':
            break



if __name__ == "__main__":
    main()

