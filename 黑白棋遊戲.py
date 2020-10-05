# Reversegam: a clone of Othello/Reversi
import random
import sys
WIDTH = 8  # Board is 8 spaces wide
HEIGHT = 8 # Board is 8 spaces tall
#player1 = ''
#player2 = ''

def drawBoard(board):
    # This function prints the board that it was passed. Returns None.
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print('%s|' % (y+1), end='')
        for x in range(WIDTH):
            print(board[x][y], end='')
        print('|%s' % (y+1))
    print(' +--------+')
    print('  12345678')

def getNewBoard():
    # Creates a brand-new, blank board data structure.
    board = []
    for i in range(WIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board

def isValidMove(board, tile, xstart, ystart):
    # Returns False if the player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False
    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection # First step in the x direction
        y += ydirection # First step in the y direction
        while isOnBoard(x, y) and board[x][y] == otherTile:
            # Keep moving in this x & y direction.
            x += xdirection
            y += ydirection
            if isOnBoard(x, y) and board[x][y] == tile:
                # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])
    if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
        return False
    return tilesToFlip

def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= WIDTH - 1 and y >= 0 and y <= HEIGHT - 1

def getBoardWithValidMoves(board, tile):
    # Returns a new board with periods marking the valid moves the player can make.
    boardCopy = getBoardCopy(board)
    for x, y in getValidMoves(boardCopy, tile):
        boardCopy[x][y] = '.'
    return boardCopy

def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    validMoves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves

def getScoreOfBoard(board):
    # Determine the score by counting the tiles. Returns a dictionary with keys 'X' and 'O'.
    xscore = 0
    oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            if board[x][y] == 'O':
                oscore += 1
    return {'X':xscore, 'O':oscore}

def whoGoesFirst():
    # Randomly choose who goes first.
    if random.randint(0, 1) == 0:
        return play1icon
    else:
        return play2icon

def makeMove(board, tile, xstart, ystart):
    # Place the tile on the board at xstart, ystart, and flip any of the opponent's pieces.
    # Returns False if this is an invalid move; True if it is valid.
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True

def getBoardCopy(board):
    # Make a duplicate of the board list and return it.
    boardCopy = getNewBoard()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            boardCopy[x][y] = board[x][y]
    return boardCopy

def isOnCorner(x, y):
    # Returns True if the position is in one of the four corners.
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)

def getPlayerMove(board, playerTile,name):
    # Let the player enter their move.
    # Returns the move as [x, y] (or returns the strings 'hints' or 'quit').
    DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('現在輪到 '+name+' 下棋。 請輸入要下棋的位置，若放棄比賽輸入"quit"，若須提示輸入"hints"。')
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move
        if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if isValidMove(board, playerTile, x, y) == False:
                continue
            else:
                break
        else:
            print('下棋無效，請再次輸入要下棋的位置。格式為column(1-8)和row(1-8)。')
            print('EX: 輸入 81 為在右上角的位置下棋。')
    return [x, y]

def getComputerMove(board, computerTile):
    # Given a board and the computer's tile, determine where to
    # move and return that move as a [x, y] list.
    possibleMoves = getValidMoves(board, computerTile)
    random.shuffle(possibleMoves) # randomize the order of the moves
    # Always go for a corner if available.
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]
    # Find the highest-scoring move possible.
    bestScore = -1
    for x, y in possibleMoves:
        boardCopy = getBoardCopy(board)
        makeMove(boardCopy, computerTile, x, y)
        score = getScoreOfBoard(boardCopy)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove

def printScore(board, playerTile, computerTile):
    scores = getScoreOfBoard(board)
    print(str(player1)+'('+str(play1icon)+'): 目前得到 '+str(scores[computerTile])+' 分。 '+str(player2)+'('+str(play2icon)+'): 目前得到 '+str(scores[playerTile])+' 分。')

def playGame(playerTile, computerTile):
    showHints = False
    turn = whoGoesFirst()
    print('由 ' + turn + ' 先行下棋。')
    # Clear the board and place starting pieces.
    board = getNewBoard()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'
    while True:
        playerValidMoves = getValidMoves(board, playerTile)
        computerValidMoves = getValidMoves(board, computerTile)
        if playerValidMoves == [] and computerValidMoves == []:
            return board # No one can move, so end the game.
        elif turn == play1icon: # Player's turn
            if playerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, playerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                #printScore(board, playerTile, computerTile)
                printScore(board,computerTile,playerTile)
                move = getPlayerMove(board, playerTile,player1)
                if move == 'quit':
                    print('感謝您參與遊戲!')
                    sys.exit() # Terminate the program.
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, playerTile, move[0], move[1])
            turn = play2icon
        elif turn == play2icon: # Player's turn
            if computerValidMoves != []:
                if showHints:
                    validMovesBoard = getBoardWithValidMoves(board, computerTile)
                    drawBoard(validMovesBoard)
                else:
                    drawBoard(board)
                printScore(board,computerTile,playerTile)
                move = getPlayerMove(board, computerTile,player2)
                if move == 'quit':
                    print('感謝您參與遊戲!')
                    sys.exit() # Terminate the program.
                elif move == 'hints':
                    showHints = not showHints
                    continue
                else:
                    makeMove(board, computerTile, move[0], move[1])
            turn = play1icon

print('歡迎您來體驗黑白棋遊戲!')
player1 = input('請輸入玩家1的姓名: ')
player2 = input('請輸入玩家2的姓名: ')
play1icon = ''
play2icon = ''
select = ''
while not (select == player1 or select == player2):
    print('哪位玩家是"O"的旗子呢?(輸入姓名)')
    select = input()
if(select == player1):
    play1icon = 'O'
    play2icon = 'X'
elif(select == player2):
    play1icon = 'X'
    play2icon = 'O' 
while True:
    finalBoard = playGame(play1icon, play2icon)
    # Display the final score.
    drawBoard(finalBoard)
    scores = getScoreOfBoard(finalBoard)
    print('"X"旗子的分數是 %s 分；"O"旗子的分數是 %s 分。' % (scores['X'], scores['O']))
    if scores[play1icon] > scores[play2icon]:
        print('恭喜!'+player1+'獲勝!!! 以差距 %s 分的分差打敗'+player2+'。' % (scores[play1icon] - scores[play2icon]))
    elif scores[play1icon] < scores[play2icon]:
        print('恭喜!'+player2+'獲勝!!! 以差距 %s 分的分差打敗'+player1+'。' % (scores[play2icon] - scores[play1icon]))
    else:
        print('哇~此場遊戲平局!')
    print('還想再玩一次嗎?(輸入"yes" or "no")')
    if not input().lower().startswith('y'):
        break