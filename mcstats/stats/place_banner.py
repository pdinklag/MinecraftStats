from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_banner',
        {
            'title': 'Flying Flags',
            'desc': 'Banners placed',
            'unit': 'int',
        },
        mcstats.StatSumMatchReader(
            ['minecraft:used'],
            ['minecraft:.*banner'])
    ))
