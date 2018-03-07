from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'use_fireworks',
        {
            'title': 'Happy New Year!',
            'desc': 'Fireworks started',
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:used','minecraft:firework_rocket'])
    ))
