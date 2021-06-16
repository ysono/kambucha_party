EMPTY = ' '
PLAYERS = ['X','O']
DIM = 3
BOARD = [ [EMPTY] * DIM for _ in range(DIM) ]
REM = DIM ** 2

def isValidMove(i, j):
    return (
        0 <= i < DIM and
        0 <= j < DIM and
        BOARD[i][j] == EMPTY
    )

def isWin(i, j, playerId):
    return (
        all(BOARD[I][j] == playerId for I in range(DIM)) or
        all(BOARD[i][J] == playerId for J in range(DIM)) or
        (i == j and all(BOARD[I][I] == playerId for I in range(DIM))) or
        (i + j == DIM - 1 and all(BOARD[I][DIM - 1 - I] == playerId for I in range(DIM)))
    )

def move(i, j, playerId):
    '''
    Return
        True if move was valid.
        None if move was invalid.
        playerId if this player won.
    '''
    if isValidMove(i, j):
        global REM
        BOARD[i][j] = playerId
        REM -= 1
        if isWin(i, j, playerId):
            return playerId
        return True

def printBoard():
    print('---')
    for row in BOARD:
        print(row)

def play_cli():
    def parseInput(ln):
        ln = ln.split(',')
        if len(ln) == 2:
            i,j = ln
            try:
                return ( int(i), int(j) )
            except: pass

    playerIdx = 0

    while True:
        ln = input('Enter i, j : ')
        if ln.lower() == 'quit':
            return
        ln = parseInput(ln)
        res = False
        if ln is not None:
            i,j = ln
            res = move(i, j, PLAYERS[playerIdx])
            if res:
                printBoard()
                if res in PLAYERS:
                    print(f'{res} won!')
                    return
                if REM == 0:
                    print('Tie!')
                    return

            playerIdx ^= 1
        if not res:
            print('Bad input. Try again')

if __name__ == '__main__':
    play_cli()
