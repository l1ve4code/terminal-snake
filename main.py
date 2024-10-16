import os
import time
import random
import sys
from pynput import keyboard

width = 32
height = 16
field_symbol = '.'
snake_tail_symbol = "s"
snake_head_symbol = "S"
food_symbol = "@"
current_score = 0
in_game = True


def get_coordinates(x=0, y=1):
    return {'x': x, 'y': y}


def place_snake(length=2):
    return [get_coordinates(width // 2, height // 4 + i) for i in range(length)]


def draw_game_field_with_snake():
    print("0_o CURRENT SCORE -> {}".format(current_score))
    for h in range(height):
        part_of_field = ""
        for w in range(width):
            coordinates = get_coordinates(w, h)
            if coordinates == food and get_snake_head() != coordinates:
                part_of_field += food_symbol
            elif get_snake_head() == coordinates:
                part_of_field += snake_head_symbol
            elif coordinates in snake:
                part_of_field += snake_tail_symbol
            else: part_of_field += field_symbol
            part_of_field += " "
        print(part_of_field)


def get_snake_head():
    return snake[len(snake) - 1]


def generate_food_position():
    return get_coordinates(random.randint(0, width - 1), random.randint(0, height - 1))


def do_snake_movement_wo_removing_tail():
    snake_head = get_snake_head()
    snake.append(get_coordinates(snake_head['x'] + direction["x"], snake_head['y'] + direction["y"]))


def show_dead_screen():
    global in_game
    in_game = False
    clear_field()
    print("-=== GAME OVER ===-")
    print("-- Your score is {} --".format(current_score))


def check_border_intersection():
    snake_head_position = get_snake_head()
    if snake_head_position["x"] > width or snake_head_position["x"] < 0 or snake_head_position["y"] > height or \
            snake_head_position["y"] < 0:
        show_dead_screen()


def do_snake_movement():
    do_snake_movement_wo_removing_tail()
    snake.remove(snake[0])
    check_border_intersection()


def do_food_collision():
    global food, current_score
    if get_snake_head() == food:
        food = generate_food_position()
        do_snake_movement_wo_removing_tail()
        current_score += 1


def process_key_press(key):
    global direction, in_game
    match key:
        case keyboard.Key.left: direction = get_coordinates(-1, 0)
        case keyboard.Key.right: direction = get_coordinates(1, 0)
        case keyboard.Key.up: direction = get_coordinates(0, -1)
        case keyboard.Key.down: direction = get_coordinates(0, 1)
        case keyboard.Key.esc: in_game = False


def clear_field():
    os.system('cls' if os.name == 'nt' else 'clear')


def start_game():
    while (True):
        if not in_game: sys.exit(0)
        time.sleep(.2)
        clear_field()
        draw_game_field_with_snake()
        do_food_collision()
        do_snake_movement()


direction = get_coordinates()
snake = place_snake()
food = generate_food_position()

listener = keyboard.Listener(on_press=process_key_press)
listener.start()
start_game()
listener.join()