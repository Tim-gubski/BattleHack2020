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
opp_index = 0
idleCount = 0
opp_team = None
finished_cols = []
friends_arr = []

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
def inDanger():
    if (check_space_wrapper(r + forward*2, c+1) != opp_team and check_space_wrapper(r + forward*2, c-1) != opp_team) or (check_space_wrapper(r, c+1) == team or check_space_wrapper(r, c-1) == team):
        return False
    else:
        return True

def areBro():
    if (check_space_wrapper(r + forward*2, c) == opp_team or check_space_wrapper(r + forward*2, c+2) == opp_team) and check_space_wrapper(r + forward, c+1) == team:
        return True
    elif (check_space_wrapper(r + forward*2, c) == opp_team or check_space_wrapper(r + forward*2, c-2) == opp_team) and check_space_wrapper(r + forward, c-1) == team:
        return True
    else:
        return False

def sense_finished():
    if team == Team.WHITE:
        idx = board_size - 1
    else:
        idx = 0
    for i in range(board_size):
        if check_space_wrapper(idx, i) == team and i not in finished_cols:
            finished_cols.append(i)

def find_friends():
    friends_arr = []
    for r in range(board_size):
        for c in range(board_size):
            if get_board()[r][c] == team:
                friends_arr.append([r, c])


def turn():
    global forward
    global r, c
    global board_size
    global team
    global turnNum
    global startPoint
    global index
    global opp_index
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
        opp_index = board_size - 1
    else:
        index = board_size - 1
        opp_index = 0

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
        elif not inDanger() and not areBro():
            try_move_forward()

        confusion = "you need a line here to avoid segfault. we aren't sure why but are working on it"
        # ^ I think this is related to the potential ambiguity of what the following else is referring to?


    #OVERLORD
    else:
        break_check = False
        spawn_check = False

        if team == Team.WHITE:
            forward = 1
            for i in range(board_size):
                if check_space_wrapper(index + 3, i) == opp_team and check_space_wrapper(index + 2, i) != team:
                    if not check_space_wrapper(index, i):
                        spawn(index, i)
                        break_check = True
                        break
        else:
            forward = -1
            for i in range(board_size):
                if check_space_wrapper(index - 3, i) == opp_team and check_space_wrapper(index - 2, i) != team:
                    if not check_space_wrapper(index, i):
                        spawn(index, i)
                        break_check = True
                        break
        if not break_check:
            find_friends()
            for i in friends_arr:
                if check_space_wrapper(i[r] + 2 * forward, i[c] + 1) == opp_team or check_space_wrapper(i[r] + 2 * forward, i[c] - 1) == opp_team:
                    if not check_space_wrapper(i[r], i[c] + 1):
                        spawn(i[r], i[c] + 1)
                        spawn_check = True
                        break
                    elif not check_space_wrapper(i[r], i[c] - 1):
                        spawn(i[r], i[c] - 1)
                        spawn_check = True
                        break

        if not spawn_check and not break_check:
            for _ in range(board_size):
                i = random.randint(0, board_size - 1)
                if not check_space(opp_index, i) == team and not check_space(index, i):
                    spawn(index, i)
                    dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                    break
        turnNum += 1
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))
