from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_sign',
        {
            'title': 'README.TXT',
            'desc': 'Signs placed',
            'unit': 'int',
        },
        # subtract mined from used
        mcstats.StatDiffReader(
            mcstats.StatReader(['minecraft:used','minecraft:sign']),
            mcstats.StatReader(['minecraft:mined','minecraft:sign']))
    ))
