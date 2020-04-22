import random

# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!

DEBUG = 1
forward = None
board_size = 16
r = None
c = None
team = None
turnNum = 0
startPoint = 0
index = 0
idleCount = 0
opp_team = None
def dlog(str):
    if DEBUG > 0:
        log(str)


def check_space_wrapper(r, c):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return None
    try:
        return check_space(r, c)
    except RobotError:
        return None

def safeSpawn(r,c):
    if check_space_wrapper(r,c) == False and check_space_wrapper(r+forward,c+1) != opp_team and check_space_wrapper(r+forward,c-1) != opp_team:
        return True
    else:
        return False


def check_adjacent(r, c):
    if check_space_wrapper(r + 1, c) == team:
        return True
    elif check_space_wrapper(r - 1, c) == team:
        return True
    elif check_space_wrapper(r, c + 1) == team:
        return True
    elif check_space_wrapper(r, c - 1) == team:
        return True
    else:
        return False

def try_move_forward():
    if check_space_wrapper(r+forward,c)==False:
        move_forward()

def column(matrix, i):
    return [row[i] for row in matrix]

def findEmpty():
    board = get_board()
    cols = {}
    for i in range(board_size):
        cols[i]=column(board,i).count(team)
    ordered = []
    for key, value in sorted(cols.items(), key=lambda item: item[1]):
        ordered.append(key)
    return ordered

def findFullest():
    board = get_board()
    cols = {}
    for i in range(board_size):
        cols[i]=column(board,i).count(team)
    ordered = []
    for key, value in sorted(cols.items(), key=lambda item: item[1], reverse=True):
        ordered.append(key)
    return ordered

def biggerInList(list, num):
    for i in list:
        if i >= num:
            return True
    return False

def findAll(array,elem):
    allInstances = []
    for i in range(len(array)):
        for x in range(len(array[i])):
            if array[i][x] == elem:
                allInstances.append([i,x])
    return allInstances

def getRatio():
    board = get_board()
    cols = {}
    for i in range(board_size):
        cols[i]=column(board,i).count(opp_team) - column(board,i).count(team)
    ordered = []
    for key, value in sorted(cols.items(), key=lambda item: item[1],reverse=True):
        ordered.append(key)
    if biggerInList(ordered,3):
        for i in ordered:
            factor = [0, -1, 1]
            random.shuffle(factor)
            for x in factor:
                if check_space_wrapper(index,i+x) == False:
                    return i+x
    else:
        for i in findFullest():
            factor = [-1, 1]
            random.shuffle(factor)
            for x in factor:
                if check_space_wrapper(index, i + x) == False:
                    return i + x


def stuckBoi():
    allys = findAll(get_board(),team)
    stuckBois = []
    for boi in allys:
        if inDanger(boi[0],boi[1]) and not stuck(boi[0],boi[1]):
            stuckBois.append(boi[1])

    random.shuffle(stuckBois)
    shift = [-1,1]
    random.shuffle(shift)
    for i in stuckBois:
        for x in shift:
            if safeSpawn(index,i+x):
                return i+x
    boardIndex = []
    for i in range(board_size):
        boardIndex.append(i)
    random.shuffle(boardIndex)
    for i in boardIndex:
        if safeSpawn(index,i):
            return i




def findBestSpawn():
    bestSpawn = None
    boardIndex = []
    board = get_board()
    cols = {}
    ally = {}
    enemy = {}
    #Find closest enemy
    for i in range(board_size):
        for x in range(board_size):
            if board[abs(index-x)][i] == opp_team:
                cols[i] = abs(index-x)
                break
            if board[abs(index-x)][i] == team:
                break
    #Sorts by closest Enemy
    if len(cols)!=0:
        ordered = []
        for key, value in sorted(cols.items(), key=lambda item: item[1], reverse=False):
            ordered.append(key)
        for i in ordered:
            if opp_team in column(board,i) and not team in column(board,i) and safeSpawn(index,i):
                return i
    return stuckBoi()

    # for i in boardIndex:
    #     if check_space_wrapper(index,i) == False:
    #         return i


def stuck(r,c):
    if check_space_wrapper(r+forward,c) == opp_team:
        return True
    return False


def inDanger(r,c):
    if (check_space_wrapper(r + forward*2, c+1) != opp_team and check_space_wrapper(r + forward*2, c-1) != opp_team) or (check_space_wrapper(r, c+1) == team or check_space_wrapper(r, c-1) == team):
        return False
    else:
        return True


def areBro(r,c):
    if (check_space_wrapper(r + forward*2, c) == opp_team or check_space_wrapper(r + forward*2, c+2) == opp_team) and check_space_wrapper(r + forward, c+1) == team:
        return True
    elif (check_space_wrapper(r + forward*2, c) == opp_team or check_space_wrapper(r + forward*2, c-2) == opp_team) and check_space_wrapper(r + forward, c-1) == team:
        return True
    else:
        return False


def turn():
    global forward
    global r, c
    global board_size
    global team
    global turnNum
    global startPoint
    global index
    global idleCount
    global opp_team
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    dlog('Starting Turn: ')
    board_size = get_board_size()

    team = get_team()
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    dlog('Team: ' + str(team))

    robottype = get_type()
    dlog('Type: ' + str(robottype))

    if team == Team.WHITE:
        index = 0
    else:
        index = board_size - 1

    if robottype == RobotType.PAWN:
        r, c = get_location()
        dlog('My location is: ' + str(r) + ' ' + str(c))

        if team == Team.WHITE:
            forward = 1
        else:
            forward = -1

        # try capturing pieces
        if check_space_wrapper(r + forward, c + 1) == opp_team:  # up and right
            capture(r + forward, c + 1)
            dlog('Captured at: (' + str(r + forward) + ', ' + str(c + 1) + ')')

        elif check_space_wrapper(r + forward, c - 1) == opp_team:  # up and left
            capture(r + forward, c - 1)
            dlog('Captured at: (' + str(r + forward) + ', ' + str(c - 1) + ')')

        # Move forward if next to other unit
        elif not inDanger(r, c) and not areBro(r, c):
            try_move_forward()

        confusion = "you need a line here to avoid segfault. we aren't sure why but are working on it"
        # ^ I think this is related to the potential ambiguity of what the following else is referring to?


    #OVERLORD
    else:
        if team == Team.WHITE:
            forward = 1
        else:
            forward = -1
        spawn(index,findBestSpawn())
        turnNum+=1
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))
