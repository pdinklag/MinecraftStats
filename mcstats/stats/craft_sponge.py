from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_sponge',
        {
            'title': 'Spongebob',
            'desc': 'Sponges dried',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:sponge'])
    ))
