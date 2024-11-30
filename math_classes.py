import random

class Operation:
    '''
    Base class for math questions
    '''
    def __init__(self, max_left, max_right, symbol, min_left = 0, min_right = 0):
        '''
        Initialise properties needed for question
        '''
        self.left_operand = random.randint(min_left, max_left)
        self.right_operand = random.randint(min_right, max_right)
        self.symbol = symbol
        self.key_answer = self.operate()
    
    def get_answer(self):
        '''
        Getter function for key answer
        '''
        return self.key_answer

    def check_answer(self, answer):
        '''
        Returns
        1 if correct
        2 if wrong
        3 if not integer
        '''
        for w in answer.split():
            try:
                ans = int(w)
                if ans == self.key_answer:
                    return 1
                else:
                    return 2
            except ValueError:
                continue
        return 3
    
    def __str__(self):
        '''
        String representation for later printing
        '''
        return f"{self.left_operand} {self.symbol} {self.right_operand} = ?"

    # Purely virtual function
    def operate(self):
        return 0

class Addition(Operation):
    def __init__(self):
        super().__init__(99, 99, '+')
    
    def operate(self):
        return self.left_operand + self.right_operand

class Substraction(Operation):
    def __init__(self):
        super().__init__(99, 99, '-')
    
    def operate(self):
        return self.left_operand - self.right_operand

class Multiplication(Operation):
    def __init__(self):
        super().__init__(99, 99, '*')
    
    def operate(self):
        return self.left_operand * self.right_operand

class Division(Operation):
    '''
    Specific for integer division
    '''
    def __init__(self):
        super().__init__(99, 99, 'integer division', 1, 1)
    
    def operate(self):
        return self.left_operand // self.right_operand

class BitShiftRight(Operation):
    def __init__(self):
        super().__init__(99, 3, '>>')
    
    def operate(self):
        return self.left_operand >> self.right_operand

class BitShiftLeft(Operation):
    def __init__(self):
        super().__init__(99, 3, '<<')
    
    def operate(self):
        return self.left_operand << self.right_operand

class BitwiseXOR(Operation):
    def __init__(self):
        super().__init__(99, 99, '^')
    
    def operate(self):
        return self.left_operand ^ self.right_operand

class BitwiseComplement(Operation):
    def __init__(self):
        super().__init__(99, 0, '~')
    
    def operate(self):
        return ~self.left_operand

    # Overrides string representation because bitwise complement only uses 1 operand
    def __str__(self):
        return f"~{self.left_operand} = ?"

class BitwiseAND(Operation):
    def __init__(self):
        super().__init__(99, 99, '&')
    
    def operate(self):
        return self.left_operand & self.right_operand

class BitwiseOR(Operation):
    def __init__(self):
        super().__init__(99, 99, '|')
    
    def operate(self):
        return self.left_operand | self.right_operand

def get_random_operation():
    '''
    Returns a random math question
    '''
    match random.randint(0, 9):
        case 0:
            ret = Addition()
        case 1:
            ret = Substraction()
        case 2:
            ret = Multiplication()
        case 3:
            ret = Division()
        case 4:
            ret = BitShiftLeft()
        case 5:
            ret = BitShiftRight()
        case 6:
            ret = BitwiseXOR()
        case 7:
            ret = BitwiseComplement()
        case 8:
            ret = BitwiseAND()
        case 9:
            ret = BitwiseOR()
    return ret

