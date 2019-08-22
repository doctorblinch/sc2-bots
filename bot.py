import sc2
from sc2.constants import NEXUS, PROBE, PYLON, ASSIMILATOR, GATEWAY,\
    CYBERNETICSCORE, STALKER, ROBOTICSFACILITY, IMMORTAL, FORGE, PROTOSSGROUNDWEAPONSLEVEL1
import random

class DoctorBlinch_Protoss_Bot(sc2.BotAI):


    async def on_step(self, iteration):

        await self.distribute_workers()
        await self.build_workers()
        await self.build_army()
        await self.build_offencive_buildings()
        await self.build_pylons()
        await self.build_assimilator()
        await self.expand()
        await self.attack()
        await self.build_technologies()
        #await self.deffend()

    async def build_technologies(self):
        if self.units(FORGE).amount < 1:
            if self.units(FORGE).ready.noqueue:# and self.minerals > 400 and self.vespene > 300:
                print('exists')
                for f in self.units(FORGE).ready.noqueue:
                    print('Forge')
                    if self.can_afford(PROTOSSGROUNDWEAPONSLEVEL1):
                        print(' can afford.\n')
                        await self.do(f.research(PROTOSSGROUNDWEAPONSLEVEL1))

            if self.minerals > 400 and self.vespene > 300 and self.units(CYBERNETICSCORE).exists:
                pylon = self.units(PYLON).ready.random
                await self.build(FORGE, near=pylon)


    def find_target(self, state):
        if len(self.known_enemy_units) > 0:
            return random.choice(self.known_enemy_units)
        elif len(self.known_enemy_structures) > 0:
            return random.choice(self.known_enemy_structures)
        else:
            return self.enemy_start_locations[0]

    async def attack(self):
        if self.units(STALKER).amount > 15:
            for s in self.units(STALKER).idle:
                await self.do(s.attack(self.find_target(self.state)))

            for i in self.units(IMMORTAL).idle:
                await self.do(i.attack(self.find_target(self.state)))

        elif self.units(STALKER).amount > 3:
            if len(self.known_enemy_units) > 0:
                for s in self.units(STALKER).idle:
                    await self.do(s.attack(random.choice(self.known_enemy_units)))

                for i in self.units(IMMORTAL).idle:
                    await self.do(i.attack(random.choice(self.known_enemy_units)))

    async def deffend(self):
        if self.units(STALKER).amount > 3:
            if len(self.known_enemy_units) > 0:
                for s in self.units(STALKER).idle:
                    await self.do(s.attack(random.choice(self.known_enemy_units)))


    async def build_offencive_buildings(self):
        if self.units(PYLON).ready.exists:
            pylon = self.units(PYLON).ready.random
            if self.units(GATEWAY).ready.exists:
                if not self.units(CYBERNETICSCORE).exists:
                    if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                        await self.build(CYBERNETICSCORE, near=pylon)
                else:
                    if not self.units(ROBOTICSFACILITY) and (self.minerals > 300 and self.vespene > 150):
                        if self.can_afford(ROBOTICSFACILITY) and not self.already_pending(ROBOTICSFACILITY):
                            await self.build(ROBOTICSFACILITY, near=pylon)

                    if self.minerals > (200 + self.units(GATEWAY).amount*100) and self.vespene > (100 + self.units(GATEWAY).amount*50):
                        if self.can_afford(GATEWAY):
                            await self.build(GATEWAY, pylon)
            else:
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon)

    async def build_army(self):
        if self.units(GATEWAY).ready.exists and self.units(CYBERNETICSCORE).ready.exists:
            for gw in self.units(GATEWAY).ready.noqueue:
                if self.can_afford(STALKER) and self.supply_left > 1:
                    await self.do(gw.train(STALKER))

        if self.units(ROBOTICSFACILITY).ready.exists and (self.minerals > 400 and self.vespene > 150):
            for rf in self.units(ROBOTICSFACILITY).ready.noqueue:
                if self.can_afford(IMMORTAL) and self.supply_left > 2:
                    await self.do(rf.train(IMMORTAL))

    async def build_workers(self):
        #print(self.units(PROBE).amount)
        if self.units(PROBE).amount >= self.units(NEXUS).amount * 14 + self.units(ASSIMILATOR).amount * 3:
            return
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))

    async def build_pylons(self):
        if self.supply_left < (3 + self.units(GATEWAY).amount + self.units(ROBOTICSFACILITY).amount * 3) and not self.already_pending(PYLON):
            if self.can_afford(PYLON):
                #while (True):
                place = self.units(NEXUS).ready.random
            #        if place.distance_to(self.units.mineral_field) > 3:
             #           break
                await self.build(PYLON, near=place)

    async def build_assimilator(self):
        if (not self.units(GATEWAY).ready.exists) or (self.minerals * 3 < self.vespene * 2):
            #print(self.minerals, self.vespene)
            return
        for nexus in self.units(NEXUS).ready:
            vaspenes = self.state.vespene_geyser.closer_than(15.0,nexus)
            for vaspene in vaspenes:
                if not self.can_afford(ASSIMILATOR):
                    break
                worker = self.select_build_worker(vaspene.position)
                if worker is None:
                    break
                if not self.units(ASSIMILATOR).closer_than(1.0, vaspene).exists:
                    await self.do(worker.build(ASSIMILATOR, vaspene))

    async def expand(self):
        if self.units(NEXUS).amount < 3 and self.can_afford(NEXUS):
            await self.expand_now()