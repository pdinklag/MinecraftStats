from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'noteblock',
        {
            'title': 'Musician',
            'desc': 'Note block interactions',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:custom','minecraft:tune_noteblock']),
            __mcstats__.StatReader(['minecraft:custom','minecraft:play_noteblock'])])
    ))
