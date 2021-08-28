from enum import Enum
from itertools import combinations
from functools import reduce

class Direction(Enum):
  RIGHT = 0
  D_RIGHT = 1
  DOWN = 2
  D_LEFT = 3
  LEFT = 4
  U_LEFT = 5
  UP = 6
  U_RIGHT = 7
  NEUTRAL = 8

class Moves(Enum):
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

  def __and__(self, o) -> tuple:
    if not isinstance(o, Moves):
      raise TypeError(f'invalid type for AND: {type(o)}')
    return tuple(map(lambda x: x[0] & x[1], zip(self.value, o.value)))


EXCLUDED_MOVES = [Moves.UNKNOWN, Moves.NEUTRAL, Moves.THROW_PRESS, Moves.THROW_HOLD, Moves.THROW_RELEASE]
ALL_MOVE_COMBOS = {(c1 & c2): [c1, c2] for c1, c2 in combinations([m for m in Moves if m not in EXCLUDED_MOVES], 2)}

'''
Based off: https://github.com/dnunez02/rnd_reader/blob/master/reader.c#L16-L72

Other Notes:
The first 7 bytes are not input data.
Input data starts on the 8th byte with Player 1 then Player 2.

Format is as follows
08 FF FF FF
move byte, then 3 button bytes

08 FF FF FF is pure neutral. No hands on controller.

LP Press:   3F FC FF ==> 0011 1111 X 1111 1100 X 1111 1111
LP Hold:    BF FE FF ==> 1011 1111 X 1111 1110 X 1111 1111
LP Release: 7F FD FF ==> 0111 1111 X 1111 1101 X 1111 1111

MP Press:   CF FC FF ==> 1100 1111 X 1111 1100 X 1111 1111
MP Hold:    EF FE FF ==> 1110 1111 X 1111 1110 X 1111 1111
MP Release: DF FD FF ==> 1101 1111 X 1111 1101 X 1111 1111

HP Press:   F3 FC FF ==> 1111 0011 X 1111 1100 X 1111 1111
HP Hold:    FB FE FF ==> 1111 1011 X 1111 1110 X 1111 1111
HP Release: F7 FD FF ==> 1111 0111 X 1111 1101 X 1111 1111

LK Press:   FC F3 FF ==> 1111 1100 X 1111 0011 X 1111 1111
LK Hold:    FE FB FF ==> 1111 1110 X 1111 1011 X 1111 1111
LK Release: FD F7 FF ==> 1111 1101 X 1111 0111 X 1111 1111

MK Press:   FF 33 FF ==> 1111 1111 X 0011 0011 X 1111 1111
MK Hold:    FF BB FF ==> 1111 1111 X 1011 1011 X 1111 1111
MK Release: FF 77 FF ==> 1111 1111 X 0111 0111 X 1111 1111

HK Press:   FF C3 FF ==> 1111 1111 X 1100 0011 X 1111 1111
HK Hold:    FF EB FF ==> 1111 1111 X 1110 1011 X 1111 1111
HK Release: FF D7 FF ==> 1111 1111 X 1101 0111 X 1111 1111

Normal double button presses are the bitwise-and of the two buttons and 
the actions done at that time.
Note that button A can be pressed while B is held. So we get
(B hold) & (A Press)


Biggest Example is Throw
LP+LK Press:   3C F0 FF ==> 0011 1100 X 1111 0000 X 1111 1111
LP+LK Hold:    BE FA FF ==> 1011 1110 X 1111 1010 X 1111 1111
LP+LK Release: 7D F5 FF ==> 0111 1101 X 1111 0101 X 1111 1111

Here is an exception to the rule
Dash does not register without that change in the last word
LP+MP Press:   0F FC CF ==> 0000 1111 X 1111 1100 X 1100 1111
LP+MP Hold:    AF FE EF ==> 1010 1111 X 1111 1110 X 1110 1111
LP+HP Release: 5F FD DF ==> 0101 1111 X 1111 1101 X 1101 1111

Here is another exception.
This could be used to check for supers
LK+MK Press:   FC 33 3F ==> 1111 1100 X 0011 0011 X 0011 1111
LK+MK Hold:    FE BB BF ==> 1111 1110 X 1011 1011 X 1011 1111
LK+MK Release: FD 77 7F ==> 1111 1101 X 0111 0111 X 0111 1111

Snaps and assist calls do not seem to use that last word
'''

PUNCH_TO_KICK_MAPPING = {
  Moves.LP_PRESS: Moves.LK_PRESS,
  Moves.LP_HOLD: Moves.LK_HOLD,
  Moves.LP_RELEASE: Moves.LK_RELEASE,
  
  Moves.MP_PRESS: Moves.MK_PRESS,
  Moves.MP_HOLD: Moves.MK_HOLD,
  Moves.MP_RELEASE: Moves.MK_RELEASE,
  
  Moves.HP_PRESS: Moves.HK_PRESS,
  Moves.HP_HOLD: Moves.HK_HOLD,
  Moves.HP_RELEASE: Moves.HK_RELEASE,
}


def read_data(replay_filename: str, ini_filename: str, modify_punches=True):
  ini_file = {k: v for k, v in map(lambda x: x.split(' ', 1), open(ini_filename).read().splitlines())}
  player_list = [ini_file['P1Name'], ini_file['P2Name']]

  print(f'Players: {", ".join(player_list)}')

  replay_data = open(replay_filename, 'rb').read()

  move_data = replay_data.split(b'\n\nGGPO log:')[0]
  player_idx = 1
  frame_idx = 0
  output_frames = 0
  for i in range(7, len(move_data), 4):
    move_num, button_1, button_2, button_3 = list(move_data[i:i + 4])

    try:
      d = Direction(move_num)
    except ValueError:
      continue

    moves = calc_moves((button_1, button_2, button_3))
    if moves[0] == Moves.UNKNOWN:
      moves = calc_moves((button_1, button_2, 0xFF))

    if moves[0] == Moves.UNKNOWN:
      continue

    player_idx = (player_idx + 1)
    if player_idx >= 2 and (frame_idx - 1) % 5 != 0:
      output_frames += 1

    frame_idx += 1
    player_idx %= 2

    if modify_punches and any(k in moves for k in PUNCH_TO_KICK_MAPPING.keys()):
      for idx, m in enumerate(moves):
        if m in PUNCH_TO_KICK_MAPPING:
          moves[idx] = PUNCH_TO_KICK_MAPPING[m]

      moves_output = reduce(lambda x, y: x & y, moves)
      move_data = move_data[:i+1] + bytes(moves_output) + move_data[i+4:]

    print(f'[F:{output_frames} @ 0x{i:04x}] {player_list[player_idx]}: {d.name} - {" + ".join([m.name for m in moves])}')

  if modify_punches:
    with open(f'{replay_filename}.modified', 'wb') as f:
      f.write(b'\n\nGGPO log:'.join([move_data] + replay_data.split(b'\n\nGGPO log:')[1:]))

def calc_moves(move_tuple):
  try:
    return [Moves(move_tuple)]
  except ValueError:
    pass

  if move_tuple in ALL_MOVE_COMBOS:
    return ALL_MOVE_COMBOS[move_tuple]

  return [Moves.UNKNOWN]


def main():
  round_id = 'round_1204'

  read_data(f'./{round_id}.rnd', f'./{round_id}.ini', modify_punches=True)



if __name__ == '__main__':
  main()
