import copy

from game.battle.battle_simulator import BattleSimulator
from game.models.position import Position
from game.models.unit import Unit
from game.player import Player

# unit(name, class, hp, atk, def, m_atk, m_def, speed, range)
unit1 = Unit('Gariusz', 'Mage', 10, 0, 0, 10, 7, 5, 6)
unit2 = Unit('Faliusz', 'Archer', 15, 7, 2, 0, 1, 7, 8)
unit3 = Unit('Bartusz', 'Warrior', 30, 5, 5, 0, 3, 3, 3)
units = [None, unit1, unit2, unit3]

board_player1 = [   [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0, 0],
                    [0, 0, 0, 0, 3, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [2, 0, 0, 0, 0, 0, 0, 0]    ]
board_player1 = [list(map(lambda x: copy.deepcopy(units[x]), arr)) for arr in board_player1]

board_player2 = [   [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 3, 3, 3],
                    [0, 0, 0, 0, 0, 0, 0, 0]    ]
board_player2 = [list(map(lambda x: copy.deepcopy(units[x]), arr)) for arr in board_player2]

if __name__ == '__main__':
    player1_units = []
    player2_units = []
    for i in range(8):
        for j in range(8):
            if board_player1[i][j]:
                board_player1[i][j].set_position(Position(j, 7-i))
                player1_units.append(board_player1[i][j])
            if board_player2[i][j]:
                board_player2[i][j].set_position(Position(j, 7-i).get_mirrored_position())
                player2_units.append(board_player2[i][j])

    player1 = Player("player1", "id1")
    player2 = Player("player2", "id2")
    player1.quiz_score = 2
    player1.units = player1_units
    player2.units = player2_units
    battle_simulator = BattleSimulator(player1, player2)
    result = battle_simulator.start_simulation(0)
    print(result)
