import sys

#TODO Document Code

class BrainfuckInterpreter:

    def __init__(self):
        self.memory = [0]
        self.pointer = 0
        self.input_buffer = ''

    def _get_current_value(self):
        return self.memory[self.pointer]

    def _set_current_value(self, value):
        self.memory[self.pointer] = value

    def _increment_pointer(self):
        self.pointer += 1
        if len(self.memory) <= self.pointer:
            self.memory.append(0)

    def _decrement_pointer(self):
        self.pointer -= 1
        if self.pointer < 0:
            raise Exception('Referencing Negative Memory Address')

    def _increment_value(self):
        self._set_current_value((self._get_current_value() + 1) % 256)

    def _decrement_value(self):
        self._set_current_value((self._get_current_value() - 1) % 256)

    def _output(self):
        print(str(chr(self._get_current_value())), end = '')

    def _input(self):
        try:
            if len(self.input_buffer) == 0:
                self.input_buffer = input('?') + '\n'
            self._set_current_value(ord(self.input_buffer[0]))
            self.input_buffer = self.input_buffer[1:]
        except EOFError:
            pass

    def _currently_zero(self):
        return self._get_current_value() == 0

    def interpret(self, code):

        bracket_stack = []

        current_position = 0
        while current_position < len(code):

            character = code[current_position]

            if character == '>':
                self._increment_pointer()
            elif character == '<':
                self._decrement_pointer()
            elif character == '+':
                self._increment_value()
            elif character == '-':
                self._decrement_value()
            elif character == '.':
                self._output()
            elif character == ',':
                self._input()
            elif character == '[':
                if self._currently_zero():
                    bracket_delta = 1
                    while bracket_delta != 0:
                        current_position += 1
                        if code[current_position] == '[':
                            bracket_delta += 1
                        elif code[current_position] == ']':
                            bracket_delta -= 1
                else:
                    bracket_stack.append(current_position)
            elif character == ']':
                if self._currently_zero():
                    bracket_stack.pop()
                else:
                    current_position = bracket_stack[-1]
            current_position += 1


def run_file(file_name):
    with open(file_name, 'r') as file:
        interpreter = BrainfuckInterpreter()
        code = file.read()
        interpreter.interpret(code)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            run_file(file_name)
    else:
        while True:
            run_file(input('Run File: '))
            print('Done')
