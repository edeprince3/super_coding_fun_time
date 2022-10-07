from rubiks_cube import *

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

class rubiks_cube_solver(rubiks_cube):

    def jumble_cube(self, n):
        """
            randomize cube

            param: n: number of random moves to make
        """

        import random

        for i in range (0, n):
            move = random.randrange(0,14,1)
            if move == 0:
                self.rotate_right_clockwise()
            if move == 1:
                self.rotate_right_counter_clockwise()
            if move == 2:
                self.rotate_left_clockwise()
            if move == 3:
                self.rotate_left_counter_clockwise()
            if move == 4:
                self.rotate_front_clockwise()
            if move == 5:
                self.rotate_front_counter_clockwise()
            if move == 6:
                self.rotate_back_clockwise()
            if move == 7:
                self.rotate_back_counter_clockwise()
            if move == 8:
                self.rotate_top_clockwise()
            if move == 9:
                self.rotate_top_counter_clockwise()
            if move == 10:
                self.rotate_bottom_clockwise()
            if move == 11:
                self.rotate_bottom_counter_clockwise()
            if move == 12:
                self.bring_to_front("left")
            if move == 13:
                self.bring_to_top("front")


    def locate_origin(self):
        """

            find the face with the white square in the center 
            and bring that face to the top

        """

        if self.front.color[4] == color_map["white"]:
            self.bring_to_top("front")
        elif self.back.color[4] == color_map["white"]:
            self.bring_to_top("back")
        elif self.left.color[4] == color_map["white"]:
            self.bring_to_top("left")
        elif self.right.color[4] == color_map["white"]:
            self.bring_to_top("right")
        elif self.bottom.color[4] == color_map["white"]:
            self.bring_to_top("bottom")

    def form_cross(self):
        """
            step 1 of solving the top layer: form cross of white squares
        """

        # four white side pieces
        for i in range (0, 4):

            # locate a white side pieces in a face other than the top
            # it always will be found in positions 1, 3, 5, 7

            which_face = "top"

            list = [self.bottom, self.front, self.back, self.left, self.right]
            for face in list:
                if face.color[1] == color_map["white"]:
                    which_face = face.name
                    break
                elif face.color[3] == color_map["white"]:
                    which_face = face.name
                    break
                elif face.color[5] == color_map["white"]:
                    which_face = face.name
                    break
                elif face.color[7] == color_map["white"]:
                    which_face = face.name
                    break

            # a side piece is on the top, possibly in the wrong place. if so, move it to the bottom
            if which_face == "top" :

                if self.top.color[1] == color_map["white"] and self.back.color[7] != self.back.color[4] :
                    self.rotate_back_clockwise_twice()
                    which_face = "bottom"

                elif self.top.color[3] == color_map["white"] and self.left.color[5] != self.left.color[4] :
                    self.rotate_left_clockwise_twice()
                    which_face = "bottom"

                elif self.top.color[5] == color_map["white"] and self.right.color[3] != self.right.color[4] :
                    self.rotate_right_clockwise_twice()
                    which_face = "bottom"

                elif self.top.color[7] == color_map["white"] and self.front.color[1] != self.front.color[4] :
                    self.rotate_front_clockwise_twice()
                    which_face = "bottom"

                # must be in the right spot ... skip the rest of the logic
                else:
                    continue


            # move that side piece to the bottom layer, if it's not already there
            if which_face != "bottom" :

                self.bring_to_front(which_face)

                if self.front.color[1] == color_map["white"] :

                    self.rotate_front_clockwise()
                    self.rotate_right_counter_clockwise()
                    self.rotate_bottom_clockwise()
                    self.rotate_right_clockwise()
                    self.rotate_front_counter_clockwise()

                elif self.front.color[3] == color_map["white"] :

                    self.rotate_left_clockwise()
                    self.rotate_bottom_clockwise()
                    self.rotate_left_counter_clockwise()

                elif self.front.color[5] == color_map["white"] :

                    self.rotate_right_counter_clockwise()
                    self.rotate_bottom_clockwise()
                    self.rotate_right_clockwise()

                elif self.front.color[7] == color_map["white"] :

                    self.rotate_front_counter_clockwise()
                    self.rotate_right_counter_clockwise()
                    self.rotate_bottom_clockwise()
                    self.rotate_right_clockwise()
                    self.rotate_front_clockwise()

            # now, bring that piece back to the top

            # 1. who is white?
            # 2. which face has my adjacent color as center? 
            me = -1
            adjacent_color = vector(-1,-1,-1)

            if self.bottom.color[1] == color_map["white"] : 
                me = 1 
                adjacent_color = self.back.color[1]

            elif self.bottom.color[3] == color_map["white"] : 
                me = 3
                adjacent_color = self.left.color[3]

            elif self.bottom.color[5] == color_map["white"] : 
                me = 5
                adjacent_color = self.right.color[5]

            elif self.bottom.color[7] == color_map["white"] : 
                me = 7
                adjacent_color = self.front.color[7]

            # bring face with adjacent matching color to the front

            if adjacent_color == self.left.color[4]:
                self.bring_to_front("left")

            elif adjacent_color == self.right.color[4]:
                self.bring_to_front("right")

            elif adjacent_color == self.back.color[4]:
                self.bring_to_front("back")

            # now, recheck who is white
            if self.bottom.color[1] == color_map["white"] and self.back.color[1] == self.front.color[4] :
                me = 1

            elif self.bottom.color[3] == color_map["white"] and self.left.color[3] == self.front.color[4] :
                me = 3

            elif self.bottom.color[5] == color_map["white"] and self.right.color[5] == self.front.color[4] :
                me = 5

            elif self.bottom.color[7] == color_map["white"] and self.front.color[7] == self.front.color[4] :
                me = 7

            # and finally bring the square back to the top
            if me == 1 :
                self.rotate_bottom_clockwise_twice()
                self.rotate_front_clockwise_twice()

            elif me == 3 :
                self.rotate_bottom_clockwise()
                self.rotate_front_clockwise_twice()

            elif me == 5 :
                self.rotate_bottom_counter_clockwise()
                self.rotate_front_clockwise_twice()

            elif me == 7 :
                self.rotate_front_clockwise_twice()


    """
        
        Here we are solving the first layer by inserting corner pieces
        in their appropriate locations. To be inserted, a corner must
        be in the third row with white exposed to a side.  
        
        There are four possible incorrect spots a white corner could be.
    
        1. top face in wrong position
        2. side face in top row
        3. side face in bottom row
        4. bottom face 
    
        and they will alwasy be in positions 0, 2, 6, or 8
        
    """

    def find_white_corner_on_side_faces(self):
        """

            find a white corner that needs to be inserted
            in the top layer and bring its face to the front.
            only consider the side faces (left, right, front, back)

            return: found_corner: did we find one?
            return: position: the position of the white corner square

        """

        found_corner = False

        face_list = [self.left, self.front, self.right, self.back]
        pos_list = [0, 2, 6, 8]

        for face in face_list:
            for pos in pos_list:
                if face.color[pos] == color_map["white"]:
                    found_corner = True
                    break

            if found_corner: 
                self.bring_to_front(face.name)
                for pos in pos_list:
                    if self.front.color[pos] == color_map["white"]:
                        return found_corner, pos

        # i guess we didn't find one
        return found_corner, -1

    def insert_white_corner(self, position):
        """

            insert a white corner into the top layer

            param: position: the position of the white corner square (on the front face)

        """

        # white corner should now be on the front face. bring to position 6 or 8

        target_side = None

        if position == 0 :

            self.rotate_front_counter_clockwise()
            self.rotate_bottom_counter_clockwise()
            self.rotate_front_clockwise()
            self.bring_to_front("left")
            target_side = "left"

        elif position == 2:

            self.rotate_front_clockwise()
            self.rotate_bottom_clockwise()
            self.rotate_front_counter_clockwise()
            self.bring_to_front("right")
            target_side = "right"

        elif position == 6:
            target_side = "left"

        elif position == 8:
            target_side = "right"

        # corner should now be on front in bottom layer on left or right

        if target_side == "left":
            pass

            # find the top corner that matches cornerprime. there are only four options

            exposed = self.left.color[6] 
            under   = self.bottom.color[6]

            if self.left.color[4] == exposed :

                if self.front.color[4] == under :

                    self.rotate_bottom_clockwise()
                    self.rotate_left_clockwise()
                    self.rotate_bottom_counter_clockwise()
                    self.rotate_left_counter_clockwise()

                else :

                   self.rotate_back_clockwise()
                   self.rotate_bottom_counter_clockwise()
                   self.rotate_back_counter_clockwise()
                
            elif self.right.color[4] == exposed :

                if self.front.color[4] == under :

                    self.rotate_down_clockwise_twice()
                    self.rotate_front_clockwise()
                    self.rotate_down_counter_clockwise()
                    self.rotate_front_couter_clockwise()

                else :

                    self.rotate_right_clockwise()
                    self.rotate_bottom_clockwise_twice()
                    self.rotate_right_counter_clockwise()

            elif self.front.color[4] == exposed :

                if self.left.color[4] == under :

                    self.rotate_bottom_clockwise()
                    self.rotate_left_clockwise()
                    self.rotate_bottom_counter_clockwise()
                    self.rotate_left_counter_clockwise()

                else :

                    self.rotate_bottom_clockwise_twice()
                    self.rotate_front_clockwise()
                    self.rotate_bottom_counter_clockwise()
                    self.rotate_front_counter_clockwise()

            elif self.back.color[4] == exposed :

                if self.left.color[4] == under :

                    self.rotate_back_clockwise()
                    self.rotate_bottom_counter_clockwise()
                    self.rotate_back_counter_clockwise()

                else :

                    self.rotate_right_clockwise()
                    self.rotate_bottom_clockwise_twice()
                    self.rotate_right_counter_clockwise()
        else:

            # find the top corner that matches cornerprime. there are only four options

            exposed = self.right.color[8]
            under   = self.bottom.color[8]

            if self.left.color[4] == exposed :

               if self.front.color[4] == under :

                  print("i don't think this is possible")
                  exit()

               else: 

                  self.rotate_left_counter_clockwise()
                  self.rotate_bottom_clockwise_twice()
                  self.rotate_left_clockwise()

            elif self.right.color[4] == exposed :

                if self.front.color[4] == under :

                    self.rotate_bottom_counter_clockwise()
                    self.rotate_right_counter_clockwise()
                    self.rotate_bottom_clockwise()
                    self.rotate_right_clockwise()

                else :

                    print("i don't think this is possible")
                    exit()

            elif self.front.color[4] == exposed :

                if self.left.color[4] == under :

                    self.rotate_bottom_clockwise_twice()
                    self.rotate_front_counter_clockwise()
                    self.rotate_bottom_clockwise()
                    self.rotate_front_clockwise()

                else :

                    print("i don't think this is possible")
                    exit()

            elif self.back.color[4] == exposed :

                if self.left.color[4] == under :

                    print("i don't think this is possible")
                    exit()

                else :

                    # R is under
                    self.rotate_back_counter_clockwise()
                    self.rotate_bottom_clockwise()
                    self.rotate_back_clockwise()

    def solve_top_layer(self):
        """
        
            solve top layer, given that the cross has already been formed
        
        """

        # four possible corners to insert

        for i in range (0, 4):

            found_corner, position = self.find_white_corner_on_side_faces()

            # if not found, piece must be on top or bottom face
            if not found_corner: 

                # must be on top or bottom face

                # check is fist layer is solved
                if self.top.color[0] == color_map["white"] :
                    if self.left.color[2] == self.left.color[5] and self.back.color[6] == self.back.color[7] :
                        if self.top.color[2] == color_map["white"] :
                            if self.right.color[0] == self.right.color[3] and self.back.color[8] == self.back.color[7] :
                                if self.top.color[8] == color_map["white"] :
                                    if self.right.color[6] == self.right.color[3] and self.front.color[2] == self.front.color[1] :
                                        if self.top.color[6] == color_map["white"] :
                                            if self.left.color[8] == self.left.color[5] or self.front.color[0] == self.front.color[1] :
                                                break

                # check if piece is in fist layer in wrong position. if so, bring it to position 6
                if self.top.color[0] == color_map["white"] :
                    if self.left.color[2] != self.left.color[5] or self.back.color[6] != self.back.color[7] :
                        found_corner = True
                        self.bring_to_front("left")

                elif self.top.color[2] == color_map["white"] :
                    if self.right.color[0] != self.right.color[3] or self.back.color[8] != self.back.color[7] :
                        found_corner = True
                        self.bring_to_front("back")

                elif self.top.color[8] == color_map["white"] :
                    if self.right.color[6] != self.right.color[3] or self.front.color[2] != self.front.color[1] :
                        found_corner = True
                        self.bring_to_front("right")

                elif self.top.color[6] == color_map["white"] :
                    if self.left.color[8] != self.left.color[5] or self.front.color[0] != self.front.color[1] :
                        found_corner = True

                # now, if we found the white corner, put it in the front face, in position 8

                if found_corner :

                    self.rotate_left_clockwise()
                    self.rotate_bottom_clockwise()
                    self.rotate_left_counter_clockwise()

                    found_corner, position = self.find_white_corner_on_side_faces()

                else : # check if piece is in the bottom layer

                    # first rerotate cube so that the empty corner is in the top face, in position 8

                    if self.top.color[0] != color_map["white"] :
                        self.bring_to_front("back")

                    elif self.top.color[2] != color_map["white"] : 
                        self.bring_to_front("right")

                    elif self.top.color[6] != color_map["white"] :
                        self.bring_to_front("left")


                     # now move white piece to bottom face, position 6

                    if self.bottom.color[0] == color_map["white"] :

                       found_corner = True
                       self.rotate_bottom_clockwise()

                    elif self.bottom.color[2] == color_map["white"] :

                       found_corner = True
                       self.rotate_bottom_clockwise_twice()

                    elif self.bottom.color[8] == color_map["white"] :

                       found_corner = True
                       self.rotate_bottom_counter_clockwise()

                    elif self.bottom.color[6] == color_map["white"] :

                       found_corner = True

                    # insert bottom white piece into top layer
                    self.rotate_right_counter_clockwise()
                    self.rotate_bottom_clockwise()
                    self.rotate_right_clockwise()

                    # look for piece again
                    found_corner, position = self.find_white_corner_on_side_faces()

                if not found_corner :

                    print("didn't find a corner ... something is very wrong here.")
                    exit()

            self.insert_white_corner(position)
            
    """
        
        Here we are solving the middle layer by inserting edge pieces
        in their appropriate locations. 
        
    """

    def solve_middle_layer(self):
        """
            solve middle layer
        """

        wrong = "front"

        # four edges to move
        for i in range (0, 4):
            found_edge = self.find_edge_piece_on_bottom_layer()

            # edge pieces must be in the middle layer
            if not found_edge :

                # first check if middle layer already solved
                wrong = None

                if self.front.color[3] != self.front.color[4] : 
                    wrong = "front"

                elif self.front.color[5] != self.front.color[4] : 
                    wrong = "front"

                elif self.left.color[1] != self.left.color[4] :
                    wrong = "left"
                    self.bring_to_front("left")

                elif self.left.color[7] != self.left.color[4] :
                    wrong = "left"
                    self.bring_to_front("left")

                elif self.right.color[1] != self.right.color[4] :
                    wrong = "right"
                    self.bring_to_front("right")

                elif self.right.color[7] != self.right.color[4] :
                    wrong = "right"
                    self.bring_to_front("right")

                elif self.back.color[3] != self.back.color[4] :
                    wrong = "back"
                    self.bring_to_front("back")

                elif self.back.color[5] != self.back.color[4] :
                    wrong = "back"
                    self.bring_to_front("back")

                if wrong == None :
                    #print("edge must be in correct position already")
                    pass

                else :

                    if self.front.color[5] != self.front.color[4] : 
                        self.bring_to_front("right")

                    self.rotate_bottom_clockwise()
                    self.rotate_left_clockwise()
                    self.rotate_bottom_counter_clockwise()
                    self.rotate_left_counter_clockwise()
                    self.rotate_bottom_counter_clockwise()
                    self.rotate_front_counter_clockwise()
                    self.rotate_bottom_clockwise()
                    self.rotate_front_clockwise()

                    found_edge = self.find_edge_piece_on_bottom_layer()

            front_color = self.front.color[7]
            if front_color == self.left.color[4] :
                self.rotate_bottom_counter_clockwise()
                self.bring_to_front("left")

            elif front_color == self.back.color[4] :
                self.rotate_bottom_clockwise_twice()
                self.bring_to_front("back")

            elif front_color == self.right.color[4] :
                self.rotate_bottom_clockwise()
                self.bring_to_front("right")

            if wrong != None :
                self.insert_edge_into_middle_layer()
    

    def insert_edge_into_middle_layer(self):
        """
            insert edge piece into the middle layer
        """

        if self.bottom.color[7] == self.left.color[4] :

            self.rotate_bottom_clockwise()
            self.rotate_left_clockwise()
            self.rotate_bottom_counter_clockwise()
            self.rotate_left_counter_clockwise()
            self.rotate_bottom_counter_clockwise()
            self.rotate_front_counter_clockwise()
            self.rotate_bottom_clockwise()
            self.rotate_front_clockwise()

        elif self.bottom.color[7] == self.right.color[4] :

            self.bring_to_front("right")
            self.rotate_bottom_counter_clockwise()
            self.rotate_front_counter_clockwise()
            self.rotate_bottom_clockwise()
            self.rotate_front_clockwise()
            self.rotate_bottom_clockwise()
            self.rotate_left_clockwise()
            self.rotate_bottom_counter_clockwise()
            self.rotate_left_counter_clockwise()

        else:

            print("uh oh my cube_data isn't solvable")
            exit()



    def find_edge_piece_on_bottom_layer(self):
        """
            find edge piece on the bottom layer that needs to be inserted
            in the middle layer. if the colors on the edge don't match
            that in position 4 of the bottom layer, then the edge
            piece is one we're looking for

            return: found_edge: did we find an edge that needs to move?
        """

        bottom_color = self.bottom.color[4]

        if self.front.color[7] != bottom_color and self.bottom.color[7] != bottom_color :
            return True

        if self.left.color[3] != bottom_color and self.bottom.color[3] != bottom_color :
            self.bring_to_front("left")
            return True

        if self.right.color[5] != bottom_color and self.bottom.color[5] != bottom_color :
            self.bring_to_front("right")
            return True

        if self.back.color[1] != bottom_color and self.bottom.color[1] != bottom_color :
            self.bring_to_front("back");
            return True

        return False


    def form_bottom_cross(self):
        """
            form cross in the last/bottom layer (which is brought to the top)
        """

        self.bring_to_top("bottom")

        state = "neither"

        while state != "solved" :

            state = self.bottom_cross_state() 
            #print(" what state is bottom in?", state)

            if state == "l-shaped" :

                if self.top.color[1] != self.top.color[4] :

                    if self.top.color[5] != self.top.color[4] :
                        self.bring_to_front("right")

                    elif self.top.color[3] != self.top.color[4] :
                        self.bring_to_front("back")

                elif self.top.color[3] != self.top.color[4] :

                    if self.top.color[7] != self.top.color[4] :  
                        self.bring_to_front("left")

                self.rotate_front_clockwise()
                self.rotate_top_clockwise()
                self.rotate_right_clockwise()
                self.rotate_top_counter_clockwise()
                self.rotate_right_counter_clockwise()
                self.rotate_front_counter_clockwise()

            if state == "line" :

                if self.top.color[1] == self.top.color[4] : 
                    self.bring_to_front("right")

                self.rotate_front_clockwise()
                self.rotate_right_clockwise()
                self.rotate_top_clockwise()
                self.rotate_right_counter_clockwise()
                self.rotate_top_counter_clockwise()
                self.rotate_front_counter_clockwise()

            if state == "neither" :
                #print("      bottom state neither l-shaped nor line")

                # apply one of the moves algorithms to try to get to a line or l-shape
                self.rotate_front_clockwise()
                self.rotate_right_clockwise()
                self.rotate_top_clockwise()
                self.rotate_right_counter_clockwise()
                self.rotate_top_counter_clockwise()
                self.rotate_front_counter_clockwise()

                #print("      checking bottom state again...")

    def bottom_cross_state(self):
        """
            determine state of bottom layer (actually the top) so the 
            cross can be formed. possible states are l-shaped, line,
            and neither
        """

        # four choices for bottom state: solved, l-shaped, line, neither

        color = self.top.color[4]

        if self.top.color[1] == color :
            if self.top.color[3] == color :
                if self.top.color[5] == color :
                    if self.top.color[7] == color :
                        return "solved"
                    return "neither"
                return "l-shaped"
            elif self.top.color[5] == color :
                if self.top.color[7] == color : 
                    return "neither"
                return "l-shaped"
            elif self.top.color[7] == color :
                return "line"
            return "neither"
        elif self.top.color[3] == color :
            if self.top.color[5] == color :
                if self.top.color[7] == color : 
                    return "neither"
                return "line"
            elif self.top.color[7] == color :
                return "l-shaped"
            return "neither"
        elif self.top.color[5] == color :
            if self.top.color[7] == color : 
                return "l-shaped"
            return "neither"

        return "neither"

    def vector_list(self, my_list):

        """
            convert list of vectors to something hashable. assume maximum
            value of vector element is 1 (true for the color vectors we're using)
        """

        new_list = []
        for vec in my_list:
            val = vec.x * 4 + vec.y * 2 + vec.z
            new_list.append(val)

        return new_list

    def permute_bottom_corners(self):

        """
            permute bottom corners to their correct positions
        """

        # can do this by checking the order of corners (clockwise)

        # identify correct order:

        corner1 = self.vector_list([ self.left.color[7], self.front.color[3], self.top.color[4] ])
        corner2 = self.vector_list([ self.back.color[3], self.left.color[1], self.top.color[4] ])
        corner3 = self.vector_list([ self.right.color[1], self.back.color[5], self.top.color[4] ])
        corner4 = self.vector_list([ self.front.color[5], self.right.color[7], self.top.color[4] ])

        # identify current state
        mycorner1 = self.vector_list([ self.front.color[0], self.left.color[8], self.top.color[6] ])
        mycorner2 = self.vector_list([ self.left.color[2], self.back.color[6], self.top.color[0] ])
        mycorner3 = self.vector_list([ self.back.color[8], self.right.color[0], self.top.color[2] ])
        mycorner4 = self.vector_list([ self.right.color[6], self.front.color[2], self.top.color[8] ])

        # which corner is corner 1? rotate top piece

        if set(mycorner2) == set(corner1) :
            self.rotate_top_counter_clockwise()

        elif set(mycorner3) == set(corner1) :
            self.rotate_top_clockwise_twice() 

        elif set(mycorner4) == set(corner1) :
            self.rotate_top_clockwise()

        # identify current state
        mycorner1 = self.vector_list([ self.front.color[0], self.left.color[8], self.top.color[6] ])
        mycorner2 = self.vector_list([ self.left.color[2], self.back.color[6], self.top.color[0] ])
        mycorner3 = self.vector_list([ self.back.color[8], self.right.color[0], self.top.color[2] ])
        mycorner4 = self.vector_list([ self.right.color[6], self.front.color[2], self.top.color[8] ])

        # LU'R'UL'U'RU2

        # which corners need to be swapped?

        # 1234 - done
        if set(mycorner2) == set(corner2) and set(mycorner3) == set(corner3) and set(mycorner4) == set(corner4) :
            return

        # 1243 - swap 3/4
        elif set(mycorner2) == set(corner2) and set(mycorner3) == set(corner4) and set(mycorner4) == set(corner3) :
            self.swap_two_corners()
            return

        # 1342 - swap 1/2 
        if set(mycorner2) == set(corner3) and set(mycorner3) == set(corner4) and set(mycorner4) == set(corner2) :
            self.bring_to_front("left")
            self.swap_two_corners()
            return

        # 1423 - swap 1/4
        if set(mycorner2) == set(corner4) and set(mycorner3) == set(corner2) and set(mycorner4) == set(corner3) :
            self.bring_to_front("back")
            self.swap_two_corners()
            return

        # 1324 - swap 2/3 (this is diagonal)
        # 1432 - swap 4/2 (this is diagonal)

        # for all diagonal options:
        self.swap_two_corners()
        self.permute_bottom_corners() 

    def swap_two_corners(self):
        """
            swap two corners on the top layer

                0|1|2        0|1|8        
                3|4|5   ->   3|4|5        
                6|7|8        6|7|2  
        """

        self.rotate_left_clockwise()
        self.rotate_top_counter_clockwise()
        self.rotate_right_counter_clockwise()
        self.rotate_top_clockwise()
        self.rotate_left_counter_clockwise()
        self.rotate_top_counter_clockwise()
        self.rotate_right_clockwise()
        self.rotate_top_clockwise_twice()

    def orient_bottom_corners(self):
        """
            once bottom corners are in correct positions, orient them correctly
        """

        # start by identify correct order:

        corner1 = self.vector_list([ self.left.color[7] , self.front.color[3], self.top.color[4] ])
        corner2 = self.vector_list([ self.back.color[3] , self.left.color[1], self.top.color[4] ])
        corner3 = self.vector_list([ self.right.color[1] , self.back.color[5], self.top.color[4] ])
        corner4 = self.vector_list([ self.front.color[5] , self.right.color[7], self.top.color[4] ])

        # and comparing that to the current state
        mycorner2 = self.vector_list([ self.left.color[2], self.back.color[6], self.top.color[0] ])
        mycorner3 = self.vector_list([ self.back.color[8], self.right.color[0], self.top.color[2] ])
        mycorner4 = self.vector_list([ self.right.color[6], self.front.color[2], self.top.color[8] ])

        if set(mycorner2) == set(corner1) :
            self.rotate_top_counter_clockwise()
        if set(mycorner3) == set(corner1) :
            self.rotate_top_clockwise_twice()
        if set(mycorner4) == set(corner1) :
            self.rotate_top_clockwise()

        # now, determine the state and solve
        state = self.which_bottom_corner_state()
        #print("      corner state", state)

        if state != 0 :
            self.solve_bottom_corner_state(state) 

    def which_bottom_corner_state(self):
        """
            determine bottom corner state so that corners can be oriented. there
            are seven possible states

            return: state: the bottom corner state
        """

        state = -999;
        count = 0

        if self.top.color[0] == self.top.color[4] :
            count += 1
        if self.top.color[2] == self.top.color[4] :
            count += 1
        if self.top.color[6] == self.top.color[4] :
            count += 1
        if self.top.color[8] == self.top.color[4] :
            count += 1

        # which state?
        if count == 4 : 
            state = 0

        elif count == 0 :

            if self.back.color[6] == self.back.color[8] and self.front.color[0] == self.front.color[2] : 
                state = 7
            elif self.right.color[0] == self.right.color[6] and self.left.color[2] == self.left.color[8] : 
                state = 7
            else :
                state = 6

        elif count == 1 :

            if self.back.color[8] == self.right.color[6] and self.right.color[6] == self.front.color[0] : 
                state = 1
            elif self.right.color[6] == self.front.color[0] and self.front.color[0] == self.left.color[2] : 
                state = 1
            elif self.front.color[0] == self.left.color[2] and self.left.color[2] == self.back.color[8] : 
                state = 1
            elif self.left.color[2] == self.back.color[8] and self.back.color[8] == self.right.color[6] : 
                state = 1
            else :
                state = 2

        else :

            if self.top.color[0] == self.top.color[8] or self.top.color[2] == self.top.color[6] : 
                state = 5
            elif self.back.color[8] == self.front.color[2] and self.back.color[8] == self.top.color[4] :
                state = 4
            elif self.back.color[6] == self.front.color[0] and self.back.color[6] == self.top.color[4] :
                state = 4
            elif self.right.color[0] == self.left.color[2] and self.right.color[0] == self.top.color[4] :
                state = 4
            elif self.right.color[6] == self.left.color[8] and self.right.color[6] == self.top.color[4] :
                state = 4
            else :
                state = 3

        return state

    def solve_bottom_corner_state(self, state):
        """
            actually orient the corners, with knowledge of the current state

            param: state: the bottom corner state
        """

        if state == 1 :

            # bring bottom-colored piece to u(0)
            if self.top.color[2]== self.top.color[4] :
                self.bring_to_front("left")
            elif self.top.color[6] == self.top.color[4] :
                self.bring_to_front("right")
            elif self.top.color[8] == self.top.color[4] :
                self.bring_to_front("back")

            self.corner_state_1_algorithm()

        elif state == 2 :

            # bring bottom-colored piece to u(6)
            if self.top.color[0] == self.top.color[4] :
                self.bring_to_front("left")
            elif self.top.color[2] == self.top.color[4] : 
                self.bring_to_front("back")
            elif self.top.color[8] == self.top.color[4] : 
                self.bring_to_front("right")

            self.corner_state_2_algorithm()

        elif state == 3 :

            if self.left.color[2] == self.top.color[4] :
                self.bring_to_front("right")
            elif self.front.color[0] == self.top.color[4] :
                self.bring_to_front("back")
            elif self.right.color[0] == self.top.color[4] :
                self.bring_to_front("left")

            self.corner_state_1_algorithm()
            self.bring_to_front("back")
            self.corner_state_2_algorithm()

        elif state == 4 :
            if self.back.color[8] == self.top.color[4] :
                self.bring_to_front("back")
            elif self.left.color[2] == self.top.color[4] :
                self.bring_to_front("left")
            elif self.left.color[8] == self.top.color[4] :
                self.bring_to_front("right")

            self.corner_state_2_algorithm()
            self.corner_state_1_algorithm()

        elif state == 5 :

            if self.left.color[8] == self.top.color[4] :
                self.bring_to_front("right")
            elif self.right.color[0] == self.top.color[4] :
                self.bring_to_front("left")
            elif self.front.color[2] == self.top.color[4] :
                self.bring_to_front("back")

            self.corner_state_1_algorithm()
            self.bring_to_front("right")
            self.corner_state_2_algorithm()

        elif state == 6 :

            if self.back.color[6] == self.top.color[4] and self.back.color[8] == self.top.color[4] :
                self.bring_to_front("left")
            elif self.right.color[0] == self.top.color[4] and self.right.color[6] == self.top.color[4] :
                self.bring_to_front("back")
            elif self.front.color[0] == self.top.color[4] and self.front.color[2] == self.top.color[4] :
                self.bring_to_front("right")

            self.corner_state_2_algorithm()
            self.bring_to_front("right")
            self.corner_state_2_algorithm()

        elif state == 7 :

            if self.back.color[6] == self.top.color[4] :
                self.bring_to_front("right");

            self.corner_state_1_algorithm()
            self.bring_to_front("back")
            self.corner_state_1_algorithm()


    def corner_state_1_algorithm(self):
        """
            orient bottom corners when in state 1
        """

        self.rotate_right_counter_clockwise()
        self.rotate_top_counter_clockwise()
        self.rotate_right_clockwise()
        self.rotate_top_counter_clockwise()
        self.rotate_right_counter_clockwise()
        self.rotate_top_clockwise_twice()
        self.rotate_right_clockwise()
        self.rotate_top_clockwise_twice()

    def corner_state_2_algorithm(self):
        """
            orient bottom corners when in state 2
        """

        self.rotate_right_clockwise()
        self.rotate_top_clockwise()
        self.rotate_right_counter_clockwise()
        self.rotate_top_clockwise()
        self.rotate_right_clockwise()
        self.rotate_top_clockwise_twice()
        self.rotate_right_counter_clockwise()
        self.rotate_top_clockwise_twice()

    def permute_bottom_edges(self):
        """
            bring bottom edges to correct posisions ("bottom" is currently the top layer)
        """

        state = self.which_bottom_edge_state();
        #print("      edge state",state)

        if state == 0 :
            pass

        elif state == 1 :

            if self.left.color[5] == self.right.color[4] :
                self.bring_to_front("left")
            elif self.back.color[7] == self.front.color[4] : 
                self.bring_to_front("back")
            elif self.right.color[3] == self.left.color[4] : 
                self.bring_to_front("right")

            self.edge_state_1_algorithm()

        elif state == 2 :

            if self.right.color[3] == self.left.color[4] : 
                self.bring_to_front("left")
            elif self.front.color[1] == self.back.color[4] :
                self.bring_to_front("back")
            elif self.left.color[5] == self.right.color[4] :
                self.bring_to_front("right")

            self.edge_state_2_algorithm()

        elif state == 3 :

            self.edge_state_1_algorithm()
            self.permute_bottom_edges()

        elif state == 4 :

            self.edge_state_1_algorithm()
            self.permute_bottom_edges()

    def which_bottom_edge_state(self):
        """
            determine bottom edge state

            return: state: bottom edge state
        """

        state = 0

        if self.front.color[1] == self.back.color[4] and self.back.color[7] == self.right.color[4] : state = 1
        elif self.left.color[5] == self.right.color[4] and self.right.color[3] == self.front.color[4] : state = 1
        elif self.back.color[7] == self.front.color[4] and self.front.color[1] == self.left.color[4] : state = 1
        elif self.right.color[3] == self.left.color[4] and self.left.color[5] == self.back.color[4] : state = 1
        elif self.back.color[7] == self.front.color[4] and self.front.color[1] == self.right.color[4] : state = 2
        elif self.left.color[5] == self.right.color[4] and self.right.color[3] == self.back.color[4] : state = 2
        elif self.front.color[1] == self.back.color[4] and self.back.color[7] == self.left.color[4] : state = 2
        elif self.right.color[3] == self.left.color[4] and self.left.color[5] == self.front.color[4] : state = 2
        elif self.back.color[7] == self.front.color[4] and self.front.color[1] == self.back.color[4] : state = 3
        elif self.back.color[7] == self.right.color[4] and self.left.color[5] == self.front.color[4] : state = 4
        elif self.back.color[7] == self.left.color[4] and self.right.color[3] == self.front.color[4] : state = 4

        return state;

    def edge_state_1_algorithm(self):
        """
            algorithm for permuting bottom edges when in state 1
        """

        self.rotate_right_clockwise_twice()
        self.rotate_top_clockwise()
        self.rotate_front_clockwise()
        self.rotate_back_counter_clockwise()
        self.rotate_right_clockwise_twice()
        self.rotate_front_counter_clockwise()
        self.rotate_back_clockwise()
        self.rotate_top_clockwise()
        self.rotate_right_clockwise_twice()

    def edge_state_2_algorithm(self):
        """
            algorithm for permuting bottom edges when in state 2
        """

        self.rotate_right_clockwise_twice()
        self.rotate_top_counter_clockwise()
        self.rotate_front_clockwise()
        self.rotate_back_counter_clockwise()
        self.rotate_right_clockwise_twice()
        self.rotate_front_counter_clockwise()
        self.rotate_back_clockwise()
        self.rotate_top_counter_clockwise()
        self.rotate_right_clockwise_twice()


