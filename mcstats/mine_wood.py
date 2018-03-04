from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'mine_wood',
        {
            'title': 'Woodcutter',
            'desc': 'Wood blocks cut',
            'unit': 'int',
        },
        __mcstats__.StatSumMatchReader(
            ['minecraft:mined'],['minecraft:.+_log'])
    ))
