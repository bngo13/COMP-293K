PACKET_COUNT = 5
WINDOW_SIZE = 2
RECOVERY_RATE = 1
DATA_VALUE = 2

DEFENDER_STRATS = [
    0,
    2,
    4
]

ATTACKER_STRATS = [
    0,
    3,
    5
]

DEFENDER_RESOURCES = 5
ATTACKER_RESOURCES = 5

def get_current_game_utils():
    payoffs = {}
    for i, dstrat in enumerate(DEFENDER_STRATS):
        if (dstrat > DEFENDER_RESOURCES):
            continue
        payoffs[i] = []
        for j, astrat in enumerate(ATTACKER_STRATS):
            if (astrat > ATTACKER_RESOURCES):
                continue
            dutil = 0
            autil = 0
            if dstrat > astrat:
                dutil = DATA_VALUE - dstrat
                autil = -astrat
            else:
                dutil = -DATA_VALUE - dstrat
                autil = DATA_VALUE - astrat
            
            payoffs[i].append((dutil, autil))
    return payoffs

def main():
    util_map = get_current_game_utils()
    print(util_map)
                

if __name__ == "__main__":
    main()
