from itertools import combinations
from functools import reduce
import argparse

from models import ButtonCombo, Direction, RND_MAGIC

LP_MOVES = [ButtonCombo.LP_PRESS, ButtonCombo.LP_HOLD, ButtonCombo.LP_RELEASE]
LK_MOVES = [ButtonCombo.LK_PRESS, ButtonCombo.LK_HOLD, ButtonCombo.LK_RELEASE]
MP_MOVES = [ButtonCombo.MP_PRESS, ButtonCombo.MP_HOLD, ButtonCombo.MP_RELEASE]
MK_MOVES = [ButtonCombo.MK_PRESS, ButtonCombo.MK_HOLD, ButtonCombo.MK_RELEASE]
HP_MOVES = [ButtonCombo.HP_PRESS, ButtonCombo.HP_HOLD, ButtonCombo.HP_RELEASE]
HK_MOVES = [ButtonCombo.HK_PRESS, ButtonCombo.HK_HOLD, ButtonCombo.HK_RELEASE]
P_DASH_MOVES = [ButtonCombo.P_DASH_PRESS, ButtonCombo.P_DASH_HOLD, ButtonCombo.P_DASH_RELEASE]
K_DASH_MOVES = [ButtonCombo.K_DASH_PRESS, ButtonCombo.K_DASH_HOLD, ButtonCombo.K_DASH_RELEASE]
THROW_MOVES = [ButtonCombo.THROW_PRESS, ButtonCombo.THROW_HOLD, ButtonCombo.THROW_RELEASE]

EXCLUSIVE_MOVE_SETS = [LP_MOVES, LK_MOVES, MP_MOVES, MK_MOVES, HP_MOVES, HK_MOVES, P_DASH_MOVES, K_DASH_MOVES, THROW_MOVES]

REQUIRED_MOVE_CONDITIONS = {
  ButtonCombo.THROW_PRESS: [[ButtonCombo.LP_PRESS, ButtonCombo.LK_PRESS]],
  ButtonCombo.THROW_HOLD: [[ButtonCombo.LP_HOLD, ButtonCombo.LK_HOLD]],
  ButtonCombo.THROW_RELEASE: [[ButtonCombo.LP_RELEASE, ButtonCombo.LK_RELEASE]],

  # punch dash enforcements
  ButtonCombo.P_DASH_PRESS: [
    [ButtonCombo.LP_PRESS, ButtonCombo.MP_PRESS],
    [ButtonCombo.LP_PRESS, ButtonCombo.HP_PRESS],
    [ButtonCombo.MP_PRESS, ButtonCombo.HP_PRESS],
  ],
  ButtonCombo.P_DASH_HOLD: [
    [ButtonCombo.LP_HOLD, ButtonCombo.MP_HOLD],
    [ButtonCombo.LP_HOLD, ButtonCombo.HP_HOLD],
    [ButtonCombo.MP_HOLD, ButtonCombo.HP_HOLD],
  ],
  ButtonCombo.P_DASH_RELEASE: [
    [ButtonCombo.LP_RELEASE, ButtonCombo.MP_RELEASE],
    [ButtonCombo.LP_RELEASE, ButtonCombo.HP_RELEASE],
    [ButtonCombo.MP_RELEASE, ButtonCombo.HP_RELEASE],
  ],

  # kick dash enforcements
  ButtonCombo.K_DASH_PRESS: [
    [ButtonCombo.LK_PRESS, ButtonCombo.MK_PRESS],
    [ButtonCombo.LK_PRESS, ButtonCombo.HK_PRESS],
    [ButtonCombo.MK_PRESS, ButtonCombo.HK_PRESS],
  ],
  ButtonCombo.K_DASH_HOLD: [
    [ButtonCombo.LK_HOLD, ButtonCombo.MK_HOLD],
    [ButtonCombo.LK_HOLD, ButtonCombo.HK_HOLD],
    [ButtonCombo.MK_HOLD, ButtonCombo.HK_HOLD],
  ],
  ButtonCombo.K_DASH_RELEASE: [
    [ButtonCombo.LK_RELEASE, ButtonCombo.MK_RELEASE],
    [ButtonCombo.LK_RELEASE, ButtonCombo.HK_RELEASE],
    [ButtonCombo.MK_RELEASE, ButtonCombo.HK_RELEASE],
  ]
}

def clean_combos(combos_list):
  # enforce that only one move in each set within ALL_MOVE_LISTS exists
  # i.e. only one LP_* move can be in a single combo
  move_set_filted_combos = []
  for combo in combos_list:
    add_combo = True
    for move_set in EXCLUSIVE_MOVE_SETS:
      # count how many moves are within each move set
      moves_in_set = 0
      for move in combo:
        if move in move_set:
          moves_in_set += 1

      # if there are more than one move in the combo from this set, skip the combo
      if moves_in_set > 1:
        add_combo = False
        break

    if add_combo:
      move_set_filted_combos.append(combo)

  # enforce certain move patterns, i.e. THROW_PRESS requires both LP_PRESS and LK_PRESS
  clean_combos = []
  for combo in move_set_filted_combos:
    is_clean_combo = True
    for move_condition, required_move_options in REQUIRED_MOVE_CONDITIONS.items():
      has_any_of_required_move_sets = any(
        all(move in combo for move in required_moves)
        for required_moves in required_move_options
      )
      if move_condition in combo and not has_any_of_required_move_sets:
        is_clean_combo = False
        break

    if is_clean_combo:
      clean_combos.append(combo)

  return clean_combos

ALL_MOVE_COMBOS = {}
EXCLUDED_MOVES = [
  ButtonCombo.UNKNOWN,
  ButtonCombo.NEUTRAL
]

# 2-move combos
print('Generating 2-move combos...')
for c1, c2 in clean_combos(combinations([m for m in ButtonCombo if m not in EXCLUDED_MOVES], 2)):
  ALL_MOVE_COMBOS[(c1 & c2)] = [c1, c2]

# 3-move combos
print('Generating 3-move combos...')
for c1, c2, c3 in clean_combos(combinations([m for m in ButtonCombo if m not in EXCLUDED_MOVES], 3)):
  ALL_MOVE_COMBOS[(c1 & c2 & c3)] = [c1, c2, c3]

# 4-move combos
print('Generating 4-move combos...')
for c1, c2, c3, c4 in clean_combos(combinations([m for m in ButtonCombo if m not in EXCLUDED_MOVES], 4)):
  ALL_MOVE_COMBOS[(c1 & c2 & c3 & c4)] = [c1, c2, c3, c4]

# 5-move combos
print('Generating 5-move combos...')
for c1, c2, c3, c4, c5 in clean_combos(combinations([m for m in ButtonCombo if m not in EXCLUDED_MOVES], 5)):
  ALL_MOVE_COMBOS[(c1 & c2 & c3 & c4 & c5)] = [c1, c2, c3, c4, c5]

# 6-move combos
print('Generating 6-move combos...')
for c1, c2, c3, c4, c5, c6 in clean_combos(combinations([m for m in ButtonCombo if m not in EXCLUDED_MOVES], 6)):
  ALL_MOVE_COMBOS[(c1 & c2 & c3 & c4 & c5 & c6)] = [c1, c2, c3, c4, c5, c6]

# 7-move combos
print('Generating 7-move combos...')
for c1, c2, c3, c4, c5, c6, c7 in clean_combos(combinations([m for m in ButtonCombo if m not in EXCLUDED_MOVES], 7)):
  ALL_MOVE_COMBOS[(c1 & c2 & c3 & c4 & c5 & c6 & c7)] = [c1, c2, c3, c4, c5, c6, c7]

# 8-move combos
print('Generating 8-move combos...')
for c1, c2, c3, c4, c5, c6, c7, c8 in clean_combos(combinations([m for m in ButtonCombo if m not in EXCLUDED_MOVES], 8)):
  ALL_MOVE_COMBOS[(c1 & c2 & c3 & c4 & c5 & c6 & c7 & c8)] = [c1, c2, c3, c4, c5, c6, c7, c8]

# 9-move combos
print('Generating 9-move combos...')
for c1, c2, c3, c4, c5, c6, c7, c8, c9 in clean_combos(combinations([m for m in ButtonCombo if m not in EXCLUDED_MOVES], 9)):
  ALL_MOVE_COMBOS[(c1 & c2 & c3 & c4 & c5 & c6 & c7 & c8 & c9)] = [c1, c2, c3, c4, c5, c6, c7, c8, c9]


PUNCH_TO_KICK_MAPPING = {
  ButtonCombo.LP_PRESS: ButtonCombo.LK_PRESS,
  ButtonCombo.LP_HOLD: ButtonCombo.LK_HOLD,
  ButtonCombo.LP_RELEASE: ButtonCombo.LK_RELEASE,

  ButtonCombo.MP_PRESS: ButtonCombo.MK_PRESS,
  ButtonCombo.MP_HOLD: ButtonCombo.MK_HOLD,
  ButtonCombo.MP_RELEASE: ButtonCombo.MK_RELEASE,

  ButtonCombo.HP_PRESS: ButtonCombo.HK_PRESS,
  ButtonCombo.HP_HOLD: ButtonCombo.HK_HOLD,
  ButtonCombo.HP_RELEASE: ButtonCombo.HK_RELEASE,
}


def read_data(replay_filename: str, ini_filename: str, replace_punches=False):
  replay_data = open(replay_filename, 'rb').read()
  if replay_data[:3] != RND_MAGIC:
    raise ValueError('invalid replay file!')

  ini_file = {k: v for k, v in map(lambda x: x.split(' ', 1), open(ini_filename).read().splitlines())}
  player_list = [ini_file['P1Name'], ini_file['P2Name']]

  print(f'Players: {", ".join(player_list)}')

  move_data = replay_data.split(b'\n\nGGPO log:')[0]

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
    if moves[0] == ButtonCombo.UNKNOWN:
      moves = calc_moves((button_1, button_2, 0xFF))

    player_idx = (player_idx + 1)
    if player_idx >= 2:
      nonskipped_framecount += 1
      if (frame_idx - 1) % 5 != 0:
        output_frames += 1

    frame_idx += 1
    player_idx %= 2

    # TODO: remove all unknowns
    if moves[0] == ButtonCombo.UNKNOWN:
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
    return [ButtonCombo(move_tuple)]
  except ValueError:
    pass

  if move_tuple in ALL_MOVE_COMBOS:
    return ALL_MOVE_COMBOS[move_tuple]

  return [ButtonCombo.UNKNOWN]


def main():
  parser = argparse.ArgumentParser(description='Parse a Skullgirls replay .rnd file')
  parser.add_argument('replay_file', action='store', help='The replay .rnd file you want to parse')
  parser.add_argument('ini_file', action='store', help='The respective .ini file for the replay you want to parse')
  parser.add_argument('--replace-punches', action='store_true', default=False, dest='replace_punches', help='Replace all punches with kicks')
  args = parser.parse_args()

  read_data(args.replay_file, args.ini_file, replace_punches=args.replace_punches)



if __name__ == '__main__':
  main()
