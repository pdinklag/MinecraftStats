from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_nether_wart',
        {
            'title': 'Nether Farmer',
            'desc': 'Nether warts planted',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:nether_wart'])
    ))
