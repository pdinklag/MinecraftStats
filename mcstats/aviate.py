from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'aviate',
        {
            'title': 'Aviator',
            'desc': 'Distance gone by elytra',
            'icon': 'items/elytra.png',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:aviate_one_cm'])
    ))
