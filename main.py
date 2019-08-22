from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer, Human
from bot import DoctorBlinch_Protoss_Bot


run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Protoss, DoctorBlinch_Protoss_Bot()),
 #   Human(Race.Random),
    Computer(Race.Random, Difficulty.Hard)
], realtime=True)