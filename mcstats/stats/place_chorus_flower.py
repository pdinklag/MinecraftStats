from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'place_chorus_flower',
        {
            'title': 'Chorus Farmer',
            'desc': 'Chorus Flowers planted',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:chorus_flower'])
    ))
