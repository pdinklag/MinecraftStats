from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_wool',
        {
            'title': 'Clothier',
            'desc': 'Wool crafted or dyed',
            'unit': 'int',
        },
        __mcstats__.StatSumMatchReader(
            ['minecraft:crafted'],
            ['minecraft:.+_wool'])
    ))
