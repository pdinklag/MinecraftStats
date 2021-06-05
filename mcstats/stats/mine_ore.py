from mcstats import mcstats

def create_ore_stat(title, oreIds, oreName, minVersion = 0):
    readers = []
    for ore in oreIds:
        readers.append(mcstats.StatReader(['minecraft:mined','minecraft:' + ore]))

    mcstats.registry.append(
        mcstats.MinecraftStat(
            'mine_' + oreIds[0],
            {
                'title': title,
                'desc': oreName + ' mined',
                'unit': 'int',
            },
            mcstats.StatSumReader(readers),
            minVersion
        ))

create_ore_stat('Archeologist', ['ancient_debris'], 'Ancient Debris', 2504) # added in 20w06a
create_ore_stat('Black Gold', ['coal_ore', 'deepslate_coal_ore'], 'Coal Ore')
create_ore_stat('Iron Heart', ['iron_ore', 'deepslate_iron_ore'], 'Iron Ore')
create_ore_stat('Copper Miner', ['copper_ore', 'copper_ore'], 'Copper Ore', 2681) # added in 20w45a
create_ore_stat('Diamonds!', ['diamond_ore', 'deepslate_diamond_ore'], 'Diamond Ore')
create_ore_stat('Gold Rush', ['gold_ore', 'deepslate_gold_ore', 'nether_gold_ore'], 'Gold Ore')
create_ore_stat('Mountain Miner', ['emerald_ore', 'deepslate_emerald_ore'], 'Emerald Ore')
create_ore_stat('Blue', ['lapis_ore', 'deepslate_lapis_ore'], 'Lapis Lazuli Ore')
create_ore_stat('Redstone Miner', ['redstone_ore', 'deepslate_redstone_ore'], 'Redstone Ore')
create_ore_stat('Quartz', ['nether_quartz_ore'], 'Nether Quartz Ore')
