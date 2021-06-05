from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'eat_veggie',
        {
            'title': 'Vegetarian',
            'desc': 'Veggie items eaten',
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:used','minecraft:apple']),
            mcstats.StatReader(['minecraft:used','minecraft:baked_potato']),
            mcstats.StatReader(['minecraft:used','minecraft:beetroot']),
            mcstats.StatReader(['minecraft:used','minecraft:beetroot_soup']),
            mcstats.StatReader(['minecraft:used','minecraft:bread']),
            mcstats.StatReader(['minecraft:used','minecraft:cake']),
            mcstats.StatReader(['minecraft:used','minecraft:carrot']),
            mcstats.StatReader(['minecraft:used','minecraft:chorus_fruit']),
            mcstats.StatReader(['minecraft:used','minecraft:cookie']),
            mcstats.StatReader(['minecraft:used','minecraft:dried_kelp']),
            mcstats.StatReader(['minecraft:used','minecraft:glow_berries']),
            mcstats.StatReader(['minecraft:used','minecraft:golden_apple']),
            mcstats.StatReader(['minecraft:used','minecraft:golden_carrot']),
            mcstats.StatReader(['minecraft:used','minecraft:melon_slice']),
            mcstats.StatReader(['minecraft:used','minecraft:mushroom_stew']),
            mcstats.StatReader(['minecraft:used','minecraft:potato']),
            mcstats.StatReader(['minecraft:used','minecraft:pumpkin_pie']),
            mcstats.StatReader(['minecraft:used','minecraft:sweet_berries']),
        ])
    ))
