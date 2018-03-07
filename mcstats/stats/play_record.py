from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'play_record',
        {
            'title': 'Disc Jockey',
            'desc': 'Records played',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:play_record'])
    ))
