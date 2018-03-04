from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_beacon',
        {
            'title': 'Power Source',
            'desc': 'Beacons crafted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:crafted','minecraft:beacon']),
    ))
