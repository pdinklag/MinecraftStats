from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'eat_meat',
        {
            'title': 'Carnivore',
            'desc': 'Meat items eaten',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:used','minecraft:cooked_porkchop']),
            __mcstats__.StatReader(['minecraft:used','minecraft:cooked_beef']),
            __mcstats__.StatReader(['minecraft:used','minecraft:cooked_chicken']),
            __mcstats__.StatReader(['minecraft:used','minecraft:cooked_mutton']),
            __mcstats__.StatReader(['minecraft:used','minecraft:cooked_rabbit']),
            __mcstats__.StatReader(['minecraft:used','minecraft:porkchop']),
            __mcstats__.StatReader(['minecraft:used','minecraft:beef']),
            __mcstats__.StatReader(['minecraft:used','minecraft:chicken']),
            __mcstats__.StatReader(['minecraft:used','minecraft:mutton']),
            __mcstats__.StatReader(['minecraft:used','minecraft:rabbit']),
            __mcstats__.StatReader(['minecraft:used','minecraft:rabbit_stew']),
        ])
    ))
