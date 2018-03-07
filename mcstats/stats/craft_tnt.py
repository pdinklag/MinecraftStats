from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_tnt',
        {
            'title': 'Bad Intentions',
            'desc': 'TNT crafted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:tnt'])
    ))
