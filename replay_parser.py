from itertools import combinations
from functools import reduce
import argparse

from models import Move, Direction

RND_MAGIC = b'\x31\x30\x02'

LP_MOVES = [Move.LP_PRESS, Move.LP_HOLD, Move.LP_RELEASE]
LK_MOVES = [Move.LK_PRESS, Move.LK_HOLD, Move.LK_RELEASE]
MP_MOVES = [Move.MP_PRESS, Move.MP_HOLD, Move.MP_RELEASE]
MK_MOVES = [Move.MK_PRESS, Move.MK_HOLD, Move.MK_RELEASE]
HP_MOVES = [Move.HP_PRESS, Move.HP_HOLD, Move.HP_RELEASE]
HK_MOVES = [Move.HK_PRESS, Move.HK_HOLD, Move.HK_RELEASE]

ALL_MOVE_LISTS = [LP_MOVES, LK_MOVES, MP_MOVES, MK_MOVES, HP_MOVES, HK_MOVES]

def clean_combos(combos_list):
  return list(filter(lambda c: all([
    n <= 1 for n in [
      sum([1 if m in move_list else 0 for m in c])
        for move_list in ALL_MOVE_LISTS
      ]
    ]), combos_list))

EXCLUDED_MOVES = [Move.UNKNOWN, Move.NEUTRAL, Move.THROW_PRESS, Move.THROW_HOLD, Move.THROW_RELEASE]
ALL_MOVE_COMBOS = {(c1 & c2): [c1, c2] for c1, c2 in clean_combos(combinations([m for m in Move if m not in EXCLUDED_MOVES], 2))}
for c1, c2, c3 in clean_combos(combinations([m for m in Move if m not in EXCLUDED_MOVES], 3)):
  # (c1 & c2) (buttons 1 and 2) returns a tuple
  # therefore we have to map generic (x & y) to a zip of:
  #     - each element of the resulting tuple of (c1 & c2)
  #     - with each element of the raw c3 (the 3rd button) move raw tuple (Move.value)
  and_res = tuple(map(lambda x: x[0] & x[1], zip(c1 & c2, c3.value)))
  ALL_MOVE_COMBOS[and_res] = [c1, c2, c3]



PUNCH_TO_KICK_MAPPING = {
  Move.LP_PRESS: Move.LK_PRESS,
  Move.LP_HOLD: Move.LK_HOLD,
  Move.LP_RELEASE: Move.LK_RELEASE,

  Move.MP_PRESS: Move.MK_PRESS,
  Move.MP_HOLD: Move.MK_HOLD,
  Move.MP_RELEASE: Move.MK_RELEASE,

  Move.HP_PRESS: Move.HK_PRESS,
  Move.HP_HOLD: Move.HK_HOLD,
  Move.HP_RELEASE: Move.HK_RELEASE,
}


def read_data(replay_filename: str, ini_filename: str, replace_punches=False):
  replay_data = open(replay_filename, 'rb').read()
  if replay_data[:3] != RND_MAGIC:
    raise ValueError('invalid replay file!')

  ini_file = {k: v for k, v in map(lambda x: x.split(' ', 1), open(ini_filename).read().splitlines())}
  player_list = [ini_file['P1Name'], ini_file['P2Name']]

  print(f'Players: {", ".join(player_list)}')

  move_data = replay_data.split(b'\n\nGGPO log:')[0]
  print(len(move_data))
  player_idx = 0
  frame_idx = 0
  output_frames = 0
  nonskipped_framecount = 0
  for i in range(7, len(move_data), 4):
    move_num, button_1, button_2, button_3 = list(move_data[i:i + 4])

    try:
      d = Direction(move_num)
    except ValueError:
      continue

    moves = calc_moves((button_1, button_2, button_3))
    if moves[0] == Move.UNKNOWN:
      moves = calc_moves((button_1, button_2, 0xFF))

    player_idx = (player_idx + 1)
    if player_idx >= 2:
      nonskipped_framecount += 1
      if (frame_idx - 1) % 5 != 0:
        output_frames += 1

    frame_idx += 1
    player_idx %= 2

    # TODO: remove all unknowns
    if moves[0] == Move.UNKNOWN:
      # print(f'[-] Unknown move: (0x{button_1:02X}, 0x{button_2:02X}, 0x{button_3:02X})')
      continue

    if replace_punches and any(k in moves for k in PUNCH_TO_KICK_MAPPING.keys()):
      for idx, m in enumerate(moves):
        if m in PUNCH_TO_KICK_MAPPING:
          moves[idx] = PUNCH_TO_KICK_MAPPING[m]

      moves_output = reduce(lambda x, y: x & y, moves)
      move_data = move_data[:i+1] + bytes(moves_output) + move_data[i+4:]

    print(f'[F:{output_frames}-{nonskipped_framecount} @ 0x{i:04x}] {player_list[player_idx]}: {d.name} - {" + ".join([m.name for m in moves])}')

  if replace_punches:
    with open(f'{replay_filename}.modified', 'wb') as f:
      f.write(b'\n\nGGPO log:'.join([move_data] + replay_data.split(b'\n\nGGPO log:')[1:]))

def calc_moves(move_tuple):
  try:
    return [Move(move_tuple)]
  except ValueError:
    pass

  if move_tuple in ALL_MOVE_COMBOS:
    return ALL_MOVE_COMBOS[move_tuple]

  return [Move.UNKNOWN]


def main():
  parser = argparse.ArgumentParser(description='Parse a Skullgirls replay .rnd file')
  parser.add_argument('replay_file', action='store', help='The replay .rnd file you want to parse')
  parser.add_argument('ini_file', action='store', help='The respective .ini file for the replay you want to parse')
  parser.add_argument('--replace-punches', action='store_true', default=False, dest='replace_punches', help='Replace all punches with kicks')
  args = parser.parse_args()

  read_data(args.replay_file, args.ini_file, replace_punches=args.replace_punches)



if __name__ == '__main__':
  main()
