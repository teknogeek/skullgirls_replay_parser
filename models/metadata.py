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
  def __init__(self,
    fighter_type: FighterType,
    voice_option: VoiceOption = VoiceOption.ENGLISH,
    transition_number: int = 0
  ) -> None:
    self.fighter_type = fighter_type
    self.color: int = 1
    self.voice_option = voice_option
    self.transition_number = transition_number

class Player:
  def __init__(self, name: str, fighters: list[Fighter]) -> None:
    self.name = name
    self.fighters = fighters

class GameMetadata:
  def __init__(self,
    player_one: Player,
    player_two: Player,
    world: str = 'Maple_Crest',
    num_rounds: int = 1,
    match_length: int = 99,
    RNG0: int = 284802,
    RNG1: int = -560138391
  ) -> None:
    self.player_one = player_one
    self.player_two = player_two

    self.world = world
    self.num_rounds = num_rounds
    self.match_length = match_length

    self.RNG0 = RNG0
    self.RNG1 = RNG1
