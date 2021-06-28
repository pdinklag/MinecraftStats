from mcstats import mcstats

def create_ore_stat(oreIds, minVersion = 0):
    readers = []
    for ore in oreIds:
        readers.append(mcstats.StatReader(['minecraft:mined','minecraft:' + ore]))

    mcstats.registry.append(
        mcstats.MinecraftStat(
            'mine_' + oreIds[0],
            {
                'unit': 'int',
            },
            mcstats.StatSumReader(readers),
            minVersion
        ))

create_ore_stat(['ancient_debris'], 2504) # added in 20w06a
create_ore_stat(['coal_ore', 'deepslate_coal_ore'])
create_ore_stat(['iron_ore', 'deepslate_iron_ore'])
create_ore_stat(['copper_ore', 'copper_ore'], 2681) # added in 20w45a
create_ore_stat(['diamond_ore', 'deepslate_diamond_ore'])
create_ore_stat(['gold_ore', 'deepslate_gold_ore', 'nether_gold_ore'])
create_ore_stat(['emerald_ore', 'deepslate_emerald_ore'])
create_ore_stat(['lapis_ore', 'deepslate_lapis_ore'])
create_ore_stat(['redstone_ore', 'deepslate_redstone_ore'])
create_ore_stat(['nether_quartz_ore'])
