from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'mine_obsidian',
        {
            'title': 'Obsidian Miner',
            'desc': 'Obsidian blocks mined',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:mined','minecraft:obsidian'])
    ))
