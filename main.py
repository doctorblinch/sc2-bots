from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer, Human
from bot import DoctorBlinch_Protoss_Bot


run_game(maps.get("AutomatonLE"), [
    Human(Race.Random),
    Bot(Race.Protoss, DoctorBlinch_Protoss_Bot()),

    #Computer(Race.Random, Difficulty.Hard)
], realtime=True)

'''
import sc2
from sc2 import Race
from sc2.player import Bot

from zerg.zerg_rush import ZergRushBot

def main():
    sc2.run_game(sc2.maps.get("Abyssal Reef LE"), [
        Bot(Race.Zerg, ZergRushBot()),
        Computer(Race.Terran, Difficulty.Medium)
    ], realtime=False)

if __name__ == '__main__':
    main()'''