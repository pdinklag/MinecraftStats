from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'mine_dimensional',
        {
            'title': 'Terraformer',
            'desc': 'Netherrack and end stone mined',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:mined','minecraft:end_stone']),
            __mcstats__.StatReader(['minecraft:mined','minecraft:netherrack'])
        ])
    ))
