#
# driver for interactive rubik's cube
#
# r: rotate right face clockwise
# R: rotate right face counter-clockwise
# l: rotate left face clockwise
# L: rotate left face counter-clockwise
# u: rotate top face clockwise
# U: rotate top face counter-clockwise
# d: rotate bottom face clockwise
# D: rotate bottom face counter-clockwise
# f: rotate front face clockwise
# F: rotate front face counter-clockwise
# b: rotate back face clockwise
# B: rotate back face counter-clockwise
#
# up: bring front face to top
# down: bring top face to front
# left: bring right face to front
# right: bring left face to front
#

from rubiks_cube import *
from rubiks_cube_solver import *

def main():

    scene = canvas(title="Rubik's cube", width = 600, height=600, range=6)
    scene.forward = vector(-0.451197, -0.479426, -0.75271)

    cube = rubiks_cube_solver(scene)

    while True:

        ev = scene.waitfor('keydown')
        if ev.key == 'r':
            cube.rotate_right_clockwise()
        if ev.key == 'R':
            cube.rotate_right_counter_clockwise()
        if ev.key == 'l':
            cube.rotate_left_clockwise()
        if ev.key == 'L':
            cube.rotate_left_counter_clockwise()
        if ev.key == 'f':
            cube.rotate_front_clockwise()
        if ev.key == 'F':
            cube.rotate_front_counter_clockwise()
        if ev.key == 'b':
            cube.rotate_back_clockwise()
        if ev.key == 'B':
            cube.rotate_back_counter_clockwise()
        if ev.key == 'u':
            cube.rotate_top_clockwise()
        if ev.key == 'U':
            cube.rotate_top_counter_clockwise()
        if ev.key == 'd':
            cube.rotate_bottom_clockwise()
        if ev.key == 'D':
            cube.rotate_bottom_counter_clockwise()
        if ev.key == 'up':
            cube.bring_to_top("front")
        if ev.key == 'down':
            cube.bring_to_top("back")
        if ev.key == 'left':
            cube.bring_to_front("right")
        if ev.key == 'right':
            cube.bring_to_front("left")

        # solve
        if ev.key == 'o':
            cube.locate_origin()
            cube.form_cross()
            cube.solve_top_layer()
            cube.solve_middle_layer()
            cube.form_bottom_cross()
            cube.permute_bottom_corners()
            cube.orient_bottom_corners()
            cube.permute_bottom_edges()

        # jumble
        if ev.key == 'j':
            cube.jumble_cube(15)


if __name__ == "__main__":
    main()
