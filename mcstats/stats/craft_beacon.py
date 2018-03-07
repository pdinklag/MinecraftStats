from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'craft_beacon',
        {
            'title': 'Power Source',
            'desc': 'Beacons crafted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:crafted','minecraft:beacon']),
    ))
