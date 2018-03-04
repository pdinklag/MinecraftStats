from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'craft_sword',
        {
            'title': 'Blacksmith',
            'desc': 'Swords crafted',
            'unit': 'int',
        },
        __mcstats__.StatSumMatchReader(
            ['minecraft:crafted'],
            ['minecraft:.+_sword'])
    ))
