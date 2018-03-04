from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'play_record',
        {
            'title': 'Disc Jockey',
            'desc': 'Records played',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:play_record'])
    ))
