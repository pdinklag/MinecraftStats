from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'mine_ground',
        {
            'title': 'Excavator',
            'desc': 'Dirt, sand and gravel mined',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:mined','minecraft:dirt']),
            __mcstats__.StatReader(['minecraft:mined','minecraft:gravel']),
            __mcstats__.StatReader(['minecraft:mined','minecraft:sand']),
        ])
    ))
