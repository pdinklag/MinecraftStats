from mcstats import mcstats

def create_ore_stat(title, oreId, oreName, minVersion = 0):
    mcstats.registry.append(
        mcstats.MinecraftStat(
            'mine_' + oreId,
            {
                'title': title,
                'desc': oreName + ' mined',
                'unit': 'int',
            },
            mcstats.StatReader(['minecraft:mined','minecraft:' + oreId]),
            minVersion
        ))

create_ore_stat('Archeologist', 'ancient_debris', 'Ancient Debris', 2504) # added in 20w06a
create_ore_stat('Black Gold', 'coal_ore', 'Coal Ore')
create_ore_stat('Iron Heart', 'iron_ore', 'Iron Ore')
create_ore_stat('Diamonds!', 'diamond_ore', 'Diamond Ore')
create_ore_stat('Mountain Miner', 'emerald_ore', 'Emerald Ore')
create_ore_stat('Blue', 'lapis_ore', 'Lapis Lazuli Ore')
create_ore_stat('Redstone Miner', 'redstone_ore', 'Redstone Ore')
create_ore_stat('Quartz', 'nether_quartz_ore', 'Nether Quartz Ore')

# gold ore
mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_gold_ore',
        {
            'title': 'Gold Rush',
            'desc': 'Gold Ore mined',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:mined','minecraft:gold_ore']),
            mcstats.StatReader(['minecraft:mined','minecraft:nether_gold_ore']),
        ])
    ))
