from enum import Enum

class VoiceOption(Enum):
  ENGLISH = 'EN'
  JAPANESE = 'JP'
  ALT = 'Alt'

class FighterType(Enum):
  ANNIE = 'Annie'
  BIG_BAND = 'BigBand'
  BEOWULF = 'Beowulf'
  CEREBELLA = 'Cerebella'
  DOUBLE = 'Double'
  ELIZA = 'Eliza'
  FILIA = 'Filia'
  FUKUA = 'Fukua'
  MS_FORTUNE = 'MsFortune'
  PAINWHEEL = 'Painwheel'
  PARASOUL = 'Parasoul'
  PEACOCK = 'Peacock'
  ROBO_FORTUNE = 'RoboFortune'
  SQUIGLY = 'Squigly'
  VALENTINE = 'Valentine'

class Fighter:
  fighter_type: FighterType
  color: int = 1
  voice_option: VoiceOption = VoiceOption.ENGLISH
  transition_number: int = 0

  def __init__(self, fighter_type: FighterType) -> None:
    self.fighter_type = fighter_type

class Player:
  name: str
  fighters: list[Fighter]

  def __init__(self, name: str, fighters: list[Fighter]) -> None:
    self.name = name
    self.fighters = fighters

class GameMetadata:
  world: str = 'Maple_Crest'
  num_rounds: int = 1
  match_length: int = 99

  RNG0: int = 284802
  RNG1: int = -560138391

  player_one: Player
  player_two: Player

  def __init__(self, player_one: Player, player_two: Player) -> None:
    self.player_one = player_one
    self.player_two = player_two