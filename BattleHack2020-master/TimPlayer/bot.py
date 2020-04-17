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
def dlog(str):
    if DEBUG > 0:
        log(str)


def check_space_wrapper(r, c):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
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


def turn():
    global forward
    global r, c
    global board_size
    global team
    global turnNum
    global startPoint
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
        elif check_adjacent(r, c):
            try_move_forward()
            dlog('Moved forward!')

        confusion = "you need a line here to avoid segfault. we aren't sure why but are working on it"
        # ^ I think this is related to the potential ambiguity of what the following else is referring to?


    #OVERLORD
    else:
        if turnNum%8==0:
            startPoint+=1
            startPoint = startPoint%2

        if team == Team.WHITE:
            index = 0
        else:
            index = board_size - 1

        for x in range(8):
            i=(startPoint+x*2)
            if not check_space(index, i):
                spawn(index, i)
                dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                break
        turnNum += 1
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))
