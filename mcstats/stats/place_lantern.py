from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_lantern',
        {
            'title': 'Fear Of The Dark',
            'desc': 'Lanterns placed',
            'unit': 'int',
        },
        mcstats.StatDiffReader(
            mcstats.StatReader(['minecraft:used','minecraft:lantern']),
            mcstats.StatReader(['minecraft:mined','minecraft:lantern']),
        ),
        1910 # lanterns added in 18w46a
    ))
