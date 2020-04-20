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
finished_cols = []
loop = 0
increment = 0


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


def check_spawn(r):
    if team == Team.WHITE and r == 0:
        return True
    elif team == Team.BLACK and r == board_size - 1:
        return True
    else:
        return False


def check_adjacent(r, c):
    if check_space_wrapper(r, c + 1) == team:
        return True
    elif check_space_wrapper(r, c - 1) == team:
        return True
    else:
        return False


def try_move_forward():
    if not check_space_wrapper(r + forward, c):
        move_forward()


def column(matrix, i):
    return [row[i] for row in matrix]


def findEmpty():
    board = get_board()
    cols = {}
    for i in range(board_size):
        cols[i] = column(board, i).count(team)

    ordered = []
    for key, value in sorted(cols.items(), key=lambda item: item[1]):
        ordered.append(key)
    return ordered


def senseThreat():
    board = get_board()
    rows = {}
    for i in range(board_size):
        rows[i] = row(board, i).count(opp_team)

    for key, value in sorted(rows.items(), key=lambda item: item[1]):
        ordered.append(key)
    return ordered


def sense_finished():
    if team == Team.WHITE:
        idx = board_size - 1
    else:
        idx = 0
    for i in range(board_size):
        if check_space_wrapper(idx, i) == team and i not in finished_cols:
            finished_cols.append(i)


def turn():
    global forward
    global r, c
    global board_size
    global team
    global turnNum
    global startPoint
    global finished_cols
    global index
    global loop
    global increment
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

        elif check_space_wrapper(r + forward + forward, c + 1) is not opp_team and \
                check_space_wrapper(r + forward + forward, c - 1) is not opp_team:
            try_move_forward()

        confusion = "you need a line here to avoid segfault. we aren't sure why but are working on it"
        # ^ I think this is related to the potential ambiguity of what the following else is referring to?


    # OVERLORD
    else:
        if team == Team.WHITE:
            index = 0
        else:
            index = board_size - 1

        sense_finished()

        if loop * 2 % board_size == 0:
            increment += 1

        if increment % 2 == 0:
            col_spawn = loop * 2 % board_size
        else:
            col_spawn = loop * 2 % board_size + 1

        break_check = False

        if team == Team.WHITE:
            for i in range(board_size - 1):
                if check_space_wrapper(index + 3, i) == opp_team and check_space_wrapper(index + 2, i) != team:
                    if not check_space_wrapper(index, i):
                        spawn(index, i)
                        break_check = True
                        break

            if not break_check:
                if not check_space_wrapper(index, col_spawn):
                    spawn(index, col_spawn)
                    loop += 1
                elif not check_space_wrapper(index, col_spawn + 1):
                    spawn(index, col_spawn - 1)
                    loop += 1
                elif not check_space_wrapper(index, col_spawn - 1):
                    spawn(index, col_spawn - 1)
                    loop += 1
                else:
                    for i in range(board_size):
                        if not check_space_wrapper(index, col_spawn):
                            spawn(index, col_spawn)
                            break

        elif team == Team.BLACK:
            for i in range(board_size):
                if check_space_wrapper(index - 3, i) == opp_team and check_space_wrapper(index - 2, i) != team:
                    if not check_space_wrapper(index, i):
                        spawn(index, i)
                        break_check = True
                        break

            if not break_check:
                if not check_space_wrapper(index, col_spawn):
                    spawn(index, col_spawn)
                    loop += 1
                elif not check_space_wrapper(index, col_spawn + 1):
                    spawn(index, col_spawn - 1)
                    loop += 1
                elif not check_space_wrapper(index, col_spawn - 1):
                    spawn(index, col_spawn - 1)
                    loop += 1
                else:
                    for i in range(board_size):
                        if not check_space_wrapper(index, col_spawn):
                            spawn(index, col_spawn)
                            break
                

        turnNum += 1
    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))
    dlog("Finished columns: " + str(finished_cols))
