from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'collect_shroom',
        {
            'unit': 'int',
        },
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:picked_up','minecraft:red_mushroom']),
            mcstats.StatReader(['minecraft:picked_up','minecraft:brown_mushroom']),
            mcstats.StatReader(['minecraft:picked_up','minecraft:crimson_fungus']),
            mcstats.StatReader(['minecraft:picked_up','minecraft:warped_fungus']),
        ]),
    ))
