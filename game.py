import numpy as np

PACKET_COUNT = 10
WINDOW_SIZE = 5
ATTACKER_SCALE = 5
RECOVERY_RATE = 1
DATA_VALUE = 50

DEFENDER_STRATS = [
    0,
    1,
    2,
    3
]

ATTACKER_STRATS = [s * ATTACKER_SCALE for s in DEFENDER_STRATS]

DEFENDER_RESOURCES = 10
ATTACKER_RESOURCES = 10

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
            if dstrat >= astrat:
                dutil = DATA_VALUE - dstrat
                autil = -astrat
            else:
                dutil = -DATA_VALUE - dstrat
                autil = DATA_VALUE - astrat
            
            payoffs[i].append((dutil, autil))
    return payoffs

def solve_game(util_map):
    dWorkUtils = {}
    # Solve Attacker First
    for dstrat, utils in util_map.items():
        aBestStrat = [None, None]
        for astrat, util in enumerate(utils):
            if None in aBestStrat:
                aBestStrat[0] = astrat
                aBestStrat[1] = util
            
            if util[1] > aBestStrat[1][1]:
                aBestStrat[0] = astrat
                aBestStrat[1] = util
        dWorkUtils[dstrat] = aBestStrat

    # Solve Defender Next
    bestStrat = None
    bestUtils = None
    for dstrat, [astrat, utils] in dWorkUtils.items():
        if None in [bestStrat, bestUtils]:
            bestStrat = (dstrat, astrat)
            bestUtils = utils
        
        if utils[0] > bestUtils[0]:
            bestStrat = (dstrat, astrat)
            bestUtils = utils

    return (bestStrat, bestUtils)

def post_game_stats(dstrats, astrats):
    # Defender Statistics
    print("Defender Statistics")
    dSum = sum(dstrats.values())
    for strat, amt in dstrats.items():
        print(f"DStrat {strat}: {amt / dSum * 100}%")
    print()

    # Attacker Statistics
    print("Attacker Statistics")
    aSum = sum(astrats.values())
    for strat, amt in astrats.items():
        print(f"AStrat {strat}: {amt / aSum * 100}%")

def save_info(gameNum, dUtil, aUtil):
    with open("data.csv", 'a') as f:
        f.write(f"{gameNum},{dUtil},{aUtil}\n")

def main():
    global DEFENDER_RESOURCES, ATTACKER_RESOURCES
    dStrats = {
        0: 0,
        1: 0,
        2: 0,
        3: 0
    }
    dTotalUtil = 0

    aStrats = {
        0: 0,
        1: 0,
        2: 0,
        3: 0
    }
    aTotalUtil = 0
    
    window = 0
    for r in np.arange(0, 1000, 0.2):
        global DATA_VALUE
        DATA_VALUE = r

        for i in range(0, PACKET_COUNT):
            if (window > WINDOW_SIZE - 1):
                DEFENDER_RESOURCES += RECOVERY_RATE
                ATTACKER_RESOURCES += RECOVERY_RATE

            util_map = get_current_game_utils()
            ((dstrat, astrat), (dutil, autil)) = solve_game(util_map)

            dStrats[dstrat] += 1
            aStrats[astrat] += 1

            DEFENDER_RESOURCES -= DEFENDER_STRATS[dstrat]
            ATTACKER_RESOURCES -= ATTACKER_STRATS[astrat]

            dTotalUtil += dutil
            aTotalUtil += autil
            window += 1

        save_info(round(r, 2), dTotalUtil, aTotalUtil)

if __name__ == "__main__":
    main()
