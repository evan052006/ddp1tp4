from enum import Enum
import random

class Coor:
    '''
    Helper class to store pairs of values that we can add or substract
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other_coor):
        return Coor(self.x + other_coor.x, self.y + other_coor.y)
    def __sub__(self, other_coor):
        return Coor(self.x - other_coor.x, self.y - other_coor.y)
    def __str__(self):
        return f"{self.x} {self.y}"

class TicTacToe:
    class Symbols(Enum):
        PLAYER = '@'
        BOT = '&'
    class Bounds(Enum):
        MAXHEIGHT = 100
        MINHEIGHT = 3
        MAXWIDTH = 100
        MINWIDTH = 3
        MINWINCON = 3

    def __init__(self, height = 10, width = 10, win_condition = 5, show_board = True):
        '''
        Initialise board properties based on parameters
        '''
        self.width = width
        self.height = height
        self.win_condition = win_condition
        self.show_board = show_board
        self.board = []
        for _ in range(self.height):
            self.board.append([" "] * self.width)
        self.players = [self.Symbols.PLAYER.value, self.Symbols.BOT.value]
        self.turn = 0
        self.last_pos = None
    
    def display_board(self):
        '''
        Returns a pretty string representation of current board
        '''
        if not self.show_board: return ""
        # store the index labels for columns
        ret = "\n"
        for i in range(self.width):
            ret += (f"{i+1:<2}" if i + 1 < 100 else '..') + "  "
        ret += '\n'

        for i in range(self.height):
            for j in range(self.width):
                # add our symbol / state of that tile
                ret += str(self.board[i][j]) 
                # add separators " | " as long as not at the end
                if j < self.width - 1: 
                    ret += " | "
            # add index labels for rows
            ret += "  " + str(i + 1)
            if i < self.height - 1:
                ret += '\n'
                # store border as long as not at the end
                ret += "- + " * (self.width - 1) + "-\n"
        return ret
    
    def check_draw(self):
        '''
        Checks if we reached max turns in other words, a draw
        '''
        return self.turn >= self.width * self.height

    def in_bounds(self, pos):
        '''
        Checks if a Coor is inside our board
        '''
        return pos.x >= 0 and pos.y >= 0 and pos.x < self.width and pos.y < self.height
    
    def get_empty_cells(self):
        '''
        Return a list of all Coor of empty cells
        '''
        ret = []
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == ' ':
                    ret.append(Coor(j, i))
        return ret
    
    def mark_symbol(self, pos):
        '''
        Mark a symbol at the board
        '''
        self.board[pos.y][pos.x] = self.players[self.turn % 2]
        self.last_pos = pos

    def ai_choose(self):
        '''
        Basic primitive tictactoe bot
        Blocks player wins and get it's own win
        Otherwise pick random empty cell
        '''
        empty_cells = self.get_empty_cells()
        for pos in empty_cells:
            self.board[pos.y][pos.x] = self.Symbols.BOT.value
            if self.check_win(pos = pos, symbol = self.Symbols.BOT.value, force_check = True):
                self.board[pos.y][pos.x] = " "
                return pos
            self.board[pos.y][pos.x] = " "
        
        for pos in empty_cells:
            self.board[pos.y][pos.x] = self.Symbols.PLAYER.value
            if self.check_win(pos = pos, symbol = self.Symbols.PLAYER.value, force_check = True):
                self.board[pos.y][pos.x] = " "
                return pos
            self.board[pos.y][pos.x] = " "

        return random.choice(empty_cells)
    
    def check_win(self, pos = None, symbol = None, force_check = False):
        '''
        Checks for a win, defaults to current symbol and last pos
        '''

        # Force check used for ai, otherwise dont check if not enough turns for a win yet
        if self.turn < 2*(self.win_condition - 1) and not force_check:
            return False

        # Set default parameters
        if symbol == None: symbol = self.players[self.turn % 2]
        if pos == None: pos = self.last_pos

        # Right, Down, Diagonal down, Diagonal Up stored as a list of Coors
        directions = [Coor(1, 0), Coor(0, 1), Coor(1, 1), Coor(1, -1)]

        # Check streaks of consecutive based on each direction
        for direct in directions:
            # initialise the counter and set the left and right iterators
            current_consecutive = 1
            right = pos + direct
            left = pos - direct
            while(True):
                # check if we can shift the iterator (only when its in bounds)
                valid_right = self.in_bounds(right) and self.board[right.y][right.x] == symbol
                valid_left = self.in_bounds(left) and self.board[left.y][left.x] == symbol
                if valid_right:
                    right = right + direct
                    current_consecutive += 1
                if valid_left:
                    left = left - direct
                    current_consecutive += 1
                if not valid_right and not valid_left: # escape if both iterators no longer active
                    break
            if self.win_condition <= current_consecutive: return True
        return False
