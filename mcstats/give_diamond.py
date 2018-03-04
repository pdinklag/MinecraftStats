from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'give_diamond',
        {
            'title': 'Welfare',
            'desc': 'Diamonds given away',
            'unit': 'int',
        },
        # subtract dropped from picked up
        __mcstats__.StatDiffReader(
            __mcstats__.StatReader(['minecraft:dropped','minecraft:diamond']),
            __mcstats__.StatReader(['minecraft:picked_up','minecraft:diamond']))
    ))
