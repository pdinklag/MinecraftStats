from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_obsidian',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:mined','minecraft:obsidian'])
    ))
