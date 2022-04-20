import argparse

from models import ButtonCombo, Direction, RND_MAGIC
from models.button_combo import GenericButtonCombo
from models import Game, Move, Player, Fighter, FighterType

def read_data(replay_filename: str, ini_filename: str, delay_count: int = 0):
  replay_data = open(replay_filename, 'rb').read()
  if replay_data[:3] != RND_MAGIC:
    raise ValueError('invalid replay file!')

  # TODO: parse ini properly
  # ini_file = [(k, v) for k, v in map(lambda x: x.split(' ', 1), open(ini_filename).read().splitlines())]
  ini_file = {k: v for k, v in map(lambda x: x.split(' ', 1), open(ini_filename).read().splitlines())}
  player_list = [ini_file['P1Name'], ini_file['P2Name']]

  print(f'Players: {", ".join(player_list)}')

  move_data = replay_data.split(b'\n\nGGPO log:')[0]

  player_one = Player(name='CCND | 1988 N.W.A album track 2', fighters=[
    Fighter(FighterType.FILIA), Fighter(FighterType.ROBO_FORTUNE), Fighter(FighterType.DOUBLE)
  ])

  player_two = Player(name='apg', fighters=[
    Fighter(FighterType.PEACOCK), Fighter(FighterType.ANNIE), Fighter(FighterType.FUKUA)
  ])

  game_copy = Game(player_one, player_two)
  neutral_neutral = Move(Direction.NEUTRAL.value, ButtonCombo.NEUTRAL)
  for _ in range(delay_count):
    game_copy.add_frame(neutral_neutral, neutral_neutral)

  player_idx = 0
  frame_idx = 0
  output_frames = 0
  nonskipped_framecount = 0
  frame_moves = []
  for i in range(7, len(move_data), 4):
    move_num, button_1, button_2, button_3 = list(move_data[i:i + 4])

    # try:
    #   d = Direction(move_num)
    # except ValueError as e:
    #   print(e)
    #   # continue

    # player_idx = (player_idx + 1)
    # if player_idx >= 2:
    #   nonskipped_framecount += 1
    #   if (frame_idx - 1) % 5 != 0:
    #     output_frames += 1

    # frame_idx += 1
    # player_idx %= 2

    game_copy.moves.append(Move(move_num, GenericButtonCombo((button_1, button_2, button_3))))

    # print(f'[F:{output_frames}-{nonskipped_framecount} @ 0x{i:04x}] {player_list[player_idx]}: {d.name} - {" + ".join([m.name for m in moves])}')

  round_name = f'out/round_000{delay_count}'
  with open(f'{round_name}.rnd', 'wb') as f:
    f.write(game_copy.serialize_game())

  with open(f'{round_name}.ini', 'w') as f:
    f.write(open(ini_filename).read())

def main():
  parser = argparse.ArgumentParser(description='Parse a Skullgirls replay .rnd file')
  parser.add_argument('replay_file', action='store', help='The replay .rnd file you want to parse')
  parser.add_argument('ini_file', action='store', help='The respective .ini file for the replay you want to parse')
  args = parser.parse_args()

  for i in range(1, 6):
    read_data(args.replay_file, args.ini_file, i)



if __name__ == '__main__':
  main()
