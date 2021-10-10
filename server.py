import cProfile
import sys
import os

from src.Game import Game, GLOBAL_WINS
from src.Player import Player
from src.globals import logger, clients, link

RETRY_MAX = 20

"""
    The order of connexion of the sockets is important.
    inspector is player 0, it must be represented by the first socket.
    fantom is player 1, it must be representer by the second socket.
"""


def init_connexion():
    while len(clients) != 2:
        link.listen(2)
        (clientsocket, addr) = link.accept()
        logger.info("Received client !")
        clients.append(clientsocket)
        clientsocket.settimeout(10)



def main():
    players = [Player(0), Player(1)]
    scores = []

    logger.info("no client yet")
    init_connexion()
    logger.info("received all clients")

    # profiling
    pr = cProfile.Profile()
    pr.enable()

    game = Game(players)
    game.lancer()

    link.close()

    # profiling
    pr.disable()
    # stats_file = open("{}.txt".format(os.path.basename(__file__)), 'w')
    stats_file = open("./logs/profiling.txt", 'w')
    sys.stdout = stats_file
    pr.print_stats(sort='time')

    sys.stdout = sys.__stdout__
    # os.environ['SERVER_GAME_WIN_OUT'] = '1'
    # os.putenv('SERVER_GAME_WIN_OUT', str(1))
    # os.system(f'export SERVER_GAME_WIN_OUT="{1}"')
    
    # exit(1)


if __name__ == '__main__':
    main()

    # players = [Player(0), Player(1)]
    # scores = []

    # logger.info("no client yet")
    # init_connexion()
    # logger.info("received all clients")

    # # profiling
    # pr = cProfile.Profile()
    # pr.enable()

    # game = Game(players)
    # game.lancer()

    # link.close()

    # # profiling
    # pr.disable()
    # # stats_file = open("{}.txt".format(os.path.basename(__file__)), 'w')
    # stats_file = open("./logs/profiling.txt", 'w')
    # sys.stdout = stats_file
    # pr.print_stats(sort='time')

    # sys.stdout = sys.__stdout__
