import os
import sys
import pygame
from pygame.locals import *
import objects
from colors import *
import letters, scramble
from wordlist import Wordlist

# set the window's position onscreen
x = 450
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = '%d, %d' % (x, y)

pygame.init()
clock = pygame.time.Clock()
FPS = 40
times_large = pygame.font.SysFont("Times New Roman", 72)
times_small = pygame.font.SysFont("Times New Roman", 18, bold=True)
times_tile = pygame.font.SysFont("Times New Roman", 16)

# draw constants
# a lot of the constants are related to one another to create
# proportionality
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 600
FIELD_WIDTH = SCREEN_WIDTH * 5 / 8
NUM_COLUMNS = 15
CELL_HEIGHT = CELL_WIDTH = FIELD_WIDTH / NUM_COLUMNS
NUM_ROWS = SCREEN_HEIGHT / CELL_HEIGHT

DISPLAYSURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Words With Yourself")

def terminate():
    pygame.quit()
    sys.exit()

def draw_screen(surface, field):
    '''
    Draws the given field and its current state to the display surface.
    '''
    
    for i in range(field.num_rows):
        for j in range(field.num_columns):
            if field.cells[i][j]:
                tile_rect = pygame.Rect(j * CELL_WIDTH, i * CELL_HEIGHT, \
                                         CELL_WIDTH, CELL_HEIGHT)
                draw_outlined_rect(surface, RED, tile_rect)
                if field.cells[i][j].letter:
                    letter = field.cells[i][j].letter
                    text = times_tile.render(letter, True, WHITE)
                    text_rect = text.get_rect()
                    text_rect.centery = i * CELL_HEIGHT + 10
                    text_rect.centerx = j * CELL_WIDTH + 10
                    DISPLAYSURFACE.blit(text, text_rect)
                else:
                    letter = None
                
    # field boundaries
    pygame.draw.line(surface, BLACK, (FIELD_WIDTH, 0), \
        (FIELD_WIDTH, SCREEN_HEIGHT))
    pygame.draw.line(surface, BLACK, (FIELD_WIDTH, (SCREEN_HEIGHT / 4) * 3), \
        (SCREEN_WIDTH, (SCREEN_HEIGHT / 4) * 3))
    F1HEIGHT = CELL_HEIGHT * field.floor_one
    pygame.draw.line(surface, BLACK, (0, F1HEIGHT), (FIELD_WIDTH, F1HEIGHT))
            
def draw_outlined_rect(surface, color, rect):
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BLACK, rect, 1)
       
def strip_row(field, row, column_index):
    '''
    For a given column index, return a list that consists of all items that
    are connected and can, thus, be considered in word checking.
    ex. ['A', 'C', 'F', None, 'G', 'R', None, 'Q']
    Running strip_row on the above list with an index of 4 will return
    ['G', 'R'] which would obviously be too small for word checking.
    Running it with an index of 0 would return ['A', 'C', 'F'] which can be
    used.
    '''
    if row[column_index] is None:
        return None
        
    temp_row = row[::]
    for i in range(column_index):
        if row[i] is None:
            temp_row = row[i+1:]
            
    temp_row2 = temp_row[::]
    for j in range(len(temp_row)):
        if temp_row[j] is None:
            temp_row2 = temp_row[:j]
            break
            
    return temp_row2
    
def get_stripped_rows(field, row_index, column_index):
    output = []
    
    for i in range(row_index, len(field.cells)):
        row = field.cells[i]
        if not row[column_index]:
            break
        output.append(strip_row(field, row, column_index))
        
    return output
    
def get_column(field, row_index, column_index):
    output = []
    
    current_row = row_index
    while field.cells[current_row][column_index] is not None \
        and current_row < len(field.cells):
            output.append(field.cells[current_row][column_index])
            current_row += 1
        
    return output
    
       
def tick(field, wordlist):
    if field.active_tile_has_landed():
        if field.active_tile.wildcard:
            print "Active tile's letter before: " + str(field.active_tile.letter)
            field.active_tile.wildcard = False
            field.active_tile.letter = random.choice(field.letters)
            print "Active tile's letter after: " + str(field.active_tile.letter)
        else:
            print "What?"
        at_col = field.active_tile.location[1]
        field.drop_column(at_col)
        at_row = field.active_tile.location[0]
        field.deactivate_active_tile()
        rows_to_check = get_stripped_rows(field, at_row, at_col)
        rows_to_check.append(get_column(field, at_row, at_col))
        print "Rows to check: ",
        print rows_to_check
        valid_words = []
        for row in rows_to_check:
            print "Row to check: ",
            print row
            word = wordlist.word_check(row)
            if word:
                valid_words.append(wordlist.word_check(row))
        if any(valid_words):
            print "Valid words: ",
            print valid_words
        else:
            print "No valid words found this round."
    
    if not field.active_tile:
        field.get_tile_from_queue()
        if not field.place_tile(field.active_tile, (0,4)):
            return False
    else:
        field.move_tile(field.active_tile, [1,0])
    
    return True
     

    
    
def intro():
    options = {'Play':play, 'Quit':terminate}
    option_list = sorted(options.keys())
    curr_opt_index = 0
    option_text = []
    i = 0
    for key in option_list:
        text = times_large.render(key, True, BLACK)
        rect = text.get_rect()
        rect.centerx = SCREEN_WIDTH / 2
        rect.centery = (3 * SCREEN_HEIGHT / 8) + (72 * i)
        option_text.append({'key':key, 'text':text, 'rect':rect})
        i += 1
    
    selected = option_text[0]
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_UP:
                    curr_opt_index = (curr_opt_index - 1) % len(option_list)
                    selected = option_text[curr_opt_index]
                if event.key == K_DOWN:
                    curr_opt_index = (curr_opt_index + 1) % len(option_list)
                    selected = option_text[curr_opt_index]
                if event.key == K_RETURN:
                    options[selected['key']]()
                    
        DISPLAYSURFACE.fill(LIGHT_GREY)
        for entry in option_text:
            if entry['text'] == selected['text']:
                pygame.draw.circle(DISPLAYSURFACE, BLACK, (entry['rect'].left - 25, entry['rect'].centery), 15)
            DISPLAYSURFACE.blit(entry['text'], entry['rect'])
        
        pygame.display.update()

def play():
    wordlist = Wordlist()
    
    # load font and messages
    pause_msg = "PAUSED"
    scrambler = scramble.Scrambler(pause_msg)
    pause_text = times_large.render(pause_msg, True, BLACK)
    pause_text_rect = pause_text.get_rect()
    pause_text_rect.centerx = SCREEN_WIDTH / 2
    pause_text_rect.centery = SCREEN_HEIGHT / 2
    game_over_text = times_large.render("Game Over", True, BLACK)
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = pause_text_rect.center
    
    # game-specific objects
    directions = {K_LEFT:[0,-1], K_RIGHT:[0,1]}
    field = objects.Field('english', NUM_ROWS, NUM_COLUMNS)
    field.place_tile(field.active_tile, (0,4))
    time_counter = 0
    tick_delay = 900
    pause = False
    game_over = False
    
    while True:
        if not (pause or game_over):
            time_counter += FPS
        if time_counter >= tick_delay:
            if not tick(field, wordlist):
                game_over = True
            time_counter = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_p:
                    if not game_over:
                        pause = not pause
                        if pause:
                            scrambled_msg = scrambler.get_scrambled_word()
                            pause_text = times_large.render(scrambled_msg, True, BLACK)
                if not (pause or game_over):
                    if event.key in directions:
                        field.move_tile(field.active_tile, directions[event.key])
                    if event.key == K_DOWN:
                        time_counter = tick_delay
                    if event.key == K_SPACE:
                        field.drop_active_tile()
                    if event.key == K_x:
                        field.change_wildcard_letter(forward=True)
                    if event.key == K_z:
                        field.change_wildcard_letter(forward=False)
                    if event.key == K_s:
                        field.stage_tile()
                    
        DISPLAYSURFACE.fill(LIGHT_GREY)
        if pause:
            DISPLAYSURFACE.blit(pause_text, pause_text_rect)
        else:
            draw_screen(DISPLAYSURFACE, field)
            if game_over:
                DISPLAYSURFACE.blit(game_over_text, game_over_text_rect)
                
        pygame.display.update()
        clock.tick(FPS)
        
if __name__ == '__main__':
    intro()
