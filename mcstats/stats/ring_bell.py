from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'ring_bell',
        {
            'title': 'Ding Dong Ditch!',
            'desc': 'Bells rung',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:bell_ring'])
    ))
