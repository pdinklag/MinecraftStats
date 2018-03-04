from mcstats import __mcstats__

__mcstats__.registry.append(
    __mcstats__.MinecraftStat(
        'eat_veggie',
        {
            'title': 'Vegetarian',
            'desc': 'Veggie items eaten',
            'unit': 'int',
        },
        __mcstats__.StatSumReader([
            __mcstats__.StatReader(['minecraft:used','minecraft:golden_carrot']),
            __mcstats__.StatReader(['minecraft:used','minecraft:golden_apple']),
            __mcstats__.StatReader(['minecraft:used','minecraft:carrot']),
            __mcstats__.StatReader(['minecraft:used','minecraft:potato']),
            __mcstats__.StatReader(['minecraft:used','minecraft:baked_potato']),
            __mcstats__.StatReader(['minecraft:used','minecraft:beetroot']),
            __mcstats__.StatReader(['minecraft:used','minecraft:apple']),
            __mcstats__.StatReader(['minecraft:used','minecraft:pumpkin_pie']),
            __mcstats__.StatReader(['minecraft:used','minecraft:chorus_fruit']),
            __mcstats__.StatReader(['minecraft:used','minecraft:melon']),
            __mcstats__.StatReader(['minecraft:used','minecraft:cookie']),
            __mcstats__.StatReader(['minecraft:used','minecraft:cake']),
            __mcstats__.StatReader(['minecraft:used','minecraft:bread']),
            __mcstats__.StatReader(['minecraft:used','minecraft:mushroom_stew']),
            __mcstats__.StatReader(['minecraft:used','minecraft:beetroot_soup']),
        ])
    ))
