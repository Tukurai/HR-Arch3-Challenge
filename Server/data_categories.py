from enum import Enum


class GameDataType(Enum):
    """
    Enum for the different types of game data that can be stored on or retrieved from the server.
    """
    LATEST_ACTIVE_PLAYERS = "latest_active_players"
    HIGH_SCORES = "high_scores"

