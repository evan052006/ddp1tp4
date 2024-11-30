import time
import random
from enum import Enum
from math_classes import *
from tictactoe import *

class ChatDdp:
    class States(Enum):
        # Basic enums to store states
        DEFAULT = 1
        WAITFORMATH = 2
        INITTICTACTOE = 3
        WAITFORTICTACTOEGAME = 4
    
    def __init__(self):
        # Initialise basic properties
        self.state = self.States.DEFAULT
        self.keywords_basic = {}
        self.responses_basic = {}
        self.keywords_special = {}
        self.quit_condition = ['exit', 'quit', 'end', 'finish', 'selesai']
        self.boolean_true = ['yes', 'iya', 'oke', 'y', 'ya']
        self.boolean_false = ['n', 'tidak', 'jangan', 'engga', 'g', 'ga', 'no', 'not']

        # Store strings of basic keywords and responses as dictionary from file
        with open("./basic-keywords.txt", "r") as keyword_file:
            for line in keyword_file:
                line = line.strip().split(',')
                self.responses_basic[line[0]] = line[-1]
                for keyword in line[:-1]:
                    self.keywords_basic[keyword] = line[0]
        
        # Store strings of special keywords as dictionary from file
        with open("./special-keywords.txt", "r") as keyword_file:
            for line in keyword_file:
                line = line.strip().split(',')
                for keyword in line:
                    self.keywords_special[keyword] = line[0]
        
        # Open the whole joke file and store each joke in a list
        with open("./jokes.txt", "r") as joke_file:
            self.jokes = [x.strip() for x in joke_file.readlines()]

    def get_answer(self, prompt):
        '''
        Gets answer and returns a response
        ''' 
        prompt = prompt.lower()
        # Restore to default state if user asks
        if self.state != self.States.DEFAULT and any(x in prompt for x in self.quit_condition):
            self.state = self.States.DEFAULT
            return "Oke mari kita kembali ke pembicaraan"
        # Runs following algo depending on current state
        match self.state:
            case self.States.DEFAULT:
                self.state_default(prompt)
            case self.States.WAITFORMATH:
                self.state_math_answer(prompt)
            case self.States.INITTICTACTOE:
                self.state_init_tictactoe(prompt)
            case self.States.WAITFORTICTACTOEGAME:
                self.state_tictactoe(prompt)
        # Return the response we got
        return self.response
    
    def state_default(self, prompt):
        '''
        Default state
        All states originate from here
        '''
        # Basic keywords which only outputs a single response
        for keyword, main_keyword in self.keywords_basic.items():
            if keyword in prompt:
                self.response = self.responses_basic[main_keyword]
                return
        # Special keywords which has special logic tied into
        for keyword, main_keyword in self.keywords_special.items():
            if keyword in prompt:
                match main_keyword:
                    case "buat lelucon":
                        self.response = random.choice(self.jokes) 
                    case "tanya jam":
                        current_time = time.localtime()
                        self.response = f"Saat ini pukul {current_time.tm_hour:02}:{current_time.tm_min:02}:{current_time.tm_sec:02}"
                    case "soal mat":
                        self.question = get_random_operation()
                        self.response = str(self.question)
                        self.state = self.States.WAITFORMATH
                    case "tictactoe":
                        self.init_stage = 0
                        self.init_data = []
                        self.state_init_tictactoe(None)
                        self.state = self.States.INITTICTACTOE
                return
        # If not in keywords, say we don't understand
        self.response = "Maaf, saya belum mengerti pertanyaan itu. Bisa coba yang lain!"

    def state_math_answer(self, prompt):
        '''
        State to check user's math answer
        '''
        match self.question.check_answer(prompt):
            case 1:
                self.response = f"Benar! Jawabanmu tepat.😊"
                self.state = self.States.DEFAULT
            case 2:
                self.response = f"Salah, jawaban yang benar adalah {self.question.get_answer()}"
                self.state = self.States.DEFAULT
            case 3:
                self.response = f"Masukkan angka yang valid sebagai jawaban."
               
    def state_init_tictactoe(self, prompt):
        '''
        State to initialise tictactoe board
        '''
        match self.init_stage:
            # Height
            case 0:
                self.response = "Oke, Seberapa tinggi kamu mau papannya?"
                self.init_stage += 1
            # Width
            case 1:
                height = self.find_first_integer(prompt.split())
                if height == None or height > TicTacToe.Bounds.MAXHEIGHT.value or height < TicTacToe.Bounds.MINHEIGHT.value:
                    self.response = f"Maaf saya tak bisa menemukan angka dalam rentang {TicTacToe.Bounds.MINHEIGHT.value} - {TicTacToe.Bounds.MAXHEIGHT.value}"
                else:
                    self.init_data.append(height)
                    self.response = f"Oke, Seberapa lebar kamu mau papannya?"
                    self.init_stage += 1
            # Win condition
            case 2:
                width = self.find_first_integer(prompt.split())
                if width == None or width > TicTacToe.Bounds.MAXWIDTH.value or width < TicTacToe.Bounds.MINWIDTH.value:
                    self.response = f"Maaf saya tak bisa menemukan angka dalam rentang {TicTacToe.Bounds.MINWIDTH.value} - {TicTacToe.Bounds.MAXWIDTH.value}"
                else:
                    self.init_data.append(width)
                    self.response = f"Oke, Berapa banyak simbol sejajar yang mau dibutuhkan untuk menang?"
                    self.init_stage += 1
            # Show grid or not
            case 3:
                wincon = self.find_first_integer(prompt.split())
                max_wincon = max(self.init_data[0], self.init_data[1])
                if wincon == None or wincon > max_wincon or wincon < TicTacToe.Bounds.MINWINCON.value:
                    self.response = f"Maaf saya tak bisa menemukan angka dalam rentang {TicTacToe.Bounds.MINWIDTH.value} - {max_wincon}"
                else:
                    self.init_data.append(wincon)
                    self.response = f"Oke, Apakah mau saya tampilkan gridnya?"
                    self.init_stage += 1
            # Start game based on parameters
            case 4:
                showgrid = self.find_first_boolean(prompt.split())
                if showgrid == None:
                    self.response = f"Maaf saya belum dapat memahami, mohon jawab dengan \'iya\' atau \'tidak\'"
                else:
                    self.response = f"Oke, silahkan pilih posisi dengan angka pertama posisi X dan angka kedua posisi Y"
                    self.game = TicTacToe(self.init_data[0], self.init_data[1], self.init_data[2], showgrid)
                    self.response += self.game.display_board()
                    self.state = self.States.WAITFORTICTACTOEGAME
    
    def state_tictactoe(self, prompt):
        '''
        State to play tic tac toe game loop
        '''

        # Validate inputs
        prompt = prompt.split()
        pos = self.find_first_two_integers(prompt)
        if pos == None:
            self.response = "Maaf saya tidak dapat baca inputnya, mohon pilih posisi dengan angka pertama posisi X dan angka kedua posisi Y "
            return
        pos = Coor(pos[0] - 1, pos[1] - 1)
        if not self.game.in_bounds(pos):
            self.response = "mohon pilih posisi dalam jangkauan"
            return
        if self.game.board[pos.y][pos.x] != " ":
            self.response = "mohon pilih posisi yang tidak terisi"
            return
        
        # Execute our turn
        self.game.mark_symbol(pos)

        if self.tictactoe_win_handling('Well done you win!'):
            return
        
        self.game.turn += 1

        if self.tictactoe_draw_handling():
            return
        
        # Execute bot turn
        ai_pos = self.game.ai_choose()
        self.game.mark_symbol(ai_pos)

        if self.tictactoe_win_handling(f'I choose {ai_pos + Coor(1, 1)}\nyou lose!'):
            return
        
        self.game.turn += 1

        if self.tictactoe_draw_handling():
            return

        # Display board again if no draws or wins happen
        self.response = f"I choose {ai_pos + Coor(1, 1)}{self.game.display_board()}" 

    def tictactoe_draw_handling(self):
        '''
        Tasks of what to do when draw happens
        '''
        if self.game.check_draw():
            self.response = self.game.display_board() + "\nIts a draw!"
            self.state = self.States.DEFAULT
            return True
        else:
            return False
    
    def tictactoe_win_handling(self, msg):
        '''
        Tasks of what to do when win happens
        '''
        if self.game.check_win(): 
            self.response = self.game.display_board()
            self.response += "\n" + msg
            self.state = self.States.DEFAULT
            return True
        else:
            return False

    def find_first_boolean(self, lst):
        '''
        Find first occurence of a 'boolean' like statement from list of strings
        '''
        for word in lst:
            if word in self.boolean_true:
                return True
            if word in self.boolean_false:
                return False
        return None
    
    def find_first_integer(self, lst):
        '''
        Find first occurance of an integer from list of strings
        '''
        for word in lst:
            try:
                ret = int(word)
                return ret
            except ValueError:
                continue
        return None

    def find_first_two_integers(self, lst):
        '''
        Find first and second occurence of integers from list of strings
        '''
        integers = []
        for word in lst:
            try:
                i = int(word)
                integers.append(i)
                if len(integers) == 2: return integers
            except ValueError:
                continue
        return None

    def greet(self):
        '''
        Greets the user :)
        '''
        return "Halo! Ada yang bisa saya bantu?"