from .direction import Direction
from .button_combo import ButtonCombo

class Move:
  def __init__(self, direction: Direction, button_combo: ButtonCombo) -> None:
    self.direction: Direction = direction
    self.button_combo: ButtonCombo = button_combo
