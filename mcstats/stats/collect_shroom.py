from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'collect_shroom',
        {
            'title': 'Fun Guy',
            'desc': 'Mushrooms collected',
            'unit': 'int',
        },
        # subtract placed from mined
        mcstats.StatSumReader([
            mcstats.StatReader(['minecraft:picked_up','minecraft:red_mushroom']),
            mcstats.StatReader(['minecraft:picked_up','minecraft:brown_mushroom']),
            mcstats.StatReader(['minecraft:picked_up','minecraft:crimson_fungus']),
            mcstats.StatReader(['minecraft:picked_up','minecraft:warped_fungus']),
        ]),
    ))
