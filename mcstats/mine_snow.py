from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'mine_snow',
        {
            'title': 'Snow Pusher',
            'desc': 'Snow removed',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:mined','minecraft:snow']),
            __mcstats__.StatReader(['minecraft:mined','minecraft:snow_block']),
        ])
    ))
