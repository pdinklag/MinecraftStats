from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_sponge',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:sponge'])
    ))
