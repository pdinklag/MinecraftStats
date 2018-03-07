from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'time_since_death',
        {
            'title': 'Survivor',
            'desc': 'Time since last death',
            'unit': 'ticks',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:time_since_death'])
    ))
