from enum import Enum

class GenericButtonCombo(tuple):
  def __new__(cls, t) -> None:
      return super(GenericButtonCombo, cls).__new__(cls, tuple(t))

  def __and__(self, o) -> tuple:
    if not isinstance(o, (tuple, ButtonCombo, GenericButtonCombo)):
      raise TypeError(f'invalid type for GenericButtonCombo AND: {type(o)}')
    o_tuple = o.value if isinstance(o, ButtonCombo) else o
    return GenericButtonCombo(map(lambda x: x[0] & x[1], zip(self, o_tuple)))

class ButtonCombo(Enum):
  LP_PRESS       = (0b00111111,0b11111100,0b11111111)
  MP_PRESS       = (0b11001111,0b11111100,0b11111111)
  HP_PRESS       = (0b11110011,0b11111100,0b11111111)
  LK_PRESS       = (0b11111100,0b11110011,0b11111111)
  MK_PRESS       = (0b11111111,0b00110011,0b11111111)
  HK_PRESS       = (0b11111111,0b11000011,0b11111111)
  P_DASH_PRESS   = (0b11111111,0b11111111,0b11001111)
  K_DASH_PRESS   = (0b11111111,0b11111111,0b00111111)

  LP_HOLD        = (0b10111111,0b11111110,0b11111111)
  MP_HOLD        = (0b11101111,0b11111110,0b11111111)
  HP_HOLD        = (0b11111011,0b11111110,0b11111111)
  LK_HOLD        = (0b11111110,0b11111011,0b11111111)
  MK_HOLD        = (0b11111111,0b10111011,0b11111111)
  HK_HOLD        = (0b11111111,0b11101011,0b11111111)
  P_DASH_HOLD    = (0b11111111,0b11111111,0b11101111)
  K_DASH_HOLD    = (0b11111111,0b11111111,0b10111111)

  LP_RELEASE     = (0b01111111,0b11111101,0b11111111)
  MP_RELEASE     = (0b11011111,0b11111101,0b11111111)
  HP_RELEASE     = (0b11110111,0b11111101,0b11111111)
  LK_RELEASE     = (0b11111101,0b11110111,0b11111111)
  MK_RELEASE     = (0b11111111,0b01110111,0b11111111)
  HK_RELEASE     = (0b11111111,0b11010111,0b11111111)
  P_DASH_RELEASE = (0b11111111,0b11111111,0b11011111)
  K_DASH_RELEASE = (0b11111111,0b11111111,0b01111111)

  THROW_PRESS    = (0b00111100,0b11110000,0b11111111)
  THROW_HOLD     = (0b10111110,0b11111010,0b11111111)
  THROW_RELEASE  = (0b01111101,0b11110101,0b11111111)

  NEUTRAL        = (0b11111111,0b11111111,0b11111111)
  UNKNOWN        = (-1, -1, -1)

  def __getitem__(self, item):
    if isinstance(item, (int, slice)):
      return self.value[item]
    return [self.value[i] for i in item]

  def __and__(self, o) -> GenericButtonCombo:
    if not isinstance(o, (ButtonCombo, GenericButtonCombo)):
      raise TypeError(f'invalid type for AND: {type(o)}')

    o_tuple = o.value if isinstance(o, ButtonCombo) else o
    return GenericButtonCombo(map(lambda x: x[0] & x[1], zip(self.value, o_tuple)))

