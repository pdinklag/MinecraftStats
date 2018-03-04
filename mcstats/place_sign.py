from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_sign',
        {
            'title': 'README.TXT',
            'desc': 'Signs placed',
            'unit': 'int',
        },
        # subtract mined from used
        __mcstats__.StatDiffReader(
            __mcstats__.StatReader(['minecraft:used','minecraft:sign']),
            __mcstats__.StatReader(['minecraft:mined','minecraft:sign']))
    ))
