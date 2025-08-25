from vpython import * 
import numpy as np
import time

color_map = {
    "white": vector(1, 1, 1),
    "red": vector(1, 0, 0),
    "green": vector(0, 1, 0),
    "orange": vector(1, 0.647058823529412, 0),
    "blue": vector(0, 0, 1),
    "yellow": vector(1, 1, 0),
    "garnet": vector(0.470588235294118, 0.184313725490196, 0.250980392156863),
    "gold": vector(0.807843137254902, 0.72156862745098, 0.533333333333333),
    "black": vector(44/255, 42/255, 41/255)
}

def new_apple(apple):

    return apple

def get_apple_position(dim):
    apple_x = int(floor(np.random.rand() * (2*dim+1)))
    apple_y = int(floor(np.random.rand() * (2*dim+1)))
    if apple_x == 0:
        apple_x += 1
    if apple_x == 2*dim:
        apple_x -= 1
    if apple_y == 0:
        apple_y += 1
    if apple_y == 2*dim:
        apple_y -= 1
    return apple_x, apple_y

def play_snake(snake, dim):

    direction = vector(1, 0, 0)
    right = vector(1, 0, 0)
    left = vector(-1, 0, 0)
    up = vector(0, 1, 0)
    down = vector(0, -1, 0)

    apple_x, apple_y = get_apple_position(dim)
    apple = sphere(pos=vector(apple_x-dim, apple_y-dim, 1), radius=0.5, size=vector(1,1,1), color = color_map['black'])

    extra_boxes = []

    while True:

        rate(10)
        k = keysdown() # a list of keys that are down
        print(k)
        if 'up' in k:
            direction = up
        if 'right' in k:
            direction = right
        if 'down' in k:
            direction = down
        if 'left' in k:
            direction = left
            
        newsnake = []
        newsnake.append(snake[-1])
        for i in range (0, len(snake)-1):
            newsnake.append(snake[i])
        newsnake[0].pos = snake[0].pos + direction
        snake = newsnake


        for extra in extra_boxes: 
            snake.append(extra)
        extra_boxes.clear()

        if snake[0].pos.x == apple_x-dim and snake[0].pos.y == apple_y-dim:
            apple_x, apple_y = get_apple_position(dim)
            apple.pos = vector(apple_x-dim, apple_y-dim, 1)

            extra_boxes.append(box(pos=snake[-1].pos, color=snake[-1].color, size=snake[-1].size))

        #time.sleep(0.5)

def main():

    dim = 20

    scene = canvas(title="Snake!", width = 500, height=500, range=dim)

    boxes = []
    for i in range (0, 2*dim+1, 1):
        x = i - dim
        tmp = []
        for j in range (0, 2*dim+1, 1):
            y = j - dim 

            mycolor = color_map["garnet"]
            if np.random.rand() < 10000.5 :
                mycolor = color_map["gold"]

            tmp.append(box(pos = vector(x, y, 0), size = vector(0.98, 0.98, 0.98), color = mycolor))
            #tmp.append(box(pos = vector(x, y, 0), size = vector(1,1,1), color = mycolor))

        boxes.append(tmp)

    snake = []
    snake.append(box(pos = vector(0, 0, 1),  size = vector(1, 1, 1), color = color_map['garnet']))
    snake.append(box(pos = vector(-1, 0, 1), size = vector(1, 1, 1), color = color_map['garnet']))
    snake.append(box(pos = vector(-2, 0, 1), size = vector(1, 1, 1), color = color_map['garnet']))
    snake.append(box(pos = vector(-3, 0, 1), size = vector(1, 1, 1), color = color_map['garnet']))
    snake.append(box(pos = vector(-4, 0, 1), size = vector(1, 1, 1), color = color_map['garnet']))
    snake.append(box(pos = vector(-5, 0, 1), size = vector(1, 1, 1), color = color_map['garnet']))
    snake.append(box(pos = vector(-6, 0, 1), size = vector(1, 1, 1), color = color_map['garnet']))
    snake.append(box(pos = vector(-7, 0, 1), size = vector(1, 1, 1), color = color_map['garnet']))
    snake.append(box(pos = vector(-8, 0, 1), size = vector(1, 1, 1), color = color_map['garnet']))
    snake.append(box(pos = vector(-9, 0, 1), size = vector(1, 1, 1), color = color_map['garnet']))

    while True:

        ev = scene.waitfor('mousedown keydown')
        if ev.event == 'mousedown':
            pass
        elif ev.key == '\n':
            play_snake(snake, dim)
        
if __name__ == "__main__":
    main()
