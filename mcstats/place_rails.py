from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'place_rails',
        {
            'title': 'Railway Company',
            'desc': 'Rails placed',
            'unit': 'int',
        },
        __mcstats__.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.*rail'])
    ))
