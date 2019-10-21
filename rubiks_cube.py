'''
Rubiks Cube
Author: John Kinder

Requirements: PyGame

Description: A Computer version of Rubik's Cube.
Creates an instance with the colored squares for each 3 x 3 side.
Shuffles the rows / columns prior to initial view being presented.
Externally available methods:
To move the current view:
- move_right()
- move_left()
- move_up()
- move_down()

To shift cells:
- shift_h(direction['left','right'], row[0,1,2])
- shift_v(direction['up','down'], column[0,1,2])

Viewing:
- get_adjacent(['up','down','left','right','back'])
    Returns 3x3 list of colors for the side given.
- check_matched: Returns True if all sides colors match. False otherwise.
'''

from collections import defaultdict

class RubiksCube:
    '''Class for the game.'''
    def __init__(self, debug=False):
        '''Do all initializations and set the current view to side 0'''
        self.__DEBUG = debug
        self.__side = 0
        self.__orientation = 0
        self.__views = defaultdict(list)
        self.__build_views()
        self.__sides = defaultdict(dict)
        for i in range(6):
            self.__build_side(i)
        self.__fill_squares()
        self.__shuffle()

    def __fill_squares(self):
        '''Used by __init__ to populate each side with a color.
        They are shuffled in another method.'''
        for side, color in ((0, 'red'), (1, 'blue'), (2, 'green'), (3, 'yellow'),
                            (4, 'white'), (5, 'orange')):
            for row in range(3):
                for col in range(3):
                    self.__sides[side][(row, col)] = color

    def __build_views(self):
        '''There are 4 possible top left positions of a Rubiks Cube.
        Each 3 x 3 side cell is labeled 0 through 8, so the 4 corners are:
        0, 2, 6, and 8.
        Each of the 3 x 3 arrays per side contain a tuple that relates
        to the [row][column] position of the side in view depending on
        top left.
        Also builds shift_left and shift_right lists to re-position colors for
        adjacent sides.'''
        self.__views[0] = [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)]]
        self.__views[2] = [[(0, 2), (1, 2), (2, 2)], [(0, 1), (1, 1), (2, 1)], [(0, 0), (1, 0), (2, 0)]]
        self.__views[6] = [[(2, 0), (1, 0), (0, 0)], [(2, 1), (1, 1), (0, 1)], [(2, 2), (1, 2), (0, 2)]]
        self.__views[8] = [[(2, 2), (2, 1), (2, 0)], [(1, 2), (1, 1), (1, 0)], [(0, 2), (0, 1), (0, 0)]]

    def __build_side(self, side):
        '''Used by __init__ to set up how each side (0 - 5) relates to
        those adjacent to it and what the top left cell would be
        if you move to one of the available adjacent sides.'''
        if side == 0:
            self.__sides[side][0] = {1: 0, 3: 0, 4: 0, 5: 0,
                                     'left': 3, 'right': 1, 'up': 4, 'down': 5}
            self.__sides[side][2] = {1: 2, 3: 2, 4: 2, 5: 2,
                                     'left': 4, 'right': 5, 'up': 1, 'down': 3}
            self.__sides[side][6] = {1: 6, 3: 6, 4: 6, 5: 6,
                                     'left': 5, 'right': 4, 'up': 3, 'down': 1}
            self.__sides[side][8] = {1: 8, 3: 8, 4: 8, 5: 8,
                                     'left': 1, 'right': 3, 'up': 5, 'down': 4}
        elif side == 1:
            self.__sides[side][0] = {0: 0, 2: 0, 4: 6, 5: 2,
                                     'left': 0, 'right': 2, 'up': 4, 'down': 5}
            self.__sides[side][2] = {0: 2, 2: 2, 4: 0, 5: 8,
                                     'left': 4, 'right': 5, 'up': 2, 'down': 0}
            self.__sides[side][6] = {0: 6, 2: 6, 4: 8, 5: 0,
                                     'left': 5, 'right': 4, 'up': 0, 'down': 2}
            self.__sides[side][8] = {0: 8, 2: 8, 4: 2, 5: 6,
                                     'left': 2, 'right': 0, 'up': 5, 'down': 4}
        elif side == 2:
            self.__sides[side][0] = {1: 0, 3: 0, 4: 8, 5: 8,
                                     'left': 1, 'right': 3, 'up': 4, 'down': 5}
            self.__sides[side][2] = {1: 2, 3: 2, 4: 6, 5: 6,
                                     'left': 4, 'right': 5, 'up': 3, 'down': 1}
            self.__sides[side][6] = {1: 6, 3: 6, 4: 2, 5: 2,
                                     'left': 5, 'right': 4, 'up': 1, 'down': 3}
            self.__sides[side][8] = {1: 8, 3: 8, 4: 0, 5: 0,
                                     'left': 3, 'right': 1, 'up': 5, 'down': 4}
        elif side == 3:
            self.__sides[side][0] = {0: 0, 2: 0, 4: 2, 5: 6,
                                     'left': 2, 'right': 0, 'up': 4, 'down': 5}
            self.__sides[side][2] = {0: 2, 2: 2, 4: 8, 5: 0,
                                     'left': 4, 'right': 5, 'up': 0, 'down': 2}
            self.__sides[side][6] = {0: 6, 2: 6, 4: 0, 5: 8,
                                     'left': 5, 'right': 4, 'up': 2, 'down': 0}
            self.__sides[side][8] = {0: 8, 2: 8, 4: 6, 5: 2,
                                     'left': 0, 'right': 2, 'up': 5, 'down': 4}
        elif side == 4:
            self.__sides[side][0] = {0: 0, 1: 2, 2: 8, 3: 6,
                                     'left': 3, 'right': 1, 'up': 2, 'down': 0}
            self.__sides[side][2] = {0: 2, 1: 8, 2: 6, 3: 0,
                                     'left': 2, 'right': 0, 'up': 1, 'down': 3}
            self.__sides[side][6] = {0: 6, 1: 0, 2: 2, 3: 8,
                                     'left': 0, 'right': 2, 'up': 3, 'down': 1}
            self.__sides[side][8] = {0: 8, 1: 6, 2: 0, 3: 2,
                                     'left': 1, 'right': 3, 'up': 0, 'down': 2}
        elif side == 5:
            self.__sides[side][0] = {0: 0, 1: 6, 2: 8, 3: 2,
                                     'left': 3, 'right': 1, 'up': 0, 'down': 2}
            self.__sides[side][2] = {0: 2, 1: 0, 2: 6, 3: 8,
                                     'left': 0, 'right': 2, 'up': 1, 'down': 3}
            self.__sides[side][6] = {0: 6, 1: 8, 2: 2, 3: 0,
                                     'left': 2, 'right': 0, 'up': 3, 'down': 1}
            self.__sides[side][8] = {0: 8, 1: 2, 2: 0, 3: 6,
                                     'left': 1, 'right': 3, 'up': 2, 'down': 0}


    def __get_color(self, side, top_left, row, col):
        '''Return the current color of a side, row, col'''
        view = self.__views[top_left]
        current_row, current_col = view[row][col]
        color = self.__sides[side][(current_row, current_col)]
        return color


    def __shift_side(self, side, direction):
        '''Used to shift the outter row, col combinations when the horizontal
        row or vertical column being manipulated is 0 or 2'''
        right_shift = ([(0, 0),(0, 2)],[(0, 1),(1, 2)],[(0, 2),(2, 2)],[(1, 0),(0, 1)],
                      [(1, 2), (2, 1)], [(2, 0), (0, 0)], [(2, 1), (1, 0)], [(2, 2), (2, 0)])
        left_shift = ([(0, 0),(2, 0)],[(0, 1),(1, 0)],[(0, 2),(0, 0)],[(1, 0),(2, 1)],
                       [(1, 2), (0, 1)], [(2, 0), (2, 2)], [(2, 1), (1, 2)], [(2, 2), (0, 2)])
        temp_dict = {}
        if self.__DEBUG:
            print('{} Shift Side {} - {} {}'.format('-' * 5, side, direction, '-' * 5))
        # Same loop can be used for making these changes, so determine which direction
        # and set to it
        if direction == 'left':
            shift_tup = left_shift
        else:
            shift_tup = right_shift

        # We need a listing of the current colors for each cell
        for cell in shift_tup:
            cell = cell[0]
            temp_dict[cell] = self.__sides[side][cell]

        for from_cell, to_cell in shift_tup:
            self.__sides[side][to_cell] = temp_dict[from_cell]

    def __shuffle(self):
        '''Used by __init__ to make random row and column moves.'''
        from random import choice
        if self.__DEBUG:
            print('{}\nSTARTING SHUFFLE\n{}'.format('*' * 30, '*' * 30))
        for i in range(10):
            row = choice([0,1,2])
            direction = choice(['left','right'])
            self.shift_h(direction, row)
            col = choice([0,1,2])
            direction = choice(['up', 'down'])
            self.shift_v(direction, col)
        if self.__DEBUG:
            print('{}\nFINISHED SHUFFLE\n{}'.format('*' * 30, '*' * 30))

    def shift_h(self, direction, row):
        '''Shift the cells horizontally for the direction and row given'''
        # If not valid entries for either, ignore.
        if direction not in ['left','right'] or row not in [0,1,2]:
            return None
        current_side = self.__side
        current_top_left = self.__orientation
        if self.__DEBUG:
            print('{} Move horizontal {}, Row {} {}'.format('=' * 5, direction, row, '=' * 5))
            print('Start: Side = {}\tTop Left = {}'.format(current_side, current_top_left))

        current_values = [] # To hold the three colors to use on the next side
        for col in range(3):
            color = self.__get_color(current_side, current_top_left, row, col)
            #color = self.__sides[current_side][(row, col)]
            if self.__DEBUG:
                print('({:d}, {:d}) - {:s}'.format(row, col, color))
            current_values.append(color)

        # Shift the given row around the cube.
        for _ in range(4):
            side = self.__sides[current_side][current_top_left][direction]
            top_left = self.__sides[current_side][current_top_left][side]
            if self.__DEBUG:
                print('Next Side: {}, Next TopLeft: {}'.format(side, top_left))
                print('Current colors:', current_values)
            new_values = []
            for col in range(3):
                color = self.__get_color(side, top_left, row, col)
                if self.__DEBUG:
                    print('({:d}, {:d}) - {:s}'.format(row, col, color))
                new_values.append(color)
                if self.__DEBUG:
                    print('Replace {} with {}'.format(color, current_values[col]))
                self.__sides[side][self.__views[top_left][row][col]] = current_values[col]
            current_side = side
            current_top_left = top_left
            current_values = new_values.copy()
        if row != 1:
            # Row is either 0 or 2, which require a bottom or top shift
            if row == 0:
                side = self.__sides[current_side][current_top_left]['up']
                if direction == 'right': direction = 'left'
                else: direction = 'right'
            else:
                side = self.__sides[current_side][current_top_left]['down']
            self.__shift_side(side, direction)


    def shift_v(self, direction, col):
        '''Shift the cells vertically for the direction and column given'''
        # If not valid entries for either, ignore.
        if direction not in ['up','down'] or col not in [0,1,2]:
            return None
        current_side = self.__side
        current_top_left = self.__orientation
        if self.__DEBUG:
            print('{} Move vertical {}, Column {} {}'.format('=' * 5, direction, col, '=' * 5))
            print('Start: Side = {}\tColumn = {}\tTop Left = {}'.format(current_side, col, current_top_left))

        current_values = [] # Hold the 3 colors to use on the next side.
        for row in range(3):
            color = self.__get_color(current_side, current_top_left, row, col)
            #color = self.__sides[current_side][(row, col)]
            if self.__DEBUG:
                print('({:d}, {:d}) - {:s}'.format(row, col, color))
            current_values.append(color)

        # Shift the given column around the cube
        for _ in range(4):
            side = self.__sides[current_side][current_top_left][direction]
            top_left = self.__sides[current_side][current_top_left][side]
            if self.__DEBUG:
                print('Next Side: {}, Next TopLeft: {}'.format(side, top_left))
                print('Current colors:', current_values)
            new_values = []
            for row in range(3):
                color = self.__get_color(side, top_left, row, col)
                if self.__DEBUG:
                    print('({:d}, {:d}) - {:s}'.format(row, col, color))
                new_values.append(color)
                if self.__DEBUG:
                    print('Replace {} with {}'.format(color, current_values[row]))
                self.__sides[side][self.__views[top_left][row][col]] = current_values[row]
            current_side = side
            current_top_left = top_left
            current_values = new_values.copy()

        if col != 1:
            # Either column 0 or 2, requiring a shift on the left or right
            # For the sides, there is only a left or right shift, not up or down.
            if col == 0:
                side = self.__sides[current_side][current_top_left]['left']
                if direction == 'up': direction = 'left'
                else: direction = 'right'
            else:
                side = self.__sides[current_side][current_top_left]['right']
                if direction == 'up': direction = 'right'
                else: direction = 'left'
            self.__shift_side(side, direction)


    def get_adjacent(self, direction):
        '''Used to get the 3 x 3 colors of the up, left, right, or bottom
        direction based on the current view side and orientatin (top left)'''
        side = self.__side
        orientation = self.__orientation
        return_list = [['', '', ''], ['', '', ''], ['', '', '']]
        if direction == 'back':
            tmp_side = self.__sides[side][orientation]['right']
            tmp_orientation = self.__sides[side][orientation][tmp_side]
            adjacent_side = self.__sides[tmp_side][tmp_orientation]['right']
            adjacent_orientation = self.__sides[tmp_side][tmp_orientation][adjacent_side]
        else:
            adjacent_side = self.__sides[side][orientation][direction]
            adjacent_orientation = self.__sides[side][orientation][adjacent_side]

        for row in range(3):
            for col in range(3):
                current_row, current_col = self.__views[adjacent_orientation][row][col]
                return_list[row][col] = self.__sides[adjacent_side][(current_row, current_col)]
        return return_list


    def check_matched(self):
        '''See if all cells on a side are the same color.'''
        for side in (0, 1, 2, 3, 4, 5):
            match_color = self.__sides[side][(0, 0)]
            for row in range(3):
                for col in range(3):
                    if row == 0:
                        col = 1
                    if self.__sides[side][(row, col)] != match_color:
                        return False
        return True


    def move_right(self):
        '''Move the current side in view to the next gong right.'''
        new_side = self.__sides[self.__side][self.__orientation]['right']
        self.__orientation = self.__sides[self.__side][self.__orientation][new_side]
        self.__side = new_side


    def move_left(self):
        '''Move the current side in view to the next gong left.'''
        new_side = self.__sides[self.__side][self.__orientation]['left']
        self.__orientation = self.__sides[self.__side][self.__orientation][new_side]
        self.__side = new_side


    def move_up(self):
        '''Move the current side in view to the next gong up.'''
        new_side = self.__sides[self.__side][self.__orientation]['up']
        self.__orientation = self.__sides[self.__side][self.__orientation][new_side]
        self.__side = new_side


    def move_down(self):
        '''Move the current side in view to the next gong down.'''
        new_side = self.__sides[self.__side][self.__orientation]['down']
        self.__orientation = self.__sides[self.__side][self.__orientation][new_side]
        self.__side = new_side


    def get_view(self):
        '''Returns the 3x3 list of colors for the rows / columns'''
        side = self.__side
        return_list = [['','',''],['','',''],['','','']]
        current_view = self.__views[self.__orientation]
        for i in range(3):
            for j in range(3):
                current_row, current_col = current_view[i][j]
                return_list[i][j] = self.__sides[side][(current_row, current_col)]
        return side, self.__orientation, return_list
