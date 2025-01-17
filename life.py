import argparse
import os
import sys
import time
from random import randint

# ANSI color codes
ALIVE_COLOR = "\033[92m"
DEAD_COLOR = "\033[90m"
RESET_COLOR = "\033[0m"
CLEAR_SCREEN = "\033[H\033[J"

def create_world(size, config):
    world = [[0 for _ in range(size)] for _ in range(size)]

    if config == 1:  # Random pattern
        for row in range(size):
            for col in range(size):
                world[row][col] = randint(0, 1)

    elif config == 2:  # Glider
        glider = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        for r, c in glider:
            world[r][c] = 1

    elif config == 3:  # Small Exploder
        pattern = [(1, 1), (0, 2), (1, 2), (2, 2), (0, 3), (2, 3), (1, 4)]
        for r, c in pattern:
            world[r][c] = 1

    elif config == 4:  # Spaceship
        spaceship = [(1, 2), (1, 3), (1, 4), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3)]
        for r, c in spaceship:
            world[r][c] = 1

    elif config == 5:  # Beacon
        beacon = [(1, 1), (1, 2), (2, 1), (2, 2), (3, 3), (3, 4), (4, 3), (4, 4)]
        for r, c in beacon:
            world[r][c] = 1

    return world

def print_world(world):
    print(CLEAR_SCREEN, end="")
    for row in world:
        for cell in row:
            if cell:
                print(f"{ALIVE_COLOR}█{RESET_COLOR}", end="")
            else:
                print(f"{DEAD_COLOR}·{RESET_COLOR}", end="")
        print()
    sys.stdout.flush()

def count_neighbors(world, x, y, size):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for dx, dy in directions:
        nx, ny = (x + dx) % size, (y + dy) % size  # Wrap around
        count += world[nx][ny]
    return count

def next_generation(world, size):
    new_world = [[0 for _ in range(size)] for _ in range(size)]
    for x in range(size):
        for y in range(size):
            neighbors = count_neighbors(world, x, y, size)
            if world[x][y] == 1 and (neighbors == 2 or neighbors == 3):
                new_world[x][y] = 1
            elif world[x][y] == 0 and neighbors == 3:
                new_world[x][y] = 1
    return new_world

def main():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("--size", type=int, required=True, help="Size of the world")
    parser.add_argument("--config", type=int, required=True, help="Starting configuration (1-5)")
    args = parser.parse_args()

    size = args.size
    config = args.config

    if config not in range(1, 6):
        print("Invalid configuration. Choose a number between 1 and 5.")
        sys.exit(1)

    world = create_world(size, config)

    try:
        while True:
            print_world(world)
            world = next_generation(world, size)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nGame terminated.")

if __name__ == "__main__":
    main()

