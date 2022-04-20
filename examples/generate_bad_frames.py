from models.button_combo import ButtonCombo, GenericButtonCombo
from models import Game, Move, Direction, Player, Fighter, FighterType

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
    Fighter(FighterType.FILIA), Fighter(FighterType.CEREBELLA), Fighter(FighterType.PAINWHEEL)
  ])

  player_two = Player(name='bot', fighters=[
    Fighter(FighterType.BIG_BAND), Fighter(FighterType.ELIZA)
  ])

  game = Game(player_one, player_two)
  neutral_neutral = Move(Direction.NEUTRAL, ButtonCombo.NEUTRAL)

  # 600 frames of neutral/neutral
  for _ in range(600):
    game.add_frame(neutral_neutral, neutral_neutral)

  game.add_frame(
    Move(Direction.NEUTRAL,
      GenericButtonCombo(
        ButtonCombo.LP_PRESS
        & ButtonCombo.MP_PRESS
        & ButtonCombo.LK_PRESS
        & ButtonCombo.MK_PRESS
        & ButtonCombo.P_DASH_PRESS
        & ButtonCombo.K_DASH_PRESS
        & ButtonCombo.THROW_PRESS
      )
    ),
    neutral_neutral,
  )
  game.add_frame(
    Move(Direction.NEUTRAL,
      GenericButtonCombo(
        ButtonCombo.LP_HOLD
        & ButtonCombo.MP_HOLD
        & ButtonCombo.LK_HOLD
        & ButtonCombo.MK_HOLD
        & ButtonCombo.P_DASH_HOLD
        & ButtonCombo.K_DASH_HOLD
        & ButtonCombo.THROW_HOLD
      )
    ),
    neutral_neutral
  )

  for _ in range(80):
    game.add_frame(
      Move(
        Direction.NEUTRAL,
        GenericButtonCombo((0x9E, 0xB9, 0xBF))
      ),
      neutral_neutral
    )

  for _ in range(7):
    game.add_frame(
      Move(Direction.NEUTRAL,
        GenericButtonCombo(
          ButtonCombo.LP_HOLD
          & ButtonCombo.LK_HOLD
          & ButtonCombo.MK_HOLD
          & ButtonCombo.K_DASH_HOLD
          & ButtonCombo.THROW_HOLD
        )
      ),
      neutral_neutral
    )

  game.add_frame(
    Move(Direction.NEUTRAL,
      GenericButtonCombo(
        ButtonCombo.LP_HOLD
        & ButtonCombo.MP_PRESS
        & ButtonCombo.LK_HOLD
        & ButtonCombo.MK_HOLD
        & ButtonCombo.K_DASH_HOLD
        & ButtonCombo.THROW_HOLD
      )
    ),
    neutral_neutral
  )

  for _ in range(2):
    game.add_frame(
      Move(Direction.NEUTRAL,
        GenericButtonCombo(
          ButtonCombo.LP_HOLD
          & ButtonCombo.MP_HOLD
          & ButtonCombo.LK_HOLD
          & ButtonCombo.MK_HOLD
          & ButtonCombo.P_DASH_HOLD
          & ButtonCombo.K_DASH_HOLD
          & ButtonCombo.THROW_HOLD
        )
      ),
      neutral_neutral
    )

  for _ in range(80):
    game.add_frame(
      Move(
        Direction.NEUTRAL,
        GenericButtonCombo((0xAE, 0x76, 0xEF))
      ),
      neutral_neutral
    )


  for _ in range(2):
    game.add_frame(
      Move(Direction.NEUTRAL,
        GenericButtonCombo(
          ButtonCombo.LP_HOLD
          & ButtonCombo.MP_HOLD
          & ButtonCombo.LK_HOLD
          & ButtonCombo.P_DASH_HOLD
          & ButtonCombo.THROW_HOLD
        )
      ),
      neutral_neutral
    )

  game.add_frame(
    Move(Direction.NEUTRAL,
      GenericButtonCombo(
        ButtonCombo.LP_HOLD
        & ButtonCombo.MP_HOLD
        & ButtonCombo.P_DASH_HOLD
        & ButtonCombo.LK_RELEASE
      )
    ),
    neutral_neutral
  )
  game.add_frame(
    Move(Direction.NEUTRAL,
      GenericButtonCombo(
        ButtonCombo.LP_HOLD
        & ButtonCombo.MP_HOLD
        & ButtonCombo.P_DASH_HOLD
      )
    ),
    neutral_neutral
  )

  for _ in range(80):
    game.add_frame(
      Move(
        Direction.NEUTRAL,
        GenericButtonCombo((0x6F, 0xFD, 0xFF))
      ),
      neutral_neutral
    )

  game.add_frame(
    Move(Direction.NEUTRAL, ButtonCombo.MP_RELEASE),
    neutral_neutral
  )

  # 100 more frames of neutral/neutral
  for _ in range(100):
    game.add_frame(neutral_neutral, neutral_neutral)

  round_name = 'round_0002'
  with open(f'{round_name}.rnd', 'wb') as f:
    f.write(game.serialize_game())

  with open(f'{round_name}.ini', 'w') as f:
    f.write(game.generate_ini())

if __name__ == '__main__':
  main()
