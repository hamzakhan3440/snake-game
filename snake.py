import random

# Board dimensions
WIDTH = 20
HEIGHT = 20

def create_food(snake):
    while True:
        pos = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        if pos not in snake:
            return pos

def move_snake(snake, direction):
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    return [new_head] + snake[:-1]

def check_collision(snake):
    head = snake[0]
    hx, hy = head
    if hx < 0 or hx >= WIDTH or hy < 0 or hy >= HEIGHT:
        return True
    if head in snake[1:]:
        return True
    return False

def has_eaten(snake, food):
    
    return snake[0] == food

def grow_snake(snake, food_pos):
    
    return snake + [food_pos]
