from .move import Move
from .metadata import GameMetadata
from struct import pack

RND_MAGIC = b'\x31\x30\x02'

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
        f'Fighter {f.fighter_type.value}',
        f'Color {f.color}',
        f'TransitionNum {f.transition_number}',
        f'{f.voice_option.value}VO 1'
      ]

    ini_lines.append('Player 2')
    for f in self.metadata.player_two.fighters:
      ini_lines += [
        f'Fighter {f.fighter_type.value}',
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