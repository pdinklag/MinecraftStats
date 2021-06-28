from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_tnt',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:tnt'])
    ))
