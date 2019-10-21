'''
RCGame.py

Author: John Kinder
Description: A Rubik's Cube display using pygame.
'''

import pygame, sys
from rubiks_cube import RubiksCube

pygame.init()

# Allow a single argument of debug in order to see printed
# processing information
debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == 'debug':
        debug = True

# Some constants
WHITE_BG = (255,255,255)    # Background color
GREY_BG = (128, 128, 128)   # Background color for bottom portion
BLACK = (0,0,0)             # Text color
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 725
START_X = 150               # X start position of the cube
START_Y = 100               # Y start position of the cube
# Image sizes - Small for displaying adjacent sides
IMAGE_SIZE = 100
SMALL_IMAGE_SIZE = 20
CUBE_SIZE = 300
# Center of the display with Y eliminating the lower section for adjacent sides
X_CENTER = SCREEN_WIDTH / 2
Y_CENTER = (START_Y * 2 + CUBE_SIZE) / 2

# Grey rect for adjacent sides display area
BOTTOM_GREY_RECT = pygame.Rect(0, START_Y * 2 + CUBE_SIZE - 20, SCREEN_WIDTH,
                          SCREEN_HEIGHT - (START_Y * 2 + CUBE_SIZE + 10))

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Rubiks Cube')

# Flag to indicate whether or not to do something
process_event = False


'''
Below are for shifting a column or row on the cube.
We capture the postions up to CAPTURE_SIZE while MOUSEMOTION and RIGHT_BTN_DOWN.
Analysis is done on the postions to determine either a vertical or horizontal shift
and the column or row.
'''
RIGHT_BTN_DOWN = False
positions = []
capture_count = 0
CAPTURE_SIZE = 25

'''
The 3 x 3 list returns colornames for each element.
Matching the image loaded to those and creating small
images to use in the grey adjacent sides display area.
'''
colors_dict = {}
for color in ['white', 'blue', 'yellow', 'orange', 'green', 'red']:
    image = '{}.png'.format(color)
    small_image = 'small_{}'.format(color)
    colors_dict[color] = pygame.image.load(image)
    colors_dict[small_image] = pygame.image.load(image)
    colors_dict[small_image] = pygame.transform.scale(colors_dict[small_image],
                                            (SMALL_IMAGE_SIZE, SMALL_IMAGE_SIZE))



def display_adjacent_sides():
    '''For displaying the up, down, left, and right adjacent side, and the back side.'''
    for i, direction in enumerate(['up', 'left', 'right', 'down', 'back']):
        color_list = cube.get_adjacent(direction)
        if i == 0:      # up direction
            start_x = X_CENTER - ((SMALL_IMAGE_SIZE * 3 / 2) + 100)
            start_y = START_Y * 2 + CUBE_SIZE
            message_display('Top', 10, start_x + (SMALL_IMAGE_SIZE * 1.5), start_y - 10)
        elif i == 1:    # left direction
            start_x = START_X - 100
            start_y = START_Y * 2 + CUBE_SIZE + SMALL_IMAGE_SIZE * 3
            message_display('Left', 10,start_x + (SMALL_IMAGE_SIZE * 1.5), start_y - 10)
        elif i == 2:    # right direction
            start_x = (START_X - 100 + CUBE_SIZE) - SMALL_IMAGE_SIZE * 3
            start_y = START_Y * 2 + CUBE_SIZE + SMALL_IMAGE_SIZE * 3
            message_display('Right', 10, start_x + (SMALL_IMAGE_SIZE * 1.5), start_y - 10)
        elif i == 3:
            # down direction
            start_x = X_CENTER - ((SMALL_IMAGE_SIZE * 3 / 2) + 100)
            start_y = (START_Y * 2 + CUBE_SIZE) + SMALL_IMAGE_SIZE * 6
            message_display('Bottom', 10, start_x + (SMALL_IMAGE_SIZE * 1.5), start_y - 10)
        else:   # back
            start_x = (START_X  + 50 + CUBE_SIZE) - SMALL_IMAGE_SIZE * 3
            start_y = START_Y * 2 + CUBE_SIZE + SMALL_IMAGE_SIZE * 3
            message_display('Back', 10, start_x + (SMALL_IMAGE_SIZE * 1.5), start_y - 10)

        x = start_x
        y = start_y
        for i in range(3):
            for j in range(3):
                color = 'small_{}'.format(color_list[i][j])
                img = colors_dict[color]
                put_square(img, x, y)
                x += SMALL_IMAGE_SIZE
            y += SMALL_IMAGE_SIZE
            x = start_x


def put_square(image_name, x, y):
    '''blit the image at the given coordinates'''
    gameDisplay.blit(image_name, (x, y))


def text_objects(text, text_font):
    '''Builds a text object'''
    text_surface = text_font.render(text, True, BLACK)
    return text_surface, text_surface.get_rect()


def message_display(text, text_size, x_cord, y_cord):
    '''Displays a text object'''
    text_font = pygame.font.Font('freesansbold.ttf', text_size)
    text_surface, text_rect = text_objects(text, text_font)
    text_rect.center = ((x_cord, y_cord))
    gameDisplay.blit(text_surface, text_rect)


def draw_display():
    '''Draws the display area within the white background.'''
    side, orientation, side_colors = cube.get_view()
    gameDisplay.fill(WHITE_BG)
    gameDisplay.fill(GREY_BG, rect=BOTTOM_GREY_RECT)
    msg_string = 'Side: {} - Top Left: {}'.format(side, orientation)
    message_display(msg_string, 20, X_CENTER, 10)
    message_display('Up', 20, X_CENTER, START_Y - 20)
    message_display('Down', 20, X_CENTER, START_Y + CUBE_SIZE + 15)
    message_display('Left', 20, START_X - 25, Y_CENTER)
    message_display('Right', 20, START_X + CUBE_SIZE + 30, Y_CENTER)
    msg_string = 'Hold down the right mouse button and drag across a row or column, then release to shift the cells.'
    message_display(msg_string, 12, X_CENTER, SCREEN_HEIGHT - 18)
    # Loop through the rows and columns keeping up with the screen position to use.
    start_x = START_X
    start_y = START_Y
    for i in range(3):
        for j in range(3):
            img = colors_dict[side_colors[i][j]]
            put_square(img, start_x, start_y)
            start_x += IMAGE_SIZE
        start_y += IMAGE_SIZE
        start_x = START_X
    display_adjacent_sides()
    # Check for all squares on each side being the same color
    all_matched = cube.check_matched()
    if all_matched:
        message_display('ALL MATCHED!', 50, X_CENTER, 50)
    pygame.display.update()


def check_motions():
    '''Called when the right mouse button is released.
    Checks the motion mouse positions gathered to determine
    if we are to shift a column or row, or do nothing'''
    x_positions = [positions[x][0] for x in range(CAPTURE_SIZE)]
    y_positions = [positions[x][1] for x in range(CAPTURE_SIZE)]
    x_min = min(x_positions)
    x_max = max(x_positions)
    y_min = min(y_positions)
    y_max = max(y_positions)

    # Expecting first and last captures to be within the CUBE
    if x_min < START_X or x_max > (START_X + CUBE_SIZE):
        return False
    if y_min < START_Y or y_max > (START_Y + CUBE_SIZE):
        return False
    # Determine the shift direction
    direction = None
    if (x_max - x_min) < (y_max - y_min):
        if y_positions[0] < y_positions[CAPTURE_SIZE - 1]:
            direction = 'down'
        else:
            direction = 'up'
    elif (y_max - y_min) < (x_max - x_min):
        if x_positions[0] < x_positions[CAPTURE_SIZE - 1]:
            direction = 'right'
        else:
            direction = 'left'
    # Determination of direction not made... just return
    if not direction:
        return False

    # Determine column for vertical shift
    if direction in ['up', 'down']:
        col = None
        x_avg = sum(x_positions) / CAPTURE_SIZE
        current_x = START_X
        for i in range(3):
            if x_avg > current_x and x_avg < (current_x + IMAGE_SIZE):
                col = i
                break
            current_x += IMAGE_SIZE
        if col != None:
            if debug:
                print('{}\nShift col {} - {}\n{}'.format('=' * 20, col, direction, '=' * 20))
            cube.shift_v(direction, col)
            return True
    # Determine row for horizontal shift
    if direction in ['left', 'right']:
        row = None
        y_avg = sum(y_positions) / CAPTURE_SIZE
        current_y = START_Y
        for i in range(3):
            if y_avg > current_y and y_avg < (current_y + IMAGE_SIZE):
                row = i
                break
            current_y += IMAGE_SIZE
        if row != None:
            if debug:
                print('{}\nShift row {} - {}\n{}'.format('=' * 20, row, direction, '=' * 20))
            cube.shift_h(direction, row)
            return True
    return False


cube = RubiksCube(debug)
# Initial Screen presentation
draw_display()

# Loop until the screens top right 'x' is clicked.
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Good Bye')
            sys.exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            (left_pressed, _, right_pressed) = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
            # Left button to move the current view
            if left_pressed:
                if y < START_Y and x > START_X and x < (START_X + CUBE_SIZE):
                    cube.move_up()
                elif y > (START_Y + CUBE_SIZE) and y < (START_Y * 2 + CUBE_SIZE) \
                        and x > START_X and x < (START_X + CUBE_SIZE):
                    cube.move_down()
                elif x < START_X and y > START_Y and y < (START_Y + CUBE_SIZE):
                    cube.move_left()
                elif x > (START_X + CUBE_SIZE) and y > START_Y and y < (START_Y + CUBE_SIZE):
                    cube.move_right()
                else:
                    break
                process_event = True
            # If right button, start gathering the positions
            elif right_pressed:
                RIGHT_BTN_DOWN = True
                x, y = pygame.mouse.get_pos()
                positions.append((x,y))
                capture_count += 1
        # Collect x, y positions on MOUSEMOTION while right button held down
        if event.type == pygame.MOUSEMOTION and RIGHT_BTN_DOWN and capture_count < CAPTURE_SIZE:
            x, y = pygame.mouse.get_pos()
            positions.append((x,y))
            capture_count += 1
        # Mouse released... see if we have valid request to shift a row or column
        if event.type == pygame.MOUSEBUTTONUP:
            if RIGHT_BTN_DOWN:
                if debug:
                    print('Capture count:', capture_count)
                move_made = False
                if capture_count == CAPTURE_SIZE:
                    move_made = check_motions()
                # In any case, clear all the positions / captures
                positions.clear()
                capture_count = 0
                RIGHT_BTN_DOWN = False
                if move_made:
                    process_event = True

    if process_event:
        draw_display()
        process_event = False


