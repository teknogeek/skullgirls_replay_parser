from enum import Enum

class GenericButtonCombo(tuple):
  def __new__(cls, t) -> None:
      return super(GenericButtonCombo, cls).__new__(cls, tuple(t))

  def __and__(self, o) -> tuple:
    if not isinstance(o, (tuple, ButtonCombo, GenericButtonCombo)):
      raise TypeError(f'invalid type for GenericButtonCombo AND: {type(o)}')
    return GenericButtonCombo(map(lambda x: x[0] & x[1], zip(self, o.value)))

class ButtonCombo(Enum):
  LP_PRESS = (0x3F, 0xFC, 0xFF)
  LP_HOLD = (0xBF, 0xFE, 0xFF)
  LP_RELEASE = (0x7F, 0xFD, 0xFF)

  MP_PRESS = (0xCF, 0xFC, 0xFF)
  MP_HOLD = (0xEF, 0xFE, 0xFF)
  MP_RELEASE = (0xDF, 0xFD, 0xFF)

  HP_PRESS = (0xF3, 0xFC, 0xFF)
  HP_HOLD = (0xFB, 0xFE, 0xFF)
  HP_RELEASE = (0xF7, 0xFD, 0xFF)

  LK_PRESS = (0xFC, 0xF3, 0xFF)
  LK_HOLD = (0xFE, 0xFB, 0xFF)
  LK_RELEASE = (0xFD, 0xF7, 0xFF)

  MK_PRESS = (0xFF, 0x33, 0xFF)
  MK_HOLD = (0xFF, 0xBB, 0xFF)
  MK_RELEASE = (0xFF, 0x77, 0xFF)

  HK_PRESS = (0xFF, 0xC3, 0xFF)
  HK_HOLD = (0xFF, 0xEB, 0xFF)
  HK_RELEASE = (0xFF, 0xD7, 0xFF)

  THROW_PRESS = (0x3C, 0xF0, 0xFF)
  THROW_HOLD = (0xBE, 0xFA, 0xFF)
  THROW_RELEASE = (0x7D, 0xF5, 0xFF)

  NEUTRAL = (0xFF, 0xFF, 0xFF)
  UNKNOWN = (-1, -1, -1)

  def __getitem__(self, item):
    if isinstance(item, (int, slice)):
      return self.value[item]
    return [self.value[i] for i in item]

  def __and__(self, o) -> GenericButtonCombo:
    if not isinstance(o, (ButtonCombo, GenericButtonCombo)):
      raise TypeError(f'invalid type for AND: {type(o)}')

    o_tuple = o.value if isinstance(o, ButtonCombo) else o
    return GenericButtonCombo(map(lambda x: x[0] & x[1], zip(self.value, o_tuple)))

