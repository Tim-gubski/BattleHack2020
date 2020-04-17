from typing import List, Optional, Tuple

from battlehack20.engine.game.game import *


# Type-agnostic methods

def get_board_size() -> int:
    """
    Returns the board size.
    """
    ...


def get_bytecode() -> int:
    """
    Returns the number of bytecodes left.
    """
    ...


def get_team() -> Team:
    """
    Returns the robot’s team, either Team.WHITE or Team.BLACK.
    """
    ...


def get_type() -> RobotType:
    """
    Returns the robot’s type, either RobotType.OVERLORD or RobotType.PAWN.
    """
    ...


def check_space(row: int, col: int) -> bool:
    """
    Returns False if there is no robot at the location, the robot type of the robot if there is one there, and throws a RobotError if outside the vision range.
    """
    ...


def log(msg: str):
    """
    Logs a message.
    """
    ...


# Overlord methods


def get_board() -> List[List[Optional[Team]]]:
    """
    Returns the current state of the board as an array of Team.WHITE, Team.BLACK, and None, representing white-occupied, black-occupied, and empty squares, respectively.
    """
    ...


def spawn(row: int, col: int):
    """
    Spawns a pawn at the given location, but throws a RobotError if the pawn is not spawned at the edge on your side of the board, or if you have already spawned a pawn in this turn.
    """
    ...


# Pawn methods

def capture(row: int, col: int):
    """
    Captures an enemy piece at the given location, but throws a RobotError if the there is not an enemy pawn there or if the location is not diagonally in front of you.
    """
    ...


def get_location() -> Tuple[int, int]:
    """
    Returns a (row, col) tuple of the robot’s location.
    """
    ...


def move_forward():
    """
    Moves forward one step, but throws a RobotError if you have already moved, if the location is outside the board or if there is another pawn in front of you.
    """
    ...


def sense() -> List[Tuple[int, int, Team]]:
    """
    Returns a list of tuples of the form (row, col, robot.team) visible to this robot (excluding yourself), that is, if max(|robot.x - other.x|, |robot.y - other.y|) <= 2.
    """
    ...