import random
from letters import Alphabet

class Field(object):
    '''
    The Field is the data structure that will hold all tiles
    currently on-screen, as well as the tile currently falling.
    It is a list of lists, where for any <self.cells[i][j]>, i represents
    the row and j represents the column.
    '''

    def __init__(self, language, num_rows, num_columns):
        self.language = language
        self.letters = Alphabet(language).letters + [None]
        self.num_rows = num_rows
        self.floor_one = (num_rows / 2) - 1
        self.floor_two = num_rows
        self.num_columns = num_columns
        self.cells = []
        self.active_tile = None
        self.tile_queue = []
        self.queue_limit = 5

        for i in range(num_rows):
            self.cells.append([])
            for j in range(num_columns):
                self.cells[i].append(None)
                
        self.load_queue()
        self.get_tile_from_queue()
                
    def __getitem__(self, key):
        return self.cells[key]
        
    def __str__(self):
        output = '\n'.join([str([cell for cell in row]) for row in self.cells])
        
        return "Field state:\n" + output
        
    def __repr__(self):
        tokens = (self.language, self.num_rows, self.num_columns)
        output = "Field, language: %s, dimensions: (%d,%d)" % tokens
            
        return output
        
    def active_tile_has_landed(self):
        tile = self.active_tile
        
        row, column = tile.location
        row_beneath = row + 1
        return (row_beneath >= self.floor_one) or \
                self[row_beneath][column] != None
                
    def add_tile_to_queue(self, tile):
        self.tile_queue.append(tile)
    
    def create_random_tile(self):
        # TODO: Create weighted random letter algorithm that takes into account
        # letter frequency
        return Tile(self, random.choice(self.letters))
        
    def drop_active_tile(self):
        while not self.active_tile_has_landed():
            self.move_active_tile([1,0])
    
    def get_tile_from_queue(self):
        if self.tile_queue:
            self.active_tile = self.tile_queue.pop(0)
            self.add_tile_to_queue(self.create_random_tile())
        else:
            print "Queue is empty!"
            
    def load_queue(self):
        while len(self.tile_queue) < self.queue_limit:
            tile = self.create_random_tile()
            self.add_tile_to_queue(tile)
            
    def move_active_tile(self, direction):
        tile = self.active_tile
        delta_row, delta_column = direction
        
        for coordinate in tile.locations:
            row, column = coordinate
            new_row, new_column = (row + delta_row, column + delta_column)
            if new_column >= self.num_columns:
                return False
            if self.cells[new_row][new_column] and \
               not self.cells[new_row][new_column]['active']:
                return False
            
                
        for coordinate in tile.locations:
            row, column = coordinate
            self.cells[row][column] = None
        
        row, column = tile.locations[0]
        self.place_active_tile((row + delta_row, column + delta_column))
    
    def place_active_tile(self, location):
        pass
        # TODO

class Tile(object):
    '''
    A simple, one-square tile representing one of the 26 letters of the 
    English alphabet, or a blank wild-card square.
    
    Although for right now I am working with English to get a prototype
    going, I plan on loading the alphabet into the game in a way that will
    allow for extensibility.
    '''
    def __init__(self, field, letter=None):
        self.location = None
        self.field = field
        if letter:
            self.letter = letter
        else:
            self.letter = 'wildcard'
        
    def __repr__(self):
        return "%s" % self.letter
        
    __str__ = __repr__
    
    def push_tile_below(self, field):
        row, column = self.location
        if (row + 1) >= self.field.num_rows:
            return False
        
        if self.field[row+1][column]:
            tile_below = self.field[row+1][column]
        
            if tile_below.push_tile_below(field):
                self.location = (row + 1, column)
                self.field[row+1][column] = self # adjust to Field method
                self.field[row][column] = None
                return True
            else:
                return False
                
        else:
            self.location = (row + 1, column)
            self.field[row+1][column] = self
            self.field[row][column] = None
            return True
            