from mcstats import __mcstats__

def create_ore_stat(title, oreId, oreName):
    __mcstats__.registry.append(
        __mcstats__.MinecraftStat(
            'mine_' + oreId + '_ore',
            {
                'title': title,
                'desc': oreName + ' ore mined',
                'unit': 'int',
            },
            __mcstats__.StatReader(['minecraft:mined','minecraft:' + oreId + '_ore'])
        ))

create_ore_stat('Black Gold', 'coal', 'Coal')
create_ore_stat('Iron Heart', 'iron', 'Iron')
create_ore_stat('Gold Rush', 'gold', 'Gold')
create_ore_stat('Diamonds!', 'diamond', 'Diamond')
create_ore_stat('Mountain Miner', 'emerald', 'Emerald')
create_ore_stat('Blue', 'lapis', 'Lapis Lazuli')
create_ore_stat('Redstone Miner', 'redstone', 'Redstone')
create_ore_stat('Quartz', 'nether_quartz', 'Nether Quartz')
