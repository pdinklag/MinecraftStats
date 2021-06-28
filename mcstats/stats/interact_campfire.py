from mcstats import mcstats

mcstats.registry.append(
    mcstats.MinecraftStat(
        'interact_campfire',
        {
            'unit': 'int',
        },
        mcstats.StatReader(['minecraft:custom','minecraft:interact_with_campfire']),
        1921 # campfires added in 19w02a
    ))
