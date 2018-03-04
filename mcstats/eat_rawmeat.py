from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'eat_rawmeat',
        {
            'title': 'Raw Eater',
            'desc': 'Raw meat items eaten',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:used','minecraft:porkchop']),
            __mcstats__.StatReader(['minecraft:used','minecraft:beef']),
            __mcstats__.StatReader(['minecraft:used','minecraft:chicken']),
            __mcstats__.StatReader(['minecraft:used','minecraft:mutton']),
            __mcstats__.StatReader(['minecraft:used','minecraft:rabbit']),
        ])
    ))
