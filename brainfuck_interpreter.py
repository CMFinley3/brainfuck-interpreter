import sys

#TODO Document Code

class BrainfuckInterpreter:
    def __init__(self):        
        """
        This class represents a Brainfuck Iterpreter
        """
        self._memory = [0]
        self._pointer = 0
        self._input_buffer = ''
        self._bracket_stack = []
        self._operations = {
            '>' : self._increment_pointer,
            '<' : self._decrement_pointer,
            '+' : self._increment_value,
            '-' : self._decrement_value,
            '.' : self._output,
            ',' : self._input,
        }

    def _get_current_value(self):
        """        
        Returns:
            byte -- value at current memory address
        """
        return self._memory[self._pointer]

    def _set_current_value(self, value):
        """        
        Arguments:
            value {byte} -- sets the current memory address to the given value
        """
        self._memory[self._pointer] = ((value + 2560) % 256)

    def _currently_zero(self):
        """        
        Returns:
            bool -- is the current memory address 0
        """
        return self._get_current_value() == 0

    def _increment_pointer(self):
        """
        Increments the pointer to the next memory address
        """
        self._pointer += 1
        if len(self._memory) <= self._pointer:
            self._memory.append(0)

    def _decrement_pointer(self):
        """ 
        Decrements the pointer to the previous memory address

        Raises:
            IndexError: You can't decrement the pointer past 0
        """
        self._pointer -= 1
        if self._pointer < 0:
            raise IndexError ('Referencing Negative Memory Address')

    def _increment_value(self):
        """
        Increments the value at the current memory address by 1
        """
        self._set_current_value((self._get_current_value() + 1))

    def _decrement_value(self):
        """
        Decrements the value at the current memory address by 1
        """
        self._set_current_value((self._get_current_value() - 1))

    def _output(self):
        """
        Outputs the current memory address as its ASCII value
        """
        print(str(chr(self._get_current_value())), end = '')

    def _input(self):
        """
        Takes input from the user and buffers it. When programs ask for it,
        they get the ASCII values of the input. EOFs leave the memory unaffected.
        """
        try:
            if len(self._input_buffer) == 0:
                self._input_buffer = input('?') + '\n'
            self._set_current_value(ord(self._input_buffer[0]))
            self._input_buffer = self._input_buffer[1:]
        except EOFError:
            pass
    
    def interpret(self, code):
        """
        Interprets the string of code passed in

        Arguments:
            code {str} -- Code to interpret
        """

        # Used a while loop here because brackets can move around your position in code
        current_position = 0
        while current_position < len(code):

            # Character for current operation
            character = code[current_position]

            # If not a loop operation, execute
            if character in self._operations:
                self._operations[character]()
            elif character == '[':
                if self._currently_zero():
                    # Ignore all code until you have as many closed brackets as you do open                    
                    bracket_delta = 1
                    while bracket_delta != 0:
                        current_position += 1
                        if code[current_position] == '[':
                            bracket_delta += 1
                        elif code[current_position] == ']':
                            bracket_delta -= 1
                else:
                    # Save a bracket position to the stack and continue
                    self._bracket_stack.append(current_position)
            elif character == ']':
                if self._currently_zero():
                    # Remove a bracket position from the stack and continue
                    self._bracket_stack.pop()
                else:
                    # Go back to the position of the last bracket
                    current_position = self._bracket_stack[-1]
            
            #Move forward to next operation
            current_position += 1


def run_file(file_name):
    """
    Runs the file specified
    
    Arguments:
        file_name {str} -- name for file to run
    """
    with open(file_name, 'r') as file:
        interpreter = BrainfuckInterpreter()
        code = file.read()
        interpreter.interpret(code)


if __name__ == '__main__':
    # If passed in as an argument, run those files.
    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            run_file(file_name)
    while True:
        run_file(input('Run File: '))
        print('Done')
