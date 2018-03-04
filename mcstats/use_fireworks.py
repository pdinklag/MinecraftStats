from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'use_fireworks',
        {
            'title': 'Happy New Year!',
            'desc': 'Fireworks started',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:firework_rocket'])
    ))
