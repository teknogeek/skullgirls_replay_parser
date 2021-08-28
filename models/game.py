from enum import Enum
from .move import Move
from struct import pack

RND_MAGIC = b'\x31\x30\x02'

class VoiceOption(Enum):
  ENGLISH = 'EN'
  JAPANESE = 'JP'
  ALT = 'Alt'

class Fighter:
  name: str
  color: int = 1
  voice_option: VoiceOption = VoiceOption.ENGLISH
  transition_number: int = 0

  def __init__(self, name: str) -> None:
    self.name = name

class Player:
  name: str
  fighters: list[Fighter]

  def __init__(self, name: str, fighters: list[Fighter]) -> None:
    self.name = name
    self.fighters = fighters

class GameMetadata:
  world = 'Maple_Crest'
  num_rounds = 1
  match_length = 99

  RNG0: int = 284802
  RNG1: int = -560138391

  player_one: Player = None
  player_two: Player = None

  def __init__(self, player_one: Player, player_two: Player) -> None:
    self.player_one = player_one
    self.player_two = player_two

class Game:
  moves: list[Move] = []
  metadata: GameMetadata = None

  def __init__(self, player_one_name: str, player_two_name: str) -> None:
    self.metadata = GameMetadata(player_one_name, player_two_name)

  def add_frame(self, player_one_move: Move, player_two_move: Move) -> None:
    self.moves += [player_one_move, player_two_move]

  def serialize_game(self):
    game_length = int(len(self.moves) / 2)

    serialized_game = RND_MAGIC + pack('<i', game_length)

    for i in range(0, len(self.moves), 2):
      player_one_move, player_two_move = self.moves[i:i + 2]

      serialized_game += bytes([player_one_move.direction.value, *player_one_move.button_combo])
      serialized_game += bytes([player_two_move.direction.value, *player_two_move.button_combo])
      serialized_game += pack('<ii', self.metadata.RNG0, self.metadata.RNG1)

    serialized_game += b'\n\nGGPO log:\n\n'
    return serialized_game

  def generate_ini(self) -> str:
    ini_lines = [
      f'World {self.metadata.world}',
      f'NumRounds {self.metadata.num_rounds}',
      f'MatchLength {self.metadata.match_length}',
    ]

    ini_lines.append('Player 1')
    for f in self.metadata.player_one.fighters:
      ini_lines += [
        f'Fighter {f.name}',
        f'Color {f.color}',
        f'TransitionNum {f.transition_number}',
        f'{f.voice_option.value}VO 1'
      ]

    ini_lines.append('Player 2')
    for f in self.metadata.player_two.fighters:
      ini_lines += [
        f'Fighter {f.name}',
        f'Color {f.color}',
        f'TransitionNum {f.transition_number}',
        f'{f.voice_option.value}VO 1'
      ]

    ini_lines += [
      f'P1Name {self.metadata.player_one.name}',
      f'P2Name {self.metadata.player_two.name}',
      f'RNG0 {self.metadata.RNG0}',
      f'RNG1 {self.metadata.RNG1}',
      ''
    ]

    return '\n'.join(ini_lines)