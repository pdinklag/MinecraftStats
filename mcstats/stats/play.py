from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'play',
        {
            'title': 'Addict',
            'desc': 'Time played on the server',
            'unit': 'ticks',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:play_one_minute'])
    ))
