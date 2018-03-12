from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'play',
        {
            'title': 'Addict',
            'desc': 'Total time played',
            'unit': 'ticks',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:play_one_minute'])
    ))
