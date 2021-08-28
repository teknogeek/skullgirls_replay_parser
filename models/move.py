from .direction import Direction
from .button_combo import ButtonCombo

class Move:
  direction: Direction = None
  button_combo: ButtonCombo = None

  def __init__(self, direction: Direction, button_combo: ButtonCombo) -> None:
    self.direction = direction
    self.button_combo = button_combo