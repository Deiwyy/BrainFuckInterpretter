import sys

class Interpretter(object):
    def __init__(self, code) -> object:
        self.functions = {
            '<>': self.move,
            '+-': self.cellShift,
            '[]': self.loop,
            '.,': self.io,
            '/1234567890\\': self.jump
        }
        self.code = self.stripCode(code)
        self.loops = []
        self.cells = [0 for _ in range(30_000)]
        self.cCell = 0
        self.currentCodeInd = 0

        self.currentJump = ''
        self.startJump = False
    
    def stripCode(self, code) -> str:
        strippedCode = ''
        for c in code:
            for fc in self.functions.keys():
                if c in fc: strippedCode += c
        return strippedCode

    def jump(self, c):
        if c == '/':
            self.startJump = True
        if c in '1234567890' and self.startJump:
            self.currentJump += c
        if c == '\\':
            self.startJump = False
            self.cCell = int(self.currentJump)
            self.currentJump = ''

    def move(self, c):
        if c == '<':
            self.cCell -= 1
            if self.cCell < 0:
                self.cCell = len(self.cells) - 1
        if c == '>':
            self.cCell += 1
            if self.cCell > len(self.cells) - 1:
                self.cCell = 0

    def cellShift(self, c):
        if c == '+':
            self.cells[self.cCell] += 1
        if c == '-':
            self.cells[self.cCell] -= 1

    def io(self, c):
        if c == ',':
            self.cells[self.cCell] = ord(input('single character: ')[0])
        if c == '.':
            print(chr(self.cells[self.cCell]), end='')


    def loop(self, c):
        if c == '[':
            self.loops.append(self.currentCodeInd)
        if c == ']':
            if self.cells[self.cCell] != 0:
                self.currentCodeInd = self.loops[-1]
            else:
                self.loops.pop(len(self.loops)-1)


    def run(self):
        while self.currentCodeInd != len(self.code):
            c = self.code[self.currentCodeInd]
            for f in self.functions.keys():
                if c in f:
                    #print(f'index: {self.currentCodeInd}  |  c: {c}  |  val: {self.cells[self.cCell]}  |  cell: {self.cCell}')
                    try:
                        self.functions[f](c)
                    except Exception as e:
                        print(f'Python Exception {e}\nAt index: {self.currentCodeInd} \nOP: {c}\ncell: {self.cCell}\n')
            self.currentCodeInd += 1
            

def run() -> None:
    interpretter = None
    if len(sys.argv) < 2:
        print('usage: BF.py [path-to-bf-file]')
        exit(1)
    with open(sys.argv[1]) as bfFile:
        bfCode = bfFile.read()
        interpretter = Interpretter(bfCode)
    interpretter.run()


if __name__ == '__main__':
    run()