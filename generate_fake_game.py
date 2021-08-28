from models.button_combo import ButtonCombo
from models import Game, Move, Direction, Player, Fighter

def main():
  '''
  Generate a fake game where:
    - both players neutral/neutral until frame 600
    - at frame 600:
      - player1: u_left
      - player2: u_right
    - end game
  '''
  player_one = Player(name='SilkTail', fighters=[
    Fighter('Filia'), Fighter('RoboFortune'), Fighter('Double')
  ])

  player_two = Player(name='Teknogeek', fighters=[
    Fighter('Filia'), Fighter('Annie'), Fighter('Fukua')
  ])

  game = Game(player_one, player_two)
  neutral_neutral = Move(Direction.NEUTRAL, ButtonCombo.NEUTRAL)

  # 600 frames of neutral/neutral
  for _ in range(600):
    game.add_frame(neutral_neutral, neutral_neutral)

  # 3 frames of up-right/left for player 1/2
  for _ in range(3):
    game.add_frame(
      Move(Direction.U_RIGHT, ButtonCombo.NEUTRAL),
      Move(Direction.U_LEFT, ButtonCombo.NEUTRAL),
    )

  # 100 more frames of neutral/neutral
  for _ in range(100):
    game.add_frame(neutral_neutral, neutral_neutral)

  round_name = 'round_1370'
  with open(f'{round_name}.rnd', 'wb') as f:
    f.write(game.serialize_game())

  with open(f'{round_name}.ini', 'w') as f:
    f.write(game.generate_ini())

if __name__ == '__main__':
  main()