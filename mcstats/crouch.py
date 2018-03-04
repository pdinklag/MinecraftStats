from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'crouch',
        {
            'title': 'Sneaky',
            'desc': 'Distance crouched',
            'unit': 'cm',
        },
        __mcstats__.StatReader(['minecraft:custom','minecraft:crouch_one_cm'])
    ))
