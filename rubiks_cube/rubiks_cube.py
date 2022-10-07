# an interactive rubik's cube, visualized with vpython

from vpython import *
import numpy as np

color_map = {
    "red": vector(1, 0, 0),
    "green": vector(0, 1, 0),
    "blue": vector(0, 0, 1),
    "white": vector(1, 1, 1),
    "orange": vector(1, 0.647058823529412, 0),
    "yellow": vector(1, 1, 0)
}

"""
    cube_data 2D layout

      b           3
    l u r       2 0 4
      f   d       1    5


    the origin (0, 0, 0) should be the back
    left corner, indicated by the arrows

    x increases toward the front of the cube
    y increases to the right
    z increases toward the top of the cube

             -> 0|1|2                            
                3|4|5                            
                6|7|8                            
                                                 
      -> 0|1|2  0|1|2  0|1|2                     
         3|4|5  3|4|5  3|4|5                     
         6|7|8  6|7|8  6|7|8                     
                                                 
                0|1|2         -> 0|1|2        
                3|4|5            3|4|5        
                6|7|8            6|7|8  
                                                
"""

class face():
    def __init__(self, name):

        """ a face of a Rubik's cube

        Attributes
        ----------

        pos: 9x3 array of describing positions of squares
        pos_copy: a copy of pos
        color: 9-dimensional array describing colors of squares
        axis: 3-dimensional array defining the orientation of the squares
        name: the name of the face

        """

        self.pos = np.zeros((9, 3))
        self.pos_copy = np.zeros((9, 3))
        self.is_movable = np.empty([9], dtype = bool)
        self.is_movable[:] = False
        self.color = [ [] for _ in range(9) ]
        self.axis = np.zeros(3)
        self.name = name

class rubiks_cube():

    def restore(self):
        """ Restore positions of squares, which should not be movable
        """

        self.top.pos[:] = self.top.pos_copy[:]
        self.bottom.pos[:] = self.bottom.pos_copy[:]
        self.left.pos[:] = self.left.pos_copy[:]
        self.right.pos[:] = self.right.pos_copy[:]
        self.front.pos[:] = self.front.pos_copy[:]
        self.back.pos[:] = self.back.pos_copy[:]

        self.top.is_movable[:] = False
        self.bottom.is_movable[:] = False
        self.left.is_movable[:] = False
        self.right.is_movable[:] = False
        self.front.is_movable[:] = False
        self.back.is_movable[:] = False

    def render_cube(self):

        """ Render the Rubik's cube
        
        return: obj: a compound movable object
        
        """

        for obj in self.scene.objects:
            obj.visible = False
            del obj

        self.object_list = []

        self.render_face(self.top)
        self.render_face(self.bottom)
        self.render_face(self.front)
        self.render_face(self.back)
        self.render_face(self.left)
        self.render_face(self.right)

        if len(self.object_list) == 0:
            return None

        return compound(self.object_list)

    def render_face(self, my_face):

        """ Render a face of the Rubik's cube
        """

        for id in range (0, 9):
            #mypos = vector(my_face.pos[id, 0], my_face.pos[id, 1], my_face.pos[id, 2])
            #myaxis = vector(my_face.axis[0], my_face.axis[1], my_face.axis[2])
            mypos = vector(my_face.pos[id, 1], my_face.pos[id, 2], my_face.pos[id, 0])
            myaxis = vector(my_face.axis[1], my_face.axis[2], my_face.axis[0])
            mysize = vector(0.98*self.width, 0.98*self.width, 0.98*self.width)
            mycolor = my_face.color[id]
            c = pyramid(pos=mypos, axis=myaxis, size=mysize, color=mycolor)
            if my_face.is_movable[id]:
                self.object_list.append(c)

    def rotate_face(self, face):
        """ Rotate squares on a face clockwise
        
        param: face: which face to rotate
        
        """
        color = [ [] for _ in range(9) ]

        if face.name != "bottom":

            color[0] = face.color[6] 
            color[1] = face.color[3] 
            color[2] = face.color[0] 
            color[3] = face.color[7] 
            color[4] = face.color[4] 
            color[5] = face.color[1] 
            color[6] = face.color[8] 
            color[7] = face.color[5] 
            color[8] = face.color[2] 

            face.color[:] = color[:]

        else:

            color[0] = face.color[2] 
            color[1] = face.color[5] 
            color[2] = face.color[8] 
            color[3] = face.color[1] 
            color[4] = face.color[4] 
            color[5] = face.color[7] 
            color[6] = face.color[0] 
            color[7] = face.color[3] 
            color[8] = face.color[6] 
            
            face.color[:] = color[:]
    # 
    # right-hand face 
    # 

    def rotate_right_clockwise(self):

        self.move_right_animate(1)
        self.move_right()
        self.render_cube()

    def rotate_right_counter_clockwise(self):

        self.move_right_animate(-1)
        self.move_right_prime()
        self.render_cube()

    def rotate_right_clockwise_twice(self):

        self.move_right_animate(1)
        self.move_right()
        self.render_cube()
        self.move_right_animate(1)
        self.move_right()
        self.render_cube()

    def move_right_animate(self, sign):
        """ Rotate right face clockwise (animation)
        """

        # animation
        self.right.is_movable[:] = True
        self.back.is_movable[2] = True
        self.back.is_movable[5] = True
        self.back.is_movable[8] = True
        self.top.is_movable[2] = True
        self.top.is_movable[5] = True
        self.top.is_movable[8] = True
        self.front.is_movable[2] = True
        self.front.is_movable[5] = True
        self.front.is_movable[8] = True
        self.bottom.is_movable[2] = True
        self.bottom.is_movable[5] = True
        self.bottom.is_movable[8] = True

        box = self.render_cube()
        dtheta = 0.2
        theta = 0.0
        while True:
            rate(30) # limit animation rate, render scene 
            box.rotate(angle= -sign * dtheta, axis=vec(1, 0, 0))
            theta += dtheta
            if theta >= 0.5 * np.pi:
                break

        # restore positions
        self.restore()

    def move_right(self):
        """ Rotate right face clockwise
        """

        # squares on the face

        self.rotate_face(self.right)

        # squares adjacent to the face

        back = [ [] for _ in range(9) ]
        bottom = [ [] for _ in range(9) ]
        front = [ [] for _ in range(9) ]
        top = [ [] for _ in range(9) ]

        back[:] = self.back.color[:]
        back[2] = self.top.color[2]
        back[5] = self.top.color[5]
        back[8] = self.top.color[8]

        bottom[:] = self.bottom.color[:]
        bottom[2] = self.back.color[8]
        bottom[5] = self.back.color[5]
        bottom[8] = self.back.color[2]

        front[:] = self.front.color[:]
        front[2] = self.bottom.color[8]
        front[5] = self.bottom.color[5]
        front[8] = self.bottom.color[2]

        top[:] = self.top.color[:]
        top[2] = self.front.color[2]
        top[5] = self.front.color[5]
        top[8] = self.front.color[8]

        self.back.color[:] = back[:]
        self.bottom.color[:] = bottom[:]
        self.front.color[:] = front[:]
        self.top.color[:] = top[:]

    def move_right_prime(self):
        """ Rotate right face counter-clockwise
        """
        self.move_right()
        self.move_right()
        self.move_right()

    # 
    # left-hand face 
    # 

    def rotate_left_clockwise(self):

        self.move_left_animate(1)
        self.move_left()
        self.render_cube()

    def rotate_left_counter_clockwise(self):

        self.move_left_animate(-1)
        self.move_left_prime()
        self.render_cube()

    def rotate_left_clockwise_twice(self):

        self.move_left_animate(1)
        self.move_left()
        self.render_cube()
        self.move_left_animate(1)
        self.move_left()
        self.render_cube()

    def move_left_animate(self, sign):

        # animation
        self.left.is_movable[:] = True
        self.top.is_movable[0] = True
        self.top.is_movable[3] = True
        self.top.is_movable[6] = True
        self.front.is_movable[0] = True
        self.front.is_movable[3] = True
        self.front.is_movable[6] = True
        self.back.is_movable[0] = True
        self.back.is_movable[3] = True
        self.back.is_movable[6] = True
        self.bottom.is_movable[0] = True
        self.bottom.is_movable[3] = True
        self.bottom.is_movable[6] = True

        box = self.render_cube()
        dtheta = 0.2
        theta = 0.0
        while True:
            rate(30) # limit animation rate, render scene 
            box.rotate(angle=sign * dtheta, axis=vec(1, 0, 0))
            theta += dtheta
            if theta >= 0.5 * np.pi:
                break

        # restore positions
        self.restore()

    def move_left(self):
        """ Rotate left face clockwise
        """

        # squares on the face

        self.rotate_face(self.left)

        # squares adjacent to the face

        top = [ [] for _ in range(9) ]
        front = [ [] for _ in range(9) ]
        bottom = [ [] for _ in range(9) ]
        back = [ [] for _ in range(9) ]

        top[:] = self.top.color[:]
        top[0] = self.back.color[0]
        top[3] = self.back.color[3]
        top[6] = self.back.color[6]

        front[:] = self.front.color[:]
        front[0] = self.top.color[0]
        front[3] = self.top.color[3]
        front[6] = self.top.color[6]

        bottom[:] = self.bottom.color[:]
        bottom[0] = self.front.color[6]
        bottom[3] = self.front.color[3]
        bottom[6] = self.front.color[0]

        back[:] = self.back.color[:]
        back[0] = self.bottom.color[6]
        back[3] = self.bottom.color[3]
        back[6] = self.bottom.color[0]

        self.top.color[:] = top[:]
        self.front.color[:] = front[:]
        self.bottom.color[:] = bottom[:]
        self.back.color[:] = back[:]

    def move_left_prime(self):
        """ Rotate left face counter-clockwise
        """
        self.move_left()
        self.move_left()
        self.move_left()

    # 
    # front face 
    # 

    def rotate_front_clockwise(self):

        self.move_front_animate(1)
        self.move_front()
        self.render_cube()

    def rotate_front_counter_clockwise(self):

        self.move_front_animate(-1)
        self.move_front_prime()
        self.render_cube()

    def rotate_front_clockwise_twice(self):

        self.move_front_animate(1)
        self.move_front()
        self.render_cube()
        self.move_front_animate(1)
        self.move_front()
        self.render_cube()

    def move_front_animate(self, sign):
        """ Rotate front face clockwise (animation)
        """

        # animation
        self.front.is_movable[:] = True
        self.left.is_movable[6] = True
        self.left.is_movable[7] = True
        self.left.is_movable[8] = True
        self.right.is_movable[6] = True
        self.right.is_movable[7] = True
        self.right.is_movable[8] = True
        self.bottom.is_movable[6] = True
        self.bottom.is_movable[7] = True
        self.bottom.is_movable[8] = True
        self.top.is_movable[6] = True
        self.top.is_movable[7] = True
        self.top.is_movable[8] = True

        box = self.render_cube()
        dtheta = 0.2
        theta = 0.0
        while True:
            rate(30) # limit animation rate, render scene 
            box.rotate(angle=-sign * dtheta, axis=vec(0, 0, 1))
            theta += dtheta
            if theta >= 0.5 * np.pi:
                break

        # restore positions
        self.restore()

    def move_front(self):
        """ Rotate front face clockwise
        """

        # squares on the face

        self.rotate_face(self.front)

        # squares adjacent to the face

        left = [ [] for _ in range(9) ]
        bottom = [ [] for _ in range(9) ]
        top = [ [] for _ in range(9) ]
        right = [ [] for _ in range(9) ]

        left[:] = self.left.color[:]
        left[6] = self.bottom.color[8]
        left[7] = self.bottom.color[7]
        left[8] = self.bottom.color[6]

        bottom[:] = self.bottom.color[:]
        bottom[6] = self.right.color[8]
        bottom[7] = self.right.color[7]
        bottom[8] = self.right.color[6]

        top[:] = self.top.color[:]
        top[6] = self.left.color[6]
        top[7] = self.left.color[7]
        top[8] = self.left.color[8]

        right[:] = self.right.color[:]
        right[6] = self.top.color[6]
        right[7] = self.top.color[7]
        right[8] = self.top.color[8]

        self.left.color[:] = left[:]
        self.bottom.color[:] = bottom[:]
        self.top.color[:] = top[:]
        self.right.color[:] = right[:]

    def move_front_prime(self):
        """ Rotate front face counter-clockwise
        """
        self.move_front()
        self.move_front()
        self.move_front()

    # 
    # back face 
    # 

    def rotate_back_clockwise(self):

        self.move_back_animate(1)
        self.move_back()
        self.render_cube()

    def rotate_back_counter_clockwise(self):

        self.move_back_animate(-1)
        self.move_back_prime()
        self.render_cube()

    def rotate_back_clockwise_twice(self):

        self.move_back_animate(1)
        self.move_back()
        self.render_cube()
        self.move_back_animate(1)
        self.move_back()
        self.render_cube()

    def move_back_animate(self, sign):
        """ Rotate back face clockwise (animation)
        """

        # animation
        self.back.is_movable[:] = True
        self.left.is_movable[0] = True
        self.left.is_movable[1] = True
        self.left.is_movable[2] = True
        self.right.is_movable[0] = True
        self.right.is_movable[1] = True
        self.right.is_movable[2] = True
        self.bottom.is_movable[0] = True
        self.bottom.is_movable[1] = True
        self.bottom.is_movable[2] = True
        self.top.is_movable[0] = True
        self.top.is_movable[1] = True
        self.top.is_movable[2] = True

        box = self.render_cube()
        dtheta = 0.2
        theta = 0.0
        while True:
            rate(30) # limit animation rate, render scene 
            box.rotate(angle=sign * dtheta, axis=vec(0, 0, 1))
            theta += dtheta
            if theta >= 0.5 * np.pi:
                break

        # restore positions
        self.restore()

    def move_back(self):
        """ Rotate back face clockwise
        """

        # squares on the face

        self.rotate_face(self.back)

        # squares adjacent to the face

        left = [ [] for _ in range(9) ]
        bottom = [ [] for _ in range(9) ]
        top = [ [] for _ in range(9) ]
        right = [ [] for _ in range(9) ]

        left[:] = self.left.color[:]
        left[0] = self.top.color[0]
        left[1] = self.top.color[1]
        left[2] = self.top.color[2]

        bottom[:] = self.bottom.color[:]
        bottom[0] = self.left.color[2]
        bottom[1] = self.left.color[1]
        bottom[2] = self.left.color[0]

        top[:] = self.top.color[:]
        top[0] = self.right.color[0]
        top[1] = self.right.color[1]
        top[2] = self.right.color[2]

        right[:] = self.right.color[:]
        right[0] = self.bottom.color[2]
        right[1] = self.bottom.color[1]
        right[2] = self.bottom.color[0]

        self.left.color[:] = left[:]
        self.bottom.color[:] = bottom[:]
        self.top.color[:] = top[:]
        self.right.color[:] = right[:]

    def move_back_prime(self):
        """ Rotate back face counter-clockwise
        """
        self.move_back()
        self.move_back()
        self.move_back()

    # 
    # top face 
    # 

    def rotate_top_clockwise(self):

        self.move_top_animate(1)
        self.move_top()
        self.render_cube()

    def rotate_top_counter_clockwise(self):

        self.move_top_animate(-1)
        self.move_top_prime()
        self.render_cube()

    def rotate_top_clockwise_twice(self):

        self.move_top_animate(1)
        self.move_top()
        self.render_cube()
        self.move_top_animate(1)
        self.move_top()
        self.render_cube()

    def move_top_animate(self, sign):
        """ Rotate top face clockwise (animation)
        """

        # animation
        self.top.is_movable[:] = True
        self.front.is_movable[0] = True
        self.front.is_movable[1] = True
        self.front.is_movable[2] = True
        self.right.is_movable[0] = True
        self.right.is_movable[3] = True
        self.right.is_movable[6] = True
        self.back.is_movable[6] = True
        self.back.is_movable[7] = True
        self.back.is_movable[8] = True
        self.left.is_movable[2] = True
        self.left.is_movable[5] = True
        self.left.is_movable[8] = True

        box = self.render_cube()
        dtheta = 0.2
        theta = 0.0
        while True:
            rate(30) # limit animation rate, render scene 
            box.rotate(angle=-sign * dtheta, axis=vec(0, 1, 0))
            theta += dtheta
            if theta >= 0.5 * np.pi:
                break

        # restore positions
        self.restore()

    def move_top(self):
        """ Rotate top face clockwise
        """

        # squares on the face

        self.rotate_face(self.top)

        # squares adjacent to the face

        front = [ [] for _ in range(9) ]
        left = [ [] for _ in range(9) ]
        back = [ [] for _ in range(9) ]
        right = [ [] for _ in range(9) ]

        front[:] = self.front.color[:]
        front[0] = self.right.color[6]
        front[1] = self.right.color[3]
        front[2] = self.right.color[0]

        left[:] = self.left.color[:]
        left[2] = self.front.color[0]
        left[5] = self.front.color[1]
        left[8] = self.front.color[2]

        back[:] = self.back.color[:]
        back[6] = self.left.color[8]
        back[7] = self.left.color[5]
        back[8] = self.left.color[2]

        right[:] = self.right.color[:]
        right[0] = self.back.color[6]
        right[3] = self.back.color[7]
        right[6] = self.back.color[8]

        self.front.color[:] = front[:]
        self.left.color[:] = left[:]
        self.back.color[:] = back[:]
        self.right.color[:] = right[:]

    def move_top_prime(self):
        """ Rotate top face counter-clockwise
        """
        self.move_top()
        self.move_top()
        self.move_top()

    # 
    # bottom face 
    # 

    def rotate_bottom_clockwise(self):

        self.move_bottom_animate(1)
        self.move_bottom()
        self.render_cube()

    def rotate_bottom_counter_clockwise(self):

        self.move_bottom_animate(-1)
        self.move_bottom_prime()
        self.render_cube()

    def rotate_bottom_clockwise_twice(self):

        self.move_bottom_animate(1)
        self.move_bottom()
        self.render_cube()
        self.move_bottom_animate(1)
        self.move_bottom()
        self.render_cube()

    def move_bottom_animate(self, sign):
        """ Rotate top face clockwise (animation)
        """

        # animation
        self.bottom.is_movable[:] = True
        self.front.is_movable[6] = True
        self.front.is_movable[7] = True
        self.front.is_movable[8] = True
        self.right.is_movable[2] = True
        self.right.is_movable[5] = True
        self.right.is_movable[8] = True
        self.back.is_movable[0] = True
        self.back.is_movable[1] = True
        self.back.is_movable[2] = True
        self.left.is_movable[0] = True
        self.left.is_movable[6] = True
        self.left.is_movable[3] = True

        box = self.render_cube()
        dtheta = 0.2
        theta = 0.0
        while True:
            rate(30) # limit animation rate, render scene 
            box.rotate(angle=+sign * dtheta, axis=vec(0, 1, 0))
            theta += dtheta
            if theta >= 0.5 * np.pi:
                break

        # restore positions
        self.restore()

    def move_bottom(self):
        """ Rotate bottom face clockwise
        """

        # squares on the face

        self.rotate_face(self.bottom)

        # squares adjacent to the face

        back = [ [] for _ in range(9) ]
        left = [ [] for _ in range(9) ]
        front = [ [] for _ in range(9) ]
        right = [ [] for _ in range(9) ]

        back[:] = self.back.color[:]
        back[0] = self.right.color[2]
        back[1] = self.right.color[5]
        back[2] = self.right.color[8]

        left[:] = self.left.color[:]
        left[0] = self.back.color[2]
        left[3] = self.back.color[1]
        left[6] = self.back.color[0]

        front[:] = self.front.color[:]
        front[6] = self.left.color[0]
        front[7] = self.left.color[3]
        front[8] = self.left.color[6]

        right[:] = self.right.color[:]
        right[2] = self.front.color[8]
        right[5] = self.front.color[7]
        right[8] = self.front.color[6]

        self.back.color[:] = back[:]
        self.left.color[:] = left[:]
        self.front.color[:] = front[:]
        self.right.color[:] = right[:]

    def move_bottom_2(self):
        """ Rotate bottom face twice
        """
        self.move_bottom()
        self.move_bottom()

    def move_bottom_prime(self):
        """ Rotate bottom face counter-clockwise
        """
        self.move_bottom()
        self.move_bottom()
        self.move_bottom()

    def move_equator_xz(self):
        """ Rotate middle squares: front->top, top->back, back->bottom, bottom->front
        """

        top = [ [] for _ in range(9) ]
        back = [ [] for _ in range(9) ]
        bottom = [ [] for _ in range(9) ]
        front = [ [] for _ in range(9) ]

        top[:] = self.top.color[:]
        top[1] = self.front.color[1]
        top[4] = self.front.color[4]
        top[7] = self.front.color[7]

        back[:] = self.back.color[:]
        back[1] = self.top.color[1]
        back[4] = self.top.color[4]
        back[7] = self.top.color[7]

        bottom[:] = self.bottom.color[:]
        bottom[1] = self.back.color[7]
        bottom[4] = self.back.color[4]
        bottom[7] = self.back.color[1]

        front[:] = self.front.color[:]
        front[1] = self.bottom.color[7]
        front[4] = self.bottom.color[4]
        front[7] = self.bottom.color[1]

        self.top.color[:] = top[:]
        self.back.color[:] = back[:]
        self.bottom.color[:] = bottom[:]
        self.front.color[:] = front[:]

    # AED - this one is untested
    def move_equator_yz(self):
        """ Rotate middle squares: left->top, top->right, right->bottom, bottom->left
        """

        # animation
        self.top.is_movable[3] = True
        self.top.is_movable[4] = True
        self.top.is_movable[5] = True
        self.right.is_movable[3] = True
        self.right.is_movable[4] = True
        self.right.is_movable[5] = True
        self.bottom.is_movable[3] = True
        self.bottom.is_movable[4] = True
        self.bottom.is_movable[5] = True
        self.left.is_movable[3] = True
        self.left.is_movable[4] = True
        self.left.is_movable[5] = True

        box = self.render_cube()
        dtheta = 0.2
        theta = 0.0
        while True:
            rate(30) # limit animation rate, render scene 
            box.rotate(angle=-dtheta, axis=vec(0, 0, 1))
            theta += dtheta
            if theta >= 0.5 * np.pi:
                break

        # restore positions 
        self.restore()

        top = [ [] for _ in range(9) ]
        right = [ [] for _ in range(9) ]
        bottom = [ [] for _ in range(9) ]
        left = [ [] for _ in range(9) ]

        top[:] = self.top.color[:]
        top[3] = self.left.color[3]
        top[4] = self.left.color[4]
        top[5] = self.left.color[5]

        right[:] = self.right.color[:]
        right[3] = self.top.color[3]
        right[4] = self.top.color[4]
        right[5] = self.top.color[5]

        bottom[:] = self.bottom.color[:]
        bottom[3] = self.right.color[5]
        bottom[4] = self.right.color[4]
        bottom[5] = self.right.color[3]

        left[:] = self.left.color[:]
        left[3] = self.bottom.color[5]
        left[4] = self.bottom.color[4]
        left[5] = self.bottom.color[3]

        self.top.color[:] = top[:]
        self.right.color[:] = right[:]
        self.bottom.color[:] = bottom[:]
        self.left.color[:] = left[:]

    def move_equator_xy(self):
        """ Rotate middle squares: front->left, left->back, back->right, right->front
        """

        left = [ [] for _ in range(9) ]
        back = [ [] for _ in range(9) ]
        right = [ [] for _ in range(9) ]
        front = [ [] for _ in range(9) ]

        left[:] = self.left.color[:]
        left[1] = self.front.color[3]
        left[4] = self.front.color[4]
        left[7] = self.front.color[5]

        back[:] = self.back.color[:]
        back[3] = self.left.color[7]
        back[4] = self.left.color[4]
        back[5] = self.left.color[1]

        right[:] = self.right.color[:]
        right[1] = self.back.color[3]
        right[4] = self.back.color[4]
        right[7] = self.back.color[5]

        front[:] = self.front.color[:]
        front[3] = self.right.color[7]
        front[4] = self.right.color[4]
        front[5] = self.right.color[1]

        self.left.color[:] = left[:]
        self.back.color[:] = back[:]
        self.right.color[:] = right[:]
        self.front.color[:] = front[:]

    def bring_to_top(self, face):
        """ Bring a given face to the top
        
        param: face: which face to bring to the top
        
        """

        if face == "front":

            # animation
            self.top.is_movable[:] = True
            self.bottom.is_movable[:] = True
            self.front.is_movable[:] = True
            self.back.is_movable[:] = True
            self.left.is_movable[:] = True
            self.right.is_movable[:] = True

            box = self.render_cube()
            dtheta = 0.2
            theta = 0.0
            while True:
                rate(30) # limit animation rate, render scene 
                box.rotate(angle=-dtheta, axis=vec(1, 0, 0))
                theta += dtheta
                if theta >= 0.5 * np.pi:
                    break

            # restore positions
            self.restore()

            self.move_equator_xz()
            self.move_right()
            self.move_left_prime()

            self.render_cube()

        elif face == "back":

            # animation
            self.top.is_movable[:] = True
            self.bottom.is_movable[:] = True
            self.front.is_movable[:] = True
            self.back.is_movable[:] = True
            self.left.is_movable[:] = True
            self.right.is_movable[:] = True

            box = self.render_cube()
            dtheta = 0.2
            theta = 0.0
            while True:
                rate(30) # limit animation rate, render scene 
                box.rotate(angle=+dtheta, axis=vec(1, 0, 0))
                theta += dtheta
                if theta >= 0.5 * np.pi:
                    break

            # restore positions
            self.restore()

            self.move_equator_xz()
            self.move_equator_xz()
            self.move_equator_xz()
            self.move_right_prime()
            self.move_left()

            self.render_cube()

        elif face == "bottom":

            self.bring_to_top("front")
            self.bring_to_top("front")

        elif face == "left":

            self.bring_to_front("left")
            self.bring_to_top("front")

        elif face == "right":

            self.bring_to_front("right")
            self.bring_to_top("front")

    def bring_to_front(self, face):
        """ Bring a given face to the front
        
        param: face: which face to bring to the front
        
        """

        if face == "right":

            # animation
            self.top.is_movable[:] = True
            self.bottom.is_movable[:] = True
            self.front.is_movable[:] = True
            self.back.is_movable[:] = True
            self.left.is_movable[:] = True
            self.right.is_movable[:] = True

            box = self.render_cube()
            dtheta = 0.2
            theta = 0.0
            while True:
                rate(30) # limit animation rate, render scene 
                box.rotate(angle=-dtheta, axis=vec(0, 1, 0))
                theta += dtheta
                if theta >= 0.5 * np.pi:
                    break

            # restore positions 
            self.restore()

            self.move_equator_xy()
            self.move_top()
            self.move_bottom_prime()

            self.render_cube()

        elif face == "left":

            # animation
            self.top.is_movable[:] = True
            self.bottom.is_movable[:] = True
            self.front.is_movable[:] = True
            self.back.is_movable[:] = True
            self.left.is_movable[:] = True
            self.right.is_movable[:] = True

            box = self.render_cube()
            dtheta = 0.2
            theta = 0.0
            while True:
                rate(30) # limit animation rate, render scene 
                box.rotate(angle=+dtheta, axis=vec(0, 1, 0))
                theta += dtheta
                if theta >= 0.5 * np.pi:
                    break

            # restore positions 
            self.restore()

            self.move_equator_xy()
            self.move_equator_xy()
            self.move_equator_xy()
            self.move_top_prime()
            self.move_bottom()

            self.render_cube()

        elif face == "back":

            self.bring_to_front("right")
            self.bring_to_front("right")

        elif face == "top":

            self.bring_to_top("back")

        elif face == "bottom":

            self.bring_to_top("front")

    def __init__(self, scene):

        """ Rubik's cube class

        param: scene: the vpython scene

        Attributes
        ----------
        
        width: the width of a square
        top: top face of the cube
        bottom: bottom face of the cube
        front: front face of the cube
        back: back face of the cube
        left: left face of the cube
        right: right face of the cube

        """

        # the scene
        self.scene = scene

        # object list
        self.object_list = []

        # width of a square
        self.width = 1.0

        # define positions of squares on each face

        # the origin (0, 0, 0) should be the back
        # left corner, indicated by the arrows

        # x increases toward the front of the cube
        # y increases to the right
        # z increases toward the top of the cube

        #          -> 0|1|2                            
        #             3|4|5                            
        #             6|7|8                            
        #                                              
        #   -> 0|1|2  0|1|2  0|1|2                     
        #      3|4|5  3|4|5  3|4|5                     
        #      6|7|8  6|7|8  6|7|8                     
        #                                              
        #             0|1|2         -> 0|1|2        
        #             3|4|5            3|4|5        
        #             6|7|8            6|7|8     

        self.top = face("top")
        for x in range (0, 3):
            for y in range (0, 3):
                id = x*3 + y
                self.top.pos[id, :] = np.array([x * self.width, y * self.width, 2.5 * self.width])
                self.top.color[id] = color_map["white"]
                self.top.axis[:] = np.array([0, 0, -1])

        self.bottom = face("bottom")
        for x in range (0, 3):
            for y in range (0, 3):
                id = x*3 + y
                self.bottom.pos[id, :] = np.array([x * self.width, y * self.width, -0.5 * self.width])
                self.bottom.axis[:] = np.array([0, 0, 1])
                self.bottom.color[id] = color_map["yellow"]

        self.front = face("front")
        for y in range (0, 3):
            for z in range (0, 3):
                id = (2-z)*3 + y
                self.front.pos[id, :] = np.array([2.5 * self.width, y * self.width, z * self.width])
                self.front.axis[:] = np.array([-1, 0, 0])
                self.front.color[id] = color_map["red"]

        self.back = face("back")
        for y in range (0, 3):
            for z in range (0, 3):
                id = z*3 + y
                self.back.pos[id, :] = np.array([-0.5 * self.width, y * self.width, z * self.width])
                self.back.axis[:] = np.array([1, 0, 0])
                self.back.color[id] = color_map["orange"]

        self.left = face("left")
        for x in range (0, 3):
            for z in range (0, 3):
                id = x*3 + z
                self.left.pos[id, :] = np.array([x * self.width, -0.5 * self.width, z * self.width])
                self.left.axis[:] = np.array([0, 1, 0])
                self.left.color[id] = color_map["blue"]

        self.right = face("right")
        for x in range (0, 3):
            for z in range (0, 3):
                id = x*3 + (2-z)
                self.right.pos[id, :] = np.array([x * self.width, 2.5 * self.width, z * self.width])
                self.right.axis[:] = np.array([0, -1, 0])
                self.right.color[id] = color_map["green"]

        # backup the positions of the faces
        self.front.pos_copy[:,:] = self.front.pos[:,:]
        self.back.pos_copy[:,:] = self.back.pos[:,:]
        self.left.pos_copy[:,:] = self.left.pos[:,:]
        self.right.pos_copy[:,:] = self.right.pos[:,:]
        self.top.pos_copy[:,:] = self.top.pos[:,:]
        self.bottom.pos_copy[:,:] = self.bottom.pos[:,:]

        # render cube
        self.render_cube()

