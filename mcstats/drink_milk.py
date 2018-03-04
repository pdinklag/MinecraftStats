from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'drink_milk',
        {
            'title': 'Milksop',
            'desc': 'Milk buckets drunk',
            'unit': 'int',
        },
        __mcstats__.StatReader(['minecraft:used','minecraft:milk_bucket'])
    ))
