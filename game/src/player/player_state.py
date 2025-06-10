from enum import Enum


class PlayerState(Enum):
    IDLE_DOWN = 0
    IDLE_UP = 1
    IDLE_LEFT = 2
    IDLE_RIGHT = 3
    MOVE_LEFT = 4
    MOVE_RIGHT = 5
    MOVE_UP = 6
    MOVE_DOWN = 7


ANIMATION_FILES = {
    PlayerState.IDLE_DOWN: 'idle_down.gif',
    PlayerState.IDLE_UP: 'idle_up.gif',
    PlayerState.IDLE_LEFT: 'idle_left.gif',
    PlayerState.IDLE_RIGHT: 'idle_right.gif',
    PlayerState.MOVE_LEFT: 'left.gif',
    PlayerState.MOVE_RIGHT: 'right.gif',
    PlayerState.MOVE_UP: 'up.gif',
    PlayerState.MOVE_DOWN: 'down.gif'
}