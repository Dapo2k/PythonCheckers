from ast import excepthandler
from xml.etree.ElementTree import TreeBuilder
import CheckersPieces
from CheckersPieces import checkersPiece
from CheckersPieces import board

def convertIndex(text):
    realIndex = ''
    realIndex = realIndex + str((8-int(text[1])))
    letters = 'abcdefgh'
    num = ''
    for i in range(8):
        if letters[i] == text[0]:
            realIndex+=str(i)
    return realIndex
def turnCanCap(turn,board):
    return (turn == -1 and board.blackCanCap) or (turn == 1 and board.whiteCanCap)
def calcScores(board):
    scores = [0,0]
    for i in range(8):
        for j in range(8):
            if board.grid[i][j].king != 0:
                score = 1
                if board.grid[i][j].king == True: score = 2
                if board.grid[i][j].team == -1:
                    scores[0]+=score
                else:
                    scores[1]+=score
    return scores

customPlacement = [
    [0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [-1,0,-1,0,-1,0,-1,0],
    [0,-1,0,-1,0,-1,0,-1],
    [-1,0,-1,0,-1,0,-1,0]
]

#edit this table to edit initital placements of the board pieces, 1's and 2's are white pieces and king pieces, -1's and -2's are black pieces and king pieces, and 0's are blank space
customPlacement = [
    [0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [-1,0,-1,0,-1,0,-1,0],
    [0,-1,0,-1,0,-1,0,-1],
    [-1,0,-1,0,-1,0,-1,0]
]


print('\nWelcome to python checkers!\n')

lastIn = ''
while lastIn != 'p':
    print('''To play game, enter \'p\'
To see rules, enter \'r\'''')
    lastIn = input()
    if lastIn == 'r':
        print('''
        - Each team starts with 12 pieces, black (O) starts first
        - all moves are diagonal and non-king pieces may only move forward
        - a non capturing move is can only move one square
        - a capture can be done by leaping over an opponent piece into an empty square in the same direction
            -- if at least one capture can be made, it must be done
            -- multiple capture jumps can be made by the same piece if possible and is up to the plaryer
        - a king is crowned when a piece makes it to the last row on the opponent's side (row 8 for black, row 1 for white)
            -- kings are denoted by an underlined piece
            -- kings can move both forwards and backwards in the diagonal direction
            -- kings can capture pieces both forwards and backwards in a similar fashion to non-king pieces
        - game ends when one team cannot move anymore
        - game may also end if there are 20 consecutive moves in which only kings move, in which case the team with the higher score wins
            -- non-king pieces add 1 to the score, kings add 2 to the score
            -- if score is tied, game ends in a tie
        ''')

checkersBoard = board(customPlacement)
game = True
turn = -1
capPiece = 0
consKingMoves = 0
kingMove = False
while game:
    checkersBoard.calcMoves()
    print('\n')
    if turn == -1:
        print('O\'S TURN')
    else:
        print('0\'S TURN')
    checkersBoard.show()
    print('Consecutive king moves: ' + str(consKingMoves))
    nextMove = 0
    curTile = ''
    newTile = ''
    passTurn = False
    while nextMove == 0:
        if capPiece != 0:
            print('Continue capturing or type \'pass\' to end the turn: ')
        else:
            print('Enter a move in the format \'(tile of piece to move)(tile to move to)\' ex: a3b4: ')
        nextMove = input()
        inMoves = False
        inCaptures = False
        if nextMove == 'pass':
            break
        try:
            curTile = convertIndex(nextMove[0:2])
            newTile = convertIndex(nextMove[2:4])
            piece = checkersBoard.grid[int(curTile[0])][int(curTile[1])]
            if piece != 0 and piece.side == turn and (capPiece == 0 or capPiece == piece):
                inMoves = False
                inCaptures = False
                for move in piece.moves:
                    if newTile == move:
                       inMoves = True
                for move in piece.captures:
                    if newTile == move:
                       inCaptures = True     
                if not (inMoves and not turnCanCap(turn,checkersBoard)) and not inCaptures:
                    nextMove = 0
                    print("invalid move or capture availabe, try another move")
            else:
                nextMove = 0            
        except:
            nextMove = 0
            print('Not valid input')
    cap = False
    capPiece = 0
    if nextMove != 'pass':
        piece = checkersBoard.grid[int(curTile[0])][int(curTile[1])]
        if piece.king == True:
            kingMove = True
        if turnCanCap(turn,checkersBoard):
            capSpotRow = int((int(newTile[0])+int(curTile[0]))/2)
            capSpotCol = int((int(newTile[1])+int(curTile[1]))/2)
            checkersBoard.grid[int(newTile[0])][int(newTile[1])] = piece
            checkersBoard.grid[int(curTile[0])][int(curTile[1])] = 0
            checkersBoard.grid[capSpotRow][capSpotCol] = 0
            cap = True
            capPiece = piece
        else:
            checkersBoard.grid[int(newTile[0])][int(newTile[1])] = piece
            checkersBoard.grid[int(curTile[0])][int(curTile[1])] = 0
        checkersBoard.calcMoves()
    if capPiece == 0 or not (len(capPiece.captures)>0):
        capPiece = 0
        if kingMove:
            consKingMoves+=1
        else:
            consKingMoves = 0
        turn *= -1

    if (checkersBoard.whiteCanMove == False and checkersBoard.whiteCanCap == False) or (checkersBoard.blackCanMove == False and checkersBoard.blackCanCap == False) or consKingMoves == 20:
        game = False
checkersBoard.show()
if checkersBoard.whiteCanMove == False and checkersBoard.whiteCanCap == False:
    print('O WINS!')
elif checkersBoard.whiteCanMove == True and checkersBoard.whiteCanCap == True:
    print('0 WINS!')
else:
    if calcScores(checkersBoard)[0]>calcScores(checkersBoard)[1]:
        print('O WINS!')
    elif calcScores(checkersBoard)[0]<calcScores(checkersBoard)[1]:
        print('0 WINS!')
    else:
        print('tie')
