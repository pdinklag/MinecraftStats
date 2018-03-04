from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'breed',
        {
            'title': 'Ranch',
            'desc': 'Animals bred',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:animals_bred'])
    ))
