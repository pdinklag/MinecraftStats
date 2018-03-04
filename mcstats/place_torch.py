from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_torch',
        {
            'title': 'Enlightened',
            'desc': 'Torches placed',
            'unit': 'int',
        },
        # subtract mined from placed
        __mcstats__.StatDiffReader(
            __mcstats__.StatReader(['minecraft:used','minecraft:torch']),
            __mcstats__.StatReader(['minecraft:mined','minecraft:torch']))
    ))
