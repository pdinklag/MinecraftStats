from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_paper',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:paper'])
    ))
