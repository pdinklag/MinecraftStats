from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'aviate',
        {
            'title': 'Aviator',
            'desc': 'Distance gone by elytra',
            'icon': 'items/elytra.png',
            'unit': 'cm',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:aviate_one_cm'])
    ))
