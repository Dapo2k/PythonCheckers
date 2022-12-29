def underline(text):
    text = text + '\u0332'
    return text
def inBoard(row,col):
    return row >= 0 and row <= 7 and col >= 0 and col <= 7
placement = [
    [0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [-1,0,-1,0,-1,0,-1,0],
    [0,-1,0,-1,0,-1,0,-1],
    [-1,0,-1,0,-1,0,-1,0]
]
class board:
    def __init__(self, grid = placement):
        self.grid = grid
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] != 0:
                    self.grid[i][j] = checkersPiece(self,self.grid[i][j]) 
    def calcMoves(self):
        self.whiteCanMove = False
        self.blackCanMove = False
        self.whiteCanCap = False
        self.blackCanCap = False
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] != 0:
                    if (self.grid[i][j].side == -1 and i == 0) or (self.grid[i][j].side == 1 and i == 7):
                        self.grid[i][j].king = True
                    self.grid[i][j].checkMoves(i,j)
                    if len(self.grid[i][j].captures)>0:
                        print(str(i)+str(j))
                        if self.grid[i][j].side == 1:
                            self.whiteCanCap = True
                        else:
                            self.blackCanCap = True

                    if len(self.grid[i][j].moves)>0:
                        if self.grid[i][j].side == 1:
                            self.whiteCanMove = True
                        else:
                            self.blackCanMove = True     
    def show(self):
        letters = 'abcdefgh'
        for i in range(8):
            black = False
            if i%2 == 1:
                black = True
            display = str(8-i) + ' '
            for square in self.grid[i]:
                all = ''
                side = ''
                mid = ''
                if black:
                    side = ' '
                    mid = ' '
                    black = False
                else:
                    side = '|'
                    mid = '|'
                    black = True
                if square != 0:
                    mid = str(square)
                all = side+mid+side
                display += all
            print(display)
        bottomLine = '  '
        for i in range(8):
            let = ' ' + letters[i] + ' '
            bottomLine += let
        print(bottomLine)
class checkersPiece:
    def __init__(self, board, side):
        self.board = board
        if abs(side) == 2:
            self.king = True
            side = int(side/2)
        else:
            self.king = False
        self.side = side
        self.sqaure = 0
        self.moves = []
        self.captures = []
    def checkMoves(self,row,col):
        self.moves = []
        self.captures = []

        for i in range(2):
            num = (-1)**(i+1)
            if inBoard(row+self.side,col+num) and self.board.grid[row+self.side][col+num] == 0:
                move = str(row+self.side)+str(col+num)
                self.moves.append(move)
            else:
                if inBoard(row+self.side,col+num) and inBoard(row+2*self.side,col+2*num) and self.board.grid[row+2*self.side][col+2*num] == 0 and self.board.grid[row+self.side][col+num]!=0 and self.board.grid[row+self.side][col+num].side != self.side:
                    move = str(row+2*self.side)+str(col+2*num)
                    self.captures.append(move)
        if self.king == True:
            for i in range(2):
                num = (-1)**(i+1)
                if inBoard(row-self.side,col+num) and self.board.grid[row-self.side][col+num] == 0:
                    move = str(row-self.side)+str(col+num)
                    self.moves.append(move)
                else:
                    if inBoard(row-self.side,col+num) and inBoard(row-2*self.side,col+2*num) and self.board.grid[row-2*self.side][col+2*num] == 0 and self.board.grid[row-self.side][col+num]!=0 and self.board.grid[row-self.side][col+num].side != self.side:
                        move = str(row-2*self.side)+str(col+2*num)
                        self.captures.append(move)

    def __str__(self) -> str:
        stringPiece = ''
        if self.side == 1:
            stringPiece = '0'
        else:
            stringPiece = 'O'
        if self.king:
            stringPiece = underline(stringPiece)
        return stringPiece

